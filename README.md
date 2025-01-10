# Building and Pushing Docker Images with GHCR and Docker Hub Using GitHub Actions

This post offers a detailed tutorial on building and deploying Docker images to the GitHub Container Registry (GHCR) and Docker Hub using GitHub Actions. Additionally, it shows how to add a workflow information endpoint to your Python application, which shows project details when the container is executed.

---

## Overview of GHCR

GitHub Container Registry (GHCR) is an all-in-one solution provided by GitHub for managing container images. It offers features like fine-grained permissions, integration with GitHub repositories, and support for OCI-compliant images. GHCR serves as an excellent alternative to Docker Hub for hosting your container images.

---

## Prerequisites

Before we begin, ensure you have the following:

1. A GitHub account.
2. A Docker Hub account.
3. A Python application to containerize.
4. GitHub repository with write access to GHCR.
5. Docker installed locally for testing (optional).
6. Repository secrets and environment variables set up for Docker Hub credentials.

### Setting Up Secrets and Environment Variables in GitHub Repository

1. **Navigate to Your Repository Settings:**
   Go to your GitHub repository and click on **Settings**.

2. **Add Secrets:**
   - Go to **Secrets and variables > Actions**.
   - Click on **New repository secret** and add the following secrets:
     - `DOCKER_HUB_USERNAME`: Your Docker Hub username.
     - `DOCKER_HUB_ACCESS_TOKEN`: Your Docker Hub access token. Generate this from your Docker Hub account.

3. **Add Environment Variables:**
   - Go to **Secrets and variables > Actions**.
   - Click on **New environment variable** and add:
     - `DOCKER_HUB_USERNAME`: Repeat your Docker Hub username here for convenience.

---

## Python Application Setup

Let’s create a simple Python application for this example. The application includes two endpoints:

- `/` - Displays a welcome message.
- `/workflow` - Displays details about the GitHub Actions workflow used to build and push the image.

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
```

### Dockerfile

Create a `Dockerfile` to containerize the application:
```dockerfile
# Use Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy application code
COPY app.py ./

# Install dependencies
RUN pip install flask

# Expose port 5000
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
```

---

## GitHub Actions Workflow

Here is the workflow file to automate the process of building, testing, and pushing the Docker image to both Docker Hub and GHCR.

### Workflow File (`.github/workflows/docker-image.yml`):
```yaml
name: Build and Push Docker Image

on:
  push:
    branches:
      - main

jobs:
  build-and-push:
    name: Build, Test, and Push Docker Image
    runs-on: ubuntu-latest

    permissions:
      contents: read
      packages: write  # Required for pushing to GHCR

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Log in to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ vars.DOCKER_HUB_USERNAME }}
          password: ${{ secrets.DOCKER_HUB_ACCESS_TOKEN }}

      - name: Log in to GitHub Container Registry (GHCR)
        uses: docker/login-action@v2
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Convert Repository Owner to Lowercase
        run: echo "REPO_OWNER=$(echo ${{ github.repository_owner }} | tr '[:upper:]' '[:lower:]')" >> $GITHUB_ENV

      - name: Build and Push Image to Both Registries
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: |
            ${{ vars.DOCKER_HUB_USERNAME }}/dummy-python-app:latest
            ghcr.io/${{ env.REPO_OWNER }}/dummy-python-app:latest

      - name: Test Docker Image
        run: |
          docker run -d -p 5000:5000 --name dummy-app-test ${{ vars.DOCKER_HUB_USERNAME }}/dummy-python-app:latest
          sleep 5
          curl -f http://localhost:5000/ || exit 1
          curl -f http://localhost:5000/workflow || exit 1
          docker stop dummy-app-test
          docker rm dummy-app-test
```

---

## Explanation of the Workflow

1. **Checkout Code:** Fetches the repository code.
2. **Log in to Docker Registries:** Authenticates with Docker Hub and GHCR using credentials.
3. **Build and Push:** Uses `docker/build-push-action@v4` to build the image and push it to both registries.
4. **Test Docker Image:** Runs the container and tests its endpoints to ensure functionality.

---

## Testing the Image

Once the workflow completes, pull the image from Docker Hub or GHCR:

- Docker Hub:
  ```bash
  docker pull your-dockerhub-username/dummy-python-app:latest
  ```

- GHCR:
  ```bash
  docker pull ghcr.io/your-username/dummy-python-app:latest
  ```

Run the container and test the endpoints:
```bash
docker run -d -p 5000:5000 your-dockerhub-username/dummy-python-app:latest
curl http://localhost:5000/
curl http://localhost:5000/workflow
```

---

## Conclusion

This project demonstrates the seamless integration of GitHub Actions with Docker Hub and GHCR for managing and deploying container images. By following this guide, you can automate your container workflows and enhance your skills.
If you like or find this guide helpful, please follow me! 🚀

---
## Feel free to reach out!

### Here are some ways to connect with me:

###  Social Media:

- [LinkedIn](www.linkedin.com/in/asif-muzammil-hussain-b6742441)
- [GitHub](https://github.com/asifMuzammil/github-actions-docker-ghcr)
- [Personal Email](m.asif.muzammil@gmail.com)
- [Medium]  (https://medium.com/@m.asif.muzammil)
---
