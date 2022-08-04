import json
from twitter_bot.client.bot_client import BotClient
import twitter_bot.utils.constants as c


def main():
    # create bot client
    bot = BotClient(c.SECRETS_FILEPATH)

    # read json containing twitter account info
    twitter_user_json = json.load(open(c.TWITTER_ACCOUNTS_FOUND_FILENAME))

    # follow all users - no errors if already following
    for user in twitter_user_json:
        try:
            bot.followUser(user)
            print(f"Successfully followed @{user.username} ({user.name})")
        except Exception:
            print(f"WARN: Could not follow user @{user.username} ({user.name})")

    return


if __name__ == "__main__":
    main()
