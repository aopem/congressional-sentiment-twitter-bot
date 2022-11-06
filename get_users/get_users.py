"""
Azure function for obtaining all Congress members on Twitter
"""
import json
import logging
import azure.functions as func

from twitter_bot.brokers import TwitterBroker
from twitter_bot.model import TwitterUser, Politician
from twitter_bot.enums import PoliticianType
from twitter_bot.serialization import Encoder
from twitter_bot.utils.functions import load_json
from twitter_bot.utils.constants import REPRESENTATIVES_WIKI_URL, SENATORS_WIKI_URL, \
    TOTAL_NUM_REPRESENTATIVES, TOTAL_NUM_SENATORS

from .get_users_helper import *


def search_possible_twitter_handles(
    politician: Politician,
    client: TwitterBroker
):
    possible_twitter_handles = politician.getPossibleTwitterHandles()

    for handle in possible_twitter_handles:
        possible_user = client.search_username(
            username=handle
        )

        # if user is found, possible_user will be populated
        if possible_user is None:
            continue

        # if user retrieved is not verified, then continue
        if not possible_user.verified:
            continue

        # if above checks pass, can return as a real account
        return TwitterUser(id=possible_user.id,
            name=possible_user.name,
            username=possible_user.username,
            verified=possible_user.verified
        )

    return None


def dump_output(
    out_current: func.Out[str],
    out_missing: func.Out[str],
    out_found: func.Out[str],
    current_list: list[Politician],
    missing_list: list[Politician],
    found_list: list[TwitterUser]
):
    current = json.dumps(current_list, cls=Encoder)
    missing = json.dumps(missing_list, cls=Encoder)
    found = json.dumps(found_list, cls=Encoder)

    out_current.set(current)
    out_missing.set(missing)
    out_found.set(found)

    num_found = len(found_list)
    num_total = TOTAL_NUM_REPRESENTATIVES + TOTAL_NUM_REPRESENTATIVES
    logging.info(f"Current total: {num_found}/{num_total} Twitter accounts")
    logging.info(f"[OUT] getusers/found.json: {found}")
    logging.info(f"[OUT] getusers/current.json: {current}")
    logging.info(f"[OUT] getusers/missing.json: {missing}")


def run(
    timer: func.TimerRequest,
    in_current: str,
    in_missing: str,
    in_found: str,
    out_current: func.Out[str],
    out_missing: func.Out[str],
    out_found: func.Out[str]
):
    # load all input JSON
    logging.info("Loading data from getusers/current.json...")
    in_current_json = load_json(in_current)

    logging.info("Loading data from getusers/missing.json...")
    in_missing_json = load_json(in_missing)

    logging.info("Loading data from getusers/found.json...")
    in_found_json = load_json(in_found)

    # load JSON for found/missing lists
    missing_politician_list = []
    if in_missing_json != None:
        missing_politician_list = create_politician_list_from_json(
            json_dict=in_missing_json
        )

    found_twitter_users_list = []
    if in_found_json != None:
        for user in in_found_json:
            found_twitter_users_list.append(TwitterUser(
                id=user["id"],
                name=user["name"],
                username=user["username"],
                verified=user["verified"]
            ))

    current_politician_list = []
    if in_current_json is None and \
       in_missing_json is not None and \
       in_found_json   is not None:
        logging.info("getusers execution complete, exiting...")
        dump_output(
            out_current=out_current,
            out_missing=out_missing,
            out_found=out_found,
            current_list=current_politician_list,
            missing_list=missing_politician_list,
            found_list=found_twitter_users_list
        )
        return

    # create politician list from input current.json if valid
    if in_current_json != None:
        current_politician_list = create_politician_list_from_json(
            json_dict=in_current_json
        )

    else:
        logging.info("current.json not found, invalid, or empty, using wiki reference to form list")

        # if error with incoming JSON, start with wiki URL
        senator_list = get_politicians(
            politician_list_wiki_url=SENATORS_WIKI_URL,
            list_size=TOTAL_NUM_SENATORS,
            politician_type=PoliticianType.SENATOR
        )
        rep_list = get_politicians(
            politician_list_wiki_url=REPRESENTATIVES_WIKI_URL,
            list_size=TOTAL_NUM_REPRESENTATIVES,
            politician_type=PoliticianType.REPRESENTATIVE
        )

        # add lists
        current_politician_list = senator_list + rep_list

    # create bot client using secrets
    bot = TwitterBroker(
        wait_on_rate_limit=False
    )

    # iterate over copy of list from current.json
    # pop() items as they have been processed
    for politician in list(current_politician_list):
        try:
            twitter_user = search_possible_twitter_handles(
                politician=politician,
                client=bot
            )

        # search will fail once twitter rate limit is achieved
        except Exception as ex:
            logging.info(f"Caught exception: {ex}")
            logging.info(f"Twitter rate limit reached. Dumping progress to storage account")

            # save all output, then return from function to end execution
            dump_output(
                out_current=out_current,
                out_missing=out_missing,
                out_found=out_found,
                current_list=current_politician_list,
                missing_list=missing_politician_list,
                found_list=found_twitter_users_list
            )

            return

        if twitter_user:
            found_twitter_users_list.append(twitter_user)

            logging.info(f"Twitter User ({politician.first_name} {politician.last_name})")
            logging.info(f"id:       {twitter_user.id}")
            logging.info(f"name:     {twitter_user.name}")
            logging.info(f"username: {twitter_user.username}")
            logging.info(f"verified: {twitter_user.verified}\n")
        else:
            missing_politician_list.append(politician)
            logging.warn(f"Could not find user: {politician.first_name} {politician.last_name}")

        # after processing, remove politician from list
        # this will always be the first item of current_politician_list
        current_politician_list.pop(0)

    # if everything completes, dump all output
    dump_output(
        out_current=out_current,
        out_missing=out_missing,
        out_found=out_found,
        current_list=current_politician_list,
        missing_list=missing_politician_list,
        found_list=found_twitter_users_list
    )

    return


def main(
    timer: func.TimerRequest,
    inCurrent: str,
    inMissing: str,
    inFound: str,
    outCurrent: func.Out[str],
    outMissing: func.Out[str],
    outFound: func.Out[str],
    context: func.Context
):
    logging.info(f"Executing function: {context.function_name}")
    logging.info(f"Invocation ID: {context.invocation_id}")
    logging.info(f"[IN] getusers/current.json: {inCurrent}")
    logging.info(f"[IN] getusers/missing.json: {inMissing}")
    logging.info(f"[IN] getusers/found.json: {inFound}")

    # run actual function
    run(
        timer=timer,
        in_current=inCurrent,
        in_missing=inMissing,
        in_found=inFound,
        out_current=outCurrent,
        out_missing=outMissing,
        out_found=outFound
    )


if __name__ == "__main__":
    main()
