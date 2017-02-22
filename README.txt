Author-
Harshal Godhia
hgodhia@cs.umass.edu

0. My Reddit API deployed at
https://cdorstats.herokuapp.com/reddit_stats/subreddit/news

1. To launch the application locally
    a. Install python and pip
    b. Run the following command to install dependencies
       pip install -r requirements.txt

2. The application is using the flask web framework, gunicorn http web server, python wrapper "praw" for reddit and is deployed on heroku.

3. Using the wrapper it talks to the reddit API in read-only mode. So basically we cannot execute user specific API calls but can get general information like top submissions in a subreddit and so on

4. It gives a rich set of queryparams rank_by and limit for example,
https://cdorstats.herokuapp.com/reddit_stats/subreddit/news?ranky_by=hot&limit=25

5. Several test cases are included in the client side testing program
client_side_test.py