from __future__ import annotations

from cleo.exceptions import CleoError


class ImgCConsoleError(CleoError):
    pass


class GroupNotFound(ImgCConsoleError):
    pass
