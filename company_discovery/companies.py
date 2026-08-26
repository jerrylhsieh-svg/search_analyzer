import requests
import json
from urllib.parse import urlparse

COLLINFO = "https://index.commoncrawl.org/collinfo.json"


def get_latest_index():
    crawls = requests.get(COLLINFO, timeout=30).json()
    print(crawls)
    return [crawls[0]["cdx-api"]]

def get_all_indexes():
    crawls = requests.get(COLLINFO, timeout=30).json()
    return [index["cdx-api"] for index in crawls]


def get_lever_urls(index_urls):
    response_lines = []
    for index_url in index_urls:
        response = requests.get(
            index_url,
            params={
                "url": "jobs.lever.co/*",
                "output": "json",
                "filter": "status:200",
            },
            timeout=60,
        )
        response.raise_for_status()
        response_lines.extend(response.text.splitlines())

    return [json.loads(line)["url"] for line in response_lines]


def extract_company(url):
    path = urlparse(url).path.strip("/")

    if not path:
        return None

    return path.split("/")[0]

urls = get_lever_urls(get_latest_index())

companies = sorted(
    {
        company
        for url in urls
        if (company := extract_company(url))
    }
)

print(f"Found {len(companies)} Lever slugs")

for company in companies[:20]:
    print(company)

