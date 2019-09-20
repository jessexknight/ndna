r"""I/O functions
"""

import os
from collections import OrderedDict as odict
import simplejson as json

def loadjson(fname, ordered=True):
  r"""Load a JSON file.

  Args:
    fname (str): the file to load
    ordered (bool): return dictionaries as: ``True`` = OrderedDict; ``False`` = dict

  Returns:
    (dict,list): the contents as a dict / list object
  """
  oargs = {'object_pairs_hook': odict} if ordered else {}
  with open(fname,'r') as f:
    return json.load(f,**oargs)

def makedir(directory):
  r"""Just make the damned directory.

  Args:
    directory (str): path to a directory to create
  """
  try:
    os.makedirs(directory,exist_ok=True)
  except AttributeError:
    if not isinstance(directory,str):
      raise TypeError('directory argument must be str, not \'{}\''.format(
        type(directory).__name__))
  except FileNotFoundError:
    if not directory:
      raise ValueError('directory argument must not be empty')
