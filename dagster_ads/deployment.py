from dagster import Definitions, define_asset_job, ScheduleDefinition
from dagster_aws.s3 import S3Resource

from dagster_ads.assets import ads_records
from dagster_ads.config import (
    ADS_CONFIG_TOKEN,
    AWS_REGION_NAME,
    AWS_ENDPOINT_URL,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
)
from dagster_ads.resources import (
    ADSSearchQueryResource,
    DO_S3_Resource,
    ADS_S3_ConfigurableIOManager,
)

configured_s3_resource = DO_S3_Resource(
    region_name=AWS_REGION_NAME,
    endpoint_url=AWS_ENDPOINT_URL,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

ads_records_job = define_asset_job("ads_records_job", selection=[ads_records])
ads_records_schedule = ScheduleDefinition(
    job=ads_records_job,
    cron_schedule="0 0 * * 4,0",
    execution_timezone="America/New_York",
)

defs = Definitions(
    assets=[ads_records],
    resources={
        "ads": ADSSearchQueryResource(config_token=ADS_CONFIG_TOKEN),
        "s3": configured_s3_resource,
        "ads_s3_io_manager": ADS_S3_ConfigurableIOManager(
            s3_resource=configured_s3_resource, s3_bucket="polyneme"
        ),
    },
    schedules=[ads_records_schedule],
)
