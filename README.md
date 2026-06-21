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

<img width="475" height="374" alt="image" src="https://github.com/user-attachments/assets/df66f2e6-8329-43c6-ba18-25884f8481ea" />


**Functions/helper_functions.py** - read_csv(path) to read csv file, with parameter set for location path of the file
<img width="568" height="256" alt="image" src="https://github.com/user-attachments/assets/4f0c8356-9526-45ae-bcd4-6584b838a955" />


**Functions/schema_definitions.py** - currently contains 2 schemas, one for silver and one for gold layer, so can easily add in more for the future if required.  Also added extra metadata "default" to fill null if required.
<img width="622" height="458" alt="image" src="https://github.com/user-attachments/assets/85cb9d45-b491-4055-a0c3-16c723e90f8c" />

**Functions/transform_functions.py** - create_missing_records(df) because "the system is known to sometimes miss entries due to sensor malfunctions"
<img width="1155" height="396" alt="image" src="https://github.com/user-attachments/assets/58968bd6-7222-4dd6-880b-6f330b825960" />

add_anomaly(df) based on business logic which is "defined as turbines whose output is outside of 2 standard deviations from the mean."
<img width="1157" height="423" alt="image" src="https://github.com/user-attachments/assets/d201c125-4ea7-4914-89bc-541f47353392" />

apply_schema(df, schema) because "The raw data contains missing values and outliers, which must be removed or imputed."
<img width="508" height="314" alt="image" src="https://github.com/user-attachments/assets/df12bcea-2469-4f2c-8717-b37b1e98afa6" />

**Notebook/WindTurbines.ipynb** - single notebook to process data in medallion architecture:

<img width="1097" height="276" alt="image" src="https://github.com/user-attachments/assets/de79e5f5-863f-4880-b9ed-53a175a92218" />
<img width="1101" height="419" alt="image" src="https://github.com/user-attachments/assets/06ae79e0-1d6b-402b-9bc9-e7c040ac73a8" />
<img width="1101" height="498" alt="image" src="https://github.com/user-attachments/assets/ad1e6148-7d18-44aa-abd1-51dbfb3d74d6" />

**Expected Behaviour:**

Bronze table will only ever pick up new records

Silver and gold table should only ever add a new partition of data, i.e. old partitions of data remain untouched unless full table refresh is triggered.
<img width="1710" height="482" alt="image" src="https://github.com/user-attachments/assets/a2354e9a-3804-47f7-8aaa-23bff81e9412" />

Number of records for this dataset is as expected because there are 15 turbines and 31 days in March 2022, i.e. 15 * 31 = 465 in gold and 465 * 24 = 11,160 in bronze and silver.
