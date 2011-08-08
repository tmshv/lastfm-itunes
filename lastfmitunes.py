import re
from urllib import quote
import urllib2
import sys
from appscript import *
from lxml import etree

try:
	username = sys.argv[1]
except:
	print 'username not found'
	exit()

def load_resource(url):
	response = urllib2.urlopen(url)
	return response.read()

def get_last_fm_track(artist, album, title):
	url = 'http://ws.audioscrobbler.com/2.0/?method=<method>&api_key=<key>&artist=<artist>&track=<title>&username=<user>&autocorrect=<correction>'
	url = re.sub('<method>', 'track.getinfo', url)
	url = re.sub('<key>', 'b25b959554ed76058ac220b7b2e0a026', url)
	url = re.sub('<artist>', quote(artist), url)
	url = re.sub('<title>', quote(title), url)
	url = re.sub('<user>', username, url)
	url = re.sub('<correction>', '1', url)
	return load_resource(url)

def get_play_count_from_xml(xml_raw):
	xmlroot = etree.XML(xml_raw)
	try:
		upc = xmlroot.xpath('/lfm/track/userplaycount')[0]
		count = int(upc.text)
	except:
		count = 0
	return count

def update_itunes_track(track, count):
	old = track.played_count.get()
	track.played_count.set(count)
	print track.name.get()+': old is '+str(old)+', new is '+str(count)

itunes = app('iTunes')
lib = itunes.windows.get()[0].view.get().tracks.get()
list = []
for t in lib:
	list.append(t)

for t in list:
	a = t.artist.get().encode('UTF-8')
	al = t.album.get().encode('UTF-8')
	n = t.name.get().encode('UTF-8')
	resp = get_last_fm_track(a, al, n)
	count = get_play_count_from_xml(resp)
	if count > 0:
		update_itunes_track(t, count)