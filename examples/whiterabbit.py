import cwriting.core as core
import cwriting.node as node

import math

d = core.Document()
t = core.Text('test', 'FOLLOW THE WHITE RABBIT'[::-1])
t.breakApart()

t.setPlacement(node.Placement(start=(2*math.sin(0), 2*math.cos(0), 0)))	
d.registerObject(t)

tl = core.Timeline('tl', True)
d.registerTimeline(tl)

for i in xrange(101):
	for l in xrange(len(t._letters)):
		p = i+l/1.5
		if t._letters[l]:
			t._letters[l].keyPlacement(tl)
			t._letters[l].setPlacement(node.Placement(start=(2*math.sin(4*p/50.0 * math.pi), 2*math.cos(2*p/50.0 * math.pi), 2*math.cos(3*p/50.0 * math.pi + math.pi/2.0) - 2.0)))
			if i + l == 60 or i + l == 100:
				t._letters[l].setVisibility(True)
				t._letters[l].keyVisibility(tl)
			elif i + l == 70 or i + l == 90:
				t._letters[l].setVisibility(False)
				t._letters[l].keyVisibility(tl)
		tl.advance(0.001)
	if i < 100:
		tl.advance(0.1)

tl.freeze(True)
d.save('whiterabbit.xml')
