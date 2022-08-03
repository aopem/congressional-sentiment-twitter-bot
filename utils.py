import pandas as pd
from .model.senator import Senator
from .model.representative import Representative
from .model.politician_type import PoliticianType


def get_member_dict(member_list_wiki_url, list_size):
    wiki_data = pd.read_html(member_list_wiki_url)

    # find correct table according to list_size
    for df in wiki_data:
        length = df.shape[0]
        if length == list_size:
            return df.to_dict(orient='index')

    raise Exception(f"No entry found for list size: {list_size} at URL: {member_list_wiki_url}")


def get_politicians(member_list_wiki_url, list_size, politician_type, name_key, party_key, state_key, residence_key, date_born_key):
    member_dict = get_member_dict(member_list_wiki_url, list_size)
    member_list = []

    for member in member_dict.values():
        try:
            if politician_type == PoliticianType.Representative:
                member_list.append(Representative(
                    first_name=member[name_key].split()[0],
                    last_name=member[name_key].split()[1],
                    party=member[party_key],
                    state=member[state_key],
                    residence=member[residence_key],
                    date_born=member[date_born_key]
                ))
            elif politician_type == PoliticianType.Senator:
                member_list.append(Senator(
                    first_name=member[name_key].split()[0],
                    last_name=member[name_key].split()[1],
                    party=member[party_key],
                    state=member[state_key],
                    residence=member[residence_key],
                    date_born=member[date_born_key]
                ))
            else:
                raise Exception(f"Incorrect type: {politician_type}")

        except IndexError:
            print(f"Name {member[name_key]} not formatted correctly")

    return member_list


def get_representatives(member_list_wiki_url, list_size, politician_type):
    representative_keys = {
        "name_key": "Member",
        "party_key": "Party.1",
        "state_key": "District",
        "residence_key": "Residence",
        "date_born_key": "Born[2]"
    }

    return get_politicians(member_list_wiki_url, list_size, politician_type, **representative_keys)


def get_senators(member_list_wiki_url, list_size, politician_type):
    senator_keys = {
        "name_key": "Senator",
        "party_key": "Party.1",
        "state_key": "State",
        "residence_key": "Residence[2]",
        "date_born_key": "Born"
    }

    return get_politicians(member_list_wiki_url, list_size, politician_type, **senator_keys)


def get_rep_twitter_handle(first_name, last_name):
    pass

