import pandas as pd
import sempy.fabric as fabric
from pyspark.sql.session import SparkSession
from uuid import UUID

from evidi_fabric.spark import get_or_create_spark

def _is_valid_uuid(val):
    try:
        UUID(str(val))
        return True
    except ValueError:
        return False
    
def get_tables_from_files_or_folders(files_or_folders:list[str]):
    """
    Either all files from bronze is passed from bronze til silver, or only a single file.
    This function will return a list of the table names
    """
    return [get_table_from_file_or_folder(file_or_folder) for file_or_folder in files_or_folders]

def get_table_from_file_or_folder(file_or_folder:str):
    """
    Either all files from bronze is passed from bronze til silver, or only a single file.
    This function will return the table name, by assuming the name of the silver table is 
    the name of the folder where the file is located. 
    
    This function looks after a "." in the file_or_folder string. If there is a dot, then
    it must be a full path if it's not, then its assumed to point to th

    E.g. 
        file_or_folder='table_name/20240101_filname.parquet' -> 'table_name'
        file_or_folder='table_name' -> 'table_name'
        file_or_folder='parent_folder/table_name' -> 'table_name'
        file_or_folder='filename.parquet' -> ValueError #Path must be specified

    """
    if "." in file_or_folder:
        if "/" in file_or_folder:
            return file_or_folder.split("/")[-2]
        else:
            raise ValueError("At least the relative path must be specified")
    else:
        if "/" in file_or_folder:
            return file_or_folder.split("/")[-1]
        else:
            return file_or_folder

def get_file_path(directory:str=None, lakehouse:str | UUID | None = None, workspace:str | UUID | None = None) -> str:
    """
    Retrieves a fully qualified file path.
    Note: 

    Params:
     - workspace: Name or id of workspace (e.g. Decide_DK_DEV, 7dae828c-f98e-4e08-aaae-d93b2774c74b, None)
        * If not provided, the current workspace is used
     - lakehouse: Name or id of the lakehouse (e.g. Decide_DK_Silver, 9be79118-d950-4662-8053-b393d021ab0f, None)
        * If not provided, the current lakehouse is used
     - directory: Name of the directory (e.g. Bronze)

    Output:
     - path (e.g. abfss://Decide_DK_DEV@onelake.dfs.fabric.microsoft.com/Decide_DK_Silver.Lakehouse/Files/Bronze/)
    """
    workspace_name = resolve_workspace_name(workspace)
    lakehouse_name = resolve_lakehouse_name(lakehouse)
    return f"abfss://{workspace_name}@onelake.dfs.fabric.microsoft.com/{lakehouse_name}.Lakehouse/Files/{directory}"


def get_table_path(table_name:str, lakehouse:str | UUID | None = None, workspace:str | UUID | None = None) -> str:
    """
    Retrieves a fully qualified table path.

    Params:
     - table_name: Name of the table (e.g. A__CUSTGROUP)
     - workspace: Name or id of workspace (e.g. Decide_DK_DEV, 7dae828c-f98e-4e08-aaae-d93b2774c74b, None)
        * If not provided, the current workspace is used
     - lakehouse: Name or id of the lakehouse (e.g. Decide_DK_Silver, 9be79118-d950-4662-8053-b393d021ab0f, None)
        * If not provided, the current lakehouse is used

    Output:
     - path (e.g. abfss://Decide_DK_DEV@onelake.dfs.fabric.microsoft.com/Decide_DK_Silver.Lakehouse/Tables/A__CUSTGROUP/
    """
    workspace_name = resolve_workspace_name(workspace)
    lakehouse_name = resolve_lakehouse_name(lakehouse)
    
    return f"abfss://{workspace_name}@onelake.dfs.fabric.microsoft.com/{lakehouse_name}.Lakehouse/Tables/{table_name}" 

            
def get_lakehouse_from_path(path:str) -> str:
    """
    Retrieves the lakehouse name from a path.

    Example:
    path = "abfss://Decide_DK_DEV@onelake.dfs.fabric.microsoft.com/Decide_DK_Bronze.Lakehouse/Files/Bronze/"
    lakehouse = "Decide_DK_Bronze"
    """
    if "/Files" in path:
        lakehouse = path.split('onelake.dfs.fabric.microsoft.com/')[-1].split('/Files')[0].replace('.Lakehouse','')
    elif "/Tables" in path:
        lakehouse = path.split('onelake.dfs.fabric.microsoft.com/')[-1].split('/Tables')[0].replace('.Lakehouse','')
    else:
        raise ValueError("The path is not a valid lakehouse path.")
    return lakehouse

def resolve_workspace_id(workspace:str | UUID | None = None) -> UUID:
    """
    From the workspace, that can be either the name, guid or None, resolve the workspace id.
    If no workspace is provided, the current workspace is used.
    """
    if workspace == None:        
        workspace_id = fabric.get_workspace_id()
    elif _is_valid_uuid(workspace):
        workspace_id = workspace
    else:
        workspace_id = fabric.resolve_workspace_id(workspace)

    return workspace_id

def resolve_workspace_name(workspace:str | UUID | None = None) -> str:
    """
    From the workspace, that can be either the name, guid or None, retrieve the workspace name.
    If no workspace id provided, the current workspace is used.
    """
    if workspace == None:
        workspace_id = resolve_workspace_id()
        workspace_name = fabric.resolve_workspace_name(workspace_id)

    elif not _is_valid_uuid(workspace):
        workspace_name=workspace
    
    else:
        workspace_id = workspace
        workspace_name = fabric.resolve_workspace_name(workspace_id)
    
    return workspace_name


def resolve_lakehouse_id(lakehouse:str | UUID | None = None) -> UUID:
    """
    From the lakehouse name, that can be either the name, guid or None, retrieves the lakehouse id.
    If no lakehouse name is provided, the current lakehouse is used.
    """
    if lakehouse == None:
        lakehouse_id = fabric.get_lakehouse_id()

    elif _is_valid_uuid(lakehouse):
        lakehouse_id = lakehouse

    else:
        df_items = fabric.list_items("Lakehouse")
        df_items = df_items[df_items['Display Name'] == lakehouse]
        lakehouse_id = df_items['Id'].iloc[0]

    return lakehouse_id

def resolve_lakehouse_name(lakehouse:str | UUID | None = None) -> str:
    """
    From the lakehouse, that can be either the name, guid or None, retrieves the lakehouse name.
    If no lakehouse id is provided, the current lakehouse is used.
    """
    if lakehouse == None:
        lakehouse_id = resolve_lakehouse_id()
    elif not _is_valid_uuid(lakehouse):
        lakehouse_name=lakehouse
        return lakehouse_name
    else:
        lakehouse_id = lakehouse

    df_items = fabric.list_items("Lakehouse")
    df_items = df_items[df_items['Id'] == lakehouse_id]
    lakehouse_name = df_items['Display Name'].iloc[0]

    return lakehouse_name


def get_lakehouse_tables_info(spark:SparkSession = None, lakehouse:str | UUID | None = None, workspace:str | UUID | None = None) -> pd.DataFrame:
    """
    Retrieves the table names and related infos from the lakehouse.
    Note: the faster method is to use the sempy API. However, due to a presumably temporary 
          pagination error, it is limited to 100 tables.
          If the number of tables equals to exactly 100, the method falls back to the spark API.
          This code should be modified (by removing the first part of the if condition) once the issue is resolved.

    If workspace_id is not provided, the current workspace is used
    If lakehouse_id is not provided, the current lakehouse is used
    """

    workspace_id = resolve_workspace_id(workspace)
    workspace_name = resolve_workspace_name(workspace)
    lakehouse_id = resolve_lakehouse_id(lakehouse)
    lakehouse_name = resolve_lakehouse_name(lakehouse)

    client = fabric.FabricRestClient()
    response = client.get(f"/v1/workspaces/{workspace_id}/lakehouses/{lakehouse_id}/tables")
    table_list = response.json()['data']
    if len(table_list)==100:
        warn_msg="Warning: The sempy API is truncated to show 100 tables."
        warn_msg+="\nFailing back to the spark API to retrieve all tables."
        warn_msg+="\nThis method is significantly slower."
        print(warn_msg)
        if not spark:
            spark = get_or_create_spark()
        tables = spark.catalog.listTables()
        table_list_formatted = [{"Workspace Name": workspace_name, 
                                 "Workspace ID": workspace_id,
                                 "Lakehouse Name": lakehouse_name, 
                                 "Lakehouse ID": lakehouse_id,
                                 "Table Name": table.name, 
                                 "Type":table.tableType, 
                                 "Location":None, 
                                 "Format":None, 
                                 "Is Temporary": table.isTemporary, 
                                 "Description": table.description} for table in tables]
    else:
        table_list_formatted = [{"Workspace Name": workspace_name, 
                                 "Workspace ID": workspace_id,
                                 "Lakehouse Name": lakehouse_name, 
                                 "Lakehouse ID": lakehouse_id,
                                 "Table Name": table['name'], 
                                 "Type": table['type'], 
                                 "Location": table['location'], 
                                 "Format": table['format'],
                                 "Is Temporary": None, 
                                 "Description": None} for table in table_list]
        
    return pd.DataFrame(table_list_formatted)

if __name__ == "__main__":
    path="abfss://Decide_DK_DEV@onelake.dfs.fabric.microsoft.com/Decide_DK_Bronze.Lakehouse/Files/Bronze/"
    workspace="DEV"
    resolve_workspace_name(None)
    lakehouse=get_lakehouse_from_path(path)
    file_path=get_file_path(workspace=workspace, 
                            lakehouse=lakehouse, 
                            directory="FO_file1")

    print('Done')