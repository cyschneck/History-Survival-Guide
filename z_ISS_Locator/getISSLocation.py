# python3 getISSLocation.py: Python 3.7.3
import urllib.request, urllib.error, urllib.parse
import json
import sys
import time # wait time between runs

def getISSPosition():
	# return the current position (latitude, longitude) of the ISS
	# http://open-notify.org/Open-Notify-API/ISS-Location-Now/
	# https://github.com/open-notify/Open-Notify-API
	open_api_request = urllib.request.Request("http://api.open-notify.org/iss-now.json")
	response = urllib.request.urlopen(open_api_request)

	iss_api_obj = json.loads(response.read())
	# example: {'iss_position': {'latitude': '39.8931', 'longitude': '147.1774'}, 'message': 'success', 'timestamp': 1664085852}
	return iss_api_obj

if __name__ == '__main__':
	# empty file for locations and populate with generic header
	header = "TIMESTAMP  | ERR_MSG | Latitude: XXXXXXX, Longitude: XXXXXXXXX"
	iss_txt_file = open("iss_live_locations.txt", 'w')
	iss_txt_file.write(header)
	iss_txt_file.close()
	# TODO: limit the length of the file to 100 lines

	get_requests = True # run indefinitely in the background to populate iss_live_locations.txt file
	while(get_requests):
		iss_api_obj = getISSPosition()
		timestamp = iss_api_obj['timestamp']
		success_error_msg = iss_api_obj['message']
		iss_latitude = iss_api_obj['iss_position']['latitude']
		iss_longitude = iss_api_obj['iss_position']['longitude']
		iss_live_location_txt = "{0} | {1} | Latitude: {2}, Longitude: {3}".format(timestamp, success_error_msg.upper(), iss_latitude, iss_longitude)
		iss_txt_file = open("iss_live_locations.txt", 'a')
		iss_txt_file.write("\n{0}".format(iss_live_location_txt))
		iss_txt_file.close()
		time.sleep(2) # seconds: wait 2 seconds between taking requests for location
		#get_requests = False # for testing


