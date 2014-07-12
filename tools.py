#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

def coupled(pathlist):
	"""
	Need for drawing lines in svg term
	"""

	it = iter(pathlist)
	itn = it.next
	return [(x, itn()) for x in it]

if __name__ in ('__main__'):
	# x1, y1, x2, y2 [...]
	pts = [50.1245689784512, 4, 12, 3, 65, 89, 0, 45]
	print(pts)

	tmp = [(float("%.4g" % e)) for e in pts]
	print tmp

	# (x1,y1), (x2, y2), [...]
	print(coupled(tmp))

	# ((x1,y1), (x2, y2)), [...]
	print(coupled(coupled(tmp)))