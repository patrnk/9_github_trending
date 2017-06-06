from datetime import date, timedelta

import requests


def get_week_ago_iso_date():
    week_ago = date.today() - timedelta(days=7)
    return week_ago.isoformat()


def get_trending_repositories(top_size):
    # For details, see https://developer.github.com/v3/search/#search-repositories
    # We're not fetching more than one page of results.
    repositories_per_page = 100
    if top_size > repositories_per_page:
        raise ValueError('top_size cannot be greater than {0}'.format(repositories_per_page))
    query = 'created:>={iso_datetime}'.format(iso_datetime=get_week_ago_iso_date())
    params = {
        'q': query,
        'sort': 'stars',
    }
    response = requests.get('https://api.github.com/search/repositories', params=params)
    return response.json()['items'][:top_size]


def get_open_issues_amount(repo_owner, repo_name):
    pass


def print_repository_with_issues(repository):
    pass


if __name__ == '__main__':
    trending_repositories = get_trending_repositories(20)
    print(trending_repositories)
