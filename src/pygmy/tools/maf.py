# boring maths stuff
import math
from typing import TypeAlias

scale_vec = lambda scalar, vector: [scalar * num for num in vector]
dot = lambda vec1, vec2: vec1[0] * vec2[0] + vec1[1] * vec2[1]

def area_reg_polygon(n, s):
    '''
    n: number of sides
    s: side_length
    '''
    return n * s * (s / (2 * math.tan(math.pi/n))) * 0.5

def key(pos, dim):
    '''
    pos: sample location
    dim: tile_size
    '''
    return str(math.floor(pos[0] / dim[0])) + ';' + str(math.floor(pos[1] / dim[1]))

def area_irreg_polygon(cords):  # use area_reg_polygon() when possible (that fast, dis slooowwwww...)
    '''
    coords: [p0, p1, p2...]

    use area_reg_polygon() when possible (that fast, dis slooowwwwwwwww...)
    '''
    s1 = math.fsum([cord[0] * cords[(i+1)%len(cords)][1] for i, cord in sorted(enumerate(cords), reverse=True)])
    s2 = math.fsum([cord[1] * cords[(i+1)%len(cords)][0] for i, cord in sorted(enumerate(cords), reverse=True)])
    return abs(s1 - s2) * 0.5

def linear_tween(t, b, c, d):
    '''
    t: current time
    b: beginning value
    c: change in value
    d: duration
    '''
    return c * t / d + b

def ease_in_quad(t, b, c, d):
    return c * (t / d) * t + b

def ease_out_quad(t, b, c, d):
    return -c * (t / d) * (t - 2) + b

def ease_inout_quad(t, b, c, d):
    if t / (d * 0.5) < 1:
        return c * 0.5 * t * t + b
    return -c * 0.5 * ((t - 1) * (t - 2) - 1) + b

def direction_to(p1, p2) -> float:
    '''
    p1: where to point to
    p2: pivot point

    Returns direction from p2 to p1
    '''
    return math.atan2(p1[1] - p2[1], p1[0] - p2[0])

def trix_mult(grid, multiplier):
    return [[[grid[y][x][0] * multiplier[0] + grid[y][x][1] * multiplier[1], grid[y][x][0] * multiplier[2] + grid[y][x][1] * multiplier[3]] for x, point in enumerate(row)] for y, row in enumerate(grid)] 
    
