from dektools.shell import shell_wrapper
from .base import MarkerShell


class ShellCommand:
    def __init__(self, kwargs):
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        kwargs = kwargs | self.kwargs
        return shell_wrapper(args[0], kwargs.get('check', True))


class EmptyMarker(MarkerShell):
    tag_head = ""
    shell_cls = ShellCommand
