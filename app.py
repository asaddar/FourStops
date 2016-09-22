import requests
import urllib2
import json
from flask import Flask, render_template, request, url_for

geo_url = 'https://maps.googleapis.com/maps/api/geocode/json'
directions_url = 'https://maps.googleapis.com/maps/api/directions/json'
foursquare_url = 'https://api.foursquare.com/v2/venues/explore'
address_container = []
id = 1

app = Flask(__name__)

def get_directions(origin, destination):
	directions_payload = {'origin': origin, 'destination': destination, 'key': 'AIzaSyBaJ5oJ6uTTQrLhBf-uVCKSX2RqdMLJPFU'}
	directions_req = requests.get(directions_url, params=directions_payload)
	directions_json = directions_req.json()
	directions_list = []

	for item in directions_json['routes'][0]['legs'][0]['steps']:
		step = item['html_instructions']
		step = step.replace("<b>", "")
		step = step.replace("</b>", "")
		step = step.replace('<div style="font-size:0.9em"', '')
		step = step.replace("</div>", "")
		step = step.replace(">", " ")
		directions_list.append(step)

	return directions_list


def get_coordinates(location):
	geo_payload = {'address': location, 'key': 'AIzaSyBaJ5oJ6uTTQrLhBf-uVCKSX2RqdMLJPFU'}
	geo_req = requests.get(geo_url, params=geo_payload)
	geo_json = geo_req.json()

	latitude = str(geo_json['results'][0]['geometry']['location']['lat'])
	longitude = str(geo_json['results'][0]['geometry']['location']['lng'])

	coordinates = {
		'latitude': latitude,
		'longitude': longitude 
	}
	
	return coordinates


def get_venue_info(lat, lng):
	foursquare_payload = {'oauth_token': 'OYOW4WMMFS5W4NOVMOY2E3AH43BAFEI5JAGAOOBYZ3UBVV5C',
						'll': lat + ',' + lng,
						'section': 'sights',
						'limit': '10',
						'v':'20131016'}
	foursquare_req = requests.get(foursquare_url, params=foursquare_payload)
	foursquare_json = foursquare_req.json()
	venues = []

	for item in foursquare_json['response']['groups'][0]['items']:
		serialized = {}
		serialized['name'] = item['venue']['name']
		try:
			serialized['address'] = item['venue']['location']['address'] + ", " + item['venue']['location']['formattedAddress'][1]
		except:
			serialized['address'] = ','.join([x for x in item['venue']['location']['formattedAddress']])

		venues.append(serialized)

	return venues


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/selectfirst", methods=['GET', 'POST'])
def selectfirst():
	starting_address = request.form["startingaddress"]
	ending_address = request.form["endingaddress"]
	address_container.append(ending_address)
	address_container.append(starting_address)

	coordinates = get_coordinates(starting_address)
	venues = get_venue_info(coordinates['latitude'], coordinates['longitude'])
	print venues

	return render_template("choosefirst.html", venues=venues)


@app.route("/directions/<choice>")
def selectnext(choice):
	global id
	address_container.append(choice)
	id += 1

	directions = get_directions(address_container[id-1], choice)
	coordinates = get_coordinates(choice)
	venues = get_venue_info(coordinates['latitude'], coordinates['longitude'])
	print venues

	return render_template("choices.html", firstspot=address_container[id-1], secondspot=choice, directions=directions, venues=venues, id=id-1)


@app.route("/directions/nearend/<choice>")
def selectfourth(choice):
	address_container.append(choice)
	print address_container
	directions = get_directions(address_container[4], choice)
	return render_template("choosefourth.html", firstspot=address_container[4], secondspot=choice, directions=directions)


@app.route("/end")
def end():
	directions = get_directions(address_container[5], address_container[0])
	print address_container
	return render_template("final.html", firstspot=address_container[5], secondspot=address_container[0], directions=directions)


if __name__ == "__main__":
	app.debug = True
	app.run()