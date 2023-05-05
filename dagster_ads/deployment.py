from dagster import Definitions
from dagster_ads.assets import assets
from dagster_ads.config import ADS_CONFIG_TOKEN
from dagster_ads.resources import ADSSearchQueryResource

defs = Definitions(
    assets=[*assets],
    resources={
        "ads": ADSSearchQueryResource(config_token=ADS_CONFIG_TOKEN),
    },
)
