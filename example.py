
from api_youtube_uc import YouTube


def main():

    with YouTube() as youtube_api:
        youtube_api.auth("your_email@gmail.com", "Your password")
        youtube_api.upload_video(r"C:\Users\Username\Downloads\download.mp4", 'Name video', ["#first_tag", "#second_tag"])
        youtube_api.DRIVER.close()


if __name__ == '__main__':
    main()
