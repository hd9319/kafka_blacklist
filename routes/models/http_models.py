import os

import pandas as pd

class Response(object):
	acceptable_codes = [200]

	status_summmary = { 
        200: "Success", 
        301: "Redirected", 
        403: "Forbidden",
        500: "Internal Error" 
    } 

	def __init__(self, request, blacklist_file, required_headers=None):
		self.required_headers = required_headers
		self.blacklist_file = blacklist_file
		self.blacklist = list(pd.read_csv(blacklist_file)['ipAddress'])
		self.http_response = self._get_http_message(request)

	def _get_http_message(self, request):
		valid = self._validate_request(request, self.blacklist, self.required_headers)
		if valid:
			status_code = valid['Status']
			return {'Status': status_code, 'Message': self.status_summmary.get(status_code, self.status_summmary[500])}
		else:
			return {'Status': 500, 'Message': self.status_summmary[500]}

	def is_acceptable(self):
		if self.http_response['Status'] in self.acceptable_codes:
			return True
		else:
			return False

	@staticmethod
	def _validate_request(request, blacklist, required_headers):
		try:
			# check if all fields are part of request
			if required_headers:
				missing_headers = set(required_headers) - set(request['Headers'].keys())
				if len(missing_headers) > 0:
					return {'Status': 403}

			# check if ip is part of blacklist
			ip = request['ipAddress']
			if ip in blacklist:
				return {'Status': 403}
			else:
				return {'Status': 200}

		except Exception as e:
			print(e)
			return None

if __name__ == '__main__':
	request = {
				'ipAddress': '127.0.0.1', 
				'Headers': {
					'Referer': 'https://www.example.com/',
					'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3)'
					}
				}
				
	blacklist_filepath = input('Enter File Path: ')
	assert os.path.isfile(blacklist_filepath)

	response = Response(request, blacklist_file=blacklist_filepath, required_headers=['User-Agent'])
	print(response.http_response)

