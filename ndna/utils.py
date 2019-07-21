r"""Utility functions
"""

import os
import csv
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

def savejson(fname,data,append=False,indent=None,**kwargs):
  r"""Save a dict / list object to a JSON file.

  Args:
    fname (str): the file to write
    data (dict,list): a the data to write to file
    append (bool): if ``True``: append to file; if ``False``: overwrite it
    indent (None,int): number of spaces of indentation or ``None`` for no newlines at all
    **kwargs: additional keyword arguments to pass to ``json.dump``
  """
  if (not append) or (not os.path.exists(fname)):
    # no append
    fdata = data
  else:
    fdata = loadjson(fname)
    if isinstance(fdata,list):
      if isinstance(data,list):
        # list to list: extend
        fdata.extend(data)
      else:
        # obj to list: append
        fdata.append(data)
    elif isinstance(fdata,dict):
      if isinstance(data,dict):
        # dict to dict: update
        fdata.update(data)
      else:
        # obj to dict: error
        raise(TypeError('Cannot add {} data to {} data found in {}'.format(
          type(data),type(fdata),fname
        )))
    else:
      # obj to obj: error
      raise(TypeError('Cannot append {} data onto {} data found in {}'.format(
        type(data),type(fdata),fname
      )))
  makedir(os.path.split(fname)[0])
  with open(fname,'w') as f:
    json.dump(fdata,f,ignore_nan=True,indent=indent,**kwargs)

def loadtxt(fname,dtype=None):
  r"""Load a text file.

  Args:
    fname (str): the file to load
    dtype (type): a datatype to cast the result; default: ``float``

  Returns:
    (dtype): the file contents
  """
  dtype = dtype if dtype is not None else float
  with open(fname,'r') as f:
    return dtype(f.read())

def savetxt(fname,obj):
  r"""Save an object to file as a string.

  Args:
    fname (str): the file to write
    obj (object): an object to write to file as a string
  """
  makedir(os.path.split(fname)[0])
  with open(fname,'w') as f:
    f.write(str(obj))

def loadcsv(fname,asdict=True):
  r"""Read a CSV file into a dict / list.

  Args:
    fname (str): the file to load
    asdict (bool): load the file as: ``True`` = a list of dictionaries; ``False`` = a list of lists

  Returns:
    (list): the file contents
  """
  opts = {
    'delimiter': ',',
    'quotechar': '"',
  }
  with open(fname,'r') as f:
    if asdict:
      reader = csv.DictReader(f,**opts)
    else:
      reader = csv.reader(f,**opts)
    return [row for row in reader]

def savecsv(fname,data,append=True):
  r"""Save a dict / list into a CSV file.

  If **data** is a dictionary, and the file is new, a header row is added to the CSV file.
  If **data** is a list, no header row is added.

  Args:
    fname (str): the file to write
    data (dict,list): an object to write to file
    append (bool): if ``True``: append to file; if ``False``: overwrite it
  """
  opts = {
    'delimiter': ',',
    'quotechar': '"',
  }
  makedir(os.path.split(fname)[0])
  if append:
    new = not os.path.isfile(fname)
    f = open(fname,'a')
  else:
    new = True
    f = open(fname,'w')
  if isinstance(data[0],list):
    writer = csv.writer(f,**opts)
  elif isinstance(data[0],dict):
    writer = csv.DictWriter(f,data[0].keys(),**opts)
    if new:
      writer.writeheader()
  else:
    raise NotImplementedError('Unsupported csv ')
  for row in data:
    writer.writerow(row)
  f.close()

def makedir(directory):
  r"""Just make the damned directory.

  Args:
    directory (str): path to a directory to create
  """
  try:
    os.makedirs(directory,exist_ok=True)
  except:
    pass

def remove(fname):
  r"""Just remove the damned file or directory.

  Args:
    fname (str): a file or directory to remove
  """
  try:
    os.remove(fname)
  except:
    try:
      os.rmdir(fname)
    except:
      pass

def walkfiles(paths,exts=None):
  r"""Walk one or more directories or files and possibly filter results by file extension.

  Args:
    paths (str,list): file path, directory path, or list of any combination of those
    exts (str): extension type with which to filter files

  Yields:
    (str): full paths to all (matching) files in the specified directories or files
  """
  def checkext(path):
    return exts is None or os.path.splitext(path)[1] in flatten(exts)
  for path in flatten(paths):
    if os.path.isfile(path):
      if checkext(path):
        yield path
    elif os.path.isdir(path):
      for root,_,f in os.walk(path):
        fpath = os.path.join(root,f)
        if checkext(fpath):
          yield fpath
    else:
      raise ValueError('Cannot find path: {}'.format(path))

def unique(iterobj):
  r"""Return the unique elements of a list of objects.

  Args:
    iterobj (Iterable): an iterable object

  Returns:
    (list): a list containing only the unique elements from **iterobj**
  """
  u = set()
  return [obj for obj in iterobj if not (obj in u or u.add(obj))]

def dictmerge(*dicts,ordered=False):
  r"""Merge the provided dictionaries.

  If a key appears in more than one dictionary, the value from the last appearance is used.

  Args:
    *dicts (Iterable[dict]): multiple dictionary objects
    ordered (bool): return the dictionary as: ``True`` = OrderedDict; ``False`` = dict

  Returns:
    (dict): A single (ordered) dictionary containing all key-value pairs from the input dictionaries
  """
  if not ordered:
    return {k:d[k] for d in dicts for k in d}
  else:
    return odict([(k,d[k]) for d in dicts for k in d])

def flatten(obj):
  r"""Ensures that **obj** is a single list containing no nested lists.

  Similar to ``np.ndarray.flatten``, except for lists which may contain heterogeneous data.

  Args:
    obj (object): a single object or list of lists or list of list of lists ...

  Returns:
    (list): a list containing all (nested) elements of **obj** in the order they appear
  """
  out = []
  if hasattr(obj,'__iter__') and not isinstance(obj,str):
    for el in obj:
      out.extend(flatten(el))
  else:
    out.append(obj)
  return out
