import requests

test404 = requests.request('GET', 'https://cdorstats.herokuapp.com/afsdasdasf')
assert str(test404.json()) == r"""{'action': 'change the endpoint to /reddit_stats/subreddit/<subr> ', 'message': "You've come to 404!"}"""

test_invalid_subreddit = requests.request('GET', 'https://cdorstats.herokuapp.com/reddit_stats/subreddit/leardgsdgsdg')
assert str(test_invalid_subreddit.json()) == r"""{'action': 'change subreddit to something else', 'message': '0 results found for given subreddit'}"""

test_invalid_queryparam_rank_by = requests.request('GET', 'https://cdorstats.herokuapp.com/reddit_stats/subreddit/news?rank_by=afadgagadf')
assert str(test_invalid_queryparam_rank_by.json()) == r"""{'action': 'rank is hot/new/rising/top only try again!', 'message': 'invalid rank query param'}"""

test_invalid_queryparam_limit = requests.request('GET', 'https://cdorstats.herokuapp.com/reddit_stats/subreddit/news?rank_by=top&limit=a')
assert str(test_invalid_queryparam_limit.json()) == r"""{'action': 'limit is a number try again!', 'message': 'invalid limit query param'}"""

test_ok = requests.request('GET', 'https://cdorstats.herokuapp.com/reddit_stats/subreddit/news?limit=1')
assert "'subreddit_name': 'news'" in str(test_ok.json())