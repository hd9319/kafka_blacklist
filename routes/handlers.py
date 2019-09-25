import os

os.environ['BOOTSTRAP_SERVERS'] = ['localhost:9092']
os.environ['REQUEST_TASK_TOPIC'] = 'http_request'

from flask import abort, request, jsonify
from flask.views import MethodView

from kafka import KafkaProducer

from .models.http_models import Response

# create kafka producer
producer = KafkaProducer(bootstrap_servers=os.environ['BOOTSTRAP_SERVERS'],
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'))

class ProductView(MethodView):
	def get(self, id):
		try:
			url = request.url
			ip_address = request.remote_addr

			response = Response(request={'ipAddress': ip_address,'url': url,
										'Headers': request.headers}, 
										blacklist_file=os.environ['BLACKLIST_FILE'], 
										required_headers=['User-Agent'])
			if response.is_acceptable():
				data = {'productId': id, 'productDescription': 'This is Product: %s' % id}
				producer.send(os.environ['REQUEST_TASK_TOPIC'], data)
			else:
				data = None

			return jsonify({'Status': response.http_response, 'data': data})

		except Exception as e:
			print(e)
			abort(404)
