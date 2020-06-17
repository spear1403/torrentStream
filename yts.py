import json
import requests

def yts_search(query):
    b = []
    source=requests.get(f'https://yts.am/api/v2/list_movies.json?query_term={query}').text
    loaded_json= (json.loads(source))
    # print(loaded_json['status_message'])
    movie_data=(loaded_json['data'])
    try:
        movies=movie_data['movies']
        result=movies[0]
    except KeyError:
        return b
    # print(result['title_long'])
    available_torrents=result['torrents']
    for i in available_torrents:
        b.append([f"[YTS] {result['title_long']} [{i['quality']}]",i['url'],i['size'],i['seeds'],i['peers']])
    return b