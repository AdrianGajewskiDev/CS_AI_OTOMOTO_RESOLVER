from concurrent.futures import ThreadPoolExecutor
from otomoto_resolver.helpers.request_body import build_request_body
from otomoto_resolver.logging.logger import InternalLogger
from otomoto_resolver.resolver.otomoto_api_resolver import OtomotoApiResolver

PAGE_SIZE = 32

def execute_api_scraper(resolver: OtomotoApiResolver, seed_data: dict):
    InternalLogger.LogDebug("Sending reconnaissance request to otomoto api.")
    body = build_request_body(seed_data)
    rec_data = resolver.send_reconnaissance_request(body)
    total_count = rec_data["data"]["advertSearch"]["totalCount"]
    pages = round(total_count / PAGE_SIZE)
    bodies = [build_request_body(seed_data, page) for page in range(1, pages)]

    InternalLogger.LogDebug("Scraping data from otomoto api.")
    InternalLogger.LogDebug(f"Total pages: {pages}")

    with ThreadPoolExecutor() as executor:
        responses = executor.map(resolver.send, bodies)
    
    return responses


    