from framespace import Framespace, Dimension

class MockRequestLib:
    def post(self, url, data):
        print(url, data)

mock_request_lib = MockRequestLib()
fsp = Framespace("127.0.0.1", request_lib=mock_request_lib)

fsp.search_axes(names=["foo"], page_size=1, page_token="tk")
fsp.search_units(ids=["1"], names=["foo"], page_size=1, page_token="tk")
fsp.search_keyspaces(keyspace_ids=["1"], names=["foo"], axis_names=["x"],
                     keys=["key1"], page_size=1, page_token="tk")
fsp.search_dataframes(dataframe_ids=["1"], keyspace_ids=["ks1"], unit_ids=["u1"],
                     page_size=1, page_token="tk")
fsp.slice_dataframe(dataframe_id="df1", new_major=Dimension("ks1", ["k1"]),
                    new_minor=Dimension("ks2", ["k2"]), page_start=1, page_end=2)

# TODO test schema validation fail
# fsp.search_units(ids=[1], names=["foo"], page_size=1, page_token="tk")
