from __future__ import print_function

import google.protobuf.text_format as text_format

from framespace import Framespace, Dimension

def output(obj):
    "Helper for printing out the response messages in manageable sizes."
    out = text_format.MessageToString(obj)
    lines = out.split("\n")
    print(out)


fsp = Framespace("http://192.168.99.100:5000")

# Search for the keyspaces ID
ks_resp = fsp.search_keyspaces(
    axis_names = ["sample"],
    keys = ["mask"],
    names = ["tcga-BRCA"]
)

output(ks_resp)

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
print(sd_resp.contents['A1BG|1']['TCGA-S3-A6ZG-01A-22R-A32P-07'])

# TODO below is old code that hasn't been migrated yet
# This response can also be formed into a pandas dataframe using the following function:
#responseDf = framespacer.genepanda(response)

# Now individual values are called like this:
#responseDf.loc['A1BG|1']['TCGA-AR-A250-01A-31R-A169-07']

# Or if you want to call all of the values for a specific gene leave the sample side blank:
#responseDf.loc['A1BG|1',]

# You can quickly get a few summary statistics directly from the response using the genestat function:
#responseStats = framespacer.genestat(response)

# Stat summaries for specific genes can be looked up using the gene name.
#responseStats['A1BG|1']

# If you don't want to get the stats for all the genes specify which genes you want using a list:
#framespacer.genestat(response, genes = ['A1BG|1', 'A1CF|29974'])
