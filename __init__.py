import os
import sys
import numpy as np

if os.isatty(sys.stdout.fileno()):
	np.set_printoptions(linewidth=os.get_terminal_size().columns, suppress=True)
