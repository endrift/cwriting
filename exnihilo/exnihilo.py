import cwriting.core as core
import cwriting.node as node
import cwriting.curve as curve

import math

def makeRiseTween(d, obj, duration, real, diff=node.Placement(start=(0, -0.2, 0))):
	tl = core.Timeline(d.next())
	d.registerTimeline(tl)
	obj.setPlacement(real.moved(diff))
	obj.setVisibility(False)
	obj.keyPlacement(tl)
	obj.keyVisibility(tl)
	objTweenIn = core.CurveTweener()
	objTweenIn.setObject(obj, 'Placement', real)
	objTweenIn.setCurve(curve.quadOut3) 
	objTweenIn.tween(duration)
	d.registerTimeline(objTweenIn.getTimeline())
	tl.changeTimeline(objTweenIn.getTimeline())
	tl.advance(duration)
	obj.setVisibility(True)
	obj.keyVisibility(tl)
	return tl

def makeFallTween(d, obj, duration, real, diff=node.Placement(start=(0, -0.2, 0))):
	tl = core.Timeline(d.next())
	d.registerTimeline(tl)
	obj.setPlacement(real)
	obj.setVisibility(True)
	obj.keyPlacement(tl)
	obj.keyVisibility(tl)
	objTweenIn = core.CurveTweener()
	objTweenIn.setObject(obj, 'Placement', real.moved(diff))
	objTweenIn.setCurve(curve.quadIn3) 
	objTweenIn.tween(duration)
	d.registerTimeline(objTweenIn.getTimeline())
	tl.changeTimeline(objTweenIn.getTimeline())
	tl.advance(duration)
	obj.setVisibility(False)
	obj.keyVisibility(tl)
	return tl

def genSceneList(d):
	tl0 = core.Timeline(d.next())
	d.registerTimeline(tl0)

	enable = core.Timeline('_linksEnable')
	d.registerTimeline(enable)

	disable = core.Timeline('_linksDisable')
	d.registerTimeline(disable)

	scenes = d.getScenes()
	y = 0
	for s in scenes:
		t = core.Text(d.next(), s['longname'])
		enable.changeLink(t, True)
		disable.changeLink(t, False)

		p = node.Placement(start=(0, 0.3*(len(scenes) / 2.0 - y), 0))
		p.relativeTo = 'RightWall'
		t.setPlacement(p)

		tl = core.Timeline(d.next())
		d.registerTimeline(tl)
		tl.changeTimeline(disable)
		tl.startScene(s['name'])
		tl.advance(s['timeline'].current())
		tl.changeTimeline(enable)

		t.link = node.Link()
		t.link.addAction(node.TimerChange(tl, 'start'))
		d.registerObject(t)
		t.keyVisibility(tl0)
		s['text'] = t
		y += 1

	tl0.advance(1)

	for s in scenes:
		s['text'].setVisibility(True)
		s['text'].keyVisibility(tl0)

	return {
		'name': '_list',
		'timeline': tl0
	}

