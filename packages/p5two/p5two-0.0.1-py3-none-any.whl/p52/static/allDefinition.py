# type: ignore

# these "import"s are only needed to have autocomplete inside the sketch
# these are never actually run by python (the execution of the python script itself terminates with the sys.exit(0) call

import sys

sys.exit(0)

from .p5definition import *  # original p5 definition
from ..utils.p52 import *  # custom stuff I added

# 'fake' empty object so that can we use it w/o warning inside the sketch
self = {}
