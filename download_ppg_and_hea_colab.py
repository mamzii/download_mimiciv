import os
import requests

# Base URL for the MIMIC-IV Waveform Database
base_url = 'https://physionet.org/files/mimic4wdb/0.1.0/'

# Directory to save the PPG signals in Google Drive
output_dir = '/content/drive/MyDrive/mimicppg'
os.makedirs(output_dir, exist_ok=True)

def download_ppg_files(record_path):
    # URLs for the .dat and .hea files
    dat_url = f"{base_url}{record_path}.dat?download"
    hea_url = f"{base_url}{record_path[:-1]}.hea?download"  # Remove last 'p' for .hea file

    # Download the .dat file
    dat_response = requests.get(dat_url)
    if dat_response.status_code != 200:
        raise Exception(f"Failed to download .dat file for {record_path}")

    dat_file_path = os.path.join(output_dir, f"{record_path.replace('/', '_')}.dat")
    with open(dat_file_path, 'wb') as dat_file:
        dat_file.write(dat_response.content)
    print(f'Downloaded PPG signal .dat file: {dat_file_path}')

    # Download the .hea file
    hea_response = requests.get(hea_url)
    if hea_response.status_code != 200:
        print(f"Failed to download .hea file for {record_path}. Trying without 'p' suffix.")

        # Try again without 'p' suffix
        hea_url = f"{base_url}{record_path[:-1]}.hea?download"
        hea_response = requests.get(hea_url)
        if hea_response.status_code != 200:
            raise Exception(f"Failed to download .hea file for {record_path} after removing 'p'")

    hea_file_path = os.path.join(output_dir, f"{record_path.replace('/', '_')[:-1]}.hea")
    with open(hea_file_path, 'wb') as hea_file:
        hea_file.write(hea_response.content)
    print(f'Downloaded PPG signal .hea file: {hea_file_path}')

def process_all_records(records_file_url):
    # Download the main RECORDS file
    records_response = requests.get(records_file_url)
    if records_response.status_code != 200:
        raise Exception(f"Failed to download main RECORDS file: {records_response.status_code}")

    if 'text/html' in records_response.headers['Content-Type']:
        raise Exception("Main RECORDS file URL is returning HTML content instead of plain text.")

    main_records_list = records_response.text.splitlines()

    for subdir in main_records_list:
        print(f'Processing subdirectory: {subdir}')

        # URL of the subdirectory's RECORDS file
        subdir_records_url = f"{base_url}{subdir}/RECORDS?download"
        subdir_response = requests.get(subdir_records_url)

        if subdir_response.status_code != 200:
            print(f"Failed to download subdirectory RECORDS file: {subdir}")
            continue

        subdir_records_list = subdir_response.text.splitlines()

        for subdir_record in subdir_records_list:
            base_name = subdir_record.split('/')[-1]
            for i in range(1, 201):
                record_suffix = f"_{i:04}p"
                record_path = f"{subdir}/{subdir_record}{record_suffix}"

                dat_url = f"{base_url}{record_path}.dat?download"
                dat_response = requests.head(dat_url)

                if dat_response.status_code == 200:
                    try:
                        download_ppg_files(record_path)
                    except Exception as e:
                        print(f'Failed to process {record_path}: {e}')

# URL of the main RECORDS file with ?download to get the plain text file
records_file_url = f'{base_url}RECORDS?download'

# Process all records to download and save PPG signals
process_all_records(records_file_url)
