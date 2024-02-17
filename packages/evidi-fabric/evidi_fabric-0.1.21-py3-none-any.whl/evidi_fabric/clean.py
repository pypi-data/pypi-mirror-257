from pyspark.sql import DataFrame, functions as f
from evidi_fabric.fs import get_table_path, resolve_workspace_name, resolve_lakehouse_name

try:
    spark
except NameError:
    from evidi_fabric.spark import get_or_create_spark
    spark = get_or_create_spark()


def clean_df(df:DataFrame, table_name:str, config:dict, lakehouse:str=None, workspace:str=None) -> DataFrame:
    df = df.dropDuplicates()
    df = add_currency_converted_cols(df=df, 
                                     table_name=table_name, 
                                     config=config, 
                                     lakehouse=lakehouse, 
                                     workspace=workspace)    
    return df

def add_currency_converted_cols(df:DataFrame, table_name:dict[str,str], config:dict, lakehouse:str=None, workspace:str=None) -> DataFrame:
    """
    Adds three column to the existing dataframe for each col_name in the "convert_currency_cols" element of the CONFIG_SILVER

    Input:
        df: DataFrame
        directory_info: {"directory": <table_name>,
                         "path": <absolute path to table>}

    Output:
        df: The same dataframe, but with added columns, for each of the above mentioned element:

        Added columns:
            f"{col_name}__Rate": Conversion rate
            f"{col_name}__CONV": The converted price
            f"{col_name}__CONV_ERR": 1 if the price could not be converted. Zero otherwise
    """
    if workspace == None:
        workspace = resolve_workspace_name()
    if lakehouse == None:
        lakehouse = resolve_lakehouse_name()

    df_merged=df
    if table_name in config.keys():
        config_table=config[table_name]
        if "convert_currency" in config_table:
            config_currency=config_table["convert_currency"]
            currency_table_name=config_currency["depends_on"]
            currency_table_path=get_table_path(currency_table_name, lakehouse)
            df_currency=spark.read.load(currency_table_path)
            for convert_currency_col_info in config_currency["convert_currency_cols"]:
                date_col:str=convert_currency_col_info["date_col"]
                col_name:str=convert_currency_col_info["col"]
                if "dataareaid_col" in convert_currency_col_info.keys():
                    dataareaid_col=convert_currency_col_info["dataareaid_col"]
                    join_clause:tuple=(f.col(f"df.{date_col}") == df_currency.Date)&\
                                      (f.upper(f.col(f"df.{dataareaid_col}")) == df_currency.DataAreaId)
                elif "currency_col" in convert_currency_col_info.keys():
                    currency_col=convert_currency_col_info["currency_col"]
                    join_clause:tuple=(f.col(f"df.{date_col}").cast("date") == df_currency.Date)&\
                                      (f.upper(f.col(f"df.{currency_col}")) == f.upper(df_currency.CurrencyCode))
                #TODO: join_clause must be wrong, but is as Flemming defined it
                #join_clause:tuple=(datetime(2024,1,1) == df_currency.Date)&(f.upper(df_merged.DATAAREAID) == df_currency.DataAreaId)
                df_merged=df_merged.alias("df") \
                            .join(df_currency.alias("currency"), join_clause, how="left") \
                            .select(f"df.*", f.col("currency.Rate") \
                                              .alias(f"{col_name}__RATE"))
                df_merged=df_merged.withColumn(f"{col_name}__CONV", f.col(col_name) * f.col(f"{col_name}__Rate"))
                df_merged=df_merged.withColumn(f"{col_name}__CONV_ERR", f.when(f.col(f"{col_name}__CONV").isNull(),1) \
                                                                         .otherwise(0))
    return df_merged

if __name__ == "__main__":
    pass