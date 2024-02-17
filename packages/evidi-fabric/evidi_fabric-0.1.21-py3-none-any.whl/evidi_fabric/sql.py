import re
from uuid import UUID
from evidi_fabric.fs import get_table_path

try:
    spark
except NameError:
    from evidi_fabric.spark import get_or_create_spark
    spark = get_or_create_spark()


def find_all_tables_in_sql(sql_query:str) -> list[str]:
    """
    From any sql_query, returns a list of all dependent tables.
    
    e.g. 
    sql_query="SELECT * FROM A" -> ["A"]
    sql_query="WITH CTE (SELECT * FROM A)\n SELECT * FROM CTE" -> ["A","CTE"]
    sql_query="WITH CTE (SELECT * FROM A)\n SELECT * FROM CTE INNER JOIN B ON A.key = B.key" -> ["A","CTE","B"]
    
    """
    pattern = re.compile(r'\b(?:FROM|JOIN)\s+([a-zA-Z_]\w*)\b', re.IGNORECASE)
    matches = pattern.findall(sql_query)
    return matches

def create_sql_views_from_sql(table_sql:str, lakehouse:str | UUID | None = None) -> None:
    """
    When reading a table from an sql query, i.e. spark.sql(table_sql), 
    you cannot reference the absolute path to the source.

    To overcome this, this function 
    1) finds all source tables used in the sql_query,
    2) finds their absolute paths
    3) create a temporary view of the data

    This view can then be accessed from sql, but refere to the table name 
    without specifying the schema

    Example:
        table_sql = "SELECT sales_amount FROM transactions"
        lakehouse = "Decide_DK_Silver"

    then a view is created called transactions, 
    so that spark.sql(table_sql) can be executed pointing to the 
    absolute path of transactions
    """
    table_names=find_all_tables_in_sql(table_sql)
    for table_name in table_names:
        table_path=get_table_path(table_name=table_name, lakehouse=lakehouse)
        df_temp=spark.read.load(table_path)
        df_temp.createOrReplaceTempView(table_name)

def add_default_where_clause(config:dict) -> dict:
    """
    In the silver layer every destination table and its corresponding company
    must have a where clause. In case that it is 
    1) not set or
    2) set to None or
    3) set to empty string
    
    then it is replaced with 1=1.
    """
    for destination_table in config.keys():
        for company in config[destination_table]["companies"].keys():
            if config[destination_table]["companies"][company].get("where_clause") in [None, ""]:
                config[destination_table]["companies"][company]["where_clause"]="1=1"
    return config


def get_table_name_and_alias(table_name_raw:str) -> tuple[str, str]:
    """
    Retrieves the table name from the table name string and the alias if exists.
    If alias is not set, then the table name is used as the alias.

    Examples:
        - 'A__CUSTABLE' -> ('A__CUSTABLE', 'A__CUSTABLE')
        - 'A__CUSTABLE as A' -> ('A__CUSTABLE', 'A')
        - 'A__CUSTABLE AS   B ' -> ('A__CUSTABLE', 'B')
    """
    table_name_raw=table_name_raw.strip()

    if " as " in table_name_raw.lower():
        table_name_raw=re.sub(" +", " ", table_name_raw)
        index=table_name_raw.lower().find(" as ")
        table_name=table_name_raw[:index]
        table_alias=table_name_raw[index+4:]
    
    else:
        table_name=table_name_raw
        table_alias=table_name_raw
    return table_name, table_alias

if __name__=="__main__":
    table_sql = "WITH CTE (SELECT * FROM A)\n SELECT * FROM CTE INNER JOIN B ON A.key"
    tables = find_all_tables_in_sql(table_sql)
    print(tables)

    table_sql = "SELECT sales_amount FROM transactions"
    lakehouse = "Decide_DK_Silver"
    create_sql_views_from_sql(lakehouse, table_sql)

    