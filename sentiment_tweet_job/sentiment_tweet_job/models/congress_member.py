from sentiment_tweet_job.enums import Chamber

class CongressMember:
    def __init__(
        self,
        id: str,
        first_name: str,
        last_name: str,
        gender: str,
        party: str,
        state: str,
        twitter_account_name: str,
        chamber: Chamber,
        middle_name: str = None
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.party = party
        self.state = state
        self.twitter_account_name = twitter_account_name
        self.chamber = chamber
        self.middle_name = middle_name
