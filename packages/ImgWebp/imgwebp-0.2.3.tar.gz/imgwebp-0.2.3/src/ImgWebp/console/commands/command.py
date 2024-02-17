from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

from cleo.commands.command import Command as BaseCommand
from cleo.exceptions import CleoValueError


if TYPE_CHECKING:
    from ImgWebp.console.application import Application


class Command(BaseCommand):
    loggers: list[str] = []

    def get_application(self) -> Application:
        from ImgWebp.console.application import Application

        application = self.application
        assert isinstance(application, Application)
        return application


    def option(self, name: str, default: Any = None) -> Any:
        try:
            return super().option(name)
        except CleoValueError:
            return default
