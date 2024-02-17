import sys
import typer
from dektools.shell import shell_wrapper
from dektools.file import remove_path

app = typer.Typer(add_completion=False)


@app.command(
    context_settings=dict(resilient_parsing=True)
)
def install():
    argv = sys.argv[sys.argv.index(install.__name__) + 1:]
    shell_wrapper(f'pdm install {" ".join(argv)}')


@app.command()
def clear():
    from .core import get_pdm_cache_dir
    shell_wrapper(f'pdm cache clear')
    remove_path(get_pdm_cache_dir())


@app.command()
def clear_hash():
    from .core import get_pdm_cache_dir_hash
    remove_path(get_pdm_cache_dir_hash())
