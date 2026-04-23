# CyberGurad

## Malicious URL Detector - Cyber Security Command Center

An advanced, machine learning-powered web application designed to detect malicious URLs. Built with Streamlit, Scikit-Learn, and Python, this tool features a high-contrast "Cyber Security" UI aesthetic and provides real-time analysis of web addresses for potential threats like phishing, malware delivery, and suspicious formatting.

## Features

- **Real-Time URL Scanning**: Instantly analyzes any provided URL.
- **Machine Learning Detection**: Uses a Random Forest Classifier trained on lexical features of URLs.
- **Feature Extraction**: Evaluates 14+ distinct URL characteristics (e.g., URL length, presence of IP addresses, suspicious keywords, excessive hyphens).
- **Cyber Security UI**: A highly stylized, dark-mode, neo-brutalist interface designed to mimic professional security dashboards.
- **Detailed Threat Breakdown**: Instead of just a "Safe" or "Malicious" label, the app shows exactly *why* a URL was flagged.

## Project Structure

- `app.py`: The main Streamlit web application interface.
- `feature_extraction.py`: Contains the logic to parse and extract numerical features from raw URL strings.
- `train_model.py`: Script used to train the Random Forest Classifier on the dataset.
- `generate_dataset.py`: Utility script used to combine and format benign and malicious URLs into a usable CSV dataset.
- `malicious_url_model.pkl`: The serialized, pre-trained machine learning model.
- `requirements.txt`: List of Python dependencies required to run the application.

## Local Installation

1. **Clone the repository or download the files** to your local machine.
2. **Ensure Python 3.8+ is installed.**
3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```
5. **Open your browser** and navigate to the local URL provided in your terminal (usually `http://localhost:8501`).

## How the Detection Works

When you input a URL, the system performs the following steps:
1. **Parser**: Breaks the URL down into its core components (scheme, netloc, path).
2. **Feature Extractor**: Counts suspicious elements (like `@` symbols, multiple domains, shorteners) and measures structural properties.
3. **ML Classifier**: Feeds the extracted properties into the pre-trained `malicious_url_model.pkl`.
4. **Scoring**: Calculates a confidence score. If it exceeds the threshold, the URL is flagged as malicious.

*Disclaimer: This tool is built for educational (Ethical Hacking / Cyber Security coursework) and informational purposes. No automated system is 100% accurate at detecting malicious domains.*
