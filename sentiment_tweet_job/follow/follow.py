"""
Azure function for following users
"""
import json
import logging
import azure.functions as func

from twitter_bot_app.brokers import TwitterBroker
from twitter_bot_app.model import TwitterAccount


def run(
    in_found: str
):
    # create bot client
    bot = TwitterBroker()

    # create set of users already following
    logging.info("Retrieving currently followed users from Twitter...")
    following = bot.get_my_following()
    following_ids = set()
    for user in following:
        following_ids.add(user.id)

    # read json containing twitter account info
    logging.info("Loading twitter accounts to follow from getusers/found.json...")
    twitter_user_json = json.loads(in_found)

    # follow all users - no errors if already following
    num_users_followed = 0
    for user_json in twitter_user_json:
        if user_json["id"] not in following_ids:
            user = TwitterAccount(
                id=user_json["id"],
                name=user_json["name"],
                username=user_json["username"],
                verified=user_json["verified"]
            )

            try:
                status = bot.follow_user(user)
                if status.following:
                    num_users_followed += 1
                    logging.info(f"Successfully followed @{user.username} ({user.name})")
                else:
                    logging.info(f"Attempted to follow @{user.username} ({user.name})")
                    logging.info(f"Follow status = {status}")
            except Exception:
                logging.warn(f"Could not follow @{user.username} ({user.name})")

    logging.info(f"New users followed: {num_users_followed}")
    return


def main(
    inFound: str,
    context: func.Context
):
    logging.info(f"Executing function: {context.function_name}")
    logging.info(f"Invocation ID: {context.invocation_id}")
    logging.info(f"[IN] getusers/found.json: {inFound}")
    run(inFound)


if __name__ == "__main__":
    main()
