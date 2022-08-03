import re
import pandas as pd
from model.senator import Senator
from model.representative import Representative
from model.politician_type import PoliticianType

TWITTER_USERNAME_CHARACTER_LIMIT=15
TWITTER_USERNAME_REGEX_PATTERN=r"^[A-Za-z0-9_]{1,15}$"

def get_politician_dict(politician_list_wiki_url, list_size):
    wiki_data = pd.read_html(politician_list_wiki_url)

    # find correct table according to list_size
    for df in wiki_data:
        length = df.shape[0]
        if length == list_size:
            return df.to_dict(orient='index')

    raise Exception(f"No entry found for list size: {list_size} at URL: {politician_list_wiki_url}")


def get_politician_list(politician_list_wiki_url, list_size, politician_type, name_key, party_key, state_key, residence_key, date_born_key):
    politician_dict = get_politician_dict(politician_list_wiki_url, list_size)
    politician_list = []

    for politician in politician_dict.values():
        try:
            if politician_type == PoliticianType.Representative:
                politician_list.append(Representative(
                    first_name=politician[name_key].split()[0],
                    last_name=politician[name_key].split()[1],
                    party=politician[party_key],
                    state=politician[state_key],
                    residence=politician[residence_key],
                    date_born=politician[date_born_key]
                ))
            elif politician_type == PoliticianType.Senator:
                politician_list.append(Senator(
                    first_name=politician[name_key].split()[0],
                    last_name=politician[name_key].split()[1],
                    party=politician[party_key],
                    state=politician[state_key],
                    residence=politician[residence_key],
                    date_born=politician[date_born_key]
                ))
            else:
                raise Exception(f"Invalid type: {politician_type}")

        except IndexError:
            print(f"Name {politician[name_key]} not formatted correctly")

    return politician_list


def get_politicians(politician_list_wiki_url, list_size, politician_type):
    if politician_type == PoliticianType.Representative:
        keys = {
            "name_key": "Member",
            "party_key": "Party.1",
            "state_key": "District",
            "residence_key": "Residence",
            "date_born_key": "Born[2]"
        }
    elif politician_type == PoliticianType.Senator:
        keys = {
            "name_key": "Senator",
            "party_key": "Party.1",
            "state_key": "State",
            "residence_key": "Residence[2]",
            "date_born_key": "Born"
        }
    else:
        raise Exception(f"Invalid type: {politician_type}")

    return get_politician_list(politician_list_wiki_url, list_size, politician_type, **keys)


def get_possible_twitter_handles(politician):
    prefixes = []
    if politician.getPoliticianType() == PoliticianType.Representative:
        prefixes.append("Rep")
    elif politician.getPoliticianType() == PoliticianType.Senator:
        prefixes.append("Sen")
        prefixes.append("Senator")
    else:
        raise Exception(f"Invalid type: {politician.getPoliticianType()}")

    possible_handles = []
    for prefix in prefixes:
        unfiltered_possible_handles = []
        unfiltered_possible_handles.append(f"{prefix}{politician.first_name}{politician.last_name}")
        unfiltered_possible_handles.append(f"{prefix}{politician.last_name}")
        unfiltered_possible_handles.append(f"{prefix}{politician.first_name}")

        for possible_handle in unfiltered_possible_handles:
            if len(possible_handle) > TWITTER_USERNAME_CHARACTER_LIMIT:
                possible_handle = possible_handle[:TWITTER_USERNAME_CHARACTER_LIMIT]

            if not re.match(TWITTER_USERNAME_REGEX_PATTERN, possible_handle):
                continue

            # if above checks pass, could be a real handle
            possible_handles.append(possible_handle)

    return possible_handles
