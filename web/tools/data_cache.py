import pandas as pd
import os
from config import load_config
from web.tools.histories import merge_all_histories, pomofocus_to_df, superprod_to_df


def get_cached_histories():
    config = load_config()
    parquet_path = config["PARQUET_FILEPATH"]
    if os.path.exists(parquet_path):
        return pd.read_parquet(parquet_path)
    else:
        pomofocus_file = config["POMOFOCUS_FILEPATH"]
        pom_df = pomofocus_to_df(pomofocus_file)
        superprod_file = config["SUPERPROD_FILEPATH"]
        super_df = superprod_to_df(superprod_file)
        webprod_file = config["WEBPROD_FILEPATH"]
        web_df = superprod_to_df(webprod_file)
        all_df = merge_all_histories(pom_df, super_df, web_df)
        all_df.to_parquet(parquet_path)
        return all_df


if __name__ == "__main__":

    get_cached_histories()
