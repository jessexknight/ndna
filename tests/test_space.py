import pytest
import numpy as np
from copy import deepcopy
from ndna.space import Dimension,Space,Array
from tests import data

def test_dimension():
  # Dimensions.__init__
  with pytest.raises(TypeError,match='is not iterable'):
    Dimension('a','a',None)
    Dimension('a','a',0)
  # Dimension.name
  assert data.dims['sex'].name == 'sex'
  # Dimension.key
  assert data.dims['sex'].key == 'k'
  # Dimension.values
  assert data.dims['sex'].values == ['male','female']
  # Dimension.__str__
  assert str(data.dims['sex']) == '< Dimension "sex" (k): [male,female] >'
  # Dimension.__repr__
  assert repr(data.dims['sex']) == 'sex (k)'
  # Dimension.__len__
  assert len(data.dims['sex']) == 2

def test_space():
  # Space.__init__
  with pytest.raises(TypeError,match='is not iterable'):
    Space(0)
  with pytest.raises(TypeError,match='required positional argument'):
    Space()
  # Space.dims
  assert data.space.dims[0] == data.dims['activity']
  # Space.ndim
  assert data.space.ndim == len(data.dims)
  # Space.shape
  assert data.space.shape == (3,7,2)
  # Space.keys
  assert data.space.keys == ('i','j','k')
  # Space.index
  with pytest.raises(KeyError):
    data.space.index[0]
  assert data.space.index['j'] == 1
  # Space.dim
  with pytest.raises(KeyError):
    data.space.dim[0]
  assert data.space.dim['j'] == data.dims['age']
  # Space.__str__
  assert str(data.space) == '< Space [\n  activity (i)\n  age (j)\n  sex (k)] >'
  # Space.__repr__
  assert repr(data.space) == '< Space [i, j, k] >'
  # Space.__len__
  assert len(data.space) == 3
  # Space.keyfilter
  assert data.space.keyfilter([1,2,3],[]) == []
  assert data.space.keyfilter([1,2,3],['j']) == [2]
  with pytest.raises(TypeError,match='is not iterable'):
    data.space.keyfilter([1,2,3],0)
  with pytest.raises(AssertionError,match='len(.*) must equal'):
    data.space.keyfilter([],[])
  # Space.keysub
  assert data.space.keysub([1,2,3],None,[]) == [None,None,None]
  assert data.space.keysub([1,2,3],None,['j']) == [None,2,None]
  with pytest.raises(TypeError,match='is not iterable'):
    data.space.keysub([1,2,3],None,0)
  with pytest.raises(AssertionError,match='len(.*) must equal'):
    data.space.keysub([],None,[])
  # Space.iter
  with pytest.raises(TypeError,match='is not iterable'):
    list(data.space.iter(0))
  assert list(data.space.iter([])) == [{}]
  assert list(data.space.iter(['x'])) == [{}]
  assert next(data.space.iter()) == {'i': 'high', 'j': 10, 'k': 'male'}
  # Space.subshape
  with pytest.raises(TypeError,match='is not iterable'):
    data.space.subshape(0)
  assert data.space.subshape([]) == (1,1,1)
  assert data.space.subshape(['i','j']) == (3,7,1)
  # Space.coords
  assert data.space.coords()[0,0,0] == 'high  ,10,male  '
  assert np.all(data.space.coords(['k']) == np.array([[['male  ','female']]]))
  # Space.slicer
  assert data.space.slicer() == (slice(None),slice(None),slice(None))
  assert data.space.slicer(i='high') == (None,0,slice(None),slice(None))
  assert str(data.space.slicer(j=[10,20])) == str(np.ix_(range(3),[0,1],range(2)))
  assert str(data.space.slicer(['i','j'],j=[10,20])) == str(np.ix_(range(3),[0,1],[0]))

def test_array():
  def update(X,arr,**kwargs):
    return deepcopy(X).update(arr,**kwargs)
  # Array.__new__ & Array.__array_finalize__
  assert Array(0,data.space,[]).shape == (1,1,1)
  assert np.all(Array([0,1],data.space,['k']) == np.reshape([0,1],(1,1,2)))
  assert data.space is Array(0,data.space,[]).space
  with pytest.raises(AssertionError):
    assert deepcopy(data.space) is Array(0,data.space,[]).space
  with pytest.raises(ValueError,match='Mismatched data shape and space shape'):
    Array([0,1,2],data.space,[])
  # TODO: test subclassing Array
  # Array.__getitem__
  assert data.Xijk[2,6,1] == (3*7*2)-1
  assert data.Xijk[0].shape == (7,2)
  assert data.Xijk[{'i':'high'}].shape == (1,7,2)
  # Array.__call__
  assert data.Xijk(i='low',j=70,k='female') == (3*7*2)-1
  assert data.Xijk(i='high').shape == (1,7,2)
  # Array.coords
  assert data.X.coords() == np.array([[[': 0.0']]])
  assert np.all(data.Xk.coords() == np.array([[['male  : 1.0','female: 2.0']]]))
  assert data.Xijk.coords()[0,0,0] == 'high  ,10,male  :  0.0'
  # Array.slice
  assert np.all(data.Xijk.slice() == data.Xijk)
  assert data.Xi.slice(i='high') == np.array([[[1]]])
  assert np.all(data.Xi.slice(i=['high','low']) == np.array([[[1]],[[3]]]))
  assert data.Xijk.slice(i='low',j=70,k='female').shape == (1,1,1)
  assert data.Xijk.slice(i='low',j=70,k='female') == (3*7*2)-1
  assert np.all(data.Xijk.slice(i=['high','low'],j=70,k='female') ==\
                np.array([[[(1*7*2)-1]],[[(3*7*2)-1]]]))
  assert data.X.slice(x=None) == data.X # TEMP
  with pytest.raises(ValueError,match='not in list'):
    data.X.slice(i=None)
  # Array.update
  with pytest.raises(TypeError,match='Cannot cast'):
    update(data.X,None)
  with pytest.raises(ValueError,match='cannot reshape'):
    update(data.X,[])
    update(data.X,[1,2])
  with pytest.raises(ValueError,match='not in list'):
    update(data.Xi,9,i=0)
  assert np.all(update(data.Xk,[3,4]) == np.array([[[3,4]]]))
  assert np.all(update(data.Xk,3,k='male') == np.array([[[3,2]]]))
  assert np.all(update(data.Xik,9,i='high',k='male') == np.array([[[9,2]],[[3,4]],[[5,6]]]))
  assert np.all(update(data.Xik,[11,12],i='high') == np.array([[[11,12]],[[3,4]],[[5,6]]]))
  assert np.all(update(data.Xik,[[11,12],[15,16]],i=['high','low']) ==\
                np.array([[[11,12]],[[3,4]],[[15,16]]]))
