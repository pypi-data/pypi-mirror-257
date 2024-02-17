from evidi_fabric.sql import find_all_tables_in_sql

def extract_depends_on(table_infos, source_table_names:list[str]):
    """
	Looks through the table_infos and returns a list of all tables that the table depends on
    and are in the source_table_names.

    This function is recursive and will look through all nested dictionaries.
	"""

    depends_on_list = []
    if "depends_on" in table_infos:
        depends_on = table_infos["depends_on"]
        if isinstance(depends_on, list):
            for item in depends_on:
                if isinstance(item, dict) and "table" in item:
                    if item["table"] in source_table_names:
                        depends_on_list.append(item["table"])
                if isinstance(item, dict) and "table_sql" in item:
                    tables = find_all_tables_in_sql(sql_query=item["table_sql"])
                    tables = [table for table in tables if table in source_table_names]
                    depends_on_list.extend(tables)
                elif isinstance(item, str):
                    if item in source_table_names:
                        depends_on_list.append(item)
        elif isinstance(depends_on, str):
            if depends_on in source_table_names:
                depends_on_list.append(depends_on)

    for _, value in table_infos.items():
        if isinstance(value, dict):
            depends_on_list.extend(extract_depends_on(table_infos=value, 
                                                      source_table_names=source_table_names))

    return depends_on_list


def get_dependencies(config, source_table_names:list[str]) -> dict[str, list[str]]:
    """
    Returns a dictionary of all dependencies for each table in the config 
    where the dependencies are in the source_table_names.
    """
    relevant_dependencies = {}
    for table_name, table_infos in config.items():
        depends_on_list = extract_depends_on(table_infos=table_infos, 
                                             source_table_names=source_table_names)
        if depends_on_list:
            relevant_dependencies[table_name] = depends_on_list
    return relevant_dependencies

def _get_DAG_from_dependencies(silver_tables_with_new_data:list, 
                               silver_dependencies:dict[str,list[str]], 
                               gold_dependencies:dict[str,list[str]], 
                               max_concurrency:int=20,
                               timeout_in_secs:int=3600) -> dict:
    """
    Returns a Directed Acyclic Graph (DAG) from the silver and gold dependencies.

    First, silver tables that depends on other silver tables, e.g. currency tables, are added to the DAG.
    Then, the remaining silver tables added to the DAG, with there eventual dependencies.
    Finally, the gold tables are added to the DAG, with there eventual dependencies.

    Args:
        silver_tables_with_new_data (list): List of silver tables with new data.
        silver_dependencies (dict): Dictionary mapping silver tables to their dependencies.
        gold_dependencies (dict): Dictionary mapping gold tables to their dependencies.
        max_concurrency (int, optional): Maximum number of concurrent activities in the DAG. Defaults to 20.
        timeout_in_secs (int, optional): Timeout for the entire pipeline, in seconds. Defaults to 3600.

    """

    # Convert to DAG
    DAG = {"activities": []}

    # Add dependent silver activities to DAG
    silver_dependencies_tables=list(set([dependency for dependencies in silver_dependencies.values() for dependency in dependencies]))
    for dependency in silver_dependencies_tables:
        activity = {
            "name": dependency,
            "path": "STD",
            "args": {"tables":dependency, "useRootDefaultLakehouse": True},
            
        }
        DAG["activities"].append(activity)

    # Add remaining silver activities to DAG
    silver_tables_with_new_data = [table for table in silver_tables_with_new_data if table not in silver_dependencies_tables]
    for table in silver_tables_with_new_data:
        if table in silver_dependencies.keys():
            dependencies = silver_dependencies[table]
        else:
            dependencies = []
        activity = {
            "name": table,
            "path": "STD__FO_A",
            "args": {"tables":table, "useRootDefaultLakehouse": True},
            "dependencies": dependencies,
        }
        DAG["activities"].append(activity)

    # Add gold activities to DAG
    for table, dependency in gold_dependencies.items():
        activity = {
            "name": table,
            "path": "TRANS",  
            "args": {"destination_table_name":table, "useRootDefaultLakehouse": True},
            "dependencies": dependency, 
        }
        DAG["activities"].append(activity)
        DAG["concurrency"] = max_concurrency # max 5 notebooks in parallel
        #see more: https://www.linkedin.com/pulse/micosoft-fabric-run-multiple-notebooks-parallel-dependencies-uerrc/?trk=organization_guest_main-feed-card_feed-article-content
        DAG["timeoutInSeconds"] = timeout_in_secs, # max 1 hour for the entire pipeline
    return DAG


def get_DAG(config_silver:dict[str,list[str]], 
            config_gold:dict[str,list[str]], 
            tables:list[str],
            max_concurrency:int=20,
            timeout_in_secs:int=3600) -> dict:
    """
    From a list of tables and config files that entails dependency infos, retrieve a DAG
    """
    silver_dependencies = get_dependencies(config=config_silver, 
                                           source_table_names=tables)
    
    silver_tables_with_new_data=list(set(list(silver_dependencies.keys())+tables))

    gold_dependencies = get_dependencies(config=config_gold, 
                                         source_table_names=silver_tables_with_new_data)
    
    DAG = _get_DAG_from_dependencies(silver_tables_with_new_data=silver_tables_with_new_data, 
                                     silver_dependencies=silver_dependencies, 
                                     gold_dependencies=gold_dependencies, 
                                     max_concurrency=max_concurrency, 
                                     timeout_in_secs=timeout_in_secs)
    return DAG


if __name__=="__main__":
    import json
    config_silver = {}
    config_gold = {"DimCompany":
	{
		"load_type": "FULL",
		 "primary_keys" : [
			"CompanyKey"
		 ],
		 "companies":{
			"A":{
			 "depends_on": [
				{
					"table": "FO_A__DATAAREA"
				}
			 ],
			 "columns": [
				"LOWER(CONCAT('A#',FO_A__DATAAREA.ID)) AS CompanyKey",
				"CONCAT(FO_A__DATAAREA.ID, ' - ', FO_A__DATAAREA.NAME) AS Company",
				"FO_A__DATAAREA.ID AS CompanyId",
				"FO_A__DATAAREA.NAME AS CompanyName",
			  ],
			 "where_clause":"FO_A__DATAAREA.PARTITION=5637144576",
			}
		}
	}}
    tables = ["FO_A__DATAAREA"]
    DAG = get_DAG(config_silver, config_gold, tables)
    print(json.dumps(DAG, indent=2))
    