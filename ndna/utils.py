r"""Utility functions
"""

from collections import OrderedDict as odict

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

def olen(obj):
  r"""Returns the length of **obj** if it is iterable and not a string else 1

  Args:
    obj (object): any object

  Returns:
    (int): the length of **obj** or 1 if **obj** is a string or not iterable
  """
  if hasattr(obj,'__iter__') and not isinstance(obj,str):
    return len(obj)
  else:
    return 1

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
