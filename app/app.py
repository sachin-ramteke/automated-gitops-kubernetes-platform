from flask import Flask, jsonify
import os
import socket

app = Flask(__name__)

@app.route('/')
def home():
    hostname = socket.gethostname()
    return jsonify({
        "status": "Online",
        "message": "Production GitOps Platform Active",
        "pod_name": hostname,
        "environment": os.getenv("APP_ENV", "production")
    })

@app.route('/healthz')
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
