import os
import requests
import time
import zipfile

def send_file(file_path, webhook_urls):
    file_size = os.path.getsize(file_path)
    webhook_count = len(webhook_urls)

    if file_size <= 25000000: 
        with open(file_path, "rb") as file:
            files = {
                "file": file.read(),
            }

            for webhook_url in webhook_urls:
                requests.post(webhook_url, files=files)
                time.sleep(1) 
    else:
    	
        file_name = os.path.basename(file_path)
        archive_counter = 1
        chunk_size = 25000000

        with open(file_path, "rb") as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break

                archive_name = f"{file_name}_part{archive_counter}.zip"
                with zipfile.ZipFile(archive_name, "w", zipfile.ZIP_DEFLATED) as zip_file:
                    zip_file.writestr(file_name, chunk)

                archive_counter += 1

        current_webhook_index = 0
        for i in range(1, archive_counter):
            archive_name = f"{file_name}_part{i}.zip"
            files = {
                "file": open(archive_name, "rb"),
            }

            webhook_url = webhook_urls[current_webhook_index]
            requests.post(webhook_url, files=files)
            time.sleep(1)

            current_webhook_index = (current_webhook_index + 1) % webhook_count

        for i in range(1, archive_counter):
            archive_name = f"{file_name}_part{i}.zip"
            os.remove(archive_name)

file_name = "Download.7z"  # Replace with the name of the file you want to send
file_path = os.path.join(os.getcwd(), file_name)
webhook_urls = [
    "WEBHOOK",  # Replace with your first Discord webhook URL
    "WEBHOOK",  # Replace with your second Discord webhook URL
    "WEBHOOK"   # Replace with your third Discord webhook URL
]
send_file(file_path, webhook_urls)
