"""
Azure function for obtaining all Congress members on Twitter
"""
import json
import logging
import azure.functions as func

from twitter_bot_func_app.brokers import TwitterBroker
from twitter_bot_func_app.data import PoliticianDataService, WikipediaDataBroker, Politician
from twitter_bot_func_app.model import TwitterAccount
from twitter_bot_func_app.enums import PoliticianType
from twitter_bot_func_app.serialization import Encoder
from twitter_bot_func_app.utils.functions import load_json
from twitter_bot_func_app.utils.constants import REPRESENTATIVES_WIKI_URL, SENATORS_WIKI_URL, \
    TOTAL_NUM_REPRESENTATIVES, TOTAL_NUM_SENATORS


def dump_output(
    out_current: func.Out[str],
    out_missing: func.Out[str],
    out_found: func.Out[str],
    current_list: list[Politician],
    missing_list: list[Politician],
    found_list: list[TwitterAccount]
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

    # create data brokers
    sen_data_broker =  WikipediaDataBroker(
        wiki_url=SENATORS_WIKI_URL,
        size=TOTAL_NUM_SENATORS
    )
    rep_data_broker =  WikipediaDataBroker(
        wiki_url=REPRESENTATIVES_WIKI_URL,
        size=TOTAL_NUM_REPRESENTATIVES
    )

    # create twitter broker for interacting with API
    bot = TwitterBroker(
        wait_on_rate_limit=False
    )

    # create politician data service
    politician_data_service = PoliticianDataService(
        rep_wiki_data_broker=rep_data_broker,
        sen_wiki_data_broker=sen_data_broker,
        twitter_broker=bot
    )

    # load JSON for found/missing lists
    missing_politician_list = []
    if in_missing_json is not None:
        missing_politician_list = politician_data_service.create_politician_list(
            data=in_missing_json
        )

    found_twitter_users_list = []
    if in_found_json is not None:
        for user in in_found_json:
            found_twitter_users_list.append(TwitterAccount(
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
    if in_current_json is not None:
        current_politician_list = politician_data_service.create_politician_list(
            data=in_current_json
        )

    else:
        logging.info("current.json not found, invalid, or empty, using wiki reference to form list")

        # if error with incoming JSON, start with wiki URL data
        senator_list = politician_data_service.get_politician_list(
            politician_type=PoliticianType.SENATOR
        )
        rep_list = politician_data_service.get_politician_list(
            politician_type=PoliticianType.REPRESENTATIVE
        )

        # combine lists
        current_politician_list = senator_list + rep_list

    # iterate over copy of list from current.json
    # pop() items as they have been processed
    for politician in list(current_politician_list):
        try:
            possible_usernames = politician_data_service.get_possible_twitter_usernames(
                politician=politician
            )
            twitter_user = politician_data_service.search_possible_twitter_usernames(
                possible_usernames=possible_usernames
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
