from __future__ import annotations


from cleo.helpers import argument
from cleo.helpers import option

from ImgWebp.console.commands.command import Command



class VersionCommand(Command):
    name = "version"
    description = (
        "Shows the version of the project or bumps it when a valid "
        "bump rule is provided."
    )

    arguments = [
        argument(
            "version",
            "The version number or the rule to update the version.",
            optional=True,
        ),
    ]


    def handle(self) -> int:
        version = self.argument("version")

        print(version)

        return 0
