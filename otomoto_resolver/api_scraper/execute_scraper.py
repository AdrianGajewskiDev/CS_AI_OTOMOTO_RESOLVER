from concurrent.futures import ThreadPoolExecutor
from otomoto_resolver.helpers.request_body import build_request_body
from otomoto_resolver.resolver.otomoto_api_resolver import OtomotoApiResolver
from cs_ai_common.logging.internal_logger import InternalLogger
from cs_ai_common.models.filters import Filter
PAGE_SIZE = 32

def execute_api_scraper(resolver: OtomotoApiResolver, seed_data: dict, filter: Filter) -> list:
    InternalLogger.LogDebug("Sending reconnaissance request to otomoto api.")
    InternalLogger.LogDebug(f"Filter data: {filter.__dict__}")
    body = build_request_body(seed_data, filter)
    rec_data = resolver.send_reconnaissance_request(body)
    total_count = rec_data["data"]["advertSearch"]["totalCount"]

    if total_count > 0 and total_count < PAGE_SIZE:
        pages = 1
    else:
        pages = round(total_count / PAGE_SIZE)
    bodies = [build_request_body(seed_data, filter, page) for page in range(pages)]

    InternalLogger.LogDebug("Scraping data from otomoto api.")
    InternalLogger.LogDebug(f"Total pages: {pages}")

    with ThreadPoolExecutor() as executor:
        responses = executor.map(resolver.send, bodies)
    
    return responses


    
