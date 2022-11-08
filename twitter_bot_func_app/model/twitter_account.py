"""
Twitter user model class
"""

class TwitterAccount:
    """
    Generic Twitter user class

    Attributes:
        id (str): user ID
        name (str): name of user
        username (str): Twitter username
        verified (bool): true if user is verified (has blue check)
    """
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
