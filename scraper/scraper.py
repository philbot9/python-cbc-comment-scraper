from bootstrap import bootstrap
from comments import fetch_comments
from thread import fetch_thread
from csv_result import export_csv_result


def scrape(article_url, output_filepath):
    print("Fetching details for " + article_url)

    bootstrap_data = bootstrap(article_url)

    print("Scraping " + str(bootstrap_data["num_replies"]) + " comments from article \"" + bootstrap_data["page_title"] + "\"")

    page_id = bootstrap_data.get('page_id')
    params = {
        'section': bootstrap_data.get('section', ''),
    }

    comments = fetch_comment_pages(page_id, params)
    comments_with_threads = fetch_comment_threads(comments, params)
    sorted_comments = sort_comments_by_date(comments_with_threads)

    export_csv_result(sorted_comments, output_filepath)

    print("Exported " + str(bootstrap_data["num_replies"]) + " comments to " + output_filepath)


def fetch_comment_pages(page_id, params):
    fetch_next_comment_page = make_comment_page_fetcher(page_id, params)
    return fetch_all(fetch_next_comment_page)


def make_comment_page_fetcher(page_id, params):
    def fetch_next(after_id):
        return fetch_comments(page_id, params, after_id)

    return fetch_next


def fetch_comment_threads(comments, params):
    comments_with_threads = []

    for comment in comments:
        if 'thread' in comment:
            thread = comment['thread']

            if thread['total_count'] > len(thread['results']):
                comment = fetch_full_thread(comment, params)
            else:
                comment['thread'] = sort_comments_by_date(thread['results'])

        comments_with_threads.append(comment)

    return comments_with_threads


def fetch_full_thread(comment, params):
    fetch_next_thread_page = make_thread_page_fetcher(comment['id'], params)
    thread_comments = fetch_all(fetch_next_thread_page)
    comment['thread'] = sort_comments_by_date(thread_comments)


def make_thread_page_fetcher(thread_id, params):
    def fetch_next(after_id):
        return fetch_thread(thread_id, params, after_id)

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


def sort_comments_by_date(comments):
    return sorted(comments, key=lambda x: x['date_created'], reverse=True)

