import os
import csv
import json
from datetime import datetime

from kafka import KafkaConsumer

os.environ['BOOTSTRAP_SERVER'] = ['localhost:9092']
os.environ['REQUEST_TASK_TOPIC'] = 'http_request'

class Client(object):
	def __init__(self, ip_address, max_requests=20, reset=timedelta(minutes=10)):
		self.created_date = datetime.now()
		self.start = datetime.now()
		self.ip_address = ip_address
		self.max_requests = max_requests
		self.reset = reset
		self.counter = 1

	def increment(self):
		if datetime.now() - self.start > reset:
			self.start = datetime.now()
			self.counter = 1
		else:
			self.counter += 1

	def has_exceeded_max(self):
		if self.counter > self.max_requests:
			return True
		else:
			return False

def main():
	ipAddresses = {}

	consumer = KafkaConsumer(
		os.environ['REQUEST_TASK_TOPIC'],
	    bootstrap_servers=os.environ['BOOTSTRAP_SERVER'],
	    enable_auto_commit=True,
	    group_id='blacklist',
	    value_deserializer=lambda x: json.loads(x.decode('utf-8')))

	for message in consumer:
		ip_address = message['ipAddress']
		user = ipAddresses.get(ip_address)
		if not user:
			user = Client(ip_address=ip_address)
			ipAddresses[ip_address] = user

		if user.has_exceeded_max():
			with open(os.environ['BLACKLIST_FILE'], 'a', newline='') as outfile:
				writer = csv.writer(outfile)
    			writer.writerow([ip_address])
    	else:
    		user.increment()


if __name__ == '__main__':
	main()