def genScene0(d):
	tl0 = core.Timeline(d.next())
	d.registerTimeline(tl0)
	
	tlBegin = core.Timeline('begin')
	d.registerTimeline(tlBegin)
	
	exnihilo = core.Text(d.next(), 'Ex Nihilo')
	exnihilo.setScale(3)
	exnihilo.setVisibility(False)
	exnihilo.setPlacement(node.Placement(start=(0, -2, -2)))
	d.registerObject(exnihilo)
	
	begin = core.Text(d.next(), 'begin')
	begin.setVisibility(False)
	begin.setPlacement(node.Placement(start=(0, -2, -3)))
	begin.link = node.Link()
	begin.link.addAction(node.TimerChange(tlBegin, 'start'))
	d.registerObject(begin)
	
	exnihilo.keyVisibility(tl0)
	exnihiloTweenIn = core.CurveTweener()
	exnihiloTweenIn.setObject(exnihilo, 'Placement', node.Placement(start=(0, 1, -2)))
	exnihiloTweenIn.setCurve(curve.quadOut3)
	exnihiloTweenIn.tween(3)
	d.registerTimeline(exnihiloTweenIn.getTimeline())
	tl0.changeTimeline(exnihiloTweenIn.getTimeline())
	
	tl0.advance(0.5)
	begin.keyVisibility(tl0)
	beginTweenIn = core.CurveTweener()
	beginTweenIn.setObject(begin, 'Placement', node.Placement(start=(0, 0, -2)))
	beginTweenIn.setCurve(curve.quadOut3)
	beginTweenIn.tween(2.5)
	d.registerTimeline(beginTweenIn.getTimeline())
	tl0.changeTimeline(beginTweenIn.getTimeline())
	
	tl0.advance(2.5)
	exnihilo.setVisibility(True)
	exnihilo.keyVisibility(tl0)
	exnihilo.keyVisibility(tlBegin)
	tl0.advance(0.5)
	begin.setVisibility(True)
	begin.keyVisibility(tl0)

	beginSfx = node.Sound(d.next(), './res/00_s00.mp3')
	d.registerSound(beginSfx)
	tlBegin.playSound(beginSfx)
	exnihilo.keyVisibility(tlBegin)
	exnihiloTweenOut = core.CurveTweener()
	exnihiloTweenOut.setObject(exnihilo, 'Placement', node.Placement(start=(0, 4, -2)))
	exnihiloTweenOut.setCurve(curve.quadIn3)
	exnihiloTweenOut.tween(2)
	d.registerTimeline(exnihiloTweenOut.getTimeline())
	tlBegin.changeTimeline(exnihiloTweenOut.getTimeline())


	tlBegin.advance(1)
	begin.keyVisibility(tlBegin)
	tlBegin.advance(1)
	exnihilo.setVisibility(False)
	exnihilo.keyVisibility(tlBegin)
	tlBegin.advance(1)
	begin.setVisibility(False)
	begin.keyVisibility(tlBegin)
	tlBegin.startScenes(d)

	return {
		'name': 'begin', 
		'timeline': tl0
	}

def genSceneEnd(d):
	tl0 = core.Timeline(d.next())
	d.registerTimeline(tl0)

	tl = core.Timeline(d.next())
	d.registerTimeline(tl)

	t = core.Text(d.next(), 'restart')
	t.setPlacement(node.Placement(start=(0, 0, -2)))
	t.link = node.Link()
	t.link.addAction(node.TimerChange(tl, 'start'))
	d.registerObject(t)

	tl0.advance(1)

	t.keyVisibility(tl0)
	tl0.advance(1)
	t.setVisibility(True)
	t.keyVisibility(tl0)
	t.keyVisibility(tl)

	tTweenOut = core.CurveTweener()
	tTweenOut.setObject(t, 'Placement', node.Placement(start=(0, 0, 4)))
	tTweenOut.setCurve(curve.quadIn3)
	tTweenOut.tween(2)
	d.registerTimeline(tTweenOut.getTimeline())
	tl.changeTimeline(tTweenOut.getTimeline())
	tl.advance(2)
	t.setVisibility(False)
	t.keyVisibility(tl)
	tl.advance(1)
	tl.restart()

	return {
		'name': 'end',
		'timeline': tl0
	}

