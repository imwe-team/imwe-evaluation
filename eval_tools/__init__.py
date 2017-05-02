import matplotlib as mpl
import matplotlib.font_manager as fm
from matplotlib import cm
import os

from . import plotting
from . import io
from . import tools

fpath = '/home/jbuss/.local/share/fonts/CaesarDressing-Regular.ttf'

if os.path.exists(fpath):
    prop = fm.FontProperties(fname=fpath, size=16)
    fname = os.path.split(fpath)[1]
else:
    prop = fm.FontProperties(fname=None)
    fname = None



age_categories=['< 18', '18-25', '26-30', '> 30']

rating_categories = ['Very good', 'Good', 'Okay', 'Not so good', 'Bad']

binary_categories=['Yes', 'No']
