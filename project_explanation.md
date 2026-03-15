# Project Explanation: Smart ECG Analysis System

This document provides a comprehensive yet simple explanation of the **Smart ECG** project. It is designed to help students explain the project during a review or viva.

---

## 1. Project Overview
**What is this project?**
Smart ECG is an AI-powered healthcare system that analyzes ECG (electrocardiogram) signals to detect heart rhythm irregularities (arrhythmias). It doesn't just give a "Normal" or "Abnormal" result; it explains *why* it made that decision and secures the result using blockchain technology.

**The Goal:**
The primary goal is to provide a reliable, transparent, and secure tool for heart health monitoring. By combining AI for detection, SHAP for explanation, and Blockchain for security, the system ensures that medical data is both understandable and tamper-proof.

---

## 2. Technology Stack
*   **Django:** The "brain" of the web application. It handles user accounts, file uploads, and connects all the backend pieces together.
*   **Python:** The core programming language used to write all the logic, from AI models to blockchain simulations.
*   **SQLite:** A lightweight database that stores user profiles, ECG record metadata, and audit logs.
*   **SHAP (SHapley Additive exPlanations):** An "Explainable AI" tool. It shows which parts of the heart signal (like heart rate or beat timing) most influenced the AI's prediction.
*   **Web3 / Blockchain:** Used to create a digital "seal" for every medical result. It ensures that once a prediction is made, it cannot be changed or faked.
*   **WFDB (Waveform Database):** A library used to read specialized medical ECG file formats (`.dat`, `.hea`).
*   **MIT-BIH Dataset:** A world-standard collection of ECG recordings used to train and test our AI model.

---

## 3. Folder Structure Explanation
*   **[dashboard/](file:///d:/smart_ecg/ecg/views.py#213-216)**: Handles the main user interface that the doctor or patient sees.
*   **[ecg/](file:///d:/smart_ecg/ecg/views.py#30-211)**: Contains the core logic for processing heart signals and handling uploads.
*   **`mlmodel/`**: The "AI Lab" where the model is stored and where the prediction logic lives.
*   **[blockchain/](file:///d:/smart_ecg/blockchain/views.py#4-8)**: Contains the security logic for hashing data and logging it to a simulated ledger.
*   **`modern_auth/`**: Manages secure user login, registration, and password resets.
*   **[quality/](file:///d:/smart_ecg/quality/quality_check.py#3-26)**: Checks if the uploaded ECG signal is "clean" enough for the AI to analyze.
*   **`alerts/`**: Responsible for notifying users (e.g., via email or on-screen) if an abnormality is detected.

---

## 4. Important Files Explanation
*   **[views.py](file:///d:/smart_ecg/ecg/views.py)**: The "Controller." It receives requests from the user (like "upload this file"), calls the right functions, and returns a response page.
*   **[models.py](file:///d:/smart_ecg/ecg/models.py)**: Defines the "Data Structure." It tells the database how to store things like user records or blockchain hashes.
*   **[urls.py](file:///d:/smart_ecg/ecg/urls.py)**: The "Router." It maps web addresses (URLs) to specific functions in the backend.
*   **[services.py](file:///d:/smart_ecg/ecg/services.py)**: Contains helper functions for specialized tasks, like reading ECG files or generating graphs.
*   **[shap_explain.py](file:///d:/smart_ecg/mlmodel/shap_explain.py)**: Generates the "Reasoning" behind a prediction by calculating feature importance.
*   **`blockchain_logger.py` / [web3_logger.py](file:///d:/smart_ecg/blockchain/web3_logger.py)**: Handles the communication with the blockchain to store and verify data.
*   **[hqcnn.py](file:///d:/smart_ecg/mlmodel/hqcnn.py)**: Loads the trained AI model and uses it to make predictions on new data.
*   **[features.py](file:///d:/smart_ecg/mlmodel/features.py)**: The "Translator." it converts raw heart signals into numbers (like heart rate) that the AI can understand.
*   **[quality_check.py](file:///d:/smart_ecg/quality/quality_check.py)**: Calculates a "Quality Score" for the ECG to ensure the signal isn't just static or noise.

---

## 5. Backend Workflow
1.  **User Login:** The user signs in securely.
2.  **Dashboard:** The user accesses the main control panel.
3.  **Upload ECG:** The user uploads three files (`.dat`, `.hea`, `.atr`) representing one ECG recording.
4.  **Quality Check:** The system checks if the signal is clear.
5.  **Signal Processing:** The raw data is cleaned and split into smaller segments.
6.  **Feature Extraction:** The system calculates heart rate, beat intervals, and variability.
7.  **AI Prediction:** The HQCNN model analyzes these features to detect arrhythmias.
8.  **SHAP Explainability:** SHAP calculates which features (e.g., high Heart Rate) led to the result.
9.  **Result Generation:** A human-readable report is created with graphs and explanations.
10. **SHA-256 Hashing:** All result data is combined into a unique "fingerprint" (hash).
11. **Blockchain Storage:** This hash is stored on a blockchain ledger for security.
12. **Blockchain Verification:** The system can later re-calculate the hash to prove the data hasn't been changed.

---

## 6. AI Model Explanation
The project uses a model called **HQCNN** (High-Quality Convolutional Neural Network).
*   **Training:** It was trained using the **MIT-BIH Arrhythmia Dataset**, which contains thousands of labeled heartbeats.
*   **Mechanism:** During training, the model "learned" patterns that distinguish a normal heartbeat from various types of arrhythmias.
*   **Prediction:** When a new ECG is uploaded, the model looks for these learned patterns and outputs a classification (Normal or Abnormal).

---

## 7. SHAP Explainability
SHAP is used to solve the "Black Box" problem of AI.
*   **What it does:** It assigns a "contribution value" to each feature. For example, it might say "Heart Rate contributed +0.4 to the abnormality score."
*   **How it works:** It compares what the model predicted with what it *would* have predicted if a certain feature was different.
*   **Clinical Interpretation:** We translate these numbers into simple text, like "The abnormality was detected mainly due to an irregular Heart Rate."

---

## 8. Blockchain Workflow
*   **Hashing:** We take the patient ID, prediction, and timestamp and run them through a **SHA-256** algorithm.
*   **SHA-256:** This is a "one-way" function. Even a tiny change in the data (like changing "Normal" to "Abnormal") will result in a completely different hash.
*   **Storage:** We store this hash on a simulated Ethereum blockchain.
*   **Tamper Detection:** If anyone tries to change the record in the database, the stored blockchain hash will no longer match the recalculated hash, alerting us to the tampering.

---

## 9. Database Usage (SQLite)
The database stores:
*   **Users:** Usernames and encrypted passwords.
*   **ECG Records:** Metadata like patient ID, upload time, and file paths.
*   **Blockchain Records:** A local copy of the hashes and transaction IDs for quick display on the dashboard.
*   **Alerts:** A history of critical logs for abnormal detections.

---

## 10. Complete System Flow (End-to-End)
1.  **Upload:** Patient uploads their ECG files.
2.  **Analyze:** AI Model predicts the health status.
3.  **Explain:** SHAP generates visual and text explanations for the doctor.
4.  **Secure:** The result is hashed and signed onto the Blockchain.
5.  **Report:** The user sees a dashboard with the prediction, the explanation, and a "Verified" badge from the blockchain.
