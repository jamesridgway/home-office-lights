import ui
from random import random
from console import hud_alert
from rsmq import RedisSMQ

queue = RedisSMQ(host="192.168.75.243", qname="home-office-lights")

def slider_action(sender):
	# Get the root view:
	v = sender.superview
	# Get the sliders:
	r = v['slider1'].value
	g = v['slider2'].value
	b = v['slider3'].value
	# Create the new color from the slider values:
	v['view1'].background_color = (r, g, b)
	v['label1'].text = '#%.02X%.02X%.02X' % (int(r*255), int(g*255), int(b*255))

def set_action(sender):
	r = int(sender.superview['slider1'].value*255)
	g = int(sender.superview['slider2'].value*255)
	b = int(sender.superview['slider3'].value*255)
	queue.sendMessage().message({"type": "solid-colour", "r": r, "g": g, "b": b}).execute()
	hud_alert('Colour Set')

def off_action(sender):
	queue.sendMessage().message({"type": "off"}).execute()
	hud_alert('Lights off!')

def shuffle_action(sender):
	v = sender.superview
	s1 = v['slider1']
	s2 = v['slider2']
	s3 = v['slider3']
	s1.value = random()
	s2.value = random()
	s3.value = random()
	slider_action(s1)

v = ui.load_view('set-colour')
slider_action(v['slider1'])
if ui.get_screen_size()[1] >= 768:
	# iPad
	v.present('sheet')
else:
	# iPhone
	v.present()
