import os
import requests

# Base URL for the waveform data
base_url = "https://physionet.org/files/mimic-iv-waveforms/1.0.0/"

# List of patient IDs you want to download data for
patient_ids = ["patientNNNN1", "patientNNNN2", "patientNNNN3"]  # Replace with actual patient IDs

# Directory to save downloaded files
download_dir = "mimic_waveforms"

# Ensure the download directory exists
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Function to download a file using wget
def download_file(url, dest):
    command = f"wget -q -O {dest} {url}"
    os.system(command)

# Loop through each patient ID and download the PPG data
for patient_id in patient_ids:
    ppg_url = f"{base_url}{patient_id}/ppg.dat"
    dest_path = os.path.join(download_dir, f"{patient_id}_ppg.dat")

    # Check if the URL exists
    response = requests.head(ppg_url)
    if response.status_code == 200:
        print(f"Downloading {ppg_url}...")
        download_file(ppg_url, dest_path)
        print(f"Downloaded to {dest_path}")
    else:
        print(f"URL does not exist: {ppg_url}")
