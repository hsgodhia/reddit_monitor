from flask import Flask, jsonify, request, redirect
import praw, os, redis

redis_url = os.environ('REDIS_URL')
redis_conn = redis.from_url(redis_url)

client_id = redis_conn.get('CLIENT_ID').decode("utf-8") 
client_secret = redis_conn.get('CLIENT_SECRET').decode("utf-8") 
user_agent = redis_conn.get('USER_AGENT').decode("utf-8") 

reddit_inst = praw.Reddit(client_id = client_id, client_secret = client_secret , user_agent = user_agent)
reddapp = Flask(__name__)

class Error:
    def make_error(self, status_code, message, action):
        response = jsonify({'message': message,'action': action})
        response.status_code = status_code
        return response

@reddapp.errorhandler(404)
def not_found(error):
    err = Error()
    return err.make_error(404, "You've come to 404!", "change the endpoint to /reddit_stats/subreddit/<subr> ")

@reddapp.route('/reddit_stats/subreddit/<subr>', methods=['GET'])
def getSubredditSubmissions(subr):
    err = Error()
    rank_by = request.args.get('rank_by', 'hot')
    results_limit = request.args.get('limit', '10')
    response_object = {}
    articles = []
    try:
        subreddit_found = reddit_inst.subreddit(subr)
        response_object['subreddit_name'] = subr
        response_object['subreddit_title'] = subreddit_found.title
    except Exception:
        return err.make_error(202, "0 results found for given subreddit", "change subreddit to something else")
    
    try:
        results_limit = int(results_limit)
    except Exception:
        return err.make_error(400, "invalid limit query param", "limit is a number try again!")
    
    listing = None
    if rank_by == 'hot':
        listing = subreddit_found.hot(limit=results_limit)
    elif rank_by == 'new':
        listing = subreddit_found.new(limit=results_limit)
    elif rank_by == 'top':
        listing = subreddit_found.top(limit=results_limit)
    elif rank_by == 'rising':
        listing = subreddit_found.rising(limit=results_limit)
    else:
        return err.make_error(400, "invalid rank query param", "rank is hot/new/rising/top only try again!")

    for submission in listing:
        story = {}
        story['title'] = submission.title
        story['score'] = submission.score
        story['link'] = submission.url
        articles.append(story)

    if len(articles) < 1:
        return err.make_error(202, "0 results found for given ranking type", "change rank type to something else")
    
    response_object['results_limit'] = str(results_limit)
    response_object['ranking_method'] = rank_by
    response_object['stories'] = articles

    http_response = jsonify(response_object)
    http_response.status_code = 200
    return http_response

if __name__ == '__main__':
    reddapp.run(debug=True)