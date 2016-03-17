import urllib2
import json
from flask import Flask, render_template, request, url_for

app = Flask(__name__)

addresscontainer = []

def get_directions(origin, destination):
	origin = origin.replace(" ", "+")
	destination = destination.replace(" ", "+")

	urlbegin = "https://maps.googleapis.com/maps/api/directions/json?origin="+origin+"&destination="+destination
	urlcreate = urllib2.urlopen(urlbegin)
	dataJSON = json.load(urlcreate)

	directions_list = []

	for item in dataJSON['routes'][0]['legs'][0]['steps']:
		tempstr = item['html_instructions']
		tempstr = tempstr.replace("<b>", "")
		tempstr = tempstr.replace("</b>", "")
		tempstr = tempstr.replace('<div style="font-size:0.9em"', '')
		tempstr = tempstr.replace("</div>", "")
		directions_list.append(tempstr)

	return directions_list


def get_latlng(location):
	location = location.replace(" ", "+")
	maps_url = "http://maps.googleapis.com/maps/api/geocode/json?address="
	full_maps_url = maps_url+location

	data_maps = urllib2.urlopen(full_maps_url)
	data_maps_json = json.load(data_maps)

	data_lat = str(data_maps_json['results'][0]['geometry']['location']['lat'])
	data_lng = str(data_maps_json['results'][0]['geometry']['location']['lng'])

	data_coordinates = [data_lat, data_lng]
	return data_coordinates


def get_venues(lat, lng):
	foursquareurl = "https://api.foursquare.com/v2/venues/explore?oauth_token="ACCESS TOKEN HERE"&v=20131016&ll=" + lat + "%2C" + lng + "&section=sights&limit=10"
	foururlcreate = urllib2.urlopen(foursquareurl)
	fourdataJSON = json.load(foururlcreate)

	venue_names = []

	for item in fourdataJSON['response']['groups'][0]['items']:
		venue_names.append(item['venue']['name'])

	return venue_names


def get_venueaddresses(lat, lng):
	foursquareurl = "https://api.foursquare.com/v2/venues/explore?oauth_token="ACCESS TOKEN HERE"&v=20131016&ll=" + lat + "%2C" + lng + "&section=sights&limit=10"
	foururlcreate = urllib2.urlopen(foursquareurl)
	fourdataJSON = json.load(foururlcreate)

	address_list = []

	for item in fourdataJSON['response']['groups'][0]['items']:
		tempstr = item['venue']['location']['address'] + ", " + item['venue']['location']['formattedAddress'][1]
		address_list.append(tempstr)

	return address_list


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/selectfirst", methods=['GET', 'POST'])
def selectfirst():
	startingaddress = request.form["firstaddr"]
	endingaddress = request.form["secondaddr"]
	addresscontainer.append(startingaddress)
	addresscontainer.append(endingaddress)

	geo_startaddr = get_latlng(startingaddress)
	venue_namelist = get_venues(geo_startaddr[0], geo_startaddr[1])
	venue_addrlist = get_venueaddresses(geo_startaddr[0], geo_startaddr[1])
	return render_template("choosefirst.html", firstval=venue_namelist[0], secondval=venue_namelist[1], thirdval=venue_namelist[2], fourthval=venue_namelist[3], fifthval=venue_namelist[4], sixthval=venue_namelist[5], seventhval=venue_namelist[6], eighthval=venue_namelist[7], ninthval=venue_namelist[8], tenthval=venue_namelist[9], firstaddr=venue_addrlist[0], secondaddr=venue_addrlist[1], thirdaddr=venue_addrlist[2], fourthaddr=venue_addrlist[3], fifthaddr=venue_addrlist[4], sixthaddr=venue_addrlist[5], seventhaddr=venue_addrlist[6], eighthaddr=venue_addrlist[7], ninthaddr=venue_addrlist[8], tenthaddr=venue_addrlist[9])


