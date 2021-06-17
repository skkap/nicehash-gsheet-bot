import requests
import time
import json

def current_milli_time():
    return round(time.time() * 1000)

def push_metric(name, value, attributes, newrelic_api_key):
    metrics_host = 'https://metric-api.newrelic.com/metric/v1'
    headers = {'user-agent': 'my-app/0.0.1', 'Api-Key': newrelic_api_key}

    metrics_payload = [{
        "metrics": [{
            "name": name,
            "type": "gauge",
            "value": value,
            "timestamp": current_milli_time(),
            "attributes": attributes # { "one": "two"}
        }]
    }]

    requests.post(metrics_host, headers=headers, data=json.dumps(metrics_payload))
