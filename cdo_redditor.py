from flask import Flask, jsonify, request, redirect
from collections import OrderedDict
import praw

reddit = praw.Reddit(client_id='p8Hs4qPd7HD1Wg',client_secret='9rEQJxxC7Tp_DD8wQLsshAOudNU', user_agent='App by /u/hershey92')
reddapp = Flask(__name__)

class Error:
    def make_error(self, status_code, sub_code, message, action):
        response = jsonify({'status': status_code,'sub_code': sub_code,'message': message,'action': action})
        response.status_code = status_code
        return response

@reddapp.route('/')
def home():
    err = Error()
    return err.make_error(200, 2, "This app was coded overnight, doesn't have a good 404 page", "change the URL to /reddit_stats/subreddit/<subr> ")

@reddapp.route('/reddit_stats/subreddit/<subr>', methods=['GET'])
def getSubredditSubmissions(subr):
    err = Error()
    rank_by = request.args.get('rank_by', 'hot')
    k = request.args.get('limit', '10')
    f_resp = OrderedDict()
    result = []
    try:
        subrredit_found = reddit.subreddit(subr)
        f_resp[subr + ' is about'] = subrredit_found.title
    except Exception:
        return err.make_error(200, 1, "No results found for given subreddit", "change subreddit to something else")

    k = int(k)
    listing = None
    if rank_by == 'hot':
        listing = subrredit_found.hot(limit=k)
    elif rank_by == 'new':
        listing = subrredit_found.new(limit=k)
    elif rank_by == 'top':
        listing = subrredit_found.top(limit=k)
    elif rank_by == 'rising':
        listing = subrredit_found.rising(limit=k)
    for submission in listing:
        r = {}
        r['title'] = submission.title
        r['score'] = submission.score
        r['Link'] = submission.url
        result.append(r)
    if len(result) < 1:
        return err.make_error(200, 0, "No results found for given ranking type", "change rank type to something else")
    f_resp[rank_by + " " + str(k)] = result
    return jsonify(f_resp)

if __name__ == '__main__':
    reddapp.run(debug=True)