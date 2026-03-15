from django.shortcuts import render, redirect
from django.utils import timezone
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os

from ecg.services import (
    load_ecg_record,
    get_abnormal_sample,
    extract_abnormal_window,
    generate_ecg_graph
)

from quality.quality_check import check_ecg_quality
from mlmodel.features import extract_feature_vector
from mlmodel.hqcnn import hqcnn_predict
from mlmodel.explain import explain_prediction
from mlmodel.shap_explain import generate_shap_explanations
from blockchain.web3_logger import log_to_blockchain
from alerts.notifier import send_alert


# ==============================
# DEMO MODE (keep False normally)
# ==============================
DEMO_MODE = False

from django.contrib.auth.decorators import login_required

@login_required
def upload_ecg(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        dat_file = request.FILES.get('dat_file')
        hea_file = request.FILES.get('hea_file')
        atr_file = request.FILES.get('atr_file')

        if not patient_id or not dat_file or not hea_file:
            return render(request, 'upload.html', {
                'error': "Patient ID, .dat and .hea files are required"
            })

        # ------------------------------
        # Save uploaded files
        # ------------------------------
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads', patient_id)
        os.makedirs(upload_dir, exist_ok=True)

        fs_store = FileSystemStorage(location=upload_dir)
        fs_store.save(f"{patient_id}.dat", dat_file)
        fs_store.save(f"{patient_id}.hea", hea_file)
        if atr_file:
            fs_store.save(f"{patient_id}.atr", atr_file)

        try:
            # ------------------------------
            # Load ECG
            # ------------------------------
            signal, fs, _ = load_ecg_record(patient_id, base_path=upload_dir)

            # ------------------------------
            # 1️⃣ Signal Quality Index
            # ------------------------------
            valid, sqi = check_ecg_quality(signal)
            if not valid:
                return render(request, 'upload.html', {
                    'error': f"Low signal quality (SQI: {sqi:.2f})"
                })

            # ------------------------------
            # 2️⃣ Build ECG segments
            # ------------------------------
            segments = []

            # ATR-guided abnormal segment (optional)
            abnormal_sample = get_abnormal_sample(patient_id, upload_dir)
            if abnormal_sample is not None:
                segments.append(
                    extract_abnormal_window(signal, abnormal_sample, fs)
                )

            # Add normal segments across signal
            for i in range(0, len(signal), fs * 5):
                seg = signal[i:i + fs * 5]
                if len(seg) >= fs * 3:
                    segments.append(seg)
                if len(segments) >= 6:
                    break

            # ------------------------------
            # 3️⃣ Predict each segment
            # ------------------------------
            predictions = []
            last_valid_feature = None
            last_valid_segment = None

            for seg in segments:
                fv = extract_feature_vector(seg, sampling_rate=fs)
                if fv is not None:
                    predictions.append(hqcnn_predict(fv))
                    last_valid_feature = fv
                    last_valid_segment = seg

            if not predictions:
                return render(request, 'upload.html', {
                    'error': "Unable to extract valid ECG features"
                })

            # ------------------------------
            # 4️⃣ Majority Voting
            # ------------------------------
            abnormal_ratio = predictions.count("Abnormal") / len(predictions)

            if abnormal_ratio >= 0.5:
                prediction = "Abnormal"
            elif abnormal_ratio >= 0.2:
                prediction = "Borderline"
            else:
                prediction = "Normal"

            # ------------------------------
            # 5️⃣ Rule-based clinical override
            # ------------------------------
            fv = last_valid_feature.reshape(-1)

            hr = fv[0]      # Heart Rate
            rr = fv[1]      # Mean RR interval
            sdnn = fv[2]    # HRV SDNN
            rmssd = fv[3]   # HRV RMSSD

            rule_abnormal = False

            if hr < 50 or hr > 120:
                rule_abnormal = True

            if rr < 0.5 or rr > 1.3:
                rule_abnormal = True

            if sdnn > 0.15 or rmssd > 0.15:
                rule_abnormal = True

            if rule_abnormal:
                prediction = "Abnormal"

            # ------------------------------
            # 6️⃣ Explainable AI
            # ------------------------------
            explanation = explain_prediction(last_valid_feature, prediction)
            shap_outputs = generate_shap_explanations(last_valid_feature, patient_id)

            try:
                from mlmodel.gemini_explain import generate_gemini_explanation
                if shap_outputs and "feature_contributions" in shap_outputs:
                    ai_text = generate_gemini_explanation(shap_outputs["feature_contributions"], prediction)
                    if ai_text:
                        explanation.append(f"AI Insight: {ai_text}")
            except Exception as e:
                print(f"Failed to generate Gemini explanation: {e}")

            # ------------------------------
            # 7️⃣ ECG Graph
            # ------------------------------
            graph_url = generate_ecg_graph(last_valid_segment, patient_id)

            # ------------------------------
            # 8️⃣ Blockchain
            # ------------------------------
            timestamp_str = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
            shap_summary = "Abnormal regions detected" if prediction == "Abnormal" else "Normal baseline"
            
            # Use 0.99 for confidence as HQCNN doesn't output probability array currently
            confidence = 0.99
            
            record = log_to_blockchain(
                record_id=patient_id,
                predicted_class=prediction,
                confidence=confidence,
                timestamp_str=timestamp_str,
                shap_summary=shap_summary
            )

            # ------------------------------
            # 9️⃣ Save Result
            # ------------------------------
            request.session["latest_result"] = {
                "record": patient_id,
                "sqi": round(sqi, 2),
                "prediction": prediction,
                "explanation": explanation,
                "shap_outputs": shap_outputs,
                "block_hash": record.stored_hash,
                "tx_receipt": record.transaction_receipt,
                "graph_url": graph_url,
                "time": timezone.now().strftime("%b %d, %Y %H:%M")
            }

            # ------------------------------
            # 🔔 Alert
            # ------------------------------
            if prediction == "Abnormal":
                send_alert(f"Critical arrhythmia detected for {patient_id}")

            return redirect('dashboard')

        except Exception as e:
            return render(request, 'upload.html', {
                'error': f"Processing failed: {str(e)}"
            })

    return render(request, 'upload.html')


def ecg_dashboard(request):
    result = request.session.get("latest_result")
    return render(request, "dashboard/result.html", {"result": result})
