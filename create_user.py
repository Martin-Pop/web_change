import requests

BASE_URL = "http://localhost:5151"
CREATE_USER_ENDPOINT = BASE_URL + "/api/users/create"


USER_DATA_FORM = {
    "Id": 0, 
    "Name": "test_aiohttp_user", 
    "AccessKey": "ws_secure_pass", 
    "Messages": '{"text":"Initial message","magnitude":1,"type":1}' 
}

def create_user_and_get_token():
    try:
        response = requests.post(CREATE_USER_ENDPOINT, data=USER_DATA_FORM, verify=False)
        response.raise_for_status()
        data = response.json()
        if "accessKey" in data:
            return data["accessKey"]
    except Exception as e:
        print(f"Error getting token: {e}")
    return None

if __name__ == "__main__":
    token = create_user_and_get_token()
    print(token)