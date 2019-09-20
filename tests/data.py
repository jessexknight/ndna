import os
from ndna.space import Dimension,Space,Array
from ndna.io import loadjson,odict

dims = odict([
  (key, Dimension(**spec))
  for key,spec in loadjson(os.path.join('tests','data','dimensions.json')).items()
])
space = Space(dims.values())
X    = Array(0, space=space, keys=[])
Xi   = Array([1,2,3], space=space, keys=['i'])
Xk   = Array([1,2], space=space, keys=['k'])
Xik  = Array([[1,2,3],[4,5,6]], space=space, keys=['i','k'])
Xijk = Array(range(3*7*2), space=space, keys=['i','j','k'])
