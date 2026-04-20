# ThreatScan

# Malicious URL Detector - Cyber Security Command Center

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

## Deployment Guide (Streamlit Community Cloud)

The easiest way to put this app on the internet is using [Streamlit Community Cloud](https://streamlit.io/cloud).

### Prerequisites
- A GitHub account.
- A Streamlit Cloud account (linked to your GitHub).

### Steps to Deploy:
1. **Upload your code to GitHub:**
   - Create a new public (or private) repository on GitHub.
   - Upload all the project files (`app.py`, `feature_extraction.py`, `malicious_url_model.pkl`, `requirements.txt`, etc.) to this repository.
   - *Note: You can exclude `url_dataset.csv` if it's too large, as the app only needs the `.pkl` model file to run.*

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io) and log in.
   - Click the **"New app"** button.
   - Select the GitHub repository you just created.
   - Set the **Main file path** to `app.py`.
   - Click **"Deploy!"**

Within a few minutes, Streamlit will install the dependencies from your `requirements.txt` and your application will be live on the internet with a public, sharable link!

## Note on Custom Fonts and UI (Windows vs Unix Deployments)
The UI heavily relies on custom CSS injected into Streamlit. Ensure that your deployment environment supports the HTML/CSS rendering exactly as viewed locally. Streamlit Cloud handles this perfectly out of the box.

---
*Disclaimer: This tool is built for educational (Ethical Hacking / Cyber Security coursework) and informational purposes. No automated system is 100% accurate at detecting malicious domains.*
