#Python Framespace Client

This is a python package to help access and manipulate data from the framespace server.

#Example

Suppose you want to access data on a few genes from the tcga.BRCA tsv but you don't know the keyspaces Id for that tsv nor the dataframe id for the dataset you wish to access.

First, you would need submit a request to find the keyspaces id:
```
>>> keyResponse = framesacer.keysearch(host = "192.168.99.100", port = "5000", axisNames = ['sample'], keys = ['mask'], names = ['tcga.BRCA'])
```

You can now access the keyspaces id:
```
>>> keyResponse['keyspaces'][0]['id']
u'579128f46ac4ff507bde9091'
```

Now that you have the keyspaces id you can use it to find the dataframe id you want:
```
>>> dfResponse = framespacer.dfsearch(host = "192.168.99.100", port = "5000", keyspaceIds = ['579128f46ac4ff507bde9091'])
>>> dfResponse['dataframes'][0]['id']
u'57912977105a6c0d293bbe8e'
```

You can then use the dataframe id in the bufferreq function to retreive the data:
```
>>> response = framespacer.bufferslice(dataframeId = '57912977105a6c0d293bbe8e', host = "192.168.99.100", port = "5000", newMajor = ["TCGA-S3-A6ZG-01A-22R-A32P-07", "TCGA-AR-A250-01A-31R-A169-07", "TCGA-C8-A1HK-01A-21R-A13Q-07"], pageEnd = 3, buffer = 1000)
```
(In this example we only requested the first 3 genes and 3 specific samples so that it would be easier to look at)

Values are accessed in the contents section under the gene and sample names:
```
>>> response['contents']['A1BG|1']['TCGA-AR-A250-01A-31R-A169-07']
139.351
```

This response can also be formed into a pandas dataframe using the following function:
```
>>> responseDf = framespacer.genepanda(response)
```

Now individual values are called like this:
```
>>> responseDf.loc['A1BG|1']['TCGA-AR-A250-01A-31R-A169-07']
139.351
```

Or if you want to call all of the values for a specific gene leave the sample side blank:
```
>>> responseDf.loc['A1BG|1',]
TCGA-AR-A250-01A-31R-A169-07    139.3510
TCGA-C8-A1HK-01A-21R-A13Q-07     15.5039
TCGA-S3-A6ZG-01A-22R-A32P-07    160.6870
```

You can quickly get a few summary statistics directly from the response using the genestat function:
```
>>> responseStats = framespacer.genestat(response)
```

Stat summaries for specific genes can be looked up using the gene name.
```
>>> responseStats['A1BG|1']
{'variance': 4096.8290666688899, 'max': 160.687, 'min': 15.5039, 'median': 139.351, 'mean': 105.18063333333333}
```

If you don't want to get the stats for all the genes specify which genes you want using a list:
```
>>> responseStats = framespacer.genestat(response, genes = ['A1BG|1', 'A1CF|29974']
>>> responseStats
{u'A1BG|1':
  {'variance': 4096.8290666688899, 
  'max': 160.687, 
  'min': 15.5039, 
  'median': 139.351, 
  'mean': 105.18063333333333},
u'A1CF|29974':
  {'variance': 0.17466804222222221, 
  'max': 0.9355, 
  'min': 0.0, 
  'median': 0.82779999999999998, 
  'mean': 0.58776666666666666}
}
```
