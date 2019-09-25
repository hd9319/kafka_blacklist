import requests
import sleep

def send_request(endpoint, num_requests, request_delay=0):
	for i in range(num_requests):
		if i % 100 == 0:
			print('Completed: %s/%s' % (i, len(num_requests)))

		_ = requests.get(endpoint)
		time.sleep(request_delay)

	print('Completed.')

if __name__ == '__main__':
	localhost = 'http://localhost:5000'
	_ = send_request(localhost, num_requests=1000, request_delay=0.1)
