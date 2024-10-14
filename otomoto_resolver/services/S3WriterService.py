from cs_ai_common.s3.resolver_results import write_result_to_s3
from otomoto_resolver.services.ResultWriterService import ResultWriterService


class S3WriterService(ResultWriterService): 
    def write_result(self, content: dict, key: str) -> None:
        write_result_to_s3(content, key)