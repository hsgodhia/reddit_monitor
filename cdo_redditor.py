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

@reddapp.errorhandler(404)
def not_found(error):
    err = Error()
    return err.make_error(200, 2, "...coded overnight, you've come to 404!", "change the endpoint to /reddit_stats/subreddit/<subr> ")

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
    
    try:
        k = int(k)
    except Exception:
        return err.make_error(200, 3, "invalid limit query param", "limit is a number try again!")
    
    listing = None
    if rank_by == 'hot':
        listing = subrredit_found.hot(limit=k)
    elif rank_by == 'new':
        listing = subrredit_found.new(limit=k)
    elif rank_by == 'top':
        listing = subrredit_found.top(limit=k)
    elif rank_by == 'rising':
        listing = subrredit_found.rising(limit=k)
    else:
        return err.make_error(200, 3, "invalid rank query param", "rank is hot/new/rising/top only try again!")
    
    for submission in listing:
        r = {}
        r['title'] = submission.title
        r['score'] = submission.score
        r['Link'] = submission.url
        result.append(r)
    if len(result) < 1:
        return err.make_error(200, 0, "0 results found for given ranking type", "change rank type to something else")
    f_resp[rank_by + " " + str(k)] = result
    return jsonify(f_resp)

if __name__ == '__main__':
    reddapp.run(debug=True)