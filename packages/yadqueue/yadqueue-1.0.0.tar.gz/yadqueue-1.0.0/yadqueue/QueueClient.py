import requests


class QueueClient:
    def __init__(self, base_url, token=None):
        self.base_url = base_url
        self.token = token

    def set_token(self, token):
        self.token = token

    def authenticate(self, username, password):
        auth_url = f"{self.base_url}/users/login"
        response = requests.post(auth_url, json={"username": username, "password": password})
        if response.status_code == 200:
            self.token = response.json().get("token")
            return self._process_response(response)
        else:
            print("Authentication failed: HTTP status code " + str(response.status_code))

    def send_code(self, code):
        if not self.token:
            raise Exception("No token provided. Please set the token or authenticate first.")

        headers = {'Authorization': f"{self.token}"}
        code_url = f"{self.base_url}/tasks"
        response = requests.post(code_url, json={"code": code}, headers=headers)
        return self._process_response(response)

    def get_result(self):
        if not self.token:
            raise Exception("No token provided. Please set the token or authenticate first.")

        headers = {'Authorization': f"{self.token}"}
        result_url = f"{self.base_url}/tasks/result"
        response = requests.get(result_url, headers=headers)
        return self._process_response(response)

    def get_queue_position(self):
        if not self.token:
            raise Exception("No token provided. Please set the token or authenticate first.")

        headers = {'Authorization': f"{self.token}"}
        queue_position_url = f"{self.base_url}/tasks/queue-position"
        response = requests.get(queue_position_url, headers=headers)
        return self._process_response(response)

    def cancel_task(self):
        if not self.token:
            raise Exception("No token provided. Please set the token or authenticate first.")

        headers = {'Authorization': f"{self.token}"}
        cancel_task_url = f"{self.base_url}/tasks/cancel"
        response = requests.delete(cancel_task_url, headers=headers)
        return self._process_response(response)

    def _process_response(self, response):
        def print_json(data, indent=0):
            for key, value in data.items():
                if isinstance(value, dict):
                    print(' ' * indent + f"{key}:")
                    print_json(value, indent + 4)
                else:
                    print(' ' * indent + f"{key}: {value}")

        data = response.json()
        print("Ответ очереди:")
        print_json(data)

