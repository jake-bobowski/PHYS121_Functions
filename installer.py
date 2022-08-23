import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm # used to generate a sequence of colours for plotting
from scipy.optimize import curve_fit
from IPython.display import HTML as html_print
from IPython.display import display, Markdown, Latex


###############################################################################
# For printing outputs in colour (copied from Stack Overflow)                 #
# - modified 20220607                                                         #
############################################################################### 
# Start the 'cstr' function.
def cstr(s, color = 'black'):
    return "<text style=color:{}>{}</text>".format(color, s)


###############################################################################
# Check to see if required packages are already installed.                    #
# If not, then install them.                                                  #
# - modified 20220822                                                         #
############################################################################### 
# Start the 'Check' function.
def Check():
    import importlib.util
    import sys
    import subprocess
    cnt = 0
    package_names = ['ipysheet', 'uncertainties', 'httpimport']
    for name in package_names:
        spec = importlib.util.find_spec(name)
        if spec is None:
            display(html_print(cstr('Installing some packages ...\n', color = 'red')))
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--user', name])
            cnt += 1
                
    if cnt == 0:
        display(html_print(cstr('All packages already installed. Please proceed.', color = 'black')))
    else:
        display(html_print(cstr('\n Some packages were installed.  Please completely log out and then login again before proceeding.', color = 'red')))