import os
import pytest
from ndna.space import Dimension,Space
from ndna.utils import loadjson

dims = {
  key: Dimension(**spec)
  for key,spec in loadjson(os.path.join('tests','data','dimensions.json')).items()
}
space = Space(dims.values())

def test_dimension():
  with pytest.raises(TypeError,match='required positional argument'):
    Dimension()
  with pytest.raises(TypeError,match='object is not iterable'):
    Dimension('a','a',None)
    Dimension('a','a',1)

def test_space():
  with pytest.raises(TypeError,match='object is not iterable'):
    Space(None)
  with pytest.raises(TypeError,match='required positional argument'):
    Space()
