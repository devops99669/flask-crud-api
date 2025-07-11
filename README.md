# Flask CRUD API CI/CD with Jenkins, Docker & Docker Hub

## ✅ Overview

This document provides a complete, well-formatted, and visually clean step-by-step guide to automate deployment of a **Flask CRUD API** using **Docker**, integrated with **Jenkins CI/CD pipeline**, and **Docker Hub**.

---

## 🔧 Project Setup Summary

* **App**: Flask CRUD API (with Swagger docs optionally)
* **Version Control**: GitHub
* **Containerization**: Docker
* **CI/CD**: Jenkins
* **Registry**: Docker Hub
* **Notification (Optional)**: Gmail SMTP

---

## ⌚ Pipeline Stages in Jenkins

### 1. 🗂️ Checkout Code

* Pulls the latest code from GitHub:

  ```bash
  git clone https://github.com/devops99669/flask-crud-api.git
  ```

### 2. ✅ Build Docker Image

* Build Docker image from the Dockerfile:

  ```bash
  docker build -t devops99669/flask-crud-api .
  ```

### 3. 🔐 Login to Docker Hub

* Use `docker login` with username/password:

  ```bash
  echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
  ```

  * Store credentials securely in Jenkins credentials manager.

### 4. 📤 Push Docker Image

* Push the built image to Docker Hub:

  ```bash
  docker push devops99669/flask-crud-api
  ```

### 5. 🛑 Stop & Remove Existing Container

* Clean up old containers (if any):

  ```bash
  docker stop flask-api-container || true
  docker rm flask-api-container || true
  ```

### 6. 🔎 Free Port 5000

* Ensure port 5000 is free:

  ```bash
  fuser -n tcp -k 5000 || true
  ```

### 7. 🚀 Run New Container

* Run the latest image:

  ```bash
  docker run -d -p 5000:5000 --name flask-api-container devops99669/flask-crud-api
  ```

### 8. 📧 Gmail Notifications (Optional)

* Configure Jenkins email plugin:

  * SMTP: `smtp.gmail.com`
  * Port: `587`
  * Requires TLS + App Password (from Google security settings)

---

## 📁 Project Structure (GitHub)

```bash
flask-crud-api/
├── app.py
├── Dockerfile
├── requirements.txt
├── test_app.py
├── Jenkinsfile (if pipeline as code)
```

---

## ⚙️ Jenkins Configuration

* **Type**: Freestyle or Pipeline project
* **SCM**: Git (GitHub Repo URL)
* **Build Triggers**:

  * Poll SCM or GitHub Webhook (`http://<jenkins-ip>/github-webhook/`)
* **Build Steps**: Execute shell script with all stages
* **Credentials**: Set up Docker Hub credentials securely
* **Post-build Actions**: Email notifications (optional)

---

## 🔹 Final Output

Once complete:

* App runs on: `http://<your-server-ip>:5000`
* Docker image: `https://hub.docker.com/r/devops99669/flask-crud-api`
* Jenkins: Shows full log & build success/failure
* Email: Receives notification on job status (if configured)

---

## 📆 Future Enhancements

* Add Swagger UI for API docs
* Add Pytest for unit testing
* Publish code coverage report
* Add Slack integration for notifications
* Deploy to Kubernetes/GCP Cloud Run

---

## ✨ Benefits

| Feature            | Benefit                               |
| ------------------ | ------------------------------------- |
| Dockerized App     | Portable, consistent deployment       |
| Jenkins CI/CD      | Automated build & deploy              |
| Docker Hub Push    | Shared image for all environments     |
| Email Notification | Build success/failure alerts to inbox |
| GitHub Integration | Real-time trigger on push             |

---

**End of Document**
