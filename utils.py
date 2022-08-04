import pandas as pd
from model.senator import Senator
from model.representative import Representative
from model.politician_type import PoliticianType


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

