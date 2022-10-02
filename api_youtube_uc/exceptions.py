class YouTubeException(Exception):
    """Generic exception that all other YouTube errors are children of."""

    def __init__(self, *args):
        self.message = args[0] if args else None
        super().__init__(self.message)

    def __str__(self):
        return f'YouTube_API -> {self.message}'


class NotFoundException(YouTubeException):
    """YouTube indicated that this object does not exist."""


class FieldInvalidException(YouTubeException):
    """This exception occurs when the field is in invalid"""


class LimitSpentException(YouTubeException):
    """Daily upload limit reached"""


class NotBackupCodeException(YouTubeException):
    """Backup code not available"""


class NotExistsProfileException(YouTubeException):
    """You don't have profile by path in Chrom on the Windows10"""


class PreventedThisUpload(YouTubeException):
    """YouTube prevented this upload because it’s a copy of a video we removed in the past."""
