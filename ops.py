r"""Operator classes: Selector
"""

from ndna import utils

class Selector(dict):
  def __init__(self,name,space,memory=True,**select):
    dict.__init__(self)
    self.update(select)
    self.name = name
    self.space = space
    self.memory = memory
    self.pre = {}

  def __str__(self):
    return '< Selector "{}" {} >'.format(
      self.name,
      str(dict(self)),
    )

  def __repr__(self):
    return str(dict(self))

  def __call__(self,arr):
    if arr.shape in self.pre:
      return arr[self.pre[arr.shape]]
    elif self.memory:
      self.register(arr.shape)
      return arr[self.pre[arr.shape]]
    else:
      return arr[self.space.slicer(**self)]

  def register(self,shape):
    self.pre.update({shape: self.space.slicer(**self)})

  def merge(self,selector):
    assert self.space == selector.space, 'selectors must be part of the same space'
    return Selector(
      name = self.name+' '+selector.name,
      space = self.space,
      **utils.dictmerge(self,selector),
    )
