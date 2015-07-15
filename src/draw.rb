require './src/sph'
require './lib/thingy'

WINSIZE = 800

class SimulationWindow < Thingy
  def initialize
    super WINSIZE, WINSIZE, 16, "Smoothed Particle Hydrodynamics"
    self.simulation = SPH.new
  end

  def update dt
    simulation.step dt
  end

  def draw dt
    blank
    simulation.particles.each do |particle|
      # Color based on pressure, just for fun
      # color = if particle.density*50 < 255 then particle.density*50 else 255 end

      # Area of influence (H)
      # screen.ellipse(
      #   (particle.position.x*scale).to_i,
      #   (particle.position.y*scale).to_i,
      #   H*scale//2, H*scale//2, :white)

      # Particles
      ellipse(
        (particle.position.x*scale).to_i,
        (particle.position.y*scale).to_i,
        H*scale.div(2),
        H*scale.div(2),
        :white
      )

      # Velocity vectors
      line(
        # start
        (particle.position.x*scale).to_i,
        (particle.position.y*scale).to_i,
        # end
        ((particle.position.x+particle.velocity.x)*scale).to_i,
         ((particle.position.y+particle.velocity.y)*scale).to_i,
        :red
      )

    end
  end
end

SimulationWindow.new.run
