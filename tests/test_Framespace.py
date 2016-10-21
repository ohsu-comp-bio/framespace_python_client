import json
import unittest

from framespace import Framespace, Dimension

class MockRequestLib:
    def __init__(self):
        self.reset()

    def reset(self):
        self.post_count = 0
        self.last_url = None
        self.last_data = None
        self.last_header = None

    def post(self, url, data, headers):
        self.last_url = url
        self.last_data = data
        self.last_header = headers

class TestFramespace(unittest.TestCase):
    def setUp(self):
        self.mock_request_lib = MockRequestLib()
        self.framespace = Framespace("framespace_host", 987654,
                                     request_lib=self.mock_request_lib)

    def assertPostedData(self, data):
        # Parse and serialize the data so that the keys are sorted
        last_data = json.dumps(json.loads(self.mock_request_lib.last_data),
                               sort_keys=True)
        data = json.dumps(data, sort_keys=True)
        self.assertEqual(last_data, data)

    def test_endpoint_url(self):
        mrl = self.mock_request_lib
        self.framespace.search_axes(names=[])
        self.assertEqual(mrl.last_url, "http://framespace_host:987654/axes/search")

    def test_valid_messages(self):
        fsp = self.framespace
        eql = self.assertPostedData

        fsp.search_axes(names=["foo"], page_size=1, page_token="tk")
        eql({
            "names": ["foo"],
            "pageSize": 1,
            "pageToken": "tk",
        })

        fsp.search_units(ids=["1"], names=["foo"], page_size=1, page_token="tk")
        eql({
            "ids": ["1"],
            "names": ["foo"],
            "pageSize": 1,
            "pageToken": "tk",
        })

        fsp.search_keyspaces(keyspace_ids=["1"], names=["foo"], axis_names=["x"],
                             keys=["key1"], page_size=1, page_token="tk")
        eql({
            "keyspaceIds": ["1"],
            "names": ["foo"],
            "axisNames": ["x"],
            "keys": ["key1"],
            "pageSize": 1,
            "pageToken": "tk",
        })

        fsp.search_dataframes(["ks1"], dataframe_ids=["1"], unit_ids=["u1"],
                             page_size=1, page_token="tk")
        eql({
            "dataframeIds": ["1"],
            "keyspaceIds": ["ks1"],
            "unitIds": ["u1"],
            "pageSize": 1,
            "pageToken": "tk",
        })

        fsp.slice_dataframe(dataframe_id="df1", new_major=Dimension("ks1", ["k1"]),
                            new_minor=Dimension("ks2", ["k2"]), page_start=1, page_end=2)
        eql({
            "dataframeId": "df1",
            "newMajor": {
                "keys": ["k1"],
                "keyspaceId": "ks1",
            },
            "newMinor": {
                "keys": ["k2"],
                "keyspaceId": "ks2",
            },
            "pageStart": 1,
            "pageEnd": 2,
        })

    def test_invalid_messages(self):
        fsp = self.framespace
        with self.assertRaises(TypeError):
            fsp.search_units(ids=[1], names=["foo"], page_size=1, page_token="tk")
        self.assertEqual(self.mock_request_lib.post_count, 0)
