"""
Excepted that you already have a "Profiles" folder with profiles
"""

# if you want to convert to executable file
from multiprocessing import freeze_support

import os

from api_youtube_uc import YouTube
from api_youtube_uc.exceptions import *


def use_api():
    profiles = os.listdir("path/to/Profiles")  # path to folder with profile

    for profile in profiles:
        print(profile)
        user_data_dir = "path/to/Profiles" / profile / "User Data"

        with YouTube(user_data_dir=user_data_dir) as youtube_api:

            try:
                youtube_api.upload_video(r"path/to/video.mp4", "title", "tags1", "tags2", "tags3", "...", "tagsN")

            except LimitSpentException:
                print(f"Limit Spent: {profile}")

                continue


if __name__ == "__main__":
    try:
        freeze_support()
        use_api()
    finally:
        print("Натисни Enter: ")







"""Best Regards"""
