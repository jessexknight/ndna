import os
import pytest
from ndna.io import loadjson,makedir,odict

datadir = os.path.join('tests','data')
dimjson = os.path.join(datadir,'dimensions.json')

def test_loadjson():
  with pytest.raises(TypeError,match='invalid file'):
    loadjson(None)
  # TODO: behaviour for loadjson(0)?
  with pytest.raises(FileNotFoundError,match='No such file or directory'):
    loadjson('lorem-ipsum-dolor-sit-amet')
  assert isinstance(loadjson(dimjson,ordered=True),odict)
  assert not isinstance(loadjson(dimjson,ordered=False),odict)

def test_makedirs():
  with pytest.raises(TypeError,match='argument must be str'):
    makedir(None)
    makedir(1)
  with pytest.raises(ValueError,match='argument must not be empty'):
    makedir('')
  directory = os.path.join(datadir,'test')
  makedir(directory)
  assert os.path.exists(directory)
  os.rmdir(directory)
