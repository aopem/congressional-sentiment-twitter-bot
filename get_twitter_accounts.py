import json
import pandas as pd

import twitter_bot.utils.constants as c
from twitter_bot.client import TweepyClient
from twitter_bot.model import TwitterAccount
from twitter_bot.model import PoliticianType
from twitter_bot.model import Senator
from twitter_bot.model import Representative
from twitter_bot.serialization import Encoder


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

    raise Exception(f"No entry found for list size: {list_size} at URL: {politician_list_wiki_url}")


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
                politician_list.append(Representative(**constructor_args))
            elif politician_type == PoliticianType.SENATOR:
                politician_list.append(Senator(**constructor_args))
            else:
                raise Exception(f"Invalid type: {politician_type}")

        except IndexError:
            print(f"Name {politician[name_key]} not formatted correctly")

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
        return TwitterAccount(id=response.data.id,
            name=response.data.name,
            username=response.data.username,
            verified=response.data.verified
        )

    return None


def main():
    secrets_file_path = "./secrets.json"
    client = TweepyClient(secrets_file_path)

    # get lists of politicians
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

    # find politician twitter accounts
    num_senators_found = 0
    num_reps_found = 0
    twitter_accounts_found = []
    twitter_accounts_missing = []
    for politician in politician_list:
        twitter_account = search_possible_twitter_handles(
            politician=politician,
            client=client
        )

        if twitter_account:
            twitter_accounts_found.append(twitter_account)

            if politician.getPoliticianType() == PoliticianType.REPRESENTATIVE:
                num_reps_found += 1
            elif politician.getPoliticianType() == PoliticianType.SENATOR:
                num_senators_found += 1

            print("\n")
            print(f"Twitter Account ({politician.first_name} {politician.last_name})")
            print(f"id:       {twitter_account.id}")
            print(f"name:     {twitter_account.name}")
            print(f"username: {twitter_account.username}")
            print(f"verified: {twitter_account.verified}")
            print("\n")
        else:
            twitter_accounts_missing.append(politician)
            print(f"WARN: Could not find account: {politician.first_name} {politician.last_name}")

    print(f"Found {num_reps_found}/{c.TOTAL_NUM_REPRESENTATIVES} representatives")
    print(f"Found {num_senators_found}/{c.TOTAL_NUM_SENATORS} senators")

    # save data to files
    with open(c.TWITTER_ACCOUNTS_FOUND_FILENAME, "w+") as file:
        json.dump(twitter_accounts_found, fp=file, cls=Encoder)

    with open(c.TWITTER_ACCOUNTS_MISSING_FILENAME, "w+") as file:
        json.dump(twitter_accounts_missing, fp=file, cls=Encoder)

    return


if __name__ == "__main__":
    main()
