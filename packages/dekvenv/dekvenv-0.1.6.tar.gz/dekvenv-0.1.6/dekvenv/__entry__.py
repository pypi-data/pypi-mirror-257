from dektools.shell import shell_wrapper
from .command import app


def main():
    shell_wrapper('pdm config check_update false')
    shell_wrapper('pdm config install.cache on')
    app()
