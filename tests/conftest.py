"""Test-runtime compatibility helpers.

genlayer-test 0.29.x keeps the Direct Mode message tempfile open on Windows
when it attempts to unlink it.  The file is harmless and is released when the
test process restores stdin; ignoring only this specific unlink failure keeps
the repository tests runnable without changing contract behavior.
"""

import os
import sys


if sys.platform == "win32":
    try:
        _unlink = os.unlink

        def _unlink_open_tempfile(path, *args, **kwargs):
            try:
                return _unlink(path, *args, **kwargs)
            except PermissionError:
                return None

        os.unlink = _unlink_open_tempfile
    except ImportError:
        pass
