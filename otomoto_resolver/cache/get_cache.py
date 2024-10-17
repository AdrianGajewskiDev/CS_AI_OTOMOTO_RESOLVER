import os
from cs_ai_common.resolver_cache.cache_key import build_cache_key
from cs_ai_common.resolver_cache.s3_cache_utils import try_get_cached_result
from cs_ai_common.s3.utils import get_bucket_name_from_arn

def try_get_cache(seed_data: dict) -> tuple:
    make, model, production_year = seed_data["Make"], seed_data["Model"], seed_data["ProductionYear"]
    cache_key = build_cache_key(make, model, production_year)
    bucket_name = get_bucket_name_from_arn(os.getenv("CACHE_BUCKET_NAME", None))
    return cache_key, try_get_cached_result(cache_key, "otomoto", bucket_name)