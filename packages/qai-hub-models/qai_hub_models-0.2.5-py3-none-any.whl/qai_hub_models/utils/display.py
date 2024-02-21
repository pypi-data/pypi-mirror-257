from __future__ import annotations

from PIL.Image import Image
from PIL.ImageShow import IPythonViewer, _viewers  # type: ignore


def is_running_in_notebook():
    try:
        from IPython import get_ipython

        if "IPKernelApp" not in get_ipython().config:  # pragma: no cover
            return False
    except ImportError:
        return False
    except AttributeError:
        return False
    return True


def display_image(image: Image) -> bool:
    """
    Return True if displaying was attempted.
    Forces inline display on iPython notebooks
    """
    # Disply IPython viewer first
    if is_running_in_notebook():
        for viewer in _viewers:
            if isinstance(viewer, IPythonViewer):
                viewer.show(image)
                return True

    try:
        image.show()
        return True
    except Exception:
        print("Failure to display demo images displayed on screen.")
        print(
            "If you are using a notebook environment like Jupyter/Collab, please use %run -m to run the script instead of python -m."
        )
        print("If running locally on Linux, please setup SSH port forwarding.")
        return False
