import os
from ndna.space import Dimension,Space,Array
from ndna.ops import Selector
from ndna.io import loadjson,odict

# Dimension
dims = odict([
  (key, Dimension(**spec))
  for key,spec in loadjson(os.path.join('tests','data','dimensions.json')).items()
])
# Space
space = Space(dims.values())
# Array
X    = Array(0,                 space=space, keys=[])
Xi   = Array([1,2,3],           space=space, keys=['i'])
Xk   = Array([1,2],             space=space, keys=['k'])
Xik  = Array([[1,2,3],[4,5,6]], space=space, keys=['i','k'])
Xijk = Array(range(3*7*2),      space=space, keys=['i','j','k'])
# Selector
si  = Selector('si',    space=space, i='high')
sio = Selector('sio',   space=space, i='high', memory=False)
sk  = Selector('sk',    space=space, k='female')
sik = Selector('si sk', space=space, i='high',k='female')
sj3 = Selector('sj2',   space=space, j=[10,20,30])
