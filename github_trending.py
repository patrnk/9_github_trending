import sys
from datetime import date, timedelta
from argparse import ArgumentParser

import requests


def get_trending_repositories(top_size, starting_days_ago):
    # For details, see https://developer.github.com/v3/search/#search-repositories
    # We're not fetching more than one page of results.
    repositories_per_page = 100
    if top_size > repositories_per_page:
        raise ValueError('top_size cannot be greater than {0}'.format(repositories_per_page))
    starting_date = date.today() - timedelta(days=starting_days_ago)
    query = 'created:>={iso_datetime}'.format(iso_datetime=starting_date.isoformat())
    params = {
        'q': query,
        'sort': 'stars',
    }
    response = requests.get('https://api.github.com/search/repositories', params=params)
    return response.json()['items'][:top_size]


def get_open_issues_amount(repo_api_url):
    # For details, see https://developer.github.com/v3/issues/#list-issues-for-a-repository
    # repo_api_url looks like https://api.github.com/repos/:owner/:repo
    issues_url = '{0}/issues'.format(repo_api_url)
    return len(requests.get(issues_url).json())


def print_repository_with_issues(repository):
    output = '{stars_count}♥ {issues_count}(!) {url}'.format(
        stars_count=repository['stargazers_count'],
        issues_count=repository['issues_count'],
        url=repository['html_url']
    )
    print(output)


def parse_args(argv):
    parser = ArgumentParser()
    parser.add_argument('--top-size', type=int, default=20)
    parser.add_argument('--starting-days-ago', type=int, default=7)
    return parser.parse_args(argv)


if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    trending_repositories = get_trending_repositories(args.top_size, args.starting_days_ago)
    for repository in trending_repositories:
        repository['issues_count'] = get_open_issues_amount(repository['url'])
    for repository in trending_repositories:
        print_repository_with_issues(repository)
