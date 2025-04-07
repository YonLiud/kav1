class Settings:
    URL = "localhost:3000"

    @classmethod
    def get_http_url(cls, endpoint: str):
        return f"http://{cls.URL}{endpoint}"

    @classmethod
    def get_ws_url(cls):
        return f"ws://{cls.URL}/ws"

    @classmethod
    def set_url(cls, input: str):
        cls.URL = input
