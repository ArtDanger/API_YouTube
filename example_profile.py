
from api_youtube_uc import YouTube
from api_youtube_uc.selenium_driver import BaseClass


def main():

    # run this function to get your Profiles(Windows 10)
    profiles = BaseClass.find_profiles()  # return list["Profile 1", "Profile 5", ...]
    for profile in profiles:
        with YouTube(profile=profile) as youtube_api:

            # upload video on the YouTube
            youtube_api.upload_video(r"path\to\video.mp4", 'Name video', ["#first_tag", "#second_tag"])


if __name__ == '__main__':
    main()
