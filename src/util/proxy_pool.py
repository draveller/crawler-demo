import requests

def get():
    """
    :return:
    {
    "anonymous": "",
    "check_count": 1,
    "fail_count": 0,
    "https": true,
    "last_status": true,
    "last_time": "2025-01-26 17:02:39",
    "proxy": "8.138.133.207:9080",
    "region": "error",
    "source": "freeProxy11"
    }
    """
    return requests.get("http://127.0.0.1:5010/get/").json()

def pop():
    return requests.get("http://127.0.0.1:5010/pop/").json()


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))
