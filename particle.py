from vec2 import Vec2, Num

class Particle(object):
    def __init__(self, pos):
        # Scalars
        self.density = 0

        # Forces
        self.position = pos
        self.velocity = Vec2(0,0)
        self.pressure_force = Vec2(0,0)
        self.viscosity_force = Vec2(0,0)

    # Just for debugging
    def __setattr__(self, name, value): 
        '''Trying to typecheck python is a bad idea AHHHH'''
        if (name == 'position'  # A vector
                or name == 'velocity'
                or name == 'pressure_force'
                or name == 'viscosity_force'):
            assert isinstance(value, Vec2), \
                name + " is " + str(value) + ", not Vec2"
            object.__setattr__(self, name, value)

        else:  # A number
            assert isinstance(value, Num), \
                name + " is " + str(value) + ", not number"
            object.__setattr__(self, name, value)
