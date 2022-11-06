"""
Helper functions for get_users Azure function
"""
import logging
import pandas as pd

from twitter_bot.enums import PoliticianType
from twitter_bot.data import Politician

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
        try:
            name = politician[name_key].split()

            politician_list.append(Politician(
                first_name=name[0],
                last_name=name[1] if len(name) <= 2 else name[2],
                party=politician[party_key],
                state=politician[state_key],
                residence=politician[residence_key],
                date_born=politician[date_born_key],
                politician_type=politician_type
            ))

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
    json_data: dict
) -> list[Politician]:
    politician_list = []
    for politician in json_data:
        if politician["type"] == PoliticianType.REPRESENTATIVE:
            type = PoliticianType.REPRESENTATIVE
        elif politician["type"] == PoliticianType.SENATOR:
            type = PoliticianType.SENATOR
        else:
            logging.error(f"Invalid politician type {politician['type']}")

        politician_list.append(Politician(
            first_name=politician["first_name"],
            last_name=politician["last_name"],
            party=politician["party"],
            state=politician["state"],
            residence=politician["residence"],
            date_born=politician["date_born"],
            politician_type=type
        ))

    return politician_list
