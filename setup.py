from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.2'
DESCRIPTION = 'Upload shorts video to the YouTube channel'
LONG_DESCRIPTION = "It doesn't use APIv.3 and. Made on the basis of the Selenium(undetected_chromedriver)"

# Setting up
setup(
    name="api_youtube_uc",
    version=VERSION,
    author="ArtDanger",
    author_email="danya221299@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['undetected_chromedriver', "pyperclip", "pyautogui"],
    keywords=['python', 'selenium', 'youtube studio', 'youtube', 'api', 'upload', 'video', 'shorts video',
              'auth google', 'undetected_chromedriver', "uc", "api_youtube_uc", "api_youtube", "youtube_api",
              "api youtube", "youtube api"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
    ]
)
