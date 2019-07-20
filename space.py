import numpy as np
from itertools import product

class Dimension():
  def __init__(self,name,key,values):
    self.name   = name
    self.key    = key
    self.values = list(values)

  def __str__(self):
    return '< Dimension "{}" ({}): [{}] >'.format(
      self.name,
      self.key,
      ','.join(str(v) for v in self.values),
    )

  def __repr__(self):
    return '{} ({})'.format(
      self.name,
      self.key,
    )

class Space():
  def __init__(self,dims):
    self.dims  = list(dims)
    self.ndim  = len(dims)
    self.shape = tuple(len(dim.values) for dim in dims)
    self.keys  = tuple(dim.key for dim in dims)

  def __str__(self):
    return '< Space [{}] >'.format(
      '\n  '.join(repr(dim) for dim in self.dims),
    )

  def __repr__(self):
    return '< Space [{}] >'.format(
      ', '.join(str(key) for key in self.keys),
    )

  def index(self,key):
    return self.keys.index(key)

  def dim(self,key):
    return self.dims[self.index(key)]

  def keyfilter(self,iter,keys):
    return [item for item,key in zip(iter,self.keys) if key in keys]

  def keysub(self,iter,sub,keys):
    return [item if key in keys else sub for item,key in zip(iter,self.keys)]

  def iter(self,keys=None):
    sdims = self.dims if keys is None else self.keyfilter(self.dims,keys)
    skeys = self.keys if keys is None else self.keyfilter(self.keys,keys)
    for values in product(*[dim.values for dim in sdims]):
      yield dict(zip(skeys,values))

  def coords(self,keys=None):
    sdims = self.dims if keys is None else self.keyfilter(self.dims,keys)
    shape = self.shape if keys is None else self.subshape(keys)
    lens = list(map(lambda dim: max(map(lambda v: len(str(v)),dim.values)),sdims))
    return np.reshape([
      ','.join([str(v).ljust(l) for v,l in zip(values,lens)])
      for values in product(*map(lambda dim: dim.values, sdims))
    ],shape)

  def subshape(self,keys):
    return tuple(self.keysub(self.shape,1,keys))

  def slicer(self,keys=None,**kwargs):
    slicer = [None]*self.ndim
    for i,key in enumerate(self.keys):
      if key in kwargs:
        slicer[i] = [self.dims[i].values.index(v) for v in kwargs[key]]
      elif (keys is None) or (key in keys):
        slicer[i] = range(0,self.shape[i])
      else:
        slicer[i] = [0]
    return np.ix_(*slicer)

class Array(np.ndarray):
  def __new__(cls,arr,space,keys):
    if issubclass(type(arr),cls):
      cls = type(arr)
    shape = space.subshape(keys)
    obj = np.asanyarray(arr).view(cls)
    if obj.shape != shape:
      try:
        obj = obj.reshape(shape)
      except:
        raise ValueError('Mismatched data shape and space shape: {} vs {}.'.format(
          list(obj.shape), list(shape)
        ))
    obj.space = space
    obj.keys  = keys
    return obj

  def __array_finalize__(self,obj):
    if obj is None:
      return
    self.space = getattr(obj,'space',None)
    self.keys  = getattr(obj,'keys',None)

  def coords(self):
    def fmt(key,value):
      return key+(': {:9f}').format(value) # TODO: clean up this assumed :9f
    return np.reshape([
      fmt(k,v) for k,v in zip(self.space.coords(self.keys).flatten(),self.flatten())
    ],self.shape)

  def slice(self,**select):
    return self[self.space.slicer(self.keys,**select)]

  def update(self,arr,**select):
    if not isinstance(arr,np.ndarray):
      arr = np.array(arr)
    if select:
      slicer = self.space.slicer(self.keys,**select)
      shape  = tuple(map(len,slicer))
      self[slicer] = arr.reshape(shape)
    else:
      np.copyto(self,arr)
    return self
