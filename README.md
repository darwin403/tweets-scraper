# What does this script do?

This script `scrape.py` scrapes for all Twitter usernames containing a particular keyword from the first `MAX_PAGES=2` pages. For example, say "[modi](https://twitter.com/search?q=modi&src=typed_query&f=user)", all usernames containing "modi" along with their tweets from last `TWEETS_SINCE=2` days are then dumped in files `users.csv` and `tweets/narendramodi.csv` for each username. The users dump `user.csv` contains the following columns and more.

| id        | screen_name  | name          | bio                                   | ... |
| --------- | ------------ | ------------- | ------------------------------------- | --- |
| 18839785  | narendramodi | Narendra Modi | Prime Minister of India               | ... |
| 471741741 | PMOIndia     | PMO India     | Office of the Prime Minister of India | ... |
| ...       | ...          | ....          | ...                                   | ... |

In the "tweets" column of each username, you find the local file path for the tweets made by the particular user in the last `TWEETS_SINCE=2` days. The tweets data is scraped and stored in a separate file at `tweets/narendramodi.csv` which contains the following columns and more.

| id                  | conversation_id     | created_at    | ... | tweet                                                                              | ... |
| ------------------- | ------------------- | ------------- | --- | ---------------------------------------------------------------------------------- | --- |
| 1260244139142086657 | 1260244139142086657 | 1589300591000 | ... | The way ahead lies in LOCAL.                                                       | ... |
| 1260243893498466309 | 1260243893498466309 | 1589300533000 | ... | एक विशेष आर्थिक पैकेज जो ‘आत्मनिर्भर भारत अभियान’ की अहम कड़ी के तौर पर काम करेगा। | ... |
| ...                 | ...                 | ...           | ... | ...                                                                                | ... |

# Requirements

One needs to create a Twitter application and obtain [Access Tokens](https://developer.twitter.com/ja/docs/basics/authentication/guides/access-tokens). We will need the following keys to search for users matching a keyword using the Twitter API.

- API Key
- API Secret Key
- Access Token
- Access Secret Token

# Usage

You will require `python3` and `pip3` to be installed on your computer before you can proceed to the next steps. Once installed, begin by installing the required libraries for this script by running

```bash
git clone git@github.com:skdcodes/bot-twitter.git # clone project
cd bot-twitter # change directory to project
pip3 install -r requirements.txt # pip installs required libraries
```

Open the file `scrape.py` and edit the following lines with your details.

```vim
.
.
API_KEY = "4PzLI2Fp1TsuQ5z9yRpTdRVSD"
API_SECRET_KEY = "cSR3RFKgVKTFjfktko61oegw0h7bRkgceR9mbdbC4PLevYoSzZ"

ACCESS_TOKEN = "1260346234503442432-oa1u8VmcQ8KscXyeVnZpONHr9Nh1ex"
ACCESS_TOKEN_SECRET = "l7JngSBFwGLoJ6PzRAAZ7nkOiduxij9ygv5Eg2kxRMK7v"

USER_CONTAINS = "modi"

.
.
```

You can now run the script

```bash
python3 scrape.py
```

Thats it! You will see the scrape progress on your console something similar to:

```bash
.
.
# Found users for "modi" on page 1.
# 1260244139142086657 2020-05-12 21:53:11 IST <narendramodi> The way ahead lies in LOCAL.  Local Manufacturing.   Local Markets.   Local Supply Chain.  Local is not merely a need but a responsibility.   Be vocal about local! #AatmanirbharBharat pic.twitter.com/eYqt5IDtBp
# 1260243893498466309 2020-05-12 21:52:13 IST <narendramodi> एक विशेष आर्थिक पैकेज जो ‘आत्मनिर्भर भारत अभियान’ की अहम कड़ी के तौर पर काम करेगा। #AatmanirbharBharat pic.twitter.com/59HERWpwJ4
# 1260243737801666561 2020-05-12 21:51:35 IST <narendramodi> आत्मनिर्भर भारत की यह भव्य इमारत, इन पांच पिलर्स पर खड़ी होगी... #AatmanirbharBharat pic.twitter.com/CmXdgEu3No
.
.
.
```

A dump file `users.csv` will be created in the same folder as the script. The corresponding tweets will be dumped in the same folder `./tweets`

# Features

- User search is done via Twitter API. There are no request limits. However, a rate limit of 900 requests/15 minutes is applied.
- Tweet search is done via [Twint](https://github.com/twintproject/twint). This library allows us to make us to make **unlimited requests with no rate limits**!
- Multithreaded with 20 workers.

# Dependencies

- [Tweepy](https://github.com/tweepy/tweepy) - Twitter API wrapper for Python.
- [Twint](https://github.com/twintproject/twint) - Unlimited tweet scraping library.

# Notes

- Its important to look at the official twitter developer documents to know what the pricing of various API routes are and the Rate limits.
- A quick comparison of various Rate-Limited API endpoint routes are given here: https://developer.twitter.com/en/docs/basics/rate-limits
- Twitter official provides a premium Tweet Search API. With a free developer account tweet searches are restricted, one can make 250 requests/month or 25K tweets/month, which ever occurs first.
