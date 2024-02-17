# -*- coding: utf-8 -*-
#
# Licensed under the terms of the BSD 3-Clause
# (see cdl/LICENSE for details)

"""
HDF5 browser test 1

Try and open all HDF5 test data available.
"""

# guitest: show

from guidata.qthelpers import exec_dialog, qt_app_context

from cdl.env import execenv
from cdl.tests.data import get_test_fnames
from cdl.widgets.h5browser import H5BrowserDialog


def test_h5browser(pattern=None):
    """HDF5 browser test"""
    with qt_app_context():
        fnames = get_test_fnames("*.h5" if pattern is None else pattern)
        for index, fname in enumerate(fnames):
            execenv.print(f"Opening: {fname}")
            dlg = H5BrowserDialog(None, size=(1050, 450))
            dlg.setup(fname)
            dlg.browser.tree.toggle_all(True)
            dlg.browser.tree.select_all(True)
            dlg.setObjectName(dlg.objectName() + f"_{index:02d}")
            exec_dialog(dlg)


if __name__ == "__main__":
    test_h5browser()
