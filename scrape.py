import tweepy
import csv
import twint
import os
import sys
from concurrent.futures import ThreadPoolExecutor as PoolExecutor
from datetime import date
from dateutil.relativedelta import relativedelta

# twitter access tokens
API_KEY = "4PzLI2Fp1TsuQ5z9yRpTdRVSD"
API_SECRET_KEY = "cSR3RFKgVKTFjfktko61oegw0h7bRkgceR9mbdbC4PLevYoSzZ"

ACCESS_TOKEN = "1260346234503442432-oa1u8VmcQ8KscXyeVnZpONHr9Nh1ex"
ACCESS_TOKEN_SECRET = "l7JngSBFwGLoJ6PzRAAZ7nkOiduxij9ygv5Eg2kxRMK7v"

# keyword to search for in user
USER_CONTAINS = "modi"

# max number pages to paginate. twitter api provides 20 usernames per page.
MAX_PAGES = 2
TWEETS_SINCE = 2 # no of days from today to scrape tweets

# fetch_users for a given keyword and page number


def fetch_users(page):
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    try:
        users = api.search_users(q=USER_CONTAINS, page=page)
        print('Found users for "%s" on page %s.' %
              (USER_CONTAINS, page)) if users else None
        return users

    except Exception as e:
        return []


# hoist users data
users = []

# create a thread pool size of 20 to scrape all users matching keyword
with PoolExecutor(max_workers=20) as executor:
    for new_users in executor.map(fetch_users, range(1, MAX_PAGES)):
        users += new_users


if not users:
    sys.exit('No users found for "%s"' % USER_CONTAINS)


# create tweets folder to save tweets
if not os.path.exists('tweets'):
    os.makedirs('tweets')

# create data file containing all users
with open("users.csv", "w+", encoding="utf-8") as f:
    doc = csv.writer(f, delimiter=",", quotechar='"',
                     quoting=csv.QUOTE_ALL)
    doc.writerow([
        "id", "screen_name", "name", "bio", "location", "followers_count", "following", "created_at", "link", "tweets_file"
    ])

    # iterate over each user and scrape the data
    for user in users:

        # write the user to users.csv
        doc.writerow([
            user.id, user.screen_name, user.name, user.description, user.location, user.followers_count, user.following, user.created_at, user.url, "tweets/%s.csv" % user.screen_name
        ])


# create tweets
for user in users:
    # assign location for tweets of a user
    tweets_file = "tweets/%s.csv" % user.screen_name

    # delete tweets file if already exists
    if os.path.exists(tweets_file):
        os.remove(tweets_file)

    # describe twint configuration
    c = twint.Config()
    c.Username = user.screen_name
    c.Since = (date.today() + relativedelta(days=-TWEETS_SINCE)  # tweets since 2 days
               ).strftime('%Y-%m-%d %H:%M:%S')
    c.Output = tweets_file
    c.Store_csv = True

    # scrape the user tweets
    twint.run.Search(c)
