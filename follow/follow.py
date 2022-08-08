import json
import azure.functions as func

from twitter_bot.client.twitter import BotClient
from twitter_bot.model import TwitterUser
import twitter_bot.utils.constants as c
import twitter_bot.utils.functions as f


def run():
    # create bot client
    secrets = f.get_secrets_dict()
    bot = BotClient(
        api_key=secrets["apiKey"],
        api_key_secret=secrets["apiKeySecret"],
        access_token=secrets["accessToken"],
        access_token_secret=secrets["accessTokenSecret"],
        bearer_token=secrets["bearerToken"]
    )

    # read json containing twitter account info
    twitter_user_json = json.load(open(c.TWITTER_ACCOUNTS_FOUND_FILENAME))

    # follow all users - no errors if already following
    for user_json in twitter_user_json:
        user = TwitterUser(
            id=user_json["id"],
            name=user_json["name"],
            username=user_json["username"],
            verified=user_json["verified"]
        )
        try:
            bot.followUser(user)
            print(f"Successfully followed @{user.username} ({user.name})")
        except Exception:
            print(f"WARN: Could not follow user @{user.username} ({user.name})")

    return


def main(timer: func.TimerRequest):
    if timer.past_due:
        run()


if __name__ == "__main__":
    main()
