class YouTubeException(Exception):
    """Generic exception that all other YouTube errors are children of."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'YouTube_API -> {self.message}'


class NotFoundException(YouTubeException):
    """YouTube indicated that this object does not exist."""


class VideoCopyrightException(YouTubeException):
    """When uploading to YouTube, the video was blocked due to copyright."""


class FieldInvalidException(YouTubeException):
    """This exception occurs when the field is in invalid"""


class LimitSpent(YouTubeException):
    """Daily upload limit reached"""
