import requests

bootstrap_url = 'https://api.viafoura.co/v2/www.cbc.ca/bootstrap'


def bootstrap(article_url):
    response = post_bootstrap(article_url)

    result = response['result']
    page = result['page']
    section_tree = result['sectionTree']
    section_id = page['section_id']

    section = extract_section(section_tree, section_id)

    return {
        "section": section,
        "page_id": page["id"],
        "page_title": page["title"],
        "url": article_url,
        "num_replies": page['num_replies']
    }


def post_bootstrap(article_url):
    payload = build_payload(article_url)
    http_response = requests.post(bootstrap_url, json=payload)
    return http_response.json()


def build_payload(article_url):
    return {
        "section":"",
        "meta": {
            "title":"CBC.ca",
            "url": article_url,
            "page_type":"website",
            "owners": []
        }
    }


def extract_section(section_tree, required_section_id):
    for section, section_id in section_tree['descendants'].items():
        if required_section_id == section_id:
            return section

    return ''
