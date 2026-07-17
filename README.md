# 🛡️ Honeypot API

A lightweight Flask-based Honeypot API designed to detect, log, and monitor suspicious or malicious requests. This project helps developers understand common attack patterns by recording unauthorized access attempts.

## 🚀 Features

- Detects suspicious API requests
- Logs attacker IP addresses
- Captures request headers and payloads
- Stores attack logs for analysis
- Simple Flask-based implementation
- Easy to customize and extend

## 🛠️ Tech Stack

- Python
- Flask
- REST API

## 📂 Project Structure

```
honeypot-api/
│── app.py
│── requirements.txt
│── README.md
```

## ⚙️ Installation

1. Clone the repository

```bash
git clone https://github.com/Muskan99113-cell/honeypot-api.git
```

2. Navigate to the project

```bash
cd honeypot-api
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Run the application

```bash
python app.py
```

## 📌 Example

After running the server, send a request to the honeypot endpoint.

Example:

```http
GET /fake-login
```

The request will be logged for monitoring and analysis.

## 📈 Future Improvements

- Dashboard for attack visualization
- Geo-location tracking
- Email alerts
- Database integration
- Docker support

## 👩‍💻 Author

**Muskan Sharma**


⭐ If you found this project useful, consider giving it a star!
