import sys
import os
from os.path import join


def get_version():
    """
    Find the value assigned to __version__ in ufunkify/__init__.py.

    This function assumes that there is a line of the form

        __version__ = "version-string"

    in __init__.py.  It returns the string version-string, or None if such a
    line is not found.
    """
    with open(join("ufunkify", "__init__.py"), "r") as f:
        for line in f:
            s = [w.strip() for w in line.split("=", 1)]
            if len(s) == 2 and s[0] == "__version__":
                return s[1][1:-1]


def generate_ufunkify_code():
    import subprocess

    cwd = os.getcwd()
    os.chdir(join(cwd, 'src'))
    subprocess.run([sys.executable, '_generate_files.py'])
    os.chdir(cwd)


def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration, get_info

    config = Configuration(None, parent_package, top_path)
    config.add_subpackage('ufunkify')

    config.add_extension('ufunkify._ufunkify',
                         extra_compile_args=['-std=c99'],
                         sources=[
                            join('src', '_ufunkify_opcodes.c'),
                            join('src', '_ufunkify_c_function_wrappers.c'),
                            join('src', '_ufunkify.c')
                         ])
    return config


if __name__ == "__main__":
    from numpy.distutils.core import setup

    # This is probably not the best way to do this...
    generate_ufunkify_code()

    setup(name='ufunkify',
          version=get_version(),
          configuration=configuration)
