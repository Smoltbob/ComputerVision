from line import *
from point import *

p = HomogeneousPoint(0, 0)
p2 = HomogeneousPoint(1, 0)
l = Line(1, 2, 0)

print(p)
print(l)

print((p in l))
print((p2 in l))

print(Line.intersection(Line(-1,0,1), Line(0,-1,1)))