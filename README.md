# Python Framespace Client

This is a python package to help access and manipulate data from the framespace server.

Tested with python 2.7 and 3.5

# Example

Suppose you want to access data on a few genes from the tcga.BRCA tsv but you don't know the keyspaces ID for that tsv nor the dataframe id for the dataset you wish to access.

```python
from framespace import Framespace, Dimension

fsp = Framespace("http://192.168.99.100:5000")

# Search for the keyspaces ID
ks_resp = fsp.search_keyspaces(
    axis_names = ["sample"],
    keys = ["mask"],
    names = ["tcga-BRCA"]
)

# You can now access the keyspaces id:
ks_id = ks_resp.keyspaces[0].id

# Now you can find the dataframe id you want
resp = fsp.search_dataframes(keyspace_ids=[ks_id])
df_id = resp.dataframes[0].id

# Now retreive the data
sd_resp = fsp.slice_dataframe(
    df_id,
    new_major = Dimension(ks_id, ["TCGA-S3-A6ZG-01A-22R-A32P-07"]),
    page_end = 3
)

# Values are accessed in the contents section under the gene and sample names:
print sd_resp.contents['A1BG|1']['TCGA-S3-A6ZG-01A-22R-A32P-07']
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

`python -m tests.example`
