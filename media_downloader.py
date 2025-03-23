import os
import yt_dlp
import instaloader
import subprocess

# ✅ Ensure the download directory exists
DOWNLOAD_DIR = "VideosDirPath"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_tiktok_video(url):
    """Download a TikTok video using yt-dlp."""
    try:
        ydl_opts = {
            "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return f"Downloaded TikTok video to {DOWNLOAD_DIR}"
    except Exception as e:
        return f"Error downloading TikTok video: {e}"

   



# def download_instagram_video(url):
#     """Download an Instagram post and return the absolute MP4 file path."""
#     try:
#         L = instaloader.Instaloader()
#         shortcode = url.split("/")[-2]
#         post = instaloader.Post.from_shortcode(L.context, shortcode)
#         L.download_post(post, target=DOWNLOAD_DIR)

#         print("DEBUG: Files in directory after download:", os.listdir(DOWNLOAD_DIR))  # ✅ Debugging

#         for file in os.listdir(DOWNLOAD_DIR):
#             if file.endswith(".mp4"):
#                 video_path = os.path.abspath(os.path.join(DOWNLOAD_DIR, file))  # ✅ Ensure absolute path
#                 print(f"DEBUG: Returning video path {video_path}")  # ✅ Debugging
#                 return video_path

#         return "Error: No MP4 video found after download."

#     except Exception as e:
#         return f"Error downloading Instagram post: {e}"


import os
import instaloader
import subprocess

DOWNLOAD_DIR = "VideosDirPath"

def download_instagram_video(url):
    """Download an Instagram post, remux it for compatibility, and return the absolute MP4 file path."""
    try:
        L = instaloader.Instaloader()
        shortcode = url.split("/")[-2]
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        L.download_post(post, target=DOWNLOAD_DIR)

        print("DEBUG: Files in directory after download:", os.listdir(DOWNLOAD_DIR))  # ✅ Debugging

        for file in os.listdir(DOWNLOAD_DIR):
            if file.endswith(".mp4"):
                original_video_path = os.path.abspath(os.path.join(DOWNLOAD_DIR, file))  # ✅ Get absolute path
                temp_remuxed_path = os.path.join(DOWNLOAD_DIR, "temp_remux.mp4")  # ✅ Temporary file

                # ✅ Remux video (without full re-encode) to fix TikTok playback issues
                ffmpeg_command = [
                    "ffmpeg", "-y", "-i", original_video_path,
                    "-c", "copy", "-movflags", "+faststart", temp_remuxed_path
                ]

                print(f"Remuxing video: {original_video_path} → {temp_remuxed_path}")
                subprocess.run(ffmpeg_command, check=True)

                # ✅ Delete the original video after remuxing
                os.remove(original_video_path)

                # ✅ Rename the remuxed file back to the original filename
                os.rename(temp_remuxed_path, original_video_path)

                print(f"Remuxed and saved: {original_video_path}")
                return original_video_path  # ✅ Return the correct final path

        return "Error: No MP4 video found after download."

    except Exception as e:
        return f"Error downloading Instagram post: {e}"
