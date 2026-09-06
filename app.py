# Flask backend
import os
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/api/health')
def health():
    return jsonify(status='ok', service='flask-backend')


@app.route('/api/message')
def message():
    return jsonify(
        message='Hello from the Flask backend!',
        host=os.environ.get('HOSTNAME', 'unknown')
    )


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
