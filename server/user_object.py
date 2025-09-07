class User:
    def __init__(self, conn=None, nickname=None, message=None):
        self.conn = conn
        self.nickname = nickname
        self.message = message

    def __str__(self):
        return f"{self.nickname}:{self.message}"