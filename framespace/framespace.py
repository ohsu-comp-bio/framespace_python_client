#import json
#import requests
#import jsonmerge
#import numpy
#import pandas

import framespace_pb2 as pb

class Dimension:
    def __init__(self, keyspace_id, keys):
        self.keyspace_id = keyspace_id
        self.keys = keys or []

class Framespace:
    def __init__(self, host, port=5000):
        self.host = host
        self.port = port

    def _get_url(self, endpoint):
        return "http://{host}:{port}/{endpoint}".format(
            host=self.host, port=self.port, endpoint=endpoint)

    def _make_request(self, endpoint, message):
        pass

    def search_axes(self, names=[], page_size=0, page_token=""):
        message = pb.SearchAxesRequest()
        message.names.extend(names)
        message.page_size = page_size
        message.page_token = page_token
        self._make_request("axes/search", message)

    def search_units(self, ids=[], names=[], page_size=0, page_token=""):
        message = pb.SearchUnitsRequest()
        message.ids.extend(ids)
        message.names.extend(names)
        message.page_size = page_size
        message.page_token = page_token
        self._make_request("units/search", message)

    def search_keyspaces(self, keyspace_ids=[], names=[], axis_names=[], keys=[],
                         page_size=0, page_token=""):
        message = pb.SearchKeySpacesRequest()
        message.keyspace_ids.extend(keyspace_ids)
        message.names.extend(names)
        message.axis_names.extend(axis_names)
        message.keys.extend(keys)
        message.page_size = page_size
        message.page_token = page_token
        self._make_request("keyspaces/search", message)

    def search_dataframes(self, dataframe_ids=[], keyspace_ids=[], unit_ids=[],
                          page_size=0, page_token=""):
        message = pb.SearchDataFramesRequest()
        message.dataframe_ids.extend(dataframe_ids)
        message.keyspace_ids.extend(keyspace_ids)
        message.unit_ids.extend(unit_ids)
        message.page_size = page_size
        message.page_token = page_token
        self._make_request("dataframes/search", message)

    def slice_dataframe(self, dataframe_id="", major=None, minor=None,
                        page_start=0, page_end=0):
        message = pb.SearchDataFrameRequest()

        if major:
            message.major.keyspace_id = major.keyspace_id
            message.major.keys.extend(major.keys)

        if minor:
            message.minor.keyspace_id = minor.keyspace_id
            message.minor.keys.extend(minor.keys)

        message.page_start = page_start
        message.page_end = page_end
        self._make_request("dataframes/slice", message)



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
