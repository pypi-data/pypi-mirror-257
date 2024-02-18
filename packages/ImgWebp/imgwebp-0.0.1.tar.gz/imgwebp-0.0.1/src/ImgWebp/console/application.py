
from importlib import import_module
from cleo.application import Application as BaseApplication

from ImgWebp.console.command_loader import CommandLoader
from ImgWebp.console.commands.command import Command

from collections.abc import Callable


def load_command(name: str) -> Callable[[], Command]:
    def _load() -> Command:
        words = name.split(" ")
        module = import_module("ImgWebp.console.commands." + ".".join(words))
        command_class = getattr(module, "".join(c.title() for c in words) + "Command")
        command: Command = command_class()
        return command

    return _load


COMMANDS = [
    "version",
]


class Application(BaseApplication):
    def __init__(self):
        super().__init__("imgc", "0.1.0")
        command_loader = CommandLoader({name: load_command(name) for name in COMMANDS})
        self.set_command_loader(command_loader)


def main() -> int:
    exit_code: int = Application().run()
    return exit_code


if __name__ == "__main__":
    main()