@app.route("/selectsecond", methods=['GET', 'POST'])
def selectsecond():
	firstchoice = request.form.get('location_choices')
	addresscontainer.append(firstchoice)

	first_set = get_directions(addresscontainer[0], firstchoice)
	geo_firstchoice = get_latlng(firstchoice)
	fc_namelist = get_venues(geo_firstchoice[0], geo_firstchoice[1])
	fc_addrlist = get_venueaddresses(geo_firstchoice[0], geo_firstchoice[1])
	return render_template("choosesecond.html", firstspot=addresscontainer[0], secondspot=firstchoice, first_set=first_set, firstval=fc_namelist[0], secondval=fc_namelist[1], thirdval=fc_namelist[2], fourthval=fc_namelist[3], fifthval=fc_namelist[4], sixthval=fc_namelist[5], seventhval=fc_namelist[6], eighthval=fc_namelist[7], ninthval=fc_namelist[8], tenthval=fc_namelist[9], firstaddr=fc_addrlist[0], secondaddr=fc_addrlist[1], thirdaddr=fc_addrlist[2], fourthaddr=fc_addrlist[3], fifthaddr=fc_addrlist[4], sixthaddr=fc_addrlist[5], seventhaddr=fc_addrlist[6], eighthaddr=fc_addrlist[7], ninthaddr=fc_addrlist[8], tenthaddr=fc_addrlist[9])


@app.route("/selectthird", methods=['GET', 'POST'])
def selectthird():
	secondchoice = request.form.get('location_choices')
	addresscontainer.append(secondchoice)

	second_set = get_directions(addresscontainer[2], secondchoice)
	geo_secondchoice = get_latlng(secondchoice)
	sc_namelist = get_venues(geo_secondchoice[0], geo_secondchoice[1])
	sc_addrlist = get_venueaddresses(geo_secondchoice[0], geo_secondchoice[1])
	return render_template("choosethird.html", firstspot=addresscontainer[2], secondspot=secondchoice, second_set=second_set, firstval=sc_namelist[0], secondval=sc_namelist[1], thirdval=sc_namelist[2], fourthval=sc_namelist[3], fifthval=sc_namelist[4], sixthval=sc_namelist[5], seventhval=sc_namelist[6], eighthval=sc_namelist[7], ninthval=sc_namelist[8], tenthval=sc_namelist[9], firstaddr=sc_addrlist[0], secondaddr=sc_addrlist[1], thirdaddr=sc_addrlist[2], fourthaddr=sc_addrlist[3], fifthaddr=sc_addrlist[4], sixthaddr=sc_addrlist[5], seventhaddr=sc_addrlist[6], eighthaddr=sc_addrlist[7], ninthaddr=sc_addrlist[8], tenthaddr=sc_addrlist[9])


@app.route("/addedextra", methods=['GET', 'POST'])
def addedextra():
	extrachoice = request.form.get('location_choices')
	addresscontainer.append(extrachoice)

	extra_set = get_directions(addresscontainer[3], extrachoice)
	geo_extrachoice = get_latlng(extrachoice)
	ec_namelist = get_venues(geo_extrachoice[0], geo_extrachoice[1])
	ec_addrlist = get_venueaddresses(geo_extrachoice[0], geo_extrachoice[1])
	return render_template("chooseextra.html", firstspot=addresscontainer[3], secondspot=extrachoice, second_set=extra_set, firstval=ec_namelist[0], secondval=ec_namelist[1], thirdval=ec_namelist[2], fourthval=ec_namelist[3], fifthval=ec_namelist[4], sixthval=ec_namelist[5], seventhval=ec_namelist[6], eighthval=ec_namelist[7], ninthval=ec_namelist[8], tenthval=ec_namelist[9], firstaddr=ec_addrlist[0], secondaddr=ec_addrlist[1], thirdaddr=ec_addrlist[2], fourthaddr=ec_addrlist[3], fifthaddr=ec_addrlist[4], sixthaddr=ec_addrlist[5], seventhaddr=ec_addrlist[6], eighthaddr=ec_addrlist[7], ninthaddr=ec_addrlist[8], tenthaddr=ec_addrlist[9])


@app.route("/selectfourth", methods=['GET', 'POST'])
def selectfourth():
	thirdchoice = request.form.get('location_choices')
	addresscontainer.append(thirdchoice)

	third_set = get_directions(addresscontainer[4], thirdchoice)
	return render_template("choosefourth.html", firstspot=addresscontainer[4], secondspot=thirdchoice, third_set=third_set)


@app.route("/fifth", methods=['GET', 'POST'])
def fifth():
	last_set = get_directions(addresscontainer[5], addresscontainer[1])
	return render_template("final.html", firstspot=addresscontainer[5], secondspot=addresscontainer[1], last_set=last_set)


if __name__ == "__main__":
    app.run()
