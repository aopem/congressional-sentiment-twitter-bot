import pandas as pd
import logging

import twitter_bot.enums.politician_type as enums
import twitter_bot.model.representative as r
import twitter_bot.model.senator as s


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
            if politician_type == enums.PoliticianType.REPRESENTATIVE:
                politician_list.append(r.Representative(constructor_args))
            elif politician_type == enums.PoliticianType.SENATOR:
                politician_list.append(s.Senator(constructor_args))
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
    if politician_type == enums.PoliticianType.REPRESENTATIVE:
        keys = {
            "name_key": "Member",
            "party_key": "Party.1",
            "state_key": "District",
            "residence_key": "Residence",
            "date_born_key": "Born[2]"
        }
    elif politician_type == enums.PoliticianType.SENATOR:
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


def create_politician_list_from_json(
    json_dict
):
    politician_list = []
    for politician_json in json_dict:
        constructor_args = {
            "name": politician_json["name"],
            "party": politician_json["party"],
            "state": politician_json["state"],
            "residence": politician_json["residence"],
            "date_born": politician_json["date_born"]
        }

        if politician_json["type"] == enums.PoliticianType.SENATOR:
            politician_list.append(s.Senator(constructor_args))
        elif politician_json["type"] == enums.PoliticianType.REPRESENTATIVE:
            politician_list.append(r.Representative(constructor_args))
        else:
            logging.error(f"Invalid type {politician_json['type']}")

    return politician_list
