# Python Framespace Client

This is a python package to help access and manipulate data from the framespace server.

Tested with python 2.7 and 3.5

# Example

Suppose you want to access data on a few genes from the tcga.BRCA tsv but you don't know the keyspaces ID for that tsv nor the dataframe id for the dataset you wish to access.

```python
from framespace import Framespace

fsp = Framespace("http://192.168.99.100:5000")

# Search for the keyspaces ID
response = fsp.search_keyspaces(axis_name=["sample"], keys=["mask"], names=["tcga.BRCA"])

# You can now access the keyspaces id:
ksid = resp.keyspaces[0].id

# Now you can find the dataframe id you want
resp = framespace.search_dataframes(keyspace_ids=[ksid])
dfid = resp.dataframes[0].id

# Now retreive the data
response = framespacer.bufferslice(dataframeId = '57912977105a6c0d293bbe8e', host = "192.168.99.100", port = "5000", newMajor = ["TCGA-S3-A6ZG-01A-22R-A32P-07", "TCGA-AR-A250-01A-31R-A169-07", "TCGA-C8-A1HK-01A-21R-A13Q-07"], pageEnd = 3, buffer = 1000)

# Values are accessed in the contents section under the gene and sample names:
response['contents']['A1BG|1']['TCGA-AR-A250-01A-31R-A169-07']

# This response can also be formed into a pandas dataframe using the following function:
responseDf = framespacer.genepanda(response)

# Now individual values are called like this:
responseDf.loc['A1BG|1']['TCGA-AR-A250-01A-31R-A169-07']

# Or if you want to call all of the values for a specific gene leave the sample side blank:
responseDf.loc['A1BG|1',]

# You can quickly get a few summary statistics directly from the response using the genestat function:
responseStats = framespacer.genestat(response)

# Stat summaries for specific genes can be looked up using the gene name.
responseStats['A1BG|1']

# If you don't want to get the stats for all the genes specify which genes you want using a list:
framespacer.genestat(response, genes = ['A1BG|1', 'A1CF|29974']
```

# Development

## Protobuf

Request messages are encoded using [Protobufs](https://developers.google.com/protocol-buffers/). Protobuf schema is defined in [proto/framespace.proto](proto/framespace.proto) and the generated Python code is output to [framespace/framespace_pb2.py](framespace/framespace_pb2.py).

## Tests

Currently there is a very simple test case for request message format.
Run it from the root of the repo with:

`python -m tests.test_Framespace`

There are also some simple integration/example tests which require a Framespace API
server. See [tests/integration.py](tests/integration.py), read the docs there, and run with:

`python -m tests.integration`
