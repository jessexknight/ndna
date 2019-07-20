import pytest
from ndna.utils import unique,dictmerge,flatten

# TODO: load / save functions

def test_unique():
  assert unique([1]) == [1]
  assert unique([1,1]) == [1]
  assert unique([1,2]) == [1,2]
  assert unique((1,2)) == [1,2]
  with pytest.raises(TypeError,match='required positional argument'):
    unique()
  with pytest.raises(TypeError,match='object is not iterable'):
    unique(1)
  with pytest.raises(TypeError,match='unhashable type'):
    unique([[]])

def test_dictmerge():
  d1 = {'a':1}
  d2 = {'b':2}
  d12 = {'a':1,'b':2}
  d1x = {'a':'x'}
  assert dictmerge() == {}
  assert dictmerge(d1) == d1
  assert dictmerge(d1,d1) == d1
  assert dictmerge(d1,d2) == d12
  assert dictmerge(d1,d1x) == d1x
  assert dictmerge(d1,d1x,d1) == d1
  with pytest.raises(TypeError,match='unexpected keyword argument'):
    dictmerge(a=1)

def test_flatten():
  assert flatten(None) == [None]
  assert flatten([]) == []
  assert flatten({}) == []
  assert flatten('') == ['']
  assert flatten(1) == [1]
  assert flatten([1]) == [1]
  assert flatten([[1]]) == [1]
  assert flatten([1,2,3]) == [1,2,3]
  assert flatten([[1,2,3]]) == [1,2,3]
  assert flatten([1,2,[3]]) == [1,2,3]
  with pytest.raises(TypeError,match='required positional argument'):
    flatten()
