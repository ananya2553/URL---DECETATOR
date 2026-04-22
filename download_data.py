import os
import requests

def download_dataset():
    """
    Downloads the Malicious URLs dataset (malicious_phish.csv) from a reliable mirror.
    The original source is Kaggle (sid321axn/malicious-urls-dataset).
    """
    url = "https://raw.githubusercontent.com/mango-cat/ECS171-Project/main/malicious_phish.csv"
    output_path = "malicious_phish.csv"

    print(f"🌐 Fetching Neural Engine Training Data...")
    print(f"Source Node: {url}")
    
    try:
        # Check if file already exists
        if os.path.exists(output_path):
            size = os.path.getsize(output_path) / (1024*1024)
            print(f"ℹ️ File already exists in this node ({size:.2f} MB). Skipping download.")
            return

        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Download with progress simulation
        print("⚡ Downloading data packets...")
        with open(output_path, "wb") as f:
            downloaded = 0
            for chunk in response.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    print(f"📡 Progress: {downloaded / (1024*1024):.1f} MB downloaded...", end="\r")
        
        print(f"\n✅ Data Node Synchronized! Path: {os.path.abspath(output_path)}")
        print(f"Total Size: {os.path.getsize(output_path) / (1024*1024):.2f} MB")
        
    except Exception as e:
        print(f"\n❌ Error during synchronization: {e}")
        print("Suggestion: Manually download from Kaggle and place in this directory as 'malicious_phish.csv'.")

if __name__ == "__main__":
    download_dataset()
