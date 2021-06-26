"""
A performant numpy extension for Galois fields and their applications.
"""
from .version import __version__

# Subpackages
from .code import *
from .field import *

# Modules
from .factor import *
from .integer import *
from .lfsr import *
from .log import *
from .math_ import *  # pylint: disable=redefined-builtin
from .modular import *
from .prime import *
from .structure import *
