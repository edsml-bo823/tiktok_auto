import argparse
from tiktok_uploader.Video import split_video_into_clips 
from tiktok_uploader import tiktok, Video
from tiktok_uploader.basics import eprint
from tiktok_uploader.Config import Config
import time
from tiktok_uploader.Video import split_video_into_clips
import re
import sys, os
from media_downloader import download_tiktok_video, download_instagram_video


if __name__ == "__main__":
    _ = Config.load("./config.txt")
    # print(Config.get().cookies_dir)
    parser = argparse.ArgumentParser(description="TikTokAutoUpload CLI, scheduled and immediate uploads")
    subparsers = parser.add_subparsers(dest="subcommand")

    # Login subcommand.
    login_parser = subparsers.add_parser("login", help="Login into TikTok to extract the session id (stored locally)")
    login_parser.add_argument("-n", "--name", help="Name to save cookie as", required=True)

    # Upload subcommand.
    upload_parser = subparsers.add_parser("upload", help="Upload video on TikTok")
    upload_parser.add_argument("-u", "--users", help="Enter cookie name from login", required=True)
    upload_parser.add_argument("-v", "--video", help="Path to video file")
    upload_parser.add_argument("-yt", "--youtube", help="Enter Youtube URL")
    upload_parser.add_argument("-t", "--title", help="Title of the video", required=True)
    upload_parser.add_argument("-sc", "--schedule", type=int, default=0, help="Schedule time in seconds")
    upload_parser.add_argument("-ct", "--comment", type=int, default=1, choices=[0, 1])
    upload_parser.add_argument("-d", "--duet", type=int, default=0, choices=[0, 1])
    upload_parser.add_argument("-st", "--stitch", type=int, default=0, choices=[0, 1])
    upload_parser.add_argument("-vi", "--visibility", type=int, default=0, help="Visibility type: 0 for public, 1 for private")
    upload_parser.add_argument("-bo", "--brandorganic", type=int, default=0)
    upload_parser.add_argument("-bc", "--brandcontent", type=int, default=0)
    upload_parser.add_argument("-ai", "--ailabel", type=int, default=0)
    upload_parser.add_argument("-p", "--proxy", default="")

    # Show cookies
    show_parser = subparsers.add_parser("show", help="Show users and videos available for system.")
    show_parser.add_argument("-u", "--users", action='store_true', help="Shows all available cookie names")
    show_parser.add_argument("-v", "--videos",  action='store_true', help="Shows all available videos")

    # Parse the command-line arguments
    args = parser.parse_args()

    if args.subcommand == "login":
        if not hasattr(args, 'name') or args.name is None:
            parser.error("The 'name' argument is required for the 'login' subcommand.")
        # Name of file to save the session id.
        login_name = args.name
        # Name of file to save the session id.
        tiktok.login(login_name)

   
# ===================================================================================================
    elif args.subcommand == "upload":
        if not hasattr(args, 'users') or args.users is None:
            parser.error("The 'cookie' argument is required for the 'upload' subcommand.")

        if args.video is None and args.youtube is None:
            eprint("No source provided. Use -v or -yt to provide video source.")
            sys.exit(1)
        if args.video and args.youtube:
            eprint("Both -v and -yt flags cannot be used together.")
            sys.exit(1)

        if args.youtube:
            if "tiktok.com" in args.youtube:
                print("Detected TikTok video 🎵...")
                download_result = download_tiktok_video(args.youtube)
                print(download_result)
                full_video_path = os.path.abspath(download_result)  # Get full path
                
#             elif "instagram.com" in args.youtube:
#                 print("Detected Instagram video 📸...")
#                 download_result = download_instagram_video(args.youtube)

#                 print(f"DEBUG: Download result path → {download_result}")  # ✅ Debugging

#                 if "Error" in download_result or not os.path.exists(download_result):
#                     print(f"[-] Video does not exist: {download_result}")
#                     sys.exit(1)

