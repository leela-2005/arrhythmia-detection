from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
import os
from ecg.services import get_beats_by_class

@login_required
def home_view(request):
    """Render the landing page with mode selection."""
    return render(request, "dashboard/home.html")

@login_required
def dashboard_view(request):
    """Legacy dashboard view, redirect or keep as Analysis Result view."""
    # Assuming this is the result view based on previous code
    result = request.session.get("latest_result")
    return render(request, "dashboard/dashboard.html", {
        "result": result
    })

@login_required
def visualize_view(request):
    """Render the subject selection for visualization."""
    # List of MIT-BIH subjects (hardcoded or fetched)
    subjects = [
        "100", "101", "102", "103", "104", "105", "106", "107", "108", "109",
        "111", "112", "113", "114", "115", "116", "117", "118", "119", "121",
        "122", "123", "124", "200", "201", "202", "203", "205", "207", "208",
        "209", "210", "212", "213", "214", "215", "217", "219", "220", "221",
        "222", "223", "228", "230", "231", "232", "233", "234"
    ]
    return render(request, "dashboard/visualize.html", {"subjects": subjects})

@login_required
def visualize_subject_view(request, subject_id):
    """Fetch and display subject's heartbeats."""
    # Path to MIT-BIH data
    # Assuming mit_bih folder is in the project root
    base_path = os.path.join(settings.BASE_DIR, 'mit_bih')
    
    beat_data = get_beats_by_class(subject_id, base_path)
    
    return render(request, "dashboard/subject_detail.html", {
        "subject_id": subject_id,
        "beat_data": beat_data
    })

from django.shortcuts import redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm
from django.contrib import messages

def register_view(request):
    """Render the registration page and handle user creation."""
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Optionally log the user in immediately
            login(request, user)
            messages.success(request, f"Account created successfully for {user.username}!")
            return redirect('home')
    else:
        form = UserRegistrationForm()
        
    return render(request, "dashboard/register.html", {"form": form})

from django.http import JsonResponse
from blockchain.models import BlockchainRecord
from blockchain.web3_logger import compute_sha256_hash

@login_required
def blockchain_records_view(request):
    """Render the dashboard page showing all logged blockchain records."""
    records = BlockchainRecord.objects.all().order_by('-timestamp')
    return render(request, "dashboard/blockchain_records.html", {"records": records})

@login_required
def verify_record(request, record_id):
    """Recalculate the hash and verify against the stored hash in the ledger."""
    try:
        record = BlockchainRecord.objects.get(id=record_id)
        
        # Format the confidence correctly as stored '0.0000'
        confidence_str = f"{record.confidence_score:.4f}"
        timestamp_str = str(record.timestamp)
        
        recomputed_hash = compute_sha256_hash(
            record.record_id,
            record.predicted_class,
            confidence_str,
            timestamp_str,
            record.shap_summary
        )
        
        is_verified = (recomputed_hash == record.stored_hash)
        
        return JsonResponse({"verified": is_verified, "recomputed_hash": recomputed_hash})
    except BlockchainRecord.DoesNotExist:
        return JsonResponse({"verified": False, "error": "Record not found"}, status=404)
