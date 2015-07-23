require './src/sph'
require './lib/thingy'

WINSIZE = 500

class SimulationWindow < Thingy
  attr_reader :simulation
  def initialize
    super WINSIZE, WINSIZE, 16, "Smoothed Particle Hydrodynamics"
    @simulation = SPH.new
    @scale = 15
    @oldtime = 0.0
  end

  def update time
    simulation.step 0.1
    simulation.make_particles_stay_in_bounds @scale
  end

  def draw time
    blank
    s = WINSIZE.div @scale

    simulation.particles.each do |particle|
      # Color based on pressure, just for fun

      pressure_as_color = spectrum particle.density*255, 1.0, -1.5
      # register_color pressure_as_color

      # text pressure_as_color.to_s, 30, 30, :white
      # Area of influence (H)
        (particle.position.x*s).to_i,
        (particle.position.y*s).to_i,
        H*s.div(2),
        H*s.div(2),
        pressure_as_color)

      # Particles
      ellipse(
        (particle.position.x*s).to_i,
        (particle.position.y*s).to_i,
        5,
        5,
        :white
      )

      # Velocity vectors
      line(
        # start
        (particle.position.x*s).to_i,
        (particle.position.y*s).to_i,
        # end
        ((particle.position.x+particle.velocity.x)*s).to_i,
         ((particle.position.y+particle.velocity.y)*s).to_i,
        :red
      )

    end
  end
end

SimulationWindow.new.run
