import google.protobuf.json_format as json_format
import requests
#import numpy
#import pandas

import framespace_pb2 as pb

class Dimension:
    def __init__(self, keyspace_id, keys):
        self.keyspace_id = keyspace_id
        self.keys = keys or []

class Framespace:
    def __init__(self, host, port=5000, request_lib=requests):
        self.host = host
        self.port = port
        self.request_lib = request_lib

    def _get_endpoint_url(self, endpoint):
        return "http://{host}:{port}/{endpoint}".format(
            host=self.host, port=self.port, endpoint=endpoint)

    def _get_request(self, endpoint, ResponseType):
        url = self._get_endpoint_url(endpoint)
        resp = self.request_lib.get(url)
        if resp.status_code == 200:
            return json_format.Parse(resp.content, ResponseType())

    def _post_request(self, endpoint, message, ResponseType):
        url = self._get_endpoint_url(endpoint)
        data = json_format.MessageToJson(message)
        headers = {'Content-Type': 'application/json'}
        resp = self.request_lib.post(url, data=data, headers=headers)
        if resp.status_code == 200:
            return json_format.Parse(resp.content, ResponseType())

    def list_keyspaces(self):
        return self._get_request("keyspaces", pb.SearchKeySpacesResponse)

    def list_axes(self):
        return self._get_request("axes", pb.SearchAxesResponse)

    # TODO not sure this one makes sense. Kinda just duplicates
    def list_dataframes(self):
        return self._get_request("dataframes", pb.SearchDataFramesResponse)

    def list_units(self):
        return self._get_request("units", pb.SearchUnitsResponse)

    def search_axes(self, names=[], page_size=0, page_token=""):
        message = pb.SearchAxesRequest()
        message.names.extend(names)
        message.page_size = page_size
        message.page_token = page_token
        return self._post_request("axes/search", message, pb.SearchAxesResponse)

    def search_units(self, ids=[], names=[], page_size=0, page_token=""):
        message = pb.SearchUnitsRequest()
        message.ids.extend(ids)
        message.names.extend(names)
        message.page_size = page_size
        message.page_token = page_token
        return self._post_request("units/search", message, pb.SearchUnitsResponse)

    def search_keyspaces(self, keyspace_ids=[], names=[], axis_names=[], keys=[],
                         page_size=0, page_token=""):
        message = pb.SearchKeySpacesRequest()
        message.keyspace_ids.extend(keyspace_ids)
        message.names.extend(names)
        message.axis_names.extend(axis_names)
        message.keys.extend(keys)
        message.page_size = page_size
        message.page_token = page_token
        return self._post_request("keyspaces/search", message,
                                  pb.SearchKeySpacesResponse)

    def search_dataframes(self, keyspace_ids, dataframe_ids=[], unit_ids=[],
                          page_size=0, page_token=""):
        message = pb.SearchDataFramesRequest()
        message.dataframe_ids.extend(dataframe_ids)
        message.keyspace_ids.extend(keyspace_ids)
        message.unit_ids.extend(unit_ids)
        message.page_size = page_size
        message.page_token = page_token
        return self._post_request("dataframes/search", message,
                                  pb.SearchDataFramesResponse)

    def slice_dataframe(self, dataframe_id="", new_major=None, new_minor=None,
                        page_start=0, page_end=0):
        message = pb.SliceDataFrameRequest()
        message.dataframe_id = dataframe_id

        if new_major:
            message.new_major.keyspace_id = new_major.keyspace_id
            message.new_major.keys.extend(new_major.keys)

        if new_minor:
            message.new_minor.keyspace_id = new_minor.keyspace_id
            message.new_minor.keys.extend(new_minor.keys)

        message.page_start = page_start
        message.page_end = page_end
        return self._post_request("dataframes/slice", message, pb.DataFrame)
