# Triangle Project Code.

# Triangle analyzes the lengths of the sides of a triangle
# (represented by a, b and c) and returns the type of triangle.
#
# It returns:
#   :equilateral  if all sides are equal
#   :isosceles    if exactly 2 sides are equal
#   :scalene      if no sides are equal
#
# The tests for this method can be found in
#   about_triangle_project.rb
# and
#   about_triangle_project_2.rb
#
def triangle(a, b, c)
  # WRITE THIS CODE
  validate_sides(a, b, c)

  unique_sides = [a, b, c].uniq.length

  if unique_sides == 1
    :equilateral
  elsif unique_sides == 2
    :isosceles
  else
    :scalene
  end
end

def validate_sides(a, b, c)
  a, b, c = [a, b, c].sort
  raise TriangleError if [a, b, c].any? { |side| side <= 0 }
  raise TriangleError if a + b <= c  
end

# Error class used in part 2.  No need to change this code.
class TriangleError < StandardError
end
