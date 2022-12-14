
from api_youtube_uc import YouTube


def main():

    with YouTube() as youtube_api:
        if youtube_api.auth_youtube("your_email@gmail.com", "Your password", "backup_code"):  # return True or False
            youtube_api.get_backup_code("your_email@gmail.com", "Your password", "backup_code")  # gets list backup codes

        # upload video on the YouTube
        youtube_api.upload_video(r"path/to/video.mp4", "title", "tags1", "tags2", "tags3", "...", "tagsN")

        # old version
        # youtube_api.upload_video(r"path\to\video.mp4", 'Name video', ["#first_tag", "#second_tag"])


if __name__ == '__main__':
    main()
