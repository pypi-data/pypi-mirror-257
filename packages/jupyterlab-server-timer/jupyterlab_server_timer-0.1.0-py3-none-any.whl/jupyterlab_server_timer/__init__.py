try:
    from ._version import __version__
except ImportError:
    # Fallback when using the package in dev mode without installing
    # in editable mode with pip. It is highly recommended to install
    # the package from a stable release or in editable mode: https://pip.pypa.io/en/stable/topics/local-project-installs/#editable-installs
    import warnings
    warnings.warn("Importing 'jupyterlab_server_timer' outside a proper installation.")
    __version__ = "dev"
from .handlers import setup_handlers


def _jupyter_labextension_paths():
    return [{
        "src": "labextension",
        "dest": "jupyterlab-server-timer"
    }]


def _jupyter_server_extension_points():
    return [{
        "module": "jupyterlab_server_timer"
    }]


def _load_jupyter_server_extension(server_app):
    setup_handlers(server_app.web_app)
    name = "jupyterlab_server_timer"
    server_app.log.info(f"Registered {name} server extension")
