import node
import copy
import curve

class Document(object):
	def __init__(self):
		self._x = 0
		self._objs = []
		self._groups = []
		self._times = []
		self._firstScene = None

	def addScene(self, (name, rootTimeline), isFirst=False):
		t = Timeline('scene:' + name)
		self.registerTimeline(t)
		t.changeTimeline(rootTimeline)
		if isFirst:
			self._firstScene = rootTimeline

	def registerObject(self, obj):
		self._objs.append(copy.deepcopy(obj))

	def registerTimeline(self, obj):
		self._times.append(obj)

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

		if self._firstScene:
			first = Timeline('scene:_autostart', True)
			first.changeTimeline(self._firstScene)
			story.addTimeline(first.distill())

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
					ta.addAction(diff)
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

	def startScene(self, scene):
		# lolhax
		s = Timeline('scene:' + scene)
		self.changeTimeline(s)

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
		self._timeline = Timeline('tween:%d' % Tweener._t)
		Tweener._t += 1
		self.grain = 0.2
		self.adaptive = False
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

	def getTimeline(self):
		return self._timeline

	def tween(self, duration):
		def frange(end, step):
			start = 0
			while start < end:
				yield start
				start += step

		for t in frange(duration + self.grain, self.grain):
			v = self._builtCurve(t/duration)
			self._obj.set(self._prop, v)
			self._obj.key(self._prop, self._timeline)
			self._timeline.advance(self.grain)

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

	def tweenAcross(self, diff, duration):
		master = Timeline('tweenset:%i' % TweenSet._x)
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

	def copyAttributes(self, other):
		self._props.clear()
		self._props.copy(other._props)

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

	def set(self, prop, v):
		getattr(self, 'set' + prop)(v)

	def get(self, prop):
		return getattr(self, 'get' + prop)()

	def key(self, prop, timeline):
		getattr(self, 'key' + prop)(timeline)

class Text(Object):
	def __init__(self, name, text):
		super(Text, self).__init__(name)
		self._text = text
		self.halign = 'center'
		self.valign = 'center'
		self.depth = 0
		self._letters = []

	def _tweenLetter(self, l, tweenSet, prop, makeEndState, makeCurve):
		if l:
			tween = Tweener()
			tween.setObject(l, prop, makeEndState(l))
			tween.setCurve(makeCurve(l))
			tweenSet.addTween(tween)
		else:
			tweenSet.addTween(None)

	def breakApart(self, curve=None):
		xOffset = 0.18
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
				# Realign
				collect(lineCollect)
				lineCollect = []
			else:
				if c == ' ':
					l = None
				else:
					l = Text('%s_%05d' % (self.name, k), c)
					l.copyAttributes(self)
					if curve:
						offset = curve(i)
						l.getPlacement().move(offset)
					else:
						# TODO set scale
						offset = node.Placement(start=(i*xOffset, -j*0.28, 0))
						l.getPlacement().move(offset)
					k += 1
				self._letters.append(l)
				lineCollect.append(l)
				i += 1

		collect(lineCollect)

		return self._letters

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
