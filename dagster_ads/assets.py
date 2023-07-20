import csv
from datetime import datetime
import gzip
import json
from io import BytesIO

from ads.exceptions import APIResponseError
from dagster import (
    OpExecutionContext,
    Output,
    asset,
    Config,
    StaticPartitionsDefinition,
)

from tenacity import wait_random_exponential, retry, retry_if_exception_type

from dagster_ads.config import ADS_FIELDS
from dagster_ads.resources import ADSSearchQueryResource, DO_S3_Resource


class ADSRecordsConfig(Config):
    query: str = 'doi:"10.*"'
    fields: list[str] = list(ADS_FIELDS)
    rows: int = 2000  # Max supported by ADS API
    sort: str = "score desc,id desc"
    max_pages: int = 10_000  # Max supported by ADS API


decades_partitions_def = StaticPartitionsDefinition(
    [f"{y}-{y+9}" for y in range(1500, 2030, 10)]
)


@asset(io_manager_key="ads_s3_io_manager", partitions_def=decades_partitions_def)
def ads_records(
    context: OpExecutionContext,
    config: ADSRecordsConfig,
    ads: ADSSearchQueryResource,
    s3: DO_S3_Resource,
):
    partition_decade_str = context.asset_partition_key_for_output()
    starting_hour: str = datetime.utcnow().isoformat().split(":")[0]
    page = {"number": 1}
    output = {"handle": BytesIO()}
    cursor = ads.find(
        q=f"{config.query} year:{partition_decade_str}",
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
                    Key=f"ads/records/{partition_decade_str}/{starting_hour}/page{page['number']:05}.ndjson.gz",
                    Body=gzip.compress(output["handle"].getvalue()),
                    ACL="public-read",
                )
                output["handle"] = BytesIO()
                page["number"] += 1

    fetch_pages()
    s3.get_client().put_object(
        Bucket="polyneme",
        Key=f"ads/records/{partition_decade_str}/{starting_hour}/page{page['number']:05}.ndjson.gz",
        Body=gzip.compress(output["handle"].getvalue()),
        ACL="public-read",
    )
    return Output(value="OK")
