import node
import copy
import curve
import math

class Document(object):
	def __init__(self):
		self._x = 0
		self._objs = []
		self._groups = []
		self._times = []
		self._pa = []
		self._sounds = []
		self._scenes = []
		self._rootTimeline = Timeline('_root')
		self._titleScene = None
		self.registerTimeline(self._rootTimeline)

	def addScene(self, scene):
		self._scenes.append(scene)
		self._rootTimeline.changeTimeline(scene['timeline'])
		self._rootTimeline.advance(scene['timeline'].current())

	def getScenes(self):
		return list(self._scenes)

	def setTitleScene(self, scene):
		self._titleScene = scene

	def registerObject(self, obj):
		self._objs.append(copy.deepcopy(obj))

	def registerGroup(self, obj):
		self._groups.append(obj)

	def registerTimeline(self, obj):
		self._times.append(obj)

	def registerParticleActions(self, obj):
		self._pa.append(obj)

	def registerSound(self, obj):
		self._sounds.append(obj)

	def distill(self):
		doc = node.Document()
		story = node.Story()
		for obj in self._objs:
			for o in obj.distill():
				story.addObject(o)

		for group in self._groups:
			story.addGroup(group.distill())

		for timeline in self._times:
			story.addTimeline(timeline.distill())

		for pa in self._pa:
			story.addParticleActions(pa)

		for sound in self._sounds:
			story.addSound(sound)

		if self._titleScene:
			tl = Timeline('_autostart', True)
			tl.changeTimeline(self._titleScene['timeline'])
			story.addTimeline(tl.distill())

		doc.setRoot(story.genNode(doc.getNode()))
		return doc

	def next(self):
		x = self._x
		self._x += 1
		return x

	def save(self, filename):
		xml = self.distill()
		xml.save(filename)

class Timeline(object):
	def __init__(self, name, autostart=False):
		self._time = 0.0
		self.name = name
		self._loop = False
		self._autostart = autostart

		self._first = {}
		self._current = {}
		self._previous = []

		self._instants = []

		self._changes = []

	def _genDiff(self, current, next):
			key = (next['object'], next['property'])
			if key in current:
				diff = current[key]['value'].genDiff(current[key], next)
				if diff:
					ta = node.TimedActions(current[key]['time'])
					ta.addAction(next['object'].encloseDiff(diff))
					self._changes.append(ta)

			current[key] = next

	def advance(self, n):
		self._time += n

	def current(self):
		return self._time

	def key(self, prop, obj, value):
		key = (prop, obj)
		data = {
			'time': self._time,
			'object': obj,
			'property': prop,
			'value': copy.deepcopy(value) }

		if key not in self._first:
			self._first[key] = data

		if key in self._current:
			self._previous.append(self._current[key])

		self._current[key] = data

	def changeTimeline(self, other, action='start'):
		ta = node.TimedActions(self._time)
		ta.addAction(node.TimerChange(other))
		self._instants.append(ta)

	def changeLink(self, link, enable):
		ta = node.TimedActions(self._time)
		o = node.ObjectChange(link)
		o.addChild(node.LinkChange('link_' + ('on' if enable else 'off')))
		ta.addAction(o)
		self._instants.append(ta)

	def playSound(self, sound):
		ta = node.TimedActions(self._time)
		ta.addAction(node.SoundRef(sound))
		self._instants.append(ta)

	def startScene(self, scene):
		# lolhax
		s = Timeline('scene:' + scene)
		self.changeTimeline(s)

	def startScenes(self, d):
		self.changeTimeline(d._rootTimeline)

	def freeze(self, loop=False):
		self._changes = []
		self._loop = loop
		current = {}

		for next in self._previous:
			self._genDiff(current, next)

		for next in self._current.itervalues():
			self._genDiff(current, next)

		for i in self._instants:
			self._changes.append(i)

		if loop:
			ta = node.TimedActions(self._time)
			ta.addAction(node.TimerChange(self))
			self._changes.append(ta)

	def distill(self):
		if not self._changes:
			self.freeze()

		topNode = node.Timeline(self.name, self._autostart)

		for change in self._changes:
			topNode.addTimedAction(change)

		return topNode

