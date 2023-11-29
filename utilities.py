# Pranav Minasandra
# pminasandra.github.io
# November 27, 2023

"""
Helpful functions used in all modules.
"""

import inspect
import os
import os.path

import config


def saveimg(obj, name, directory=config.FIGURES):
    """
    Saves given object to directory (default the FIGURES directory in config.py),
    with file formats chosen in config.py.
    Args:
        obj: a matplotlib object with a savefig method (plt or plt.Figure)
        name (str): the name to be given to the file, *without* extensions.
    """
    dirs = [os.path.join(directory, f) for f in config.formats]
    for dir_ in dirs:
        os.makedirs(dir_, exist_ok=True)

    for f in config.formats:
        obj.savefig(os.path.join(directory, f, name+f".{f}"), dpi=500.0, format=f)


def sprint(*args, **kwargs):
    """
    Replacement for ordinary print
    """
    filename = str(inspect.stack()[1].filename)
    print(os.path.basename(filename)+":", *args, **kwargs)
