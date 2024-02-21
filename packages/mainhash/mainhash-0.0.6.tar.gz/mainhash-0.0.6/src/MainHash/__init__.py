__version_tuple__=(0,0,6)
import MainHash.all as all
import MainHash.blake2b as blake2b
import MainHash.blake2s as blake2s
import MainHash.md5 as md5
import MainHash.sha1 as sha1
import MainHash.sha224 as sha224
import MainHash.sha256 as sha256
import MainHash.sha384 as sha384
import MainHash.sha3_224 as sha3_224
import MainHash.sha3_256 as sha3_256
import MainHash.sha3_384 as sha3_384
import MainHash.sha3_512 as sha3_512
import MainHash.sha512 as sha512
# Данные о модуле
__version__="{}.{}.{}".format(*__version_tuple__)
__depends__={
  "required":[
    "hashlib",
    "mainshortcuts"
    ],
  "optional":[]
  }
__functions__=[]
__classes__={}
__variables__=[]
__all__=__functions__+__variables__+list(__classes__.keys())
__scripts__=[
  "MainHash-check",
  "MainHash-gen",
  "MH-gen",
  "MH-check",
  ]
from MainHash.__algs import _algs
_alg_functions=[
  "path",
  "file",
  "text",
  "bytes",
  ]
for i1 in _algs:
  for i2 in _alg_functions:
    __functions__.append(f"{i1}.{i2}")
del i1, i2
__all__.sort()
__functions__.sort()
__scripts__.sort()
__variables__.sort()
_algs.sort()
