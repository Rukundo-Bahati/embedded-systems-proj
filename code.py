import os
import time
import subprocess
from shutil import move

# Update to Linux-compatible paths
CAMERA_ROLL = "/home/babalao/Pictures/camera_roll"
UPLOAD_FOLDER = os.path.join(CAMERA_ROLL, "uploaded")
URL = "https://projects.benax.rw/f/o/r/e/a/c/h/p/r/o/j/e/c/t/s/4e8d42b606f70fa9d39741a93ed0356c/iot_testing_202501/upload.php"

# Create the upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def upload_file(file_path):
    """Uploads the image file to the specified URL."""
    try:
        command = [
            "curl", "-X", "POST", "-F",
            f"imageFile=@{file_path}", URL
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Successfully uploaded: {file_path}")
            return True
        else:
            print(f"Failed to upload {file_path}: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error during upload of {file_path}: {e}")
        return False

def watch_directory():
    """Continuously monitors the specified folder for new image files."""
    print(f"Starting to monitor: {CAMERA_ROLL}")
    while True:
        # List all image files in the watch folder
        image_files = [
            f for f in os.listdir(CAMERA_ROLL)
            if f.lower().endswith(('.jpg', '.png', '.jpeg'))
        ]
        for image in image_files:
            full_path = os.path.join(CAMERA_ROLL, image)
            destination_path = os.path.join(UPLOAD_FOLDER, image)
            # Skip if the file has already been uploaded
            if os.path.exists(destination_path):
                continue
            print(f"New file detected: {image}")
            time.sleep(30)  # Delay before uploading
            if upload_file(full_path):
                move(full_path, destination_path)
                print(f"Moved {image} to {UPLOAD_FOLDER}")
        time.sleep(10)  # Wait before checking again

if __name__ == "__main__":
    watch_directory()
