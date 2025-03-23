import telebot
import subprocess
import logging
from pytube import YouTube
from media_downloader import download_tiktok_video, download_instagram_video

# ✅ Replace with your Telegram Bot API Token
import os
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# TELEGRAM_BOT_TOKEN = "7822601607:AAEFaxshn2gUlWMTrWbWvDnyQf2uhI-eErw"

# ✅ Initialize Telegram bot
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# ✅ Set up logging
logging.basicConfig(filename="telegram_bot.log", level=logging.INFO, format="%(asctime)s - %(message)s")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    text = message.text.strip()

    # ✅ Detect the type of video link
    try:
        if "youtube.com/watch?" in text or "youtu.be/" in text:
            bot.send_message(chat_id, f"Processing YouTube video: {text} 🎬")
            try:
                yt = YouTube(text)
                video_title = yt.title
            except Exception as e:
                bot.send_message(chat_id, f"Error fetching YouTube title: {e}")
                return

            command = f'python cli.py upload --user jeffhardy619.0 -yt "{text}" -t "{video_title}"'
            subprocess.Popen(command, shell=True)
            bot.send_message(chat_id, "Upload started! 🚀")

        elif "tiktok.com" in text:
            bot.send_message(chat_id, "Processing TikTok video 🎵...")
            download_result = download_tiktok_video(text)

            if "Error" in download_result:
                bot.send_message(chat_id, f"❌ TikTok download failed: {download_result}")
            else:
                # ✅ Run the TikTok upload after successful download
                command = f'python cli.py upload --user jeffhardy619.0 -v "{download_result}" -t "TikTok Upload"'
                subprocess.Popen(command, shell=True)
                bot.send_message(chat_id, "TikTok video uploaded! 🚀")

#         elif "instagram.com" in text:
#             bot.send_message(chat_id, "Processing Instagram video 📸...")
#             download_result = download_instagram_video(text)

#             if "Error" in download_result:
#                 bot.send_message(chat_id, f"❌ Instagram download failed: {download_result}")
#             else:
#                 # ✅ Run the Instagram upload after successful download
#                 command = f'python cli.py upload --user jeffhardy619.0 -v "{download_result}" -t "Instagram Upload"'
#                 subprocess.Popen(command, shell=True)
#                 bot.send_message(chat_id, "Instagram video uploaded! 🚀")
        elif "instagram.com" in text:
            bot.send_message(chat_id, "Processing Instagram video 📸...")
            download_result = download_instagram_video(text)

            print(f"DEBUG: Download result - {download_result}")  # ✅ Debugging

            if "Error" in download_result:
                bot.send_message(chat_id, f"❌ Instagram download failed: {download_result}")
            else:
                bot.send_message(chat_id, f"Downloaded: {download_result}")

                # ✅ Run the Instagram upload after successful download
                command = f'python cli.py upload --user jeffhardy619.0 -v "{download_result}" -t "Instagram Upload"'
                subprocess.Popen(command, shell=True)
                bot.send_message(chat_id, "Instagram video uploaded! 🚀")


        else:
            bot.send_message(chat_id, "⚠️ Please send a valid YouTube, TikTok, or Instagram link. 🎥")

    except Exception as e:
        bot.send_message(chat_id, "⚠️ An error occurred while processing your request.")
        logging.error(f"Error handling message: {e}")

# ✅ Start the bot
print("Telegram bot is running... 🚀")
bot.polling()
















# @bot.message_handler(func=lambda message: True)
# def handle_message(message):
#     chat_id = message.chat.id
#     text = message.text.strip()

#     # ✅ Check if the message is a YouTube link
#     if "youtube.com/watch?" in text or "youtu.be/" in text:
#         bot.send_message(chat_id, f"Processing YouTube video: {text} 🎬")

#         # ✅ Run TikTok upload command in the background
#         command = f'python cli.py upload --user jeffhardy619.0 -yt "{text}" -t "Auto-generated upload"'
#         subprocess.Popen(command, shell=True)

#         bot.send_message(chat_id, "Upload started! 🚀")

#     else:
#         bot.send_message(chat_id, "Please send a valid YouTube link. 🎥")

# # ✅ Start the bot
# print("Bot is running...")
# bot.polling()
