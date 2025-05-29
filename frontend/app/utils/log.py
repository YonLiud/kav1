from datetime import datetime


class Log:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Log, cls).__new__(cls)
            cls._instance.logs = []
        return cls._instance

    def write_to_log(self, *messages):
        now = datetime.now()
        log_string = f"{now} - {' '.join(map(str, messages))}"

        self.logs.append(log_string)
        print(log_string)

    def get_logs(self):
        return self.logs
