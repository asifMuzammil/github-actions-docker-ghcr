### Python Application Code (`app.py`):
```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to the Dockerized Python App!"

@app.route("/workflow")
def workflow():
    return jsonify({
        "project": "GitHub Actions Docker & GHCR  Workflow",
        "author": "Asif Muzammil",
        "description": "This project demonstrates building and pushing Docker images using GitHub Actions.",
        "repository": "https://github.com/asifMuzammil/github-actions-docker-ghcr",
        "docker_image": "https://github.com/asifMuzammil/github-actions-docker-ghcr/pkgs/container/dummy-python-app"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
