from django.conf import settings
from django.core.files.storage import FileSystemStorage


class PrivateSubmissionStorage(FileSystemStorage):
    """Filesystem storage with no public URL for learner evidence."""
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("location", settings.PRIVATE_UPLOAD_ROOT)
        kwargs.setdefault("base_url", None)
        super().__init__(*args, **kwargs)

    def url(self, name):
        raise ValueError("Private submission files do not have public URLs.")