def genSceneInTheBeginning(d):
	tl0 = core.Timeline('scene:inTheBeginning')
	d.registerTimeline(tl0)

	tl0.advance(1)
	inTheBeginning = core.Text(d.next(), 'In the beginning')
	inTheBeginning.setPlacement(node.Placement(start=(0, 1, -2)))
	d.registerObject(inTheBeginning)

	inTheBeginningSound = node.Sound(d.next(), './res/01_l00.mp3')
	d.registerSound(inTheBeginningSound)

	tl0.playSound(inTheBeginningSound)
	inTheBeginning.keyVisibility(tl0)
	tl0.advance(0.05)
	inTheBeginning.setVisibility(True)
	inTheBeginning.keyVisibility(tl0)
	tl0.advance(1)

	thereWasNothing = core.Text(d.next(), 'there was nothing.')
	thereWasNothing.setPlacement(node.Placement(start=(0, 0.8, -2)))
	d.registerObject(thereWasNothing)
	thereWasNothing.keyVisibility(tl0)

	inTheBeginningTweenUp = core.CurveTweener()
	inTheBeginningTweenUp.setObject(inTheBeginning, 'Placement', node.Placement(start=(0, 1.2, -2)))
	inTheBeginningTweenUp.setCurve(curve.quadOut3) 
	inTheBeginningTweenUp.tween(1)
	d.registerTimeline(inTheBeginningTweenUp.getTimeline())
	tl0.changeTimeline(inTheBeginningTweenUp.getTimeline())

	tl0.advance(1)
	thereWasNothing.setVisibility(True)
	thereWasNothing.keyVisibility(tl0)

	tl0.advance(2)
	inTheBeginning.setVisibility(True)
	inTheBeginning.keyVisibility(tl0)
	thereWasNothing.setVisibility(True)
	thereWasNothing.keyVisibility(tl0)

	inTheBeginningTweenOut = core.CurveTweener()
	inTheBeginningTweenOut.setObject(inTheBeginning, 'Placement', node.Placement(start=(0, 1.2, -6)))
	inTheBeginningTweenOut.setCurve(curve.quadIn3) 
	inTheBeginningTweenOut.tween(2)
	d.registerTimeline(inTheBeginningTweenOut.getTimeline())
	tl0.changeTimeline(inTheBeginningTweenOut.getTimeline())

	thereWasNothingTweenOut = core.CurveTweener()
	thereWasNothingTweenOut.setObject(thereWasNothing, 'Placement', node.Placement(start=(0, 0.8, -6)))
	thereWasNothingTweenOut.setCurve(curve.quadIn3) 
	thereWasNothingTweenOut.tween(2)
	d.registerTimeline(thereWasNothingTweenOut.getTimeline())
	tl0.changeTimeline(thereWasNothingTweenOut.getTimeline())

	tl0.advance(2)
	inTheBeginning.setVisibility(False)
	inTheBeginning.keyVisibility(tl0)
	thereWasNothing.setVisibility(False)
	thereWasNothing.keyVisibility(tl0)
	
	fromNothing = core.Text(d.next(), "From nothing,\nthe world began")
	fromNothing.setPlacement(node.Placement(start=(0, 1.2, -2)))
	fromNothing.breakApart()
	d.registerObject(fromNothing)

	fromNothingSound = node.Sound(d.next(), './res/01_l01.mp3')
	d.registerSound(fromNothingSound)

	fromNothingTweensIn = fromNothing.createTweenSet('Visibility', (lambda t: node.Boolean('Visibility', True)), (lambda t: curve.floor1))
	fromNothingTweensIn.register(d)
	fromNothingTweensIn.setLazyKeying(True)
	tlFromNothingIn = fromNothingTweensIn.tweenAcross(0.1, 1.5)
	d.registerTimeline(tlFromNothingIn)
	tl0.changeTimeline(tlFromNothingIn)
	tl0.playSound(fromNothingSound)

	tl0.advance(5)
	fromNothingTweensOut1 = fromNothing.createTweenSetBackwards('Visibility', (lambda t: node.Boolean('Visibility', False)), (lambda t: curve.floor1))
	fromNothingTweensOut1.register(d)
	fromNothingTweensOut1.setLazyKeying(True)
	tlFromNothingOut1 = fromNothingTweensOut1.tweenAcross(0.1, 1)
	d.registerTimeline(tlFromNothingOut1)
	tl0.changeTimeline(tlFromNothingOut1)
	fromNothingTweensOut2 = fromNothing.createTweenSetBackwards('Placement', (lambda t: t.getPlacement().moved(node.Placement(start=(0, -2, 0)))), (lambda t: curve.quadIn3))
	fromNothingTweensOut2.register(d)
	tlFromNothingOut2 = fromNothingTweensOut2.tweenAcross(0.1, 2)
	d.registerTimeline(tlFromNothingOut2)
	tl0.changeTimeline(tlFromNothingOut2)
	tl0.advance(4)

	return {'name': 'inTheBeginning',
		'longname': 'In The Beginning',
		'timeline': tl0
	}

