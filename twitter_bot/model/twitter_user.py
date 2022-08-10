class TwitterUser:
    def __init__(
        self,
        id: str,
        name: str,
        username: str,
        verified: bool
    ):
        self.id = id
        self.name = name
        self.username = username
        self.verified = verified
