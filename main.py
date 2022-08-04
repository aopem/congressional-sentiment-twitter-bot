import utils
import constants as c
from client.tweepy_client import TweepyClient
from model.twitter_user import TwitterUser
from model.politician_type import PoliticianType


def search_possible_twitter_handles(politician, client):
    possible_twitter_handles = politician.getPossibleTwitterHandles()

    for handle in possible_twitter_handles:
        response = client.searchUsername(handle)

        # if user is found, response.data will be populated
        if response.data == None:
            continue

        user = TwitterUser(id=response.data.id,
            name=response.data.name,
            username=response.data.username
        )

        # TODO: add validation checks here
        # if user.name == f"{politician.first_name} {politician.last_name}":
        return user

    return None


def main():
    secrets_file_path = "./secrets.json"
    client = TweepyClient(secrets_file_path)

    # get lists of politicians
    senator_list = utils.get_politicians(politician_list_wiki_url=c.SENATORS_WIKI_URL,
        list_size=c.TOTAL_NUM_SENATORS,
        politician_type=PoliticianType.Senator)
    rep_list = utils.get_politicians(politician_list_wiki_url=c.REPRESENTATIVES_WIKI_URL,
        list_size=c.TOTAL_NUM_REPRESENTATIVES,
        politician_type=PoliticianType.Representative)

    # join lists
    politician_list = senator_list + rep_list

    # process senators
    num_senators_found = 0
    num_reps_found = 0
    twitter_accounts_found = []
    for politician in politician_list:
        twitter_account = search_possible_twitter_handles(politician, client)
        if twitter_account:
            twitter_accounts_found.append(twitter_account)

            print("Twitter Account Info")
            print(f"id:       {twitter_account.id}")
            print(f"name:     {twitter_account.name}")
            print(f"username: {twitter_account.username}")
            print("\n")

            if politician.getPoliticianType() == PoliticianType.Representative:
                num_reps_found += 1
            elif politician.getPoliticianType() == PoliticianType.Senator:
                num_senators_found += 1
        else:
            print(f"Could not find twitter account for {politician.first_name} {politician.last_name}")

    print(f"Found {num_reps_found}/{c.TOTAL_NUM_REPRESENTATIVES} representatives")
    print(f"Found {num_senators_found}/{c.TOTAL_NUM_SENATORS} senators")

    # save data to file
    handle_file_name = "handles.txt"
    with open(handle_file_name, "w+") as handle_file:
        for twitter_account in twitter_accounts_found:
            handle_file.write(f"{twitter_account.username}\n")

    return


if __name__ == "__main__":
    main()