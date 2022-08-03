from client.tweepy_client import TweepyClient
import utils
from model.politician_type import PoliticianType

REPRESENTATIVES_WIKI_URL="https://en.wikipedia.org/wiki/List_of_current_members_of_the_United_States_House_of_Representatives"
SENATORS_WIKI_URL="https://en.wikipedia.org/wiki/List_of_current_United_States_senators"
TOTAL_NUM_REPRESENTATIVES=435
TOTAL_NUM_SENATORS=100

def main():
  secrets_file_path = "./secrets.json"
  twitter = TweepyClient(secrets_file_path)

  # get lists of politicians
  senator_list = utils.get_senators(member_list_wiki_url=SENATORS_WIKI_URL,
    list_size=TOTAL_NUM_SENATORS,
    politician_type=PoliticianType.Senator)
  rep_list = utils.get_representatives(member_list_wiki_url=REPRESENTATIVES_WIKI_URL,
    list_size=TOTAL_NUM_REPRESENTATIVES,
    politician_type=PoliticianType.Representative)

  # process senators first


  return

  # keyword to search tweets
  query = "(PS5 OR Playstation5 OR Playstation) (Restock OR stock)"

  # not retweet, quote, or reply
  query += " -is:retweet"
  query += " -is:quote"
  query += " -is:reply"

  # in english
  query += " lang:en"
  max_results = 10

  response = twitter.client.search_recent_tweets(
    query=query,
    max_results=max_results
  )

  tweets = response.data
  for tweet in tweets:
    print(tweet)

  return

if __name__ == "__main__":
  main()