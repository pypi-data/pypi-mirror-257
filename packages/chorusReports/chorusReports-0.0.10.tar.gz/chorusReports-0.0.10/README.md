# CHORUS Reports
[CHORUS](https://www.chorusaccess.org/) brings together funders, societies, publishers, institutions, and the public from across the open research ecosystem to share knowledge, develop solutions, advance innovation, and support collective efforts. CHORUS queries several repositories to collect data from the [Global Research Infrastructure](https://metadatagamechangers.com/blog/2023/12/25/chorus-data-journeys) and makes those data available in reports.  [Metadata Game Changers is working with CHORUS](https://metadatagamechangers.com/blog/2023/9/20/informate-metadata-game-changers-and-chorus-collaborate-to-make-the-invisible-visible) to understand these reports and help U.S. Funders and other users to understand them as well.

The CHORUSReports Package was developed by Metadata Game Changers to facilitate analysis of the CHORUS reports with focus on the All Report, the Author Affiliation Report, and the Dataset Report.

## CHORUSReports
The CHORUSReport object holds a CHORUS Report of any type and support operations on that on 

### Properties

| Property  | Description  |
|:---|:---|
|dataPath|Path to the data associated with the report.|
|dataFile|The name of the data file associated with the report (derived from dataPath.|
|organization|The acronym of the organization that the report data comes from (typically NSF, USGS, or USAID). The fileNames start with these acronymns.|
|timestamp|The timestamp (YYYYMMDD) of the data in the report, i.e., when it was retrieved from CHORUS)|
|dataType|The type of the data in the report (all, authors, datasets)|
|data_d|Data associated with the report, i.e. actual data or the summary of the data. Elements of the data_d are described below.|

### Functions
|Function  | Description  | Arguments | Returns|
|:---|:---|:---|:---|
|save|Save the data from the report to its dataFile. This can be used to save changes made during the analysis of the data to the original datafile.|None|Message with number of lines written.|
|data|Returns the data for the report as a dataframe. Dataframe commands can be used with this, e.g. cr.data('all').head()|dataType as string|data in dataframe.|
|summary|Returns the summary for the report as a dataframe. Dataframe commands can be used with this, e.g. cr.sumary('all').head()|dataType as string|summary in dataframe.|
|info|Returns data dataframe.info() for the report.|None|info() for dataframe|
|counts|Returns count information for a field in the report data, e.g. cr.report('all').counts('DOI') gives the summary information for the DOI column of the All Report|Field name|Dictionary with counts ({'report': 'all', 'field': 'DOI', 'total count': 7143, 'unique': 7143})|
|common|Counts values of a field in a report.|field name, delimiter (default=None)|Adds new data (dataframe of value, counts) to the report with the name of the item counted as the key for the data.|
|makeStandardElementNames|Convert names of columns in the report to standard names given in the dataTypes_d.|None|Dataframe in report has standard column names.|
|makePublicationYear|Creates a column in the dataframe named Publication Year which is the year of the Print Publication Date if it exists or the year of the Online Publication Date if it doesn't|None|None|
|convertDates2Years|Create new date fields with years from date fields in the report.|A list of field names to convert.|None|
|harmonizeRepositoryNames|Standardize repository names in Dataset Reports.|A list of repository synonyms (see CHORUSDataCleanup.ipynb for an example.|None|
|readDateCreatedFromDOIMetadata|Read DOI metadata from a getDOIMetadata output file (DataCite metadata) to get the date_created field for datasets and add it to the Dataset Report.|The name of a DOI metadata output file|None.|

## CHORUSRetrievals
The CHORUSRetrieval object holds a dictionary of related reports.

### Properties

| Property  | Description  |
|:---|:---|
|organization|The acronym of the organization that the report data comes from (typically NSF, USGS, or USAID). The fileNames start with these acronymns.|
|timestamp|The timestamp (YYYYMMDD) of the data in the report, i.e., when it was retrieved from CHORUS)|
|report_d|A dictionary of reports with keys = dataTypes|

### Functions
For a CHORUS Retrieval (cr) these functions are called as cr.function(arguments)

|Function  | Description  | Arguments | Returns|
|:---|:---|:---|:---|
|**dataTypes:**|Get the data types for reports in the retrieval|none|list of dataTypes in the retrieval (default: ['all', 'authors', 'datasets'])|
|**info:**|Get dataframe.info() for each dataframe in the retrieval|none|info()| 
|**data(dt):**|Get the data dataframe with dataType = dt from the retrieval|dataType, one of ['all', 'authors', 'datasets']|data dataframe for dataType.|  
|**summary(dt):**|Get the data dataframe with dataType = dt from the retrieval|dataType, one of ['all', 'authors', 'datasets']|summary dataframe for dataType.|	

