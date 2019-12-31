import json
import sys
from urllib.parse import urlencode

import requests

REPOSITORY_SEARCH_URL = "https://api.github.com/search/repositories?q="
TOPIC_SEARCH_URL = "https://api.github.com/search/topics?q="
USER_SEARCH_URL = "https://api.github.com/search/users?q="
USER_REPOSITORIES_URL = "https://api.github.com/users/"

HEADERS = {"Accept": "application/vnd.github.v3+json"}
TOPIC_HEADERS = {"Accept": "application/vnd.github.mercy-preview+json"}


def search(query, repos):
    """ Query the api and show the results """
    query = '+'.join(query.split())
    data = requests.get(REPOSITORY_SEARCH_URL + query).json()
    repolist = [repo['full_name'] for repo in data['items']]
    repos.set_repos(repolist)


def fetch_url(url, query):
    params = urlencode({'q': query})
    final = url.format(params)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))
    response = opener.open(final).read().decode('utf-8')
    dict_response = json.loads(response)
    return dict_response


def get_repo(query):
    base_url = 'https://api.github.com/search/repositories?{}&per_page=50'
    res = fetch_url(base_url, query)
    resp = []
    for item in res['items']:
        resp.append((item['html_url'], item['description']))
    return resp


def get_user(query):
    base_url = 'https://api.github.com/search/users?{}&per_page=50'
    res = fetch_url(base_url, query)
    respo = []
    for item in res['items']:
        respo.append((item['login'], item['html_url']))
    return respo


def print_results(results):
    print("****** Query returned : ******")
    for item in results:
        print(PURPLE, '-->', item[0], NO_COLOUR)
        print('    --', item[1])


def search_user(url, headers=HEADERS):
    result = requests.get(url, headers=headers)
    print(f"Searching URL: {url}")
    if result.ok:
        repo_info = result.json()
        for item in repo_info:
            for k, v in item.items():
                print(f"{k} => {v}")


def search_github(url, headers=HEADERS):
    result = requests.get(url, headers=headers)
    print(f"Searching URL: {url}")
    if result.ok:
        repo_info = result.json()
        if isinstance(repo_info, dict):
            print_item({'total': repo_info['total_count']})
            print_item({'incomplete_results': repo_info['incomplete_results']})
            with repo_info['items'] as r_items:
                for item in r_items:
                    print_keeper(item)
        elif isinstance(repo_info, list):
            with repo_info as r_items:
                for item in r_items:
                    print_keeper(item)
        else:
            print("No result found!")
    else:
        print(result.raise_for_status())


def print_keeper(stuff):
    keeper = INTERESTED_ITEMS
    print("=" * 20)
    for k, v in stuff.items():
        if k in keeper.keys() and not (k == 'size' == '0'):
            print(f"{k} => {v}")


def print_item(item):
    for k, v in item.items():
        print(f"{k} => {v}")


def process_query_url(url, query, sort, order, count):
    if not url or not query:
        msg = f"You must provide both the URL and a QUERY!\n{USAGE_FIND}"
        raise print(msg)
    url = f"{url}{query}&per_page={count}"
    if sort and order:
        url = f"{url}&{sort}&{order}"
    elif sort:
        url = f"{url}&{sort}"
    elif order:
        url = f"{url}&{order}"
    return url


def find_repo(query, sort, order, count):
    url = process_query_url(REPOSITORY_SEARCH_URL, query, sort, order, count)
    print("Find repositories via various criteria (100 results per page max).")
    return search_github(url)


def find_topic(query, sort, order, count):
    url = process_query_url(TOPIC_SEARCH_URL, query, sort, order, count)
    headers = TOPIC_HEADERS
    print("Find topics via various criteria (100 results per page max).")
    return search_github(url, headers=headers)


def find_user(query, sort, order, count):
    url = process_query_url(USER_SEARCH_URL, query, sort, order, count)
    print("Find users via various criteria (100 results per page max).")
    return search_github(url)


def gh_list(username, sort, count):
    url = USER_REPOSITORIES_URL
    print("List public repositories for the specified user.")
    url = f"{url}{username}/repos?per_page={count}"
    if sort:
        url = f"{url}?{sort}"
    return search_github(url)


def get_limit(args):
    pass


def main():
    rep = ['-r', '--repo', '--repository', ]
    usr_kw = ['-u', '--user', ]
    hlp = ['-h', '--help', '--please', '--what', ]
    lim = ['-l', '--limit', ]
    if len(sys.argv) == 1 or sys.argv[1].lower() in hlp:
        print(__doc__)

    elif sys.argv[1].lower() in rep:
        res = get_repo(sys.argv[2:])
        print_results(res)

    elif sys.argv[1].lower() in usr_kw:
        res = get_user(' '.join(sys.argv[2:]))
        print_results(res)

    elif sys.argv[1].lower() in lim:
        print(get_limit)
    else:
        print(__doc__)


if __name__ == '__main__':
    main()
