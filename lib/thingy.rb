require "sdl"

class Thingy
  attr_accessor :screen, :w, :h
  attr_accessor :step, :paused
  attr_accessor :font
  attr_accessor :color, :rgb
  attr_accessor :rgb_colr, :spectrum

  def initialize w, h, c, name
    SDL.init SDL::INIT_VIDEO
    SDL::TTF.init

    self.font = SDL::TTF.open("/System/Library/Fonts/Menlo.ttc", 32, 0)

    SDL::WM.set_caption name, name

    self.screen = SDL::Screen.open w, h, c, SDL::HWSURFACE|SDL::DOUBLEBUF
    self.w, self.h = screen.w, screen.h

    self.color = {}
    self.rgb   = Hash.new { |i, k| i[k] = screen.get_rgb(color[k]) }

    register_color :black,     0,   0,   0
    register_color :white,     255, 255, 255
    register_color :red,       255, 0,   0
    register_color :green,     0,   255, 0
    register_color :blue,      0,   0,   255
    register_color :gray,      127, 127, 127
    register_color :yellow,    255, 255, 0

    self.paused = self.step = false
  end

  #TODO (Lito): Formalize!
  def rgb_color r, g, b
    screen.format.map_rgb r, g, b
  end

  def clamp val, bot, top# :nodoc:
    [[val, top].min, bot].max
  end
  ##
  # "cubehelix" spectrum - converts a degree (0-255) into an RGB
  # color.
  #
  #TODO (Lito): Formalize! Also, shouldn't be called a degree
  def spectrum degree, start=0.5, rot=-1.5
    # Scale to 0-1 range
    degree = degree / 255.0
    gamma = 1.0 # Intensity gamma correction

    fract = degree**gamma
    amp = degree
    angle = 2.0 * Math::PI * (start / 3.0 + rot * degree + 1.0)

    red = fract + amp * (-0.14861*Math::cos(angle) + 1.78277*Math::sin(angle))
    grn = fract + amp * (-0.29227*Math::cos(angle) - 0.90649*Math::sin(angle))
    blu = fract + amp * (1.97294 * Math::cos(angle))

    red = red * 255
    grn = grn * 255
    blu = blu * 255
    # [red, grn, blu].each do |color|
    #   # Scale back to 0-255 range
    #   color = color * 255
    #   # Clamp extremes
    #   color = self.clamp color, 0, 255
    # end

    #[red, grn, blu]
    rgb_color red, grn, blu
  end

  def register_color name, r, g, b
    color[name] = screen.format.map_rgb r, g, b
  end

  def handle_event event, n
    case event
    when SDL::Event::KeyDown then
      case event.sym
      when "q".ord, "Q".ord, "\e".ord then
        exit
      when " ".ord then
        self.step = true
        self.paused = false
      when "p".ord, "P".ord then
        self.paused = ! paused
      end
    when SDL::Event::Quit then
      exit
    end
  end

  def run max = nil
    n = 0
    loop do
      self.draw n

      screen.flip

      while event = SDL::Event.poll
        handle_event event, n
      end

      update n unless paused
      n += 1 unless paused

      if step then
        self.paused = true
        self.step = false
      end

      exit if max && n >= max
    end
  end

  def update n
    # do nothing
  end

  ### drawing routines:

  def blank
    fill_rect 0, 0, w, h, :black
  end

  def line x1, y1, x2, y2, c
    if color[c]
      c = color[c]
    end
    screen.draw_line x1, y1, x2, y2, c
  end

  def text s, x, y, c, f = font
    f.draw_solid_utf8(screen, s, x, y, *rgb[c])
  end

  def ellipse x, y, w, h, c
    if color[c]
      c = color[c]
    end
    screen.draw_ellipse x, y, w, h, c
  end

  def fill_rect x, y, w, h, c
    if color[c]
      c = color[c]
    end
    screen.fill_rect x, y, w, h, c
  end
end