def genSceneRain(d):
	def waves(n):
		return (lambda s, t: 0.2*math.sin(n)*(math.sin(2.5*s+n) + math.sin(2.5*t+n)) + (t-1)*(t-1)*0.1 + n/3.5 - 3.0)

	tl0 = core.Timeline('scene:rain')
	d.registerTimeline(tl0)

	sceneText = core.Text(d.next(), 'First, the rains rained and the\n'
	                                'seas filled. An almost endless\n'
	                                'deluge filled the yawning void\n'
	                                'that had preceded the oceans.')

	sceneText2 = core.Text(d.next(), 'Slowly, the rains ceased and\n'
	                                 'the water stopped rising.\n'
	                                 '\n'
	                                 'The rain was done.')

	sceneText.setPlacement(node.Placement(start=(0, 2.0, -2)))
	d.registerObject(sceneText)
	sceneText.keyPlacement(tl0)
	sceneText.keyVisibility(tl0)
	sceneText2.setPlacement(node.Placement(start=(0, 0.5, -2)))
	d.registerObject(sceneText2)
	sceneText2.keyPlacement(tl0)
	sceneText2.keyVisibility(tl0)

	sceneSound = node.Sound(d.next(), './res/02_l00.mp3')
	sceneSound2 = node.Sound(d.next(), './res/02_l01.mp3')
	d.registerSound(sceneSound)
	d.registerSound(sceneSound2)

	rainSfx = node.Sound(d.next(), './res/02_s00.mp3')
	rainSfx.freq = 0.6
	rainSfx.volume = 0.3
	d.registerSound(rainSfx)

	tlRain = core.Timeline(d.next())
	d.registerTimeline(tlRain)
	#tl0.changeTimeline(tlRain)

	s = []
	text = 'the rains fell, the seas filled, '
	for y in range(12):
		for x in range(20):
			s.append(text[(x + 4*y) % len(text)])
		s.append('\n')
	s = ''.join(s)
	theRains = core.Text(d.next(), s)
	theRains.setScale(2.1)
	# XXX HACK ATTACK
	theRains.breakApart(lambda s, t: node.Placement(start=(s*.4, 0, t*.7 - 5)))
	theRainsG = theRains.getGroup()
	theRainsG.applyMap(curve.HeightMap(None, 2, waves(0)))
	d.registerObject(theRains)

	theRainsP = core.Text(d.next(), 'the rains')
	theRainsPGroup = core.Group('rains')
	theRainsPGroup.addObject(theRainsP)
	theRainsPSystem = core.ParticleSystem(d.next())
	theRainsPSystem.speed = 0.3
	theRainsPActions = node.ParticleActionList(d.next())
	theRainsPSystem.actions = theRainsPActions
	theRainsPActions.setRate(2)
	theRainsPGravity = node.Gravity()
	theRainsPGravity.setDirection((-0.2, -0.5, 0))
	theRainsPActions.addAction(theRainsPGravity)
	theRainsPSystem.particles = theRainsPGroup
	theRainsPSource = node.Disc()
	theRainsPSource.setCenter((0, 8, 0))
	theRainsPSource.setNormal((0.2, -1.0, 0))
	theRainsPSource.setRadius(8)
	theRainsPVel = node.Point()
	theRainsPVel.setPoint((-1, -3, -2))
	theRainsPActions.setSource(theRainsPSource)
	theRainsPActions.setVel(theRainsPVel)
	theRainsPActions.setRemoveCondition(node.Age(6))
	d.registerObject(theRainsP)
	d.registerObject(theRainsPSystem)
	d.registerGroup(theRainsPGroup)
	d.registerParticleActions(theRainsPSystem.actions)

	tlWaves = core.Timeline('waves')
	d.registerTimeline(tlWaves)
	for t in range(72):
		if t:
			tlWaves.advance(1/4.0)
		theRainsG.applyMap(curve.HeightMap(None, 2, waves(t*2.0/15.0*math.pi)))
		theRainsG.key('Placement', tlWaves)
		if t == 64:
			theRainsG.set('Visibility', True)
			theRainsG.key('Visibility', tlWaves)
	theRainsG.set('Visibility', False)
	theRainsG.key('Visibility', tlWaves)
	tlWaves.advance(0.01)
	#tlWaves.freeze(True)

	tl0.changeTimeline(tlWaves)
	theRainsG.key('Visibility', tl0)
	theRainsPSystem.key('Visibility', tl0)

	sceneTextTweenIn = core.CurveTweener()
	sceneTextTweenIn.setObject(sceneText, 'Placement', node.Placement(start=(0, 2.2, -2)))
	sceneTextTweenIn.setCurve(curve.quadOut3) 
	sceneTextTweenIn.tween(1)
	d.registerTimeline(sceneTextTweenIn.getTimeline())
	tl0.changeTimeline(sceneTextTweenIn.getTimeline())
	tl0.playSound(sceneSound)
	tl0.playSound(rainSfx)

	tl0.advance(1)
	theRainsG.set('Visibility', True)
	theRainsG.key('Visibility', tl0)
	theRainsPSystem.set('Visibility', True)
	theRainsPSystem.key('Visibility', tl0)
	sceneText.setVisibility(True)
	sceneText.keyVisibility(tl0)

	tl0.advance(15)
	tl0.playSound(sceneSound2)
	sceneText2.keyPlacement(tl0)
	sceneText2.keyVisibility(tl0)
	sceneText2TweenIn = core.CurveTweener()
	sceneText2TweenIn.setObject(sceneText2, 'Placement', node.Placement(start=(0, 0.7, -2)))
	sceneText2TweenIn.setCurve(curve.quadOut3) 
	sceneText2TweenIn.tween(1)
	d.registerTimeline(sceneText2TweenIn.getTimeline())
	tl0.changeTimeline(sceneText2TweenIn.getTimeline())
	theRainsPSystem.key('Visibility', tl0)
	tl0.advance(1)
	sceneText2.setVisibility(True)
	sceneText2.keyVisibility(tl0)

	#for i in xrange(int(tl0.current()/0.5)):
	#	tlRain.playSound(rainSfx)
	#	tlRain.advance(0.5)

	tl0.advance(2)
	theRainsPSystem.set('Visibility', False)
	theRainsPSystem.key('Visibility', tl0)

	tl0.advance(5)
	tl0.changeTimeline(makeFallTween(d, sceneText, 1, node.Placement(start=(0, 2.2, -2))))
	tl0.changeTimeline(makeFallTween(d, sceneText2, 1, node.Placement(start=(0, 0.7, -2))))
	tl0.advance(1)

	return {
		'name': 'rain',
		'longname': 'The Rains',
		'timeline': tl0
	}

