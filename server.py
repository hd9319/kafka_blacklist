from flask import Flask, jsonify

from config import Config
from routes.handlers import ProductView

PORT = 5000

"""
Simple Web Application to Show Blacklist Feature
"""

app = Flask(__name__)
app.config.from_object(Config)

# error handlers
@app.errorhandler(400)
def bad_request(error):
	return jsonify({'Error': 'Bad Request'}), 400

@app.errorhandler(403)
def bad_request(error):
	return jsonify({'Error': 'Forbiddden'}), 403

# routes
app.add_url_rule('/product/<id>', view_func=ProductView.as_view('product'))

# Running the Application Object
if __name__ == '__main__':
	app.run(port=PORT, debug=True)