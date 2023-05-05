import csv
from io import StringIO

from dagster import load_assets_from_current_module, OpExecutionContext
from dagster import Output, asset

from dagster_ads.config import ADS_FIELDS
from dagster_ads.resources import ADSSearchQueryResource


@asset
def ads_records(context: OpExecutionContext, ads: ADSSearchQueryResource):
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=ADS_FIELDS)
    count = 0
    for record in ads.find(q="""*:*""", fl=ADS_FIELDS, rows=2000, max_pages=2):
        doc = dict(record.iteritems())
        context.log.info(f"{doc}")
        writer.writerow(doc)
        count += 1
    metadata = {
        "num_records": count,
    }
    return Output(value=output.getvalue(), metadata=metadata)


assets = load_assets_from_current_module(
    group_name="ads",
)