def genSceneLands(d):
	tl0 = core.Timeline('scene:lands')
	d.registerTimeline(tl0)

	sceneText = core.Text(d.next(), 'But the oceans were unending.')
	sceneText2 = core.Text(d.next(), 'From beneath the infinite oceans\n'
	                                 'rose the lands. Solid stone jutted\n'
	                                 'out. The mountains towered, and\n'
	                                 'slowly the land emerged from the\n'
	                                 'ocean. There was a terminus\n'
	                                 'setting apart the seas.')

	sceneText.setPlacement(node.Placement(start=(0, 2.4, -2)))
	sceneText2.setPlacement(node.Placement(start=(0, 1.1, -2)))
	d.registerObject(sceneText)
	d.registerObject(sceneText2)

	sceneSound = node.Sound(d.next(), './res/03_l00.mp3')
	sceneSound2 = node.Sound(d.next(), './res/03_l01.mp3')
	d.registerSound(sceneSound)
	d.registerSound(sceneSound2)

	sceneSfx = node.Sound(d.next(), './res/03_s00.mp3')
	sceneSfx.volume = 0.7
	d.registerSound(sceneSfx)

	waterText = core.Text(d.next(), 'Into the horizon, into the eternity, the\n'
	                                'waters spread forever. North, south, east,\n'
	                                'and west: in all directions, the waters\n'
	                                'were all that could be seen, for the waters\n'
	                                'were all there was. Above the waters, the\n'
	                                'skies looked down upon her brother and saw\n'
	                                'the loneliness of his expanse. She knew\n'
	                                'something was missing, and she knew that\n'
	                                'there was more to come. There must be no\n'
	                                'infinite; there must be bounds, they must\n'
	                                'just be found. After the rains, the waters\n'
	                                'were calm. But this too must not last, for\n'
	                                'the bleak emptiness of the unending filled\n'
	                                'the waters. This pure boredom of the waters,\n'
	                                'with no waves and no motion, must be ended\n'
	                                'somehow. The end has yet to be seen, but\n'
	                                'there must be an end. There must be an end.\n'
	                                'Where is the end? The end must be found. The\n'
	                                'skies and the seas must make this end. There\n'
	                                'will be a terminus. There must be an end.')
	waterText.setScale(2)
	waterText.valign = 'bottom'
	waterText.setPlacement(node.Placement(start=(0, -3, 0), rotation=node.AxisRotation(axis=(1, 0, 0), rotation=-90)))
	d.registerObject(waterText)
	waterText.keyVisibility(tl0)

	tl0.changeTimeline(makeRiseTween(d, sceneText, 1, node.Placement(start=(0, 2.6, -2))))
	tl0.playSound(sceneSound)
	tl0.playSound(sceneSfx)
	tl0.advance(1)

	waterText.setVisibility(True)
	waterText.keyVisibility(tl0)
	tl0.advance(2)

	mountain01 = core.Text(d.next(), 'The mountains rose from beneath the seas, filling the space around them. And here did the oceans part.'.replace(' ', '\n'))
	mountain01.halign = 'right'
	mountain01.setScale(2)
	mountain01.setPlacement(node.Placement(start=(-5, -4, -5), rotation=node.LookAt(target=(-2, -2.8, -4.5), up=(0, 0, -1))))
	d.registerObject(mountain01)
	mountain01.keyVisibility(tl0)
	mountain01.keyPlacement(tl0)


	mountain02 = core.Text(d.next(), 'No longer whole, the seas were sundered by cliffs and beaches. And beyond these shores lay more still.'.replace(' ', '\n'))
	mountain02.halign = 'left'
	mountain02.setScale(2)
	mountain02.setPlacement(node.Placement(start=(5, -4, -5), rotation=node.LookAt(target=(2, -2.8, -4.5), up=(0, 0, -1))))
	d.registerObject(mountain02)
	mountain02.keyVisibility(tl0)
	mountain02.keyPlacement(tl0)

	mountain01TweenIn = core.CurveTweener()
	mountain01TweenIn.setObject(mountain01, 'Placement', mountain01.getPlacement().moved(node.Placement(start=(-0.2, 1, 0), rotation=node.LookAt(up=(0, 0, -1)))))
	mountain01TweenIn.setCurve(curve.quadOut3)
	mountain01TweenIn.tween(2)
	d.registerTimeline(mountain01TweenIn.getTimeline())
	tl0.changeTimeline(mountain01TweenIn.getTimeline())

	mountain02TweenIn = core.CurveTweener()
	mountain02TweenIn.setObject(mountain02, 'Placement', mountain02.getPlacement().moved(node.Placement(start=(0.2, 1, 0), rotation=node.LookAt(up=(0, 0, -1)))))
	mountain02TweenIn.setCurve(curve.quadOut3)
	mountain02TweenIn.tween(2)
	d.registerTimeline(mountain02TweenIn.getTimeline())
	tl0.changeTimeline(mountain02TweenIn.getTimeline())

	tl0.advance(1)

	mountain01.setVisibility(True)
	mountain01.keyVisibility(tl0)
	mountain02.setVisibility(True)
	mountain02.keyVisibility(tl0)

	tl0.playSound(sceneSound2)
	tl0.changeTimeline(makeRiseTween(d, sceneText2, 1, node.Placement(start=(0, 1.3, -2))))
	tl0.advance(15)

	tl0.changeTimeline(makeFallTween(d, sceneText, 1, node.Placement(start=(0, 2.6, -2))))
	tl0.changeTimeline(makeFallTween(d, sceneText2, 1, node.Placement(start=(0, 1.3, -2))))
	tl0.changeTimeline(makeFallTween(d, waterText, 1, node.Placement(start=(0, -3, 0), rotation=node.AxisRotation(axis=(1, 0, 0), rotation=-90)), diff=node.Placement(start=(0, 0, 2))))

	mountain01.keyVisibility(tl0)
	mountain01TweenOut = core.CurveTweener()
	mountain01TweenOut.setObject(mountain01, 'Placement', mountain01.getPlacement().moved(node.Placement(start=(-0.5, 1, 0), rotation=node.LookAt(target=(-0.2, 0, 0), up=(0, 0, -1)))))
	mountain01TweenOut.setCurve(curve.quadIn3)
	mountain01TweenOut.tween(1)
	d.registerTimeline(mountain01TweenOut.getTimeline())
	tl0.changeTimeline(mountain01TweenOut.getTimeline())

	mountain02.keyVisibility(tl0)
	mountain02TweenOut = core.CurveTweener()
	mountain02TweenOut.setObject(mountain02, 'Placement', mountain02.getPlacement().moved(node.Placement(start=(0.5, 1, 0), rotation=node.LookAt(target=(0.2, 0, 0), up=(0, 0, -1)))))
	mountain02TweenOut.setCurve(curve.quadIn3)
	mountain02TweenOut.tween(1)
	d.registerTimeline(mountain02TweenOut.getTimeline())
	tl0.changeTimeline(mountain02TweenOut.getTimeline())

	tl0.advance(1)
	
	mountain01.setVisibility(False)
	mountain01.keyVisibility(tl0)
	mountain02.setVisibility(False)
	mountain02.keyVisibility(tl0)

	tl0.advance(0.2)

	return {
		'name': 'lands',
		'longname': 'The Lands',
		'timeline': tl0
	}

