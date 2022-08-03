from client.tweepy_client import TweepyClient
import utils.utils as utils

def main():
  secrets_file_path = "./secrets.json"
  twitter = TweepyClient(secrets_file_path)

  # get lists of politicians
  rep_list = utils.get_representatives()
  senator_list = utils.get_senators()

  response = twitter.searchUserByName(rep_list[0].name)
  print(response)

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