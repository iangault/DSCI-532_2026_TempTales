# imports
from pathlib import Path

import ibis
from ibis import _

# Path Configurations
app_dir = Path(__file__).parent
data_path = app_dir / ".." / "data" / "processed"

# set up connection ibis w/ DuckDB
# Lazy reference only (data not really loaded yet)
con = ibis.duckdb.connect()
df_processed = con.read_parquet(data_path / "df_processed.parquet")

################### Pre-aggregate yearly w/ ibis expressions
df_yearly = (
    df_processed.group_by(["year", "country"])
    .aggregate(
        avg_temp=_.AvgTemp.mean(),
        avg_uncertainty=_.AvgUncertain.mean(),
        data_count=_.AvgTemp.count()
    )
    .mutate(
        temp_lower=_.avg_temp - _.avg_uncertainty,
        temp_upper=_.avg_temp + _.avg_uncertainty
    )
    .rename({"Country":"country"})
)

################### Pre-aggregate seasonal w/ ibis expressions
df_seasonal = (
    df_processed.group_by(["year", "country", "season"])
    .aggregate(AverageTemperature=_.AvgTemp.mean())
    .rename({"Country": "country"})
)


################### Pre-aggregate monthly w/ ibis expressions
df_monthly = (
    df_processed.group_by(["year", "country", "month"])
    .aggregate(AvgTemp=_.AvgTemp.mean())
    .rename({"Country": "country"})
)

################### Global UI Configurations
################### These needs immediately executed for shiny to set up for UI
country_choices = sorted(df_yearly.select("Country").distinct().execute()["Country"].tolist())
min_year = int(df_yearly.year.min().execute())
max_year = int(df_yearly.year.max().execute())
