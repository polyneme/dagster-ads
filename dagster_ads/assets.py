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
    output = BytesIO()
    count = 0
    cursor = ads.find(q="""*:*""", fl=ADS_FIELDS, rows=2000, max_pages=10_000)

    @retry(
        retry=retry_if_exception_type(APIResponseError),
        wait=wait_random_exponential(multiplier=1, max=60),
    )
    def fetch_pages():
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
                    Key="ads/ads_records.ndjson.gz",
                    Body=gzip.compress(output.getvalue()),
                    ACL="public-read",
                    Metadata={"x-n-records": f"{i}"},
                )

    fetch_pages()
    s3.get_client().put_object(
        Bucket="polyneme",
        Key="ads/ads_records.ndjson.gz",
        Body=gzip.compress(output.getvalue()),
        ACL="public-read",
        Metadata={"x-n-records": "all"},
    )
    return Output(
        value=gzip.compress(output.getvalue()),
        metadata={
            "path": MetadataValue.url(
                "https://files.polyneme.xyz/ads/ads_records.ndjson.gz"
            )
        },
    )


assets = load_assets_from_current_module(
    group_name="ads",
)
