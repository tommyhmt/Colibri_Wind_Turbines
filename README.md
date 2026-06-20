# Colibri_Wind_Turbines

**Assumptions:**

New arriving files are for append only and will never require to overwrite previous records.

Files are dropped daily into the lake with a new folder named sensibly as shown below
<img width="1206" height="110" alt="image" src="https://github.com/user-attachments/assets/318b8fd2-fa0f-47f6-b955-5c30965b727f" />



**Architecture:**

Create Unity Catalog.

Use Lakeflow Spark Declarative Pipelines, in this case making use of its auto loader feature and data quality constraints.

Set up mount point so there's no need to change the storage explorer for different environments.

<img width="282" height="21" alt="image" src="https://github.com/user-attachments/assets/0f598f4c-3341-4c25-a01a-27af565a5b1c" />


**Solution:**

**Functions** folder contains 3 files:

**helper_functions.py** - apply_schema to apply schema definition defined in schema_definitions.py

**schema_definitions.py** - currently contains 2 schemas, one for silver and one for gold layer, can easily add in more for the future if required

**transform_functions.py** - create_missing_records because "the system is known to sometimes miss entries due to sensor malfunctions"

 add_anomaly based on business logic which is "defined as turbines whose output is outside of 2 standard deviations from the mean."

**Notebook** folder contains 1 file:

**WindTurbines.ipynb** - single notebook to process data in medallion architecture


Bronze table will only ever pick up new records

Silver and gold table should only ever add a new partition of data, i.e. old partitions of data remain untouched unless full table refresh is triggered.
<img width="1710" height="482" alt="image" src="https://github.com/user-attachments/assets/a2354e9a-3804-47f7-8aaa-23bff81e9412" />

Number of records for this dataset is as expected because there are 15 turbines and 31 days in March 2022, i.e. 15 * 31 = 465 in gold and 465 * 24 = 11,160 in bronze and silver.