class Tweener(object):
	_t = 0
	def __init__(self):
		self._timeline = Timeline('tween:%05d' % Tweener._t)
		Tweener._t += 1
		self.grain = 0.2
		self.adaptive = False
		self.lazyKeying = False

	def getTimeline(self):
		return self._timeline

	def tween(self, duration):
		def frange(end, step):
			start = 0
			while 0.0001 < end - start:
				yield start
				start += step

		last = None
		for t in frange(duration + self.grain, self.grain):
			last = self._tweenFrame(t, duration, last)
			self._timeline.advance(self.grain)


class CurveTweener(Tweener):
	_t = 0
	def __init__(self):
		super(CurveTweener, self).__init__()
		self._curve = None
		self._builtCurve = None
		self._obj = None
		self._startState = None
		self._endState = None
		self._prop = None

	def setObject(self, obj, prop, endState):
		self._obj = obj
		self._prop = prop
		self._endState = endState
		self._startState = obj.get(prop)

	def setCurve(self, curve):
		self._curve = curve
		self._builtCurve = self._startState.genCurve(self._endState, curve)

	def _tweenFrame(self, t, duration, opaque):
		v = self._builtCurve(t/duration)
		if not self.lazyKeying or opaque != v:
			opaque = v
			self._obj.set(self._prop, v)
			self._obj.key(self._prop, self._timeline)
		return opaque

class TweenSet(object):
	_x = 0
	def __init__(self):
		self._tweens = []

	def addTween(self, tween):
		self._tweens.append(tween)

	def register(self, d):
		for tween in self._tweens:
			if tween:
				d.registerTimeline(tween.getTimeline())

	def setGrain(self, grain):
		for tween in self._tweens:
			if tween:
				tween.grain = grain

	def setLazyKeying(self, lazyKeying):
		for tween in self._tweens:
			if tween:
				tween.lazyKeying = lazyKeying

	def tweenAcross(self, diff, duration):
		master = Timeline('tweenset:%03d' % TweenSet._x)
		TweenSet._x += 1
		for tween in self._tweens:
			if tween:
				tween.tween(duration)
				master.changeTimeline(tween.getTimeline())
			master.advance(diff)

		return master

class Object(object):
	def __init__(self, name):
		self.name = name
		self._props = node.PropertySet()
		self._props.setProperty('Placement', node.Placement())
		self._props.setBool('Visible', False)
		self._props.setColor('Color', 255, 255, 255)
		self._props.setBool('Lighting', False)
		self._props.setBool('ClickThrough', True)
		self._props.setBool('AroundSelfAxis', False)
		self._props.setScalar('Scale', 1.0)
		self.link = None
		self.sound = None

	def copyAttributes(self, other):
		self._props.clear()
		self._props.copy(other._props)

	def encloseDiff(self, diff):
		e = node.ObjectChange(self)
		e.addChild(diff)
		return e

	# TODO privatize specialization calls

	def setPlacement(self, placement):
		self._props.setProperty('Placement', copy.deepcopy(placement))

	def getPlacement(self):
		return self._props.getProperty('Placement')

	def keyPlacement(self, timeline):
		timeline.key('Placement', self, self._props.getProperty('Placement'))

	def setVisibility(self, v):
		self._props.getProperty('Visible').setValue(v)

	def getVisibility(self):
		return self._props.getProperty('Visible')

	def keyVisibility(self, timeline):
		timeline.key('Visible', self, self._props.getProperty('Visible'))

	def setScale(self, v):
		self._props.getProperty('Scale').setValue(v)

	def getScale(self):
		return self._props.getProperty('Scale').getValue()

	def set(self, prop, v):
		getattr(self, 'set' + prop)(v)

	def get(self, prop):
		return getattr(self, 'get' + prop)()

	def key(self, prop, timeline):
		getattr(self, 'key' + prop)(timeline)