def genSceneStillYoung(d):
	tl0 = core.Timeline('scene:stillyoung')
	d.registerTimeline(tl0)
	sceneText = core.Text(d.next(), 'The world was still young,\n'
	                                'and restless. For eons, the\n'
	                                'skies battled against their\n'
	                                'younger siblings. The skies\n'
	                                'thundered bolts of raw power,\n'
	                                'the lands erupted molten lava\n'
	                                'of pure heat, and the oceans\n'
	                                'boiled clouds of solid steam.')

	sceneText.setPlacement(node.Placement(start=(0, 1.1, -2)))
	d.registerObject(sceneText)

	sceneSound = node.Sound(d.next(), './res/04_l00.mp3')
	d.registerSound(sceneSound)

	sceneSfx = node.Sound(d.next(), './res/04_s00.mp3')
	sceneSfx.volume = 0.3
	d.registerSound(sceneSfx)

	tl0.playSound(sceneSfx)
	tl0.advance(0.5)
	tl0.playSound(sceneSound)
	tl0.changeTimeline(makeRiseTween(d, sceneText, 1, node.Placement(start=(0, 1.3, -2))))

	power = core.Text(d.next(), '                         er           pow       \n'
                                '                      powe         power        \n'
                                'power power power power power power   were power\n'
                                '        wer                 er po               \n'
                                '                               power po         \n')
	powerGroup = core.Group('power')
	powerGroup.addObject(power)
	powerSystem = core.ParticleSystem(d.next())
	powerActions = node.ParticleActionList(d.next())
	powerSystem.actions = powerActions
	powerActions.setRate(0.02)
	powerGravity = node.Gravity()
	powerGravity.setDirection((0, 0.05, 0))
	powerActions.addAction(powerGravity)
	powerSystem.particles = powerGroup
	powerSource = node.Box()
	powerSource.setP1((-2, 6, -2))
	powerSource.setP2((2, 8, 2))
	powerVel = node.Box()
	powerVel.setP1((-0.5, -2, -0.5))
	powerVel.setP2((0.5, -2, 0))
	powerActions.setSource(powerSource)
	powerActions.setVel(powerVel)
	powerRemoveCondition = node.Plane()
	powerRemoveCondition.setPoint((0, -10, 0))
	powerRemoveCondition.setNormal((0, 1, 0))
	powerActions.setRemoveCondition(node.Position(powerRemoveCondition))
	d.registerObject(power)
	d.registerObject(powerSystem)
	d.registerGroup(powerGroup)
	d.registerParticleActions(powerActions)

	powerSystem.key('Visibility', tl0)

	lava = core.Text(d.next(), 'lav')
	lava.breakApart()
	lavaGroup = lava.getGroup()
	lavaActions = node.ParticleActionList(d.next())
	lavaActions.setRate(10)
	lavaGravity = node.Gravity()
	lavaGravity.setDirection((0, -1, 0))
	lavaActions.addAction(lavaGravity)
	lavaSource = node.Plane()
	lavaSource.setNormal((0, 1, 0))
	lavaSource.setPoint((0, 0, 0))
	lavaVel = node.Cone()
	lavaVel.setApex((0, 0, 0))
	lavaVel.setBaseCenter((0, 3, 0))
	lavaVel.setRadius(1)
	lavaActions.setSource(lavaSource)
	lavaActions.setVel(lavaVel)
	lavaRemoveCondition = node.Plane()
	lavaRemoveCondition.setPoint((0, -0.1, 0))
	lavaRemoveCondition.setNormal((0, 1, 0))
	lavaActions.setRemoveCondition(node.Position(lavaRemoveCondition))
	d.registerObject(lava)
	d.registerGroup(lavaGroup)
	d.registerParticleActions(lavaActions)

	lavaSystem = core.ParticleSystem(d.next())
	lavaSystem.sequential = False
	lavaSystem.speed = 0.4
	lavaSystem.actions = lavaActions
	lavaSystem.particles = lavaGroup
	lavaSystem.setPlacement(node.Placement(start=(-3.2, -4, -2.1)))
	d.registerObject(lavaSystem)

	lavaSystem2 = core.ParticleSystem(d.next())
	lavaSystem2.sequential = False
	lavaSystem2.speed = 0.4
	lavaSystem2.actions = lavaActions
	lavaSystem2.particles = lavaGroup
	lavaSystem2.setPlacement(node.Placement(start=(-0.2, -4, -2.8)))
	d.registerObject(lavaSystem2)

	lavaSystem.key('Visibility', tl0)
	lavaSystem2.key('Visibility', tl0)

	steam = core.Text(d.next(), 'steam')
	steamGroup = core.Group('steam')
	steamGroup.addObject(steam)
	steamActions = node.ParticleActionList(d.next())
	steamActions.setRate(1)
	steamGravity = node.Gravity()
	steamGravity.setDirection((0, 0.1, 0))
	steamActions.addAction(steamGravity)
	steamSource = node.Disc()
	steamSource.setCenter((0, 0, 0))
	steamSource.setNormal((0, -1, 0))
	steamSource.setRadius(1)
	steamVel = node.Disc()
	steamVel.setCenter((0, 0.1, 0))
	steamVel.setNormal((0, -1, 0))
	steamVel.setRadius(0.2)
	steamActions.setSource(steamSource)
	steamActions.setVel(steamVel)
	steamActions.setRemoveCondition(node.Age(14))
	d.registerObject(steam)
	d.registerGroup(steamGroup)
	d.registerParticleActions(steamActions)

	steamSystem = core.ParticleSystem(d.next())
	steamSystem.sequential = False
	steamSystem.lookAtCamera = True
	steamSystem.speed = 0.1
	steamSystem.actions = steamActions
	steamSystem.particles = steamGroup
	steamSystem.setPlacement(node.Placement(start=(1.4, -4, -3.4)))
	d.registerObject(steamSystem)

	steamSystem2 = core.ParticleSystem(d.next())
	steamSystem2.sequential = False
	steamSystem2.lookAtCamera = True
	steamSystem2.speed = 0.1
	steamSystem2.actions = steamActions
	steamSystem2.particles = steamGroup
	steamSystem2.setPlacement(node.Placement(start=(3.4, -4, -2.3)))
	d.registerObject(steamSystem2)

	steamSystem.key('Visibility', tl0)
	steamSystem2.key('Visibility', tl0)

	tl0.advance(1)
	powerSystem.set('Visibility', True)
	powerSystem.key('Visibility', tl0)
	lavaSystem.set('Visibility', True)
	lavaSystem.key('Visibility', tl0)
	lavaSystem2.set('Visibility', True)
	lavaSystem2.key('Visibility', tl0)
	steamSystem.set('Visibility', True)
	steamSystem.key('Visibility', tl0)
	steamSystem2.set('Visibility', True)
	steamSystem2.key('Visibility', tl0)

	tl0.advance(18)
	
	sceneText.key('Visibility', tl0)
	powerSystem.key('Visibility', tl0)
	lavaSystem.key('Visibility', tl0)
	lavaSystem2.key('Visibility', tl0)
	steamSystem.key('Visibility', tl0)
	steamSystem2.key('Visibility', tl0)

	tl0.advance(1)

	sceneText.set('Visibility', False)
	sceneText.key('Visibility', tl0)
	powerSystem.set('Visibility', False)
	powerSystem.key('Visibility', tl0)
	lavaSystem.set('Visibility', False)
	lavaSystem.key('Visibility', tl0)
	lavaSystem2.set('Visibility', False)
	lavaSystem2.key('Visibility', tl0)
	steamSystem.set('Visibility', False)
	steamSystem.key('Visibility', tl0)
	steamSystem2.set('Visibility', False)
	steamSystem2.key('Visibility', tl0)

	return {
		'name': 'stillyoung',
		'longname': 'The Battles',
		'timeline': tl0
	}

d = core.Document()

d.setTitleScene(genScene0(d))

scenes = [genSceneInTheBeginning(d),
          genSceneRain(d),
          genSceneLands(d),
          genSceneStillYoung(d)]

for s in scenes:
	d.addScene(s)

d.addScene(genSceneEnd(d))

# Scenes don't have a good method for resetting
#d.addScene(genSceneList(d))

d.save('exnihilo.xml')
