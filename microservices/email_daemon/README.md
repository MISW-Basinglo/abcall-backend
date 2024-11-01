# Email Daemon Microservice
This microservice is responsible for receiving issues from the email API and sending the cleaned data to PubSub topic.

## How to run
1. Install the dependencies:
```bash
pip install -r requirements.txt
```

2. Run the microservice:
```bash
python email_daemon.py
```
3. Alternatively, you can run the microservice using make:
```bash
make run_email_daemon
```
Note: You have to run in the root directory of the project.

## Environment variables
- `GOOGLE_CLOUD_PROJECT`: The Google Cloud project ID.
- `PUBSUB_TOPIC`: The PubSub topic to send the cleaned data.
- `GMAIL_CREDENTIALS`: The Gmail credentials to authenticate the email API.
- `DAEMON_REQUEST_HEADER_VALUE`: The header value to identify the request from the daemon.
- `BACKEND_HOST`: The host of the backend service.
- `GOOGLE_APPLICATION_CREDENTIALS`: The path to the Google Cloud credentials file. (For local development only)

# How to test
1. Install the dependencies:
```bash
pip install -r requirements.txt
```

2. Run the tests:
```bash
pytest
```
3. Alternatively, you can run the tests using make:
```bash
make test_email_daemon
```
