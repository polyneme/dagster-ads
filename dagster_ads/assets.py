import csv
from datetime import datetime
import gzip
import json
from io import BytesIO

from ads.exceptions import APIResponseError
from dagster import load_assets_from_current_module, OpExecutionContext
from dagster import Output, asset, MetadataValue, Config
from tenacity import wait_random_exponential, retry, retry_if_exception_type

from dagster_ads.config import ADS_FIELDS
from dagster_ads.resources import ADSSearchQueryResource, DO_S3_Resource


class ADSRecordsConfig(Config):
    query: str = """*:*"""
    fields: list[str] = list(ADS_FIELDS)
    rows: int = 2000
    sort: str = "score desc,id desc"
    max_pages: int = 10_000  # 10_000 to get all of ADS as of 2023-05-10


@asset(io_manager_key="ads_s3_io_manager")
def ads_records(
    context: OpExecutionContext,
    config: ADSRecordsConfig,
    ads: ADSSearchQueryResource,
    s3: DO_S3_Resource,
):
    starting_hour: str = datetime.utcnow().isoformat().split(":")[0]
    page = {"number": 1}
    output = {"handle": None}
    cursor = ads.find(
        q=config.query,
        fl=config.fields,
        rows=config.rows,
        max_pages=config.max_pages,
    )

    @retry(
        retry=retry_if_exception_type(APIResponseError),
        wait=wait_random_exponential(multiplier=1, max=60),
    )
    def fetch_pages():
        output["handle"] = BytesIO()
        for i, record in enumerate(cursor):
            doc = dict(record.iteritems())
            output["handle"].write(f"{json.dumps(doc)}\n".encode(encoding="utf-8"))
            if i % config.rows == 0:
                numerator, denominator = cursor.progress.split("/")
                context.log.info(
                    f"{cursor.progress} {int(numerator)/int(denominator):.3%}"
                )
                s3.get_client().put_object(
                    Bucket="polyneme",
                    Key=f"ads/{starting_hour}/ads_records.page{page['number']:05}.ndjson.gz",
                    Body=gzip.compress(output["handle"].getvalue()),
                    ACL="public-read",
                )
                output["handle"] = BytesIO()
                page["number"] += 1

    fetch_pages()
    s3.get_client().put_object(
        Bucket="polyneme",
        Key=f"ads/{starting_hour}/ads_records.page{page['number']:05}.ndjson.gz",
        Body=gzip.compress(output["handle"].getvalue()),
        ACL="public-read",
    )
    return Output(value="OK")
