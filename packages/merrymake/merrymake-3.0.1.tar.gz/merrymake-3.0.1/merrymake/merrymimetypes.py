class MerryMimetype:

    def __init__(self, _type, tail):

        self._type = _type
        self.tail = tail

    def __str__(self) -> str:
            return f"{self._type}/{self.tail}"

class MerryMimetypes:

    @staticmethod
    def get_mime_type(mimetype):

        value = MerryMimetypes.mimetypes.get(mimetype)

        if value is not None:
            return value
        else:
            raise Exception("Unknown file type. Add mimeType argument.")

    mimetypes = {
        "aac": MerryMimetype("audio", "aac"),
        "abw": MerryMimetype("application", "x-abiword"),
        "arc": MerryMimetype("application", "x-freearc"),
        "avif": MerryMimetype("image", "avif"),
        "avi": MerryMimetype("video", "x-msvideo"),
        "azw": MerryMimetype("application", "vnd.amazon.ebook"),
        "bin": MerryMimetype("application", "octet-stream"),
        "bmp": MerryMimetype("image", "bmp"),
        "bz": MerryMimetype("application", "x-bzip"),
        "bz2": MerryMimetype("application", "x-bzip2"),
        "cda": MerryMimetype("application", "x-cdf"),
        "csh": MerryMimetype("application", "x-csh"),
        "css": MerryMimetype("text", "css"),
        "csv": MerryMimetype("text", "csv"),
        "doc": MerryMimetype("application", "msword"),
        "docx": MerryMimetype("application", "vnd.openxmlformats-officedocument.wordprocessingml.document"),
        "eot": MerryMimetype("application", "vnd.ms-fontobject"),
        "epub": MerryMimetype("application", "epub+zip"),
        "gz": MerryMimetype("application", "gzip"),
        "gif": MerryMimetype("image", "gif"),
        "htm": MerryMimetype("text", "html"),
        "html": MerryMimetype("text", "html"),
        "ico": MerryMimetype("image", "vnd.microsoft.icon"),
        "ics": MerryMimetype("text", "calendar"),
        "jar": MerryMimetype("application", "java-archive"),
        "jpeg": MerryMimetype("image", "jpeg"),
        "jpg": MerryMimetype("image", "jpeg"),
        "js": MerryMimetype("text", "javascript"),
        "json": MerryMimetype("application", "json"),
        "jsonld": MerryMimetype("application", "ld+json"),
        "mid": MerryMimetype("audio", "midi"),
        "midi": MerryMimetype("audio", "midi"),
        "mjs": MerryMimetype("text", "javascript"),
        "mp3": MerryMimetype("audio", "mpeg"),
        "mp4": MerryMimetype("video", "mp4"),
        "mpeg": MerryMimetype("video", "mpeg"),
        "mpkg": MerryMimetype("application", "vnd.apple.installer+xml"),
        "odp": MerryMimetype("application", "vnd.oasis.opendocument.presentation"),
        "ods": MerryMimetype("application", "vnd.oasis.opendocument.spreadsheet"),
        "odt": MerryMimetype("application", "vnd.oasis.opendocument.text"),
        "oga": MerryMimetype("audio", "ogg"),
        "ogv": MerryMimetype("video", "ogg"),
        "ogx": MerryMimetype("application", "ogg"),
        "opus": MerryMimetype("audio", "opus"),
        "otf": MerryMimetype("font", "otf"),
        "png": MerryMimetype("image", "png"),
        "pdf": MerryMimetype("application", "pdf"),
        "php": MerryMimetype("application", "x-httpd-php"),
        "ppt": MerryMimetype("application", "vnd.ms-powerpoint"),
        "pptx": MerryMimetype("application", "vnd.openxmlformats-officedocument.presentationml.presentation"),
        "rar": MerryMimetype("application", "vnd.rar"),
        "rtf": MerryMimetype("application", "rtf"),
        "sh": MerryMimetype("application", "x-sh"),
        "svg": MerryMimetype("image", "svg+xml"),
        "tar": MerryMimetype("application", "x-tar"),
        "tif": MerryMimetype("image", "tiff"),
        "tiff": MerryMimetype("image", "tiff"),
        "ts": MerryMimetype("video", "mp2t"),
        "ttf": MerryMimetype("font", "ttf"),
        "txt": MerryMimetype("text", "plain"),
        "vsd": MerryMimetype("application", "vnd.visio"),
        "wav": MerryMimetype("audio", "wav"),
        "weba": MerryMimetype("audio", "webm"),
        "webm": MerryMimetype("video", "webm"),
        "webp": MerryMimetype("image", "webp"),
        "woff": MerryMimetype("font", "woff"),
        "woff2": MerryMimetype("font", "woff2"),
        "xhtml": MerryMimetype("application", "xhtml+xml"),
        "xls": MerryMimetype("application", "vnd.ms-excel"),
        "xlsx": MerryMimetype("application", "vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
        "xml": MerryMimetype("application", "xml"),
        "xul": MerryMimetype("application", "vnd.mozilla.xul+xml"),
        "zip": MerryMimetype("application", "zip"),
        "3gp": MerryMimetype("video", "3gpp"),
        "3g2": MerryMimetype("video", "3gpp2"),
        "7z": MerryMimetype("application", "x-7z-compressed"),
    }
