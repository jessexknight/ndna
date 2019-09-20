import pytest
from . import data

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
  
