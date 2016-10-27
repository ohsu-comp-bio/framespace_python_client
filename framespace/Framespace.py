import json
import google.protobuf.json_format as json_format
import requests

import framespace.framespace_pb2 as pb


class ServerException(Exception):
    def __init__(self, response):

        # Format the error message. If there's a traceback included in the response,
        # use that (when server has debug mode enabled).
        data = response.json()
        traceback = data.get("traceback")
        if traceback:
            message = "\nTraceback from server:\n" + "".join(traceback[1:])
        else:
            message = data.get("message", "Unknown error")

        msg = "HTTP status {code}:\n{message}".format(
            code=response.status_code,
            message=message
        )

        # Initialize the exception fields
        super(ServerException, self).__init__(msg)
        self.response = response


class ProtobufRequests(object):
    def __init__(self, host):
        self.host = host

    def post(self, endpoint, message, ResponseType):
        url = self.host + "/" + endpoint
        data = json_format.MessageToJson(message)
        headers = {'Content-Type': 'application/json'}
        resp = requests.post(url, data=data, headers=headers)
        if resp.status_code == 200:
            return json_format.Parse(resp.content, ResponseType())
        else:
            raise ServerException(resp)


class Dimension(object):
    def __init__(self, keyspace_id, keys):
        self.keyspace_id = keyspace_id
        self.keys = keys or []


class Framespace(object):
    def __init__(self, host):
        self.request_lib = ProtobufRequests(host)

    def search_axes(self, names=[], page_size=0, page_token=""):
        m = pb.SearchAxesRequest()
        m.names.extend(names)
        m.page_size = page_size
        m.page_token = page_token
        return self.request_lib.post("axes/search", m, pb.SearchAxesResponse)

    def search_units(self, ids=[], names=[], page_size=0, page_token=""):
        m = pb.SearchUnitsRequest()
        m.ids.extend(ids)
        m.names.extend(names)
        m.page_size = page_size
        m.page_token = page_token
        return self.request_lib.post("units/search", m, pb.SearchUnitsResponse)

    def search_keyspaces(self, keyspace_ids=[], names=[], axis_names=[], keys=[],
                         page_size=0, page_token=""):
        m = pb.SearchKeySpacesRequest()
        m.keyspace_ids.extend(keyspace_ids)
        m.names.extend(names)
        m.axis_names.extend(axis_names)
        m.keys.extend(keys)
        m.page_size = page_size
        m.page_token = page_token
        return self.request_lib.post("keyspaces/search", m,
                                  pb.SearchKeySpacesResponse)

    def search_dataframes(self, keyspace_ids, dataframe_ids=[], unit_ids=[],
                          page_size=0, page_token=""):
        m = pb.SearchDataFramesRequest()
        m.dataframe_ids.extend(dataframe_ids)
        m.keyspace_ids.extend(keyspace_ids)
        m.unit_ids.extend(unit_ids)
        m.page_size = page_size
        m.page_token = page_token
        return self.request_lib.post("dataframes/search", m,
                                  pb.SearchDataFramesResponse)

    def slice_dataframe(self, dataframe_id, new_major=None, new_minor=None,
                        page_start=0, page_end=0):
        m = pb.SliceDataFrameRequest()
        m.dataframe_id = dataframe_id

        if new_major:
            m.new_major.keyspace_id = new_major.keyspace_id
            m.new_major.keys.extend(new_major.keys)

        if new_minor:
            m.new_minor.keyspace_id = new_minor.keyspace_id
            m.new_minor.keys.extend(new_minor.keys)

        m.page_start = page_start
        m.page_end = page_end
        return self.request_lib.post("dataframe/slice", m, pb.DataFrame)
