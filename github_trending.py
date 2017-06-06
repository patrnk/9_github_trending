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


if __name__ == '__main__':
    trending_repositories = get_trending_repositories(20)
    for repository in trending_repositories:
        repository['issues_count'] = get_open_issues_amount(repository['url'])
    for repository in trending_repositories:
        print_repository_with_issues(repository)
