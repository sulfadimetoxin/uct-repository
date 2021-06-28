import requests


def run():
    print("\nREST api test started")
    res = requests.get("https://127.0.0.1:5000/api/records/", verify=False)
    assert res.status_code == 200, f"Test failed {res.status_code}"
    print("Test succeed")


if __name__ == '__main__':
    run()
