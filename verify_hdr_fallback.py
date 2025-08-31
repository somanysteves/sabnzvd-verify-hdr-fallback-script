#!/usr/bin/env python
import os
import subprocess

def get_ffprobe_output(file_path):
    result = subprocess.run(['ffprobe', file_path], capture_output=True, text=True)
    output = result.stdout + result.stderr
    return output

def verify_hdr_fallback(metadata):
    print(metadata)
    # Check for Dolby Vision profiles and HDR10 fallback
    if "dovi" in metadata or 'DOVI' in metadata:
        if "smpte2084" in metadata:
            print(f"File has Dolby Vision with an HDR fallback.")
            return True
        elif "arib-std-b67" in metadata:
            print(f"File has Dolby Vision with an HLG fallback.")
            return True
        else:
            print(f"File has Dolby Vision but no detected HDR fallback.")
            return False
    else:
        print(f"File is not a Dolby Vision file. Assuming no fallback needed.")
        return True

def install_prereqs():
    subprocess.run(['apk', 'update'], capture_output=True, text=True)
    subprocess.run(['apk', 'add', 'ffmpeg'], capture_output=True, text=True)

def verify_hdr_fallback_on_file(file_path):
    output = get_ffprobe_output(file_path)
    return verify_hdr_fallback(output)

def get_media_files(directory_path, media_extensions=None):
    """
    Retrieves a list of all media files within a specified directory and its subdirectories.

    Args:
        directory_path (str): The path to the directory to search.
        media_extensions (list, optional): A list of file extensions to consider as media.
                                          Defaults to common image, audio, and video extensions.

    Returns:
        list: A list of absolute paths to the media files found.
    """
    if media_extensions is None:
        media_extensions = [
            '.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm'   # Video
        ]

    media_files = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_extension = os.path.splitext(file)[1].lower()
            if file_extension in media_extensions:
                return os.path.join(root, file)

if __name__ == "__main__":
    install_prereqs()
    complete_path = os.environ['SAB_COMPLETE_DIR']
    file_path = get_media_files(complete_path)
    print(f"File path: {file_path}")
    result = verify_hdr_fallback_on_file(file_path)
    print(f"result was {result}")
    if result is False:
        print("No HDR fallback detected.")
        raise ValueError("No HDR fallback detected")

    print('File is fine')
