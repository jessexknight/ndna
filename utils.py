import os
import csv
from collections import OrderedDict as odict
import simplejson as json

def loadjson(fname,ordered=True):
  r"""Load a ``.json`` file.

  Args:
    fname: ``.json`` filename

  Returns:
    the contents as a dict / list object
  """
  oargs = {'object_pairs_hook': odict} if ordered else {}
  with open(fname,'r') as f:
    return json.load(f,**oargs)

def savejson(fname,data,append=False,warn=True,indent=None,**kwargs):
  r"""Save a dict / list object to a ``.json`` file.

  Args:
    fname: ``.json`` filename
    data: dict / list object
    append: append to the file **fname**
    warn: print a warning if overwriting keys during append
    indent: spaces of indentation or ``None`` for no newlines at all
    **kwargs: keyword arguments to pass to ``json.dump()``
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
        if warn:
          # warn about overwriting keys
          overwrite = [key for key in data if key in fdata]
          if overwrite:
            print('Warning: overwriting keys: {} in {}'.format(
              overwrite,fname
            ))
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
  r"""Load a ``.txt`` file.

  Args:
    fname: ``.txt`` filename
    dtype: a datatype to cast the result

  Returns:
    the file contents as dtype
  """
  dtype = dtype if dtype is not None else float
  with open(fname,'r') as f:
    return dtype(f.read())

def savetxt(fname,value):
  r"""Save a value to file.

  Args:
    fname: ``.txt`` filename
    value: some value to write to file as a string
  """
  makedir(os.path.split(fname)[0])
  with open(fname,'w') as f:
    f.write(str(value))

def loadcsv(fname,asdict=True,row=None):
  r"""Read a ``.csv`` file into a dict / list.

  Args:
    fname: ``.csv`` filename
    asdict: if ``True`` read a list of dictionaries elif ``False`` read a list of rows
    row: return only the specified row (zero-based index)
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
    if row is not None:
      for _ in range(row):
        next(reader)
      return next(reader)
    else:
      return [row for row in reader]

def savecsv(fname,data,append=True):
  r"""Save a dict / list into a ``.csv`` file.

  If **data** is a dictionary, and the file is new, a header row is added to the ``.csv`` file.
  If **data** is a list, no header row is added.

  Args:
    fname: ``.csv`` filename
    data: dict / list object
    append: if ``True`` append **data** to the existing file contents
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
  r"""Just make the damned directory

  Args:
    directory: the directory to make if it does not already exist
  """
  try:
    os.makedirs(directory,exist_ok=True)
  except:
    pass

def remove(fname):
  r"""Just remove the damned file or directory

  Args:
    fname: a file or directory to remove
  """
  try:
    os.remove(fname)
  except:
    try:
      os.rmdir(fname)
    except:
      pass

def walkfiles(paths,exts=None):
  r"""Shorthand for ``os.walk()`` for multiple directories and files yielding only files

  Args:
    paths: file path, directory path, or list of any combination of those
    exts: file extension to filter results

  Yields:
    full paths to all (matching) files in the specified directories and files
  """
  def checkext(path):
    return exts is None or os.path.splitext(path)[1] in flatten(exts)
  for path in flatten(paths):
    if os.path.isfile(path):
      if checkext(path):
        yield(path)
    elif os.path.isdir(path):
      for root,_,f in os.walk(path):
        fpath = os.path.join(root,f)
        if checkext(fpath):
          yield(fpath)
    else:
      raise ValueError('Cannot find path: {}'.format(path))

def unique(iterobj):
  r"""Returns the unique elements of a list of objects

  Args:
    iterobj: an iterable object

  Returns:
    A list containing only the unique elements from **objlist**
  """
  u = set()
  return [obj for obj in iterobj if not (obj in u or u.add(obj))]

def dictmerge(*dicts,ordered=False):
  r"""Merges the provided dictionaries

  If a key appears in more than one dictionary in the list,
  the value from the last appearance is used.

  Args:
    dicts: multiple dictionary objects
    ordered: if ``True`` return an ``OrderedDict`` else a classic dictionary

  Returns:
    A single (possibly ordered) dictionary containing all key-value pairs from the input dicts
  """
  if not ordered:
    return {k:d[k] for d in dicts for k in d}
  else:
    return odict([(k,d[k]) for d in dicts for k in d])

def flatten(obj):
  r"""Ensures that x is a single list containing no nested lists.

  Similar to ``np.ndarray.flatten``, except for lists which may contain heterogeneous data.

  Args:
    x: a single value or list of lists or list of list of lists ...

  Returns:
    a list containing all elements of x in the order they appear
  """
  out = []
  if hasattr(obj,'__iter__') and not isinstance(obj,str):
    for el in obj:
      out.extend(flatten(el))
  else:
    out.append(obj)
  return out
