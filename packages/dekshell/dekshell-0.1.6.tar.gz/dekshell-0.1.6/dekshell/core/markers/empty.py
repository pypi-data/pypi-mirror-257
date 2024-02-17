from dektools.shell import shell_wrapper
from .base import MarkerShell


class ShellCommand:
    def __init__(self, kwargs):
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        kwargs = kwargs | self.kwargs
        return shell_wrapper(*args, **kwargs)


class EmptyMarker(MarkerShell):
    tag_head = ""
    shell_cls = ShellCommand
