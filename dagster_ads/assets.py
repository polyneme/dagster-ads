import csv
import gzip
import json
from io import BytesIO

from ads.exceptions import APIResponseError
from dagster import load_assets_from_current_module, OpExecutionContext
from dagster import Output, asset, MetadataValue
from tenacity import wait_random_exponential, retry, retry_if_exception_type

from dagster_ads.config import ADS_FIELDS
from dagster_ads.resources import ADSSearchQueryResource, DO_S3_Resource


@asset(io_manager_key="ads_s3_io_manager")
def ads_records(
    context: OpExecutionContext, ads: ADSSearchQueryResource, s3: DO_S3_Resource
):
    page = {"number": 1}
    cursor = ads.find(q="""*:*""", fl=ADS_FIELDS, rows=2000, max_pages=10_000)

    @retry(
        retry=retry_if_exception_type(APIResponseError),
        wait=wait_random_exponential(multiplier=1, max=60),
    )
    def fetch_pages():
        output = BytesIO()
        for i, record in enumerate(cursor):
            doc = dict(record.iteritems())
            output.write(f"{json.dumps(doc)}\n".encode(encoding="utf-8"))
            if i % 2000 == 0:
                numerator, denominator = cursor.progress.split("/")
                context.log.info(
                    f"{cursor.progress} {int(numerator)/int(denominator):.3%}"
                )
                s3.get_client().put_object(
                    Bucket="polyneme",
                    Key=f"ads/ads_records.page{page['number']:05}.ndjson.gz",
                    Body=gzip.compress(output.getvalue()),
                    ACL="public-read",
                )
                output = BytesIO()
                page["number"] += 1

    fetch_pages()
    s3.get_client().put_object(
        Bucket="polyneme",
        Key=f"ads/ads_records.page{page['number']:05}.ndjson.gz",
        Body=gzip.compress(output.getvalue()),
        ACL="public-read",
    )
    return Output(value="OK")


assets = load_assets_from_current_module(
    group_name="ads",
)
