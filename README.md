# aws-open-data-geo

## Introduction

The [AWS Open Data Program](https://registry.opendata.aws/) hosts a lot of publicly available geospatial datasets. This repo compiles the list of all geospatial datasets on AWS as a CSV file and as a JSON file, making it easier to find and use them programmatically. The list is updated daily.

A complete list of AWS open datasets as individual YAML files is available [here](https://github.com/awslabs/open-data-registry).

## Usage

This repo provides the list of AWS open geospatial datasets in two formats:

- Tab separated values (TSV) file: [aws_geo_datasets.tsv](https://github.com/giswqs/aws-open-data-geo/blob/master/aws_geo_datasets.tsv)
- JSON file: [aws_geo_datasets.json](https://github.com/giswqs/aws-open-data-geo/blob/master/aws_geo_datasets.json)

The TSV file can be easily read into a Pandas DataFrame using the following code:

```python
import pandas as pd

url = 'https://github.com/giswqs/aws-open-data-geo/raw/master/aws_geo_datasets.tsv'
df = pd.read_csv(url, sep='\t')
df.head()
```
