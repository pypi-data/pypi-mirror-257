import requests


class OpenAiClient:
    """
    Client for interacting with the OpenAI API.
    """

    def __init__(self, openai_api_key, model="gpt-3.5-turbo-0125", max_tokens=150):
        self.openai_api_key = openai_api_key
        self.model = model
        self.max_tokens = max_tokens
        self.headers = {"Authorization": f"Bearer {self.openai_api_key}"}

    def query(self, prompt):
        try:
            data = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": self.max_tokens,
            }
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=self.headers,
                json=data,
            )
            response_json = response.json()
            if response.status_code == 200:
                return response_json["choices"][0]["message"]["content"]
            else:
                return f"An error occurred: {response_json}"
        except Exception as e:
            return f"An error occurred: {str(e)}"
