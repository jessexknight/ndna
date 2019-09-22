import os
from ndna.space import Dimension, Space, Array
from ndna.utils import odict
from ndna.io import loadjson

dims = odict([
  (key, Dimension(**spec))
  for key,spec in loadjson(os.path.join('tests','data','dimensions.json')).items()
])
space = Space(dims.values())
X = Array([[1,2,3],[4,5,6]], space=space, keys=['i','k'])

# print(space.coords())
# print(X.coords())
# X.update([0],i=['high'],k=['male'])
# print(X)
# print(X.slice(k=['male']))
