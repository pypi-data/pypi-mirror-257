from dektools.shell import shell_command
from .base import MarkerShell


class ShellCommand:
    def __init__(self, kwargs):
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        kwargs = kwargs | self.kwargs
        return shell_command(*args, **kwargs)


class ShMarker(MarkerShell):
    tag_head = "@sh"
    shell_cls = ShellCommand
