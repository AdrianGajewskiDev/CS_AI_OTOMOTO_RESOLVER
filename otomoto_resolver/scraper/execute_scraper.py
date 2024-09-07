import json
import os

import requests
from otomoto_resolver.logging.logger import InternalLogger
from otomoto_resolver.resolver.otomoto_resolver import OtomotoResolver
from otomoto_resolver.s3.writer import write_result_to_s3
from bs4 import BeautifulSoup

OXYLABS_USERNAME = os.environ["OXYLABS_USERNAME"]
OXYLABS_PASSWORD = os.environ["OXYLABS_PASSWORD"]
OXYLABS_BASE_URL = os.environ["OXYLABS_BASE_URL"]

def execute_scraper(task_id: str, resolver: OtomotoResolver, seed_data: dict) -> dict:
    pages: list = []
    resolver.resolve_url(seed_data)
    InternalLogger.LogInfo("First resolved url: {}".format(resolver.get_resolved_url()))
    for it in range(0, resolver.get_strategy().Iterations):
        resolver.execute_strategy({"page_index": it + 1})
        resolved_url = resolver.get_resolved_url()
        payload = {
            "source": "universal",
            "url": resolved_url,
        }        
        InternalLogger.LogInfo(f"Resolved url: {resolved_url}")
        result = requests.post(url=OXYLABS_BASE_URL, data=json.dumps(payload), auth=(OXYLABS_USERNAME, OXYLABS_PASSWORD))
        result_json = result.json()
        results = result_json.get("results", [])
        if not results:
            continue
        html = results[0].get("content")
        body = extract_body_content(html)
        html_data = resolver.scrap_data_from_html(body)
        pages.extend(html_data)
    
    s3_content = {
        "task_id": task_id,
        "content": [json.dumps(page.json()) for page in pages if page]
    }

    return write_result_to_s3(s3_content, key="{}/{}/{}.json".format(task_id, "otomoto", "result"))

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""