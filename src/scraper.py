from bootstrap import bootstrap
from comments import fetch_comments


def scrape(article_url):
    bootstrap_data = bootstrap(article_url)

    print(
        f'Scraping {bootstrap_data.get("num_replies", 0)} comments from article "{bootstrap_data.get("page_title", "")}"')

    page_id = bootstrap_data.get('page_id')
    params = {
        'section': bootstrap_data.get('section', ''),
    }

    comments = fetch_comment_pages(page_id, params)
    print('Comments', len(comments))


def fetch_comment_pages(page_id, params):
    fetch_next_comment_page = make_comment_page_fetcher(page_id, params)
    return fetch_all(fetch_next_comment_page)


def make_comment_page_fetcher(page_id, params):
    def fetch_next(after_id):
        return fetch_comments(page_id, params, after_id)

    return fetch_next


def fetch_all(fetch_next):
    result = []
    after_id = ''

    while True:
        data = fetch_next(after_id)

        items = data.get('results', [])
        result += items

        after_count = data.get('after_count', 0)

        if after_count > 0:
            after_id = items[-1]['id']
        else:
            return result


scrape('https://www.cbc.ca/news/health/organ-donation-presumed-consent-1.5083422')