class Group(Object):
	def __init__(self, name):
		super(Group, self).__init__(name)
		self._children = []

	def encloseDiff(self, diff):
		e = node.GroupRef(self)
		e.addChild(diff)
		return e

	def addObject(self, obj):
		self._children.append(obj)

	def applyMap(self, vmap):
		for m in self._children:
			p = m.getPlacement()
			v = vmap(*p.position)
			m.set(vmap.prop, v)

	def set(self, prop, v):
		super(Group, self).set(prop, v)
		for c in self._children:
			if c:
				c.set(prop, v)

	def key(self, prop, timeline):
		super(Group, self).key(prop, timeline)
		for c in self._children:
			if c:
				c.key(prop, timeline)

	def distill(self):
		g = node.Group(self.name)
		for m in self._children:
			for c in m.distill():
				if c:
					g.addObject(c)
		return g

class Text(Object):
	def __init__(self, name, text):
		super(Text, self).__init__(name)
		self._text = text
		self.halign = 'center'
		self.valign = 'center'
		self.depth = 0
		# TODO phase this list out
		self._letters = []

	def _tweenLetter(self, l, tweenSet, prop, makeEndState, makeCurve):
		if l:
			tween = CurveTweener()
			tween.setObject(l, prop, makeEndState(l))
			tween.setCurve(makeCurve(l))
			tweenSet.addTween(tween)
		else:
			tweenSet.addTween(None)

	def breakApart(self, curve=None):
		# TODO set scale
		xOffset = 0.18*self.getScale()
		yOffset = 0.28*self.getScale()
		def collect(line):
			offset = None
			if self.halign == 'center':
				offset = node.Placement(start=(len(line)*0.5*-xOffset, 0, 0))
			elif self.halign == 'right':
				offset = node.Placement(start=(len(line)*-xOffset, 0, 0))
			if offset:
				for letter in line:
					if letter:
						letter.getPlacement().move(offset)

		self._letters = []
		lineCollect = []
		i, j, k = (0, 0, 0)
		for c in self._text:
			if c == '\n':
				i = 0
				j += 1
				l = None
				# Realign column
				collect(lineCollect)
				lineCollect = []
			else:
				if c == ' ':
					l = None
				else:
					l = Text('%s_%05d' % (self.name, k), c)
					l.copyAttributes(self)
					if curve:
						offset = curve(i, j)
						l.getPlacement().move(offset)
					else:
						offset = node.Placement(start=(i*xOffset, -j*yOffset, 0))
						l.getPlacement().move(offset)
					k += 1
				self._letters.append(l)
				lineCollect.append(l)
				i += 1

		collect(lineCollect)

		# Realing columns
		offset = None
		if self.valign == 'center':
			offset = node.Placement(start=(0, (j+0)*0.5*yOffset, 0))
		elif self.valign == 'bottom':
			offset = node.Placement(start=(0, (j+0)*yOffset, 0))
		if offset:
			for letter in self._letters:
				if letter:
					letter.getPlacement().move(offset)

		# XXX remove when phasing _letters into _children
		self._children = self._letters
		return self._letters

	def getGroup(self):
		# TODO cache
		g = None
		if self._letters:
			g = Group('text:' + str(self.name))
			for l in self._letters:
				if l:
					g.addObject(l)
		return g

	def getText(self):
		return self._text

	def createTweenSet(self, prop, makeEndState, makeCurve):
		tweenSet = TweenSet()
		for l in self._letters:
			self._tweenLetter(l, tweenSet, prop, makeEndState, makeCurve)

		return tweenSet

	def createTweenSetBackwards(self, prop, makeEndState, makeCurve):
		tweenSet = TweenSet()
		for l in self._letters[::-1]:
			self._tweenLetter(l, tweenSet, prop, makeEndState, makeCurve)

		return tweenSet

	def distill(self):
		nodes = []
		if self._letters:
			for l in self._letters:
				if l:
					nodes.extend(l.distill())
		else:
			nodes = [node.Text(self.name, self)]

		return nodes

class ParticleSystem(Object):
	def __init__(self, name):
		super(ParticleSystem, self).__init__(name)
		self.maxParticles = 100
		self.actions = None
		self.particles = None
		self.lookAtCamera = False
		self.sequential = True
		self.speed = 1.0

	def distill(self):
		return [node.ParticleSystem(self.name, self)]
