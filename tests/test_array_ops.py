import pytest
import numpy as np
import copy
from ndna.ops import Selector
from tests import data

# TODO: performance benchmarking vs np.ndarray as another badge

def test_array_ops():
  # Array.__add__
  assert (data.Xijk + 1).keys == ['i','j','k']
  assert (1 + data.Xijk).keys == ['i','j','k']
  assert (data.Xi + data.Xk).keys == ['i','k']
  # Array.__sub__
  assert (data.Xijk - 1).keys == ['i','j','k']
  assert (1 - data.Xijk).keys == ['i','j','k']
  assert (data.Xi - data.Xk).keys == ['i','k']
  # Array.__mul__
  assert (data.Xijk * 1).keys == ['i','j','k']
  assert (1 * data.Xijk).keys == ['i','j','k']
  assert (data.Xi * data.Xk).keys == ['i','k']
  # Array.__div__ & Array.__truediv__
  assert (data.Xik / 1).keys == ['i','k']
  assert (1 / data.Xik).keys == ['i','k']
  assert (data.Xi / data.Xk).keys == ['i','k']

def test_selector():
  csio = copy.deepcopy(data.sio)
  csio.register(data.Xik.shape)
  # Selector.__str__
  assert str(data.si) == '< Selector "si" {\'i\': \'high\'} >'
  # Selector.__repr__
  assert repr(data.si) == '{\'i\': \'high\'}'
  # Selector.__call__
  with pytest.raises(AttributeError,match='has no attribute \'shape\''):
    data.si(None)
  assert np.all(data.si(data.Xik) == np.array([[[1,2]]]))
  assert data.Xik.shape in data.si.pre
  assert np.all(data.si(data.Xik) == np.array([[[1,2]]]))
  assert np.all(data.sio(data.Xik) == np.array([[[1,2]]]))
  assert data.Xik.shape not in data.sio.pre
  # Selector.register
  assert data.Xik.shape in csio.pre
  # Selector.merge
  assert data.si.merge(data.sk) == data.sik
  # complex operations
  assert data.Xijk[data.sj3.merge(data.si)].shape == (1,3,2)
