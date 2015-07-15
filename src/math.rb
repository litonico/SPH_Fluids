class Float
  ##
  # A floating-point friendly, exclusive Comparable::between?
  # Equivalent to `min < x <= max`
  ##
  def xbetween? min, max
    self.between? min+Float::EPSILON, max
  end
end
