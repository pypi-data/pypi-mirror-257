import hashlib as _hl
from MainHash.__algs import _algs
def path(p):
  d={}
  with open(p,"rb") as f:
    for alg in _algs:
      for i in f:
        h=getattr(_hl,alg)()
        h.update(i)
      d[alg]=h.hexdigest()
  return d
def file(f):
  d={}
  for alg in _algs:
    h=getattr(_hl,alg)()
    for i in f:
      h.update(i)
    d[alg]=h.hexdigest()
  return d
def text(t,encoding="utf-8"):
  d={}
  for alg in _algs:
    d[alg]=getattr(_hl,alg)(str(t).encode(encoding)).hexdigest()
  return d
def bytes(b):
  d={}
  for alg in _algs:
    d[alg]=getattr(_hl,alg)(b).hexdigest()
  return d
