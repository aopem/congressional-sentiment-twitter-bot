# congressional-sentiment-twitter-bot

[![Twitter URL](https://img.shields.io/twitter/url/https/twitter.com/CongressSentBot.svg?style=social&label=Follow%20%40CongressSentBot)](https://twitter.com/CongressSentBot)

Twitter bot that crowdsources Twitter user sentiment towards a random member of Congress each day, then tweets the results.

Built using:

* Azure Kubernetes Service
* Azure SQL Database
* Azure Cognitive Services
* C#/ASP.NET Core
* Python & tweepy

## Microservices

### CongressMemberAPI

A REST API built using C#/ASP.NET Core that allows interaction with a database that synchronizes with the [ProPublica Congress API](https://www.propublica.org/datastore/api/propublica-congress-api) to keep records of the current members of Congress, along with other useful information.

### sentiment_tweet_job

A Kubernetes cronjob that runs daily at 12PM PST. The job crowdsources the 100 latest mentions of a random member of Congress' Twitter account, sends the data to Azure Cognitive Services for analysis, then uses the sentiment information to obtain a score for that Congress member. This information is then sent out as a Tweet.

### SyncMemberDbJob

A Kubernetes cronjob built using C#/ASP.NET Core that runs once daily at 12AM PST. It creates a background service that queries the [ProPublica Congress API](https://www.propublica.org/datastore/api/propublica-congress-api) to get a list of all current members of Congress. Then, it updates the associated database using the CongressMemberAPI service.