#                 full_video_path = os.path.abspath(download_result)  # ✅ Ensure absolute path
#                 print(f"✅ Found video: {full_video_path}")  # ✅ Debugging



            elif "instagram.com" in args.youtube:
                print("Detected Instagram video 📸...")
                download_result = download_instagram_video(args.youtube)
                print(download_result)
                full_video_path = os.path.abspath(download_result)  # Get full path
            else:
                video_obj = Video(args.youtube, args.title)
                video_obj.is_valid_file_format()
                full_video_path = video_obj.source_ref  # Path to downloaded video
                args.video = full_video_path

        else:
            full_video_path = os.path.join(os.getcwd(), Config.get().videos_dir, args.video)

            if not os.path.exists(full_video_path):
                print("[-] Video does not exist")
                sys.exit(1)

        # ✅ Split video into 62-second clips
        clips_dir = os.path.join(os.getcwd(), Config.get().videos_dir, "split_clips")
        clip_data = split_video_into_clips(full_video_path, clips_dir)  # Returns list of {path, part}

        # ✅ Upload each clip every 15 minutes with "Part X" in the caption
        for clip in clip_data:
            clip_path = clip["path"]
            part_number = clip["part"]

            # ✅ Ensure "Part X" appears BEFORE hashtags only if there are multiple clips
            # ✅ Ensure hashtags are properly formatted for TikTok
            # ✅ Ensure hashtags are properly formatted for TikTok
            

            # ✅ Ensure hashtags are properly spaced & formatted
            title_parts = args.title.split("#")  # Split at hashtags
            main_caption = title_parts[0].strip()  # Main caption without hashtags
            hashtags = " ".join(f"#{tag.strip()}" for tag in title_parts[1:])  # Reformat hashtags

            if len(clip_data) > 1:
                caption = f"Part {part_number} - {main_caption} {hashtags}".strip()
            else:
                caption = f"{main_caption} {hashtags}".strip()  # No "Part X" for single videos


            print(f"Uploading {clip_path} with caption: '{caption}'")
            tiktok.upload_video(args.users, clip_path, caption, args.schedule, args.comment, args.duet, args.stitch, args.visibility, args.brandorganic, args.brandcontent, args.ailabel, args.proxy)

            # ✅ Delete the clip after upload
            if os.path.exists(clip_path):
                os.remove(clip_path)
                print(f"Deleted clip: {clip_path}")

            # ✅ Wait 15 minutes before uploading the next clip
            if clip != clip_data[-1]:  # Don't wait after last clip
                print("Waiting 15 minutes before next upload...")
                time.sleep(6)  # 900 seconds = 15 minutes



        # ✅ Delete the full original video after all clips are uploaded
        if os.path.exists(full_video_path):
            os.remove(full_video_path)
            print(f"Deleted original video: {full_video_path}")

            # ✅ Delete the metadata files (JPG, JSON.XZ, TXT)
            metadata_extensions = [".jpg", ".json.xz", ".txt"]
            metadata_dir = os.path.dirname(full_video_path)

            for file in os.listdir(metadata_dir):
                if any(file.endswith(ext) for ext in metadata_extensions):
                    file_path = os.path.join(metadata_dir, file)
                    os.remove(file_path)
                    print(f"Deleted metadata file: {file_path}")

        # ✅ Delete the video after upload (if needed)
        if args.video and os.path.exists(args.video):
            os.remove(args.video)
            print(f"Deleted video: {args.video}")


                
                
                
    elif args.subcommand == "show":
        # if flag is c then show cookie names
        if args.users:
            print("User Names logged in: ")
            cookie_dir = os.path.join(os.getcwd(), Config.get().cookies_dir)
            for name in os.listdir(cookie_dir):
                if name.startswith("tiktok_session-"):
                    print(f'[-] {name.split("tiktok_session-")[1]}')

        # if flag is v then show video names
        if args.videos:
            print("Video Names: ")
            video_dir = os.path.join(os.getcwd(), Config.get().videos_dir)
            for name in os.listdir(video_dir):
                print(f'[-] {name}')
        elif not args.users and not args.videos:
            print("No flag provided. Use -c (show all cookies) or -v (show all videos).")

    else:
        eprint("Invalid subcommand. Use 'login' or 'upload' or 'show'.")


