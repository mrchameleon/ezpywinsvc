import json, requests

ROLLBAR_TOKEN = "your_token_here"

def post_rollbar_item(token, data):
    payload = {
      "access_token": token,
      "data": data
    }

    json_encoded_payload = json.dumps(payload)
    requests.post('https://api.rollbar.com/api/1/item/', data=json_encoded_payload)

def report_generic_exception(exception):
    data = {"environment": "production", 
            "body": {
                "message": {
                    "body": "[%s] %s" % (CUSTNAME, exception)
                },
                "level": "error",
                "person": {"id": CUSTNAME },
                "exception": {
                      "class": "Exception",
                      "message": "%s" % exception,
                      "description": "Generic Exception"
                }
            }}
    try: 
        post_rollbar_item(ROLLBAR_TOKEN, data)
    except requests.exceptions.RequestException as e:
        debug_log(e) 
        handle_network_failure()
