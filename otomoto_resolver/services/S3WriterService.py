import os
from cs_ai_common.s3.resolver_results import write_result_to_s3
from otomoto_resolver.services.ResultWriterService import ResultWriterService
from cs_ai_common.resolver_cache.s3_cache_utils import save_cache_result
from cs_ai_common.s3.utils import get_bucket_name_from_arn


class S3WriterService(ResultWriterService): 
    def write_result(self, content: dict, key: str) -> None:
        write_result_to_s3(content, key)
    
    def write_cache(self, content: dict, key: str) -> None:
        bucket_name = get_bucket_name_from_arn(os.getenv("CACHE_BUCKET_NAME", None))
        save_cache_result(key, "otomoto", content, bucket_name)