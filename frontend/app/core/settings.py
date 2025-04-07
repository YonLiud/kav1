class Settings:
    BASE_URL = "http://localhost:3000"
    WS_URL = "ws://localhost:3000/ws"
    
    @classmethod
    def get_http_url(cls, endpoint: str):
        return f"{cls.BASE_URL}{endpoint}"
    
    @classmethod
    def get_ws_url(cls):
        return cls.WS_URL