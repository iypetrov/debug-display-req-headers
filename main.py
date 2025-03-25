import psutil
import socket
import requests
from flask import Flask, request, render_template_string

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Request Headers</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { border: 1px solid black; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <p><strong>Public IP:</strong> {{ public_ip }}</p>
    <p><strong>Private IP:</strong> {{ private_ip }}</p>
    <h1>Request Headers</h1>
    <table>
        <tr><th>Header</th><th>Value</th></tr>
        {% for key, value in headers.items() %}
        <tr><td>{{ key }}</td><td>{{ value }}</td></tr>
        {% endfor %}
    </table>
</body>
</html>
"""


def get_public_ip():
    response = requests.get("https://api.ipify.org")
    response.raise_for_status()
    return response.text.strip()


def get_private_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]


@app.route("/")
def index():
    psutil.net_if_addrs().items()
    headers = dict(request.headers)
    sorted_headers = dict(sorted(headers.items()))
    public_ip = get_public_ip()
    private_ip = get_private_ip()
    return render_template_string(TEMPLATE, headers=sorted_headers, public_ip=public_ip, private_ip=private_ip)


@app.route("/200")
def ok():
    return "OK", 200


@app.route("/404")
def notfound():
    return "NOT FOUND", 404


@app.route("/500")
def error():
    return "ERROR", 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
