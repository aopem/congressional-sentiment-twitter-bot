import utils
from client.tweepy_client import TweepyClient
from model.politician_type import PoliticianType

REPRESENTATIVES_WIKI_URL="https://en.wikipedia.org/wiki/List_of_current_members_of_the_United_States_House_of_Representatives"
SENATORS_WIKI_URL="https://en.wikipedia.org/wiki/List_of_current_United_States_senators"
TOTAL_NUM_REPRESENTATIVES=435
TOTAL_NUM_SENATORS=100


def search_possible_twitter_handles(politician, client):
    possible_twitter_handles = utils.get_possible_twitter_handles(politician)
    for handle in possible_twitter_handles:
        response = client.searchUsername(handle)

        # if user is found, response.data will be populated
        if response.data != None:
            return response.data

    return None

def main():
    secrets_file_path = "./secrets.json"
    client = TweepyClient(secrets_file_path)

    # get lists of politicians
    senator_list = utils.get_politicians(politician_list_wiki_url=SENATORS_WIKI_URL,
        list_size=TOTAL_NUM_SENATORS,
        politician_type=PoliticianType.Senator)
    rep_list = utils.get_politicians(politician_list_wiki_url=REPRESENTATIVES_WIKI_URL,
        list_size=TOTAL_NUM_REPRESENTATIVES,
        politician_type=PoliticianType.Representative)

    twitter_handles_found = []

    # process senators
    num_senators_found = 0
    for senator in senator_list:
        handle = search_possible_twitter_handles(senator, client)

        if handle:
            twitter_handles_found.append(handle)
            num_senators_found += 1
            print(f"Found {senator.first_name} {senator.last_name} at @{handle}!")
        else:
            print(f"Could not find twitter account for {senator.first_name} {senator.last_name}")

    # process representatives
    num_reps_found = 0
    for rep in rep_list:
        handle = search_possible_twitter_handles(rep, client)

        if handle:
            twitter_handles_found.append(handle)
            num_reps_found += 1
            print(f"Found {rep.first_name} {rep.last_name} at @{handle}!")
        else:
            print(f"Could not find twitter account for {rep.first_name} {rep.last_name}")

    print(f"Found {num_reps_found}/{TOTAL_NUM_SENATORS} representatives")
    print(f"Found {num_senators_found}/{TOTAL_NUM_SENATORS} senators")

    # save data to file
    handle_file_name = "handles.txt"
    with open(handle_file_name, "w+") as handle_file:
        handle_file.writelines(twitter_handles_found)

    return

if __name__ == "__main__":
    main()