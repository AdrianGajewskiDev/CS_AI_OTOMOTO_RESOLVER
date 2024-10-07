from otomoto_resolver.api_scraper.startup_scraper import startup_api_scraper
from otomoto_resolver.scraper.start_up_scraper import startup_scraper
from otomoto_resolver.seed_data_resolvers.lambda_event_seed_data_resolver import LambdaEventSeedDataResolver
from otomoto_resolver.services.S3WriterService import S3WriterService
from otomoto_resolver.startup.app_startup import startup_app
from requests.exceptions import ProxyError

def handler(event: dict, context):
    seed_data_provider = LambdaEventSeedDataResolver(event)
    result_writer_service = S3WriterService()
    return startup_app(
        lambda: startup_api_scraper(seed_data_provider, result_writer_service),
        retry_on=ProxyError,
        retries=3,
        raw_event=event
    )