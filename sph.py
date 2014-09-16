from random import random as rand
from vec2 import Vec2, Num, length
from particle import Particle
from math import pi
from graphics import graphics

# Constants
SCALE = 10
NUM_PARTICLES = 50
MASS = 5 # Particle mass
DENSITY = 1 # Rest density
GRAVITY = Vec2(0, 0)
H = 1  # Smoothing cutoff
k = 1  # Pressure constant
eta = 1  # Viscosity constant


def W(r, h):  # :: Num
    '''
    A weighting function (kernel) for the contribution of each neighbor
    to a particle's density
    '''
    assert isinstance(r, Vec2)
    assert isinstance(h, Num)
    if 0 < length(r) <= h:
        return 315/(64 * pi * h**9) * (h**2 - length(r)**2)**3
    else:
        return 0

    # Typecheck
    assert isinstance(ret, Num)
    return ret


def gradient_Wspiky(r, h):  # :: Vec2
    '''
    Gradient ( that is, Vec2(dx, dy) ) of a weighting function for
    a particle's pressure. This weight function is spiky (not flat or
    smooth at x=0) so particles close together repel strongly
    '''
    # TODO: overlapping particles may be problematic
    if 0 < length(r) <= h:
        ret =  -1 * r * (45/(pi * h**6 * length(r))) * (h - length(r))**2
    else:
        ret = Vec2(0, 0)

    assert isinstance(ret, Vec2)
    return ret
    

# TODO: Use laplacian
def laplacian_W_viscosity(r, h):  # :: Num
    '''
    The laplacian of a weighting function that tends towards infinity when 
    approching 0 (slows down particles moving faster than their neighbors)
    '''
    len_r = length(r)
    if 0 < len_r <= h:
        ret = 15/(2 * pi * h**3) \
                * ((-1 * len_r**3)/(2 * h**3) + \
                len_r**2/(h**2) + \
                h/(2*len_r) - 1)
    else:
        ret = 0

    assert isinstance(ret, Num)
    return ret


particles = [Particle(Vec2(rand()*SCALE, rand()*SCALE)) 
                    for p in range(NUM_PARTICLES)]


time = 0
delta_time = 0.1
while True:

    # Clear everything
    for particle in particles:
        particle.density = DENSITY
        particle.pressure_force = Vec2(0,0)
        particle.viscosity_force = Vec2(0,0)
    
    # Calculate fluid density around each particle
    for particle in particles:
        for neighbor in particles:

            # If particles are close together, density increases
            distance = particle.position - neighbor.position # A vector

            if length(distance) <= H:  # Particles are close enough to matter
                particle.density += MASS * W(distance, H)

    # Calculate forces on each particle based on density
    for particle in particles:
        for neighbor in particles:

            distance = particle.position - neighbor.position
            if length(distance) <= H:
                # Temporary terms used to caclulate forces
                density_p = particle.density
                density_n = neighbor.density

                pressure_p = k * (density_p - DENSITY)  # Constant k
                pressure_n = k * (density_n - DENSITY)

                particle.pressure_force += (
                        MASS * (pressure_p + pressure_n) / (2 * density_n)
                        * gradient_Wspiky(distance, H))

                assert(density_n != 0)  # Dividing by density
                particle.viscosity_force += (  # Constant eta
                        eta * MASS * (neighbor.velocity - particle.velocity)
                        * (1/density_n) * laplacian_W_viscosity(distance, H))

    # Apply forces to particles- make them move!
    for particle in particles:
        #TODO
        total_force = particle.pressure_force #+ particle.viscosity_force
        assert isinstance(total_force, Vec2)

        # 'Eulerian' style momentum
        # Calculate acceleration from forces
        acceleration = total_force * (1/particle.density) \
                * delta_time + GRAVITY

        # Update position and velocity
        particle.velocity += acceleration * delta_time
        particle.position += particle.velocity * delta_time

        # Make sure particles stay in bounds
        if particle.position.x >= SCALE - 0.01:
            particle.position.x = SCALE - 0.1
            particle.velocity = Vec2(-0.01, 0)
        elif particle.position.x < 0.01:
            particle.position.x = 0.1
            particle.velocity = Vec2(0.01, 0)

        if particle.position.y >= SCALE - 0.01:
            particle.position.y = SCALE - 0.1
            particle.velocity = Vec2(0, -1)
        elif particle.position.y < 0.01:
            particle.position.y = 0.1
            particle.velocity = Vec2(0, 1)

    graphics.draw(particles, H, SCALE)

    time += delta_time
