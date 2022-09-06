
from youtube_api import YouTube


def main():

    youtube_ = YouTube()
    youtube_.auth("e48320035@gmail.com", "Jesus8800")
    # youtube_.auth("your_email@gmail.com", "Your password")
    youtube_.upload_video(r"C:\Users\Username\Downloads\download.mp4", 'Name video', '#mine_first_video #hastags_for_the_video')


if __name__ == '__main__':
    main()
