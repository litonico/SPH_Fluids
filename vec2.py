from math import sqrt

Num = float, int # Numeric classes

class Vec2(object):
    def __init__(self, x, y):
        assert isinstance(x, Num) and isinstance(y, Num), \
                "Vec2 parameters "+str(x)+" and "+str(y)+" are not numbers"
        self.x = x
        self.y = y

    def __str__(self):
        return "Vec2("+str(self.x) + ", " + str(self.y)+")"

    def __add__(self, other):
        return Vec2(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        return Vec2(self.x-other.x, self.y-other.y)

    def __iadd__(self,other):
        self.x += other.x
        self.y += other.y
        return self

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def __mul__(self, scalar): # vec * scalar
        return Vec2(self.x*scalar, self.y*scalar)

    def __rmul__(self, scalar): # scalar * vec
        return Vec2(self.x*scalar, self.y*scalar)


def length(v):
    return sqrt(v.x**2 + v.y**2)
