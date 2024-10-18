from otomoto_resolver.api_scraper.startup_scraper import startup_api_scraper
from otomoto_resolver.scraper.start_up_scraper import startup_scraper
from cs_ai_common.seed_data.lambda_event_seed_data_resolver import LambdaEventSeedDataResolver
from requests.exceptions import ProxyError
from cs_ai_common.startup.startup import startup_app
from cs_ai_common.services.s3_result_writer_service import S3WriterService

def handler(event: dict, context):
    seed_data_provider = LambdaEventSeedDataResolver(event)
    result_writer_service = S3WriterService()
    return startup_app(
        lambda: startup_api_scraper(seed_data_provider, result_writer_service),
        retry_on=ProxyError,
        retries=3,
        raw_event=event
    )