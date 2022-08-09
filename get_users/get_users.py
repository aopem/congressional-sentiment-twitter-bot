import json
import pandas as pd
import logging
import azure.functions as func

from twitter_bot.client.twitter import BotClient
from twitter_bot.model import TwitterUser
from twitter_bot.model import Senator
from twitter_bot.model import Representative
from twitter_bot.enums import PoliticianType
from twitter_bot.serialization import Encoder
import twitter_bot.utils.constants as c
import twitter_bot.utils.functions as f


def get_politician_dict(
    politician_list_wiki_url,
    list_size
):
    wiki_data = pd.read_html(politician_list_wiki_url)

    # find correct table according to list_size
    for df in wiki_data:
        length = df.shape[0]
        if length == list_size:
            return df.to_dict(orient='index')

    raise logging.error(f"No entry found for list size: {list_size} at URL: {politician_list_wiki_url}")


def get_politician_list(
    politician_list_wiki_url,
    list_size,
    politician_type,
    name_key,
    party_key,
    state_key,
    residence_key,
    date_born_key
):
    politician_dict = get_politician_dict(
        politician_list_wiki_url=politician_list_wiki_url,
        list_size=list_size
    )
    politician_list = []

    for politician in politician_dict.values():
        constructor_args = {
            "name": politician[name_key],
            "party": politician[party_key],
            "state": politician[state_key],
            "residence": politician[residence_key],
            "date_born": politician[date_born_key]
        }

        try:
            if politician_type == PoliticianType.REPRESENTATIVE:
                politician_list.append(Representative(constructor_args))
            elif politician_type == PoliticianType.SENATOR:
                politician_list.append(Senator(constructor_args))
            else:
                raise Exception(f"Invalid type: {politician_type}")

        except IndexError:
            logging.warn(f"Name {politician[name_key]} not formatted correctly")

    return politician_list


def get_politicians(
    politician_list_wiki_url,
    list_size,
    politician_type
):
    if politician_type == PoliticianType.REPRESENTATIVE:
        keys = {
            "name_key": "Member",
            "party_key": "Party.1",
            "state_key": "District",
            "residence_key": "Residence",
            "date_born_key": "Born[2]"
        }
    elif politician_type == PoliticianType.SENATOR:
        keys = {
            "name_key": "Senator",
            "party_key": "Party.1",
            "state_key": "State",
            "residence_key": "Residence[2]",
            "date_born_key": "Born"
        }
    else:
        raise Exception(f"Invalid type: {politician_type}")

    return get_politician_list(
        politician_list_wiki_url=politician_list_wiki_url,
        list_size=list_size,
        politician_type=politician_type,
        **keys
    )


def search_possible_twitter_handles(
    politician,
    client
):
    possible_twitter_handles = politician.getPossibleTwitterHandles()

    for handle in possible_twitter_handles:
        response = client.searchUsername(handle)

        # if user is found, response.data will be populated
        if response.data is None:
            continue

        # if user retrieved is not verified, then continue
        if not response.data.verified:
            continue

        # if above checks pass, can return as a real account
        return TwitterUser(id=response.data.id,
            name=response.data.name,
            username=response.data.username,
            verified=response.data.verified
        )

    return None


def run(
    in_missing: str
):
    # load in_missing as JSON dict, create a list of Politician objects
    in_missing_json = None
    in_missing_list = []
    if in_missing != None and len(in_missing) > 0:
        in_missing_json = json.loads(in_missing)

        # create politician list
        for politician_json in in_missing_json:
            constructor_args = {
                "name": politician_json["name"],
                "party": politician_json["party"],
                "state": politician_json["state"],
                "residence": politician_json["residence"],
                "date_born": politician_json["date_born"]
            }

            if politician_json["type"] == PoliticianType.SENATOR:
                in_missing_list.append(Senator(constructor_args))
            elif politician_json["type"] == PoliticianType.REPRESENTATIVE:
                in_missing_list.append(Representative(constructor_args))
            else:
                logging.error(f"Invalid type {politician_json['type']}")

    secrets = f.get_secrets_dict()
    bot = BotClient(
        api_key=secrets["apiKey"],
        api_key_secret=secrets["apiKeySecret"],
        access_token=secrets["accessToken"],
        access_token_secret=secrets["accessTokenSecret"],
        bearer_token=secrets["bearerToken"]
    )

    # only create full list of senators/reps if in_missing_list not found
    politician_list = []
    if in_missing_list is None or len(in_missing_list) == 0:
        senator_list = get_politicians(
            politician_list_wiki_url=c.SENATORS_WIKI_URL,
            list_size=c.TOTAL_NUM_SENATORS,
            politician_type=PoliticianType.SENATOR
        )
        rep_list = get_politicians(
            politician_list_wiki_url=c.REPRESENTATIVES_WIKI_URL,
            list_size=c.TOTAL_NUM_REPRESENTATIVES,
            politician_type=PoliticianType.REPRESENTATIVE
        )

        # join lists
        politician_list = senator_list + rep_list
    else:
        politician_list = in_missing_list

    # find politician twitter accounts
    num_senators_found = 0
    num_reps_found = 0
    twitter_users_found = []
    twitter_users_missing = []

    # only searching missing politicians
    for politician in politician_list:
        twitter_user = search_possible_twitter_handles(
            politician=politician,
            client=bot
        )

        if len(twitter_users_found) == 5:
            break

        if twitter_user:
            twitter_users_found.append(twitter_user)

            if politician.type == PoliticianType.REPRESENTATIVE:
                num_reps_found += 1
            elif politician.type == PoliticianType.SENATOR:
                num_senators_found += 1

            logging.info(f"Twitter User ({politician.first_name} {politician.last_name})")
            logging.info(f"id:       {twitter_user.id}")
            logging.info(f"name:     {twitter_user.name}")
            logging.info(f"username: {twitter_user.username}")
            logging.info(f"verified: {twitter_user.verified}\n")
        else:
            twitter_users_missing.append(politician)
            logging.warn(f"Could not find user: {politician.first_name} {politician.last_name}")

    logging.info(f"Found {num_reps_found}/{c.TOTAL_NUM_REPRESENTATIVES} representatives")
    logging.info(f"Found {num_senators_found}/{c.TOTAL_NUM_SENATORS} senators")

    # return data as 2 JSON lists
    found = json.dumps(twitter_users_found, cls=Encoder)
    missing = json.dumps(twitter_users_missing, cls=Encoder)

    return found, missing


def main(
    getUsersTimer: func.TimerRequest,
    inMissing: str,
    outMissing: func.Out[str],
    found: func.Out[str]
):
    logging.info(f"[IN] missing.json: {inMissing}")

    if getUsersTimer.past_due:
        found_json, missing_json = run(inMissing)

        logging.info(f"[OUT] found.json: {found_json}")
        logging.info(f"[OUT] missing.json: {missing_json}")

        # save JSON lists to storage account
        found.set(found_json)
        outMissing.set(missing_json)


if __name__ == "__main__":
    main()
