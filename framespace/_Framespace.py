#import json
#import requests
#import jsonmerge
#import numpy
#import pandas

import framespace_pb2 as pb

class Framespace:
    def __init__(self, host, port=5000):
        self.host = host
        self.port = port

    def _get_url(self, endpoint):
        return "http://{host}:{port}/{endpoint}".format(
            host=self.host, port=self.port, endpoint=endpoint)

    def _make_request(self, endpoint, message):
        pass

    def axes_search(self, names=[], pageSize=0, pageToken=""):
        "axes/search"
        pass

    def unit_search(self):
        "units/search"
        pass

    def key_search(self):
        "keyspaces/search"
        pass

    def dataframe_search(self):
        "dataframes/search"
        pass

    def dataframe_slice(self):
        "dataframes/slice"
        pass

    def buffer_slice(self):
        pass



def axessearch(host = "192.168.99.100", port = "5000", names = [], pageSize = 0, pageToken = ""):
  url = 'http://' + host + ':' + port + '/axes/search'
  searchterm = {"names" : names, "pageSize" : pageSize, "pageToken" : pageToken}
  response = requests.post(url, json = searchterm)
  ans = json.loads(response.text)
  return ans

def unitssearch(host = "192.168.99.100", port = "5000", ids = [], names = [], pageSize = 0, pageToken = ""):
  url = 'http://' + host + ':' + port + '/units/search'
  searchterm = {"ids" : ids, "names" : names, "pageSize" : pageSize, "pageToken" : pageToken}
  response = requests.post(url, json = searchterm)
  ans = json.loads(response.text)
  return ans

def keysearch(host = "192.168.99.100", port = "5000", axisNames = ['sample'], keyspaceIds = [], names = [], keys = [], pageSize = 0, pageToken = ""):
  url = 'http://' + host + ':' + port + '/keyspaces/search'
  searchterm = {"axisNames" : axisNames, "names" : names, "keys" : keys, "pageSize" : pageSize, "pageToken" : pageToken}
  response = requests.post(url, json = searchterm)
  ans = json.loads(response.text)
  return ans

def dfsearch(host = "192.168.99.100", port = "5000", keyspaceIds = ['578fb4336ad2b07cd99ffd4e'], dataframeIds = [], unitIds = [], pageSize = 0, pageToken = ""):
  url = 'http://' + host + ':' + port + '/dataframes/search'
  searchterm = {"keyspaceIds" : keyspaceIds, "dataframeIds" : dataframeIds, "unitIds" : unitIds, "pageSize" : pageSize, "pageToken" : pageToken}
  response = requests.post(url, json = searchterm)
  ans = json.loads(response.text)
  return ans

def dfslice(dataframeId, host = "192.168.99.100", port = "5000", newMajor = None, newMinor = None, pageStart = 0, pageEnd = None):
  url = 'http://' + host + ':' + port + '/dataframe/slice'
  searchterm = {"dataframeId" : dataframeId, "newMajor" : newMajor, "newMinor" : newMinor, "pageStart" : pageStart, "pageEnd" : pageEnd}
  if searchterm['newMinor'] is None:
      del searchterm['newMinor']
  else:
      searchterm['newMinor'] = {"keys" : newMinor}
  if searchterm['newMajor'] is None:
      del searchterm['newMajor']
  else:
      searchterm['newMajor'] = {"keys" : newMajor}
  if searchterm['pageEnd'] is None:
      del searchterm['pageEnd']
  response = requests.post(url, json = searchterm)
  ans = json.loads(response.text)
  return ans

def bufferslice(dataframeId, host = "192.168.99.100", port = "5000", newMajor = None, newMinor = None, pageStart = 0, pageEnd = None, buffer = 1000, looplimit = 1000000):
  searchterm = {"dataframeId" : dataframeId, "newMajor" : newMajor, "newMinor" : newMinor, "pageStart" : pageStart, "pageEnd" : pageEnd}
  url = 'http://' + host + ':' + port + '/dataframe/slice'
  if searchterm['newMinor'] is None:
      del searchterm['newMinor']
  else:
      searchterm['newMinor'] = {"keys" : newMinor}
  if searchterm['newMajor'] is None:
      del searchterm['newMajor']
  else:
      searchterm['newMajor'] = {"keys" : newMajor}
  if searchterm['pageStart'] is None:
      searchterm['pageStart'] = 0
  n = pageEnd
  f = searchterm['pageStart']
  l = searchterm['pageStart'] + buffer
  if n is None:
      searchterm['pageEnd'] = l
  elif n > l:
      searchterm['pageEnd'] = l


  response = requests.post(url, json = searchterm)
  ans = json.loads(response.text)
  nans = ans
  c = 1
  if n is not None:
      if n < l:
          return ans

  while len(nans['contents']) > 0:
      f = f + buffer
      l = l + buffer
      c = c + 1
      nreq = searchterm
      nreq['pageStart'] = f
      nreq['pageEnd'] = l
      if n is not None:
          if n < l:
              nreq['pageEnd'] = n
      response = requests.post(url, json = nreq)
      nans = json.loads(response.text)
      if len(nans['contents']) < 1:
          return ans
      ans['contents'] = jsonmerge.merge(ans['contents'], nans['contents'])
      if n is not None:
          if n < l:
              return ans
      elif c >= looplimit:
          ans['loop'] = 'You were stuck in an infinite loop!'
          return ans
  return ans

def genestat(resp, genes = None):
    if genes is None:
        genes = resp['contents'].keys()
    ans = {}
    for x in range(0, len(genes)):
        samples = resp['contents'][genes[x]].keys()
        data = []
        for y in range(0, len(samples)):
            data.append(resp['contents'][genes[x]][samples[y]])
        ans[genes[x]] = {}
        ans[genes[x]]['mean'] = numpy.mean(data)
        ans[genes[x]]['variance'] = numpy.var(data)
        ans[genes[x]]['median'] = numpy.median(data)
        ans[genes[x]]['min'] = min(data)
        ans[genes[x]]['max'] = max(data)
    return ans

def genepanda(resp):
    df = pandas.DataFrame.transpose(pandas.read_json(json.dumps(resp['contents'])))
    return df
