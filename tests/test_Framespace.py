import json
import unittest

import requests

from framespace import Framespace, Dimension
import framespace.framespace_pb2 as pb


class MockRequestLib(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.post_count = 0
        self.last_data = None

    def post(self, endpoint, data, ResponseType):
        self.last_endpoint = endpoint
        self.last_data = data
        resp = requests.Response()
        resp.status_code = 200
        return resp


class TestFramespace(unittest.TestCase):
    def setUp(self):
        self.framespace = Framespace("http://framespace_host:987654")
        self.framespace.request_lib = MockRequestLib()

    def assertPostedData(self, data):
        # Parse and serialize the data so that the keys are sorted
        last_data = self.framespace.request_lib.last_data.SerializeToString()
        data = data.SerializeToString()
        self.assertEqual(last_data, data)

    def test_search_axes_request(self):
        fsp = self.framespace
        fsp.search_axes(names=["foo"], page_size=1, page_token="tk")
        exp = pb.SearchAxesRequest()
        exp.names.append("foo")
        exp.page_size = 1
        exp.page_token = "tk"
        self.assertPostedData(exp)

    def test_search_units_request(self):
        fsp = self.framespace
        fsp.search_units(ids=["1"], names=["foo"], page_size=1, page_token="tk")
        exp = pb.SearchUnitsRequest()
        exp.ids.append("1")
        exp.names.append("foo")
        exp.page_size = 1
        exp.page_token = "tk"
        self.assertPostedData(exp)

    def test_search_keyspaces_request(self):
        fsp = self.framespace
        fsp.search_keyspaces(keyspace_ids=["1"], names=["foo"], axis_names=["x"],
                             keys=["key1"], page_size=1, page_token="tk")
        exp = pb.SearchKeySpacesRequest()
        exp.keyspace_ids.append("1")
        exp.names.append("foo")
        exp.axis_names.append("x")
        exp.keys.append("key1")
        exp.page_size = 1
        exp.page_token = "tk"
        self.assertPostedData(exp)

    def test_search_dataframes_request(self):
        fsp = self.framespace
        fsp.search_dataframes(["ks1"], dataframe_ids=["1"], unit_ids=["u1"],
                             page_size=1, page_token="tk")
        exp = pb.SearchDataFramesRequest()
        exp.dataframe_ids.append("1")
        exp.keyspace_ids.append("ks1")
        exp.unit_ids.append("u1")
        exp.page_size = 1
        exp.page_token = "tk"
        self.assertPostedData(exp)

    def test_slice_dataframe_request(self):
        fsp = self.framespace
        fsp.slice_dataframe(dataframe_id="df1", new_major=Dimension("ks1", ["k1"]),
                            new_minor=Dimension("ks2", ["k2"]), page_start=1, page_end=2)
        exp = pb.SliceDataFrameRequest()
        exp.dataframe_id = "df1"
        exp.new_major.keys.append("k1")
        exp.new_major.keyspace_id = "ks1"
        exp.new_minor.keys.append("k2")
        exp.new_minor.keyspace_id = "ks2"
        exp.page_start = 1
        exp.page_end = 2
        self.assertPostedData(exp)

    def test_invalid_messages(self):
        fsp = self.framespace
        with self.assertRaises(TypeError):
            fsp.search_units(ids=[1], names=["foo"], page_size=1, page_token="tk")
        self.assertEqual(self.framespace.request_lib.post_count, 0)


if __name__ == '__main__':
    unittest.main()
