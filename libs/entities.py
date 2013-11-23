import pymunk
from pymunk import Vec2d

import utils

from math import radians,degrees

class SoftBody(object):
	def __init__(self, space, position, 
				 radius = 50, poly = 6, seg_width = 8, 
				 mass = .001, friction = .1, elasticity = .5,
				 group = 3,
				 stiff = .2, damp = .02):

		# divisible by 360
		a = 360/poly
		s = 360/a

		t = 0
		points = []
		for i in range(s):
			point = utils.point_on_circle(radius, radians(t), position)
			points.append(point)
			t += a

		shape_height = utils.distance(points[0], points[1])

		width 		= seg_width
		size 		= (width,shape_height)
		box_moment 	= pymunk.moment_for_box(mass, size[0], size[1])

		angle = 0

		shapes = []
		for point in points:
			box_body 				= pymunk.Body(mass, box_moment)
			box_body.position		= point
			box_body.angle 	  		= radians(angle)

			box_shape 				= pymunk.Poly.create_box(box_body, size=size)
			box_shape.friction 		= friction
			box_shape.elasticity 	= elasticity
			box_shape.group 		= group

			space.add(box_body, box_shape)

			box_shape.size = size
			shapes.append(box_shape)

			angle += a

		rest_ln = radius*2

		idx = (len(shapes)-1)/2
		i = 0
		for shape in shapes:
			if shape == shapes[0]:
				pin_const = pymunk.constraint.PivotJoint(shape.body, shapes[-1].body, Vec2d(0,-shape.size[1]/2), Vec2d(0,shape.size[1]/2))
				space.add(pin_const)
			else:
				pin_const = pymunk.constraint.PivotJoint(shape.body, shapes[i-1].body, Vec2d(0,-shape.size[1]/2), Vec2d(0,shape.size[1]/2))
				space.add(pin_const)

			if idx == len(shapes)-1:
				idx = 0
			spr_const = pymunk.constraint.DampedSpring(shape.body, 
													   shapes[idx].body, 
													   Vec2d(0,0), Vec2d(0,0),
													   rest_ln, 
													   stiff, 
													   damp)
			space.add(spr_const)
			idx += 1
			i += 1
