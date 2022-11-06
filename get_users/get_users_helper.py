"""
Helper functions for get_users Azure function
"""
import logging
import pandas as pd

from src.enums import PoliticianType
from src.model import Politician, Representative, Senator


def get_politician_dict(
    politician_list_wiki_url: str,
    list_size: int
) -> dict:
    wiki_data = pd.read_html(politician_list_wiki_url)

    # find correct table according to list_size
    for df in wiki_data:
        length = df.shape[0]
        if length == list_size:
            return df.to_dict(orient='index')

    error = f"No politician table found at URL: {politician_list_wiki_url}"
    logging.error(error)
    raise Exception(error)


def get_politician_list(
    politician_list_wiki_url: str,
    list_size: int,
    politician_type: PoliticianType,
    name_key: str,
    party_key: str,
    state_key: str,
    residence_key: str,
    date_born_key: str
) -> list[Politician]:
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
    politician_list_wiki_url: str,
    list_size: int,
    politician_type: PoliticianType
) -> list[Politician]:
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


def create_politician_list_from_json(
    json_dict: dict
) -> list[Politician]:
    politician_list = []
    for politician_json in json_dict:
        constructor_args = {
            "name": politician_json["name"],
            "party": politician_json["party"],
            "state": politician_json["state"],
            "residence": politician_json["residence"],
            "date_born": politician_json["date_born"]
        }

        if politician_json["type"] == PoliticianType.SENATOR:
            politician_list.append(Senator(constructor_args))
        elif politician_json["type"] == PoliticianType.REPRESENTATIVE:
            politician_list.append(Representative(constructor_args))
        else:
            logging.error(f"Invalid type {politician_json['type']}")

    return politician_list
