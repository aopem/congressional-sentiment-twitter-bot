import pandas as pd
from .model.politician import Politician

REPRESENTATIVES_WIKI_URL="https://en.wikipedia.org/wiki/List_of_current_members_of_the_United_States_House_of_Representatives"
SENATORS_WIKI_URL="https://en.wikipedia.org/wiki/List_of_current_United_States_senators"
TOTAL_NUM_REPRESENTATIVES=435
TOTAL_NUM_SENATORS=100

def get_member_dict(member_list_wiki_url, list_size):
    wiki_data = pd.read_html(member_list_wiki_url)

    # find correct table according to list_size
    for df in wiki_data:
        length = df.shape[0]
        if length == list_size:
            return df.to_dict(orient='index')

    raise Exception(f"No entry found for list size: {list_size} at URL: {member_list_wiki_url}")


def get_representatives():
    representative_dict = get_member_dict(REPRESENTATIVES_WIKI_URL, TOTAL_NUM_REPRESENTATIVES)
    representative_list = []

    # use dict to create Politician objects
    for rep in representative_dict.values():
        representative_list.append(Politician(
            name=rep["Member"],
            party=rep["Party.1"],
            state=rep["District"],
            residence=rep["Residence"],
            date_born=rep["Born[2]"]
        ))

    return representative_list


def get_senators():
    senator_dict = get_member_dict(SENATORS_WIKI_URL, TOTAL_NUM_SENATORS)
    senator_list = []

    # use dict to create Politician objects
    for senator in senator_dict.values():
        senator_list.append(Politician(
            name=senator["Senator"],
            party=senator["Party.1"],
            state=senator["State"],
            residence=senator["Residence[2]"],
            date_born=senator["Born"]
        ))

    return senator_list
