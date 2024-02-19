from __future__ import annotations

import subprocess
import os

from ImgWebp.utils.path import get_unpack_path
from ImgWebp.console.commands.command import Command


class VersionCommand(Command):
    name = "version"
    description = (
        "View the version of libwebp."
    )


    def handle(self):
        script_path = os.path.join(get_unpack_path(), "bin", "dwebp")
        args = ['-version']
        self.add_style('fire', fg='green', options=['bold', 'blink'])
        text = 'libwebp version: '
        try:
            result = subprocess.run([script_path] + args, capture_output=True, text=True)
            if result.returncode == 0:
                text += result.stdout
            else:
                text += result.stderr

            self.line(f'<fire>{text}</>')

        except Exception as e:
            raise e
