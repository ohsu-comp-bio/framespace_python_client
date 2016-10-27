"""
This is a runnable script which provides some rough integration testing
and examples for how the client is used.

Run this from the repo root with `python -m tests.integration`

This requires a framespace server to be running.
See github.com/ohsu-computational-biology/framespace-ref
If you have Docker engine/machine/compose, it's pretty easy to set up by following
the instructions there. A few of the examples here expect the test data from
that repo, but that's easy enough to change if needed.

You might need to override the SERVER_HOST variable. If you're using Docker
locally, you can get the IP by running `docker-machine ip default`.
"""
from __future__ import print_function

import google.protobuf.text_format as text_format

from framespace import Framespace

TRUNCATE_OUTPUT = True
# This is the IP/host of the framespace server
SERVER_HOST = "http://192.168.99.100:5000"
    

def run_tests():
    fsp = Framespace(SERVER_HOST)

    example("Get all keyspaces")
    ks_res = fsp.search_keyspaces()
    ks_id = ks_res.keyspaces[1].id
    output(ks_res)

    example("Search keyspaces by ID = " + ks_id)
    output(fsp.search_keyspaces(keyspace_ids=[ks_id]))

    example("Get all axes")
    output(fsp.search_axes())

    example("List dataframes for keyspace ID = " + ks_id)
    df_res = fsp.search_dataframes([ks_id])
    df_id = df_res.dataframes[0].id
    output(df_res)

    example("Get all units")
    u_res = fsp.search_units()
    u_id = u_res.units[0].id
    output(u_res)

    example("Search axes by name = sample")
    output(fsp.search_axes(names=["sample"]))

    example("Search units by ID = " + u_id)
    output(fsp.search_units(ids=[u_id]))

    example("Slice dataframe")
    output(fsp.slice_dataframe(df_id))


def example(name):
    "Helper for printing out the example name."
    bar = "=" * 50
    print("\n".join(["", bar, name, bar]))

def output(obj):
    "Helper for printing out the response messages in manageable sizes."
    out = text_format.MessageToString(obj)
    lines = out.split("\n")
    if TRUNCATE_OUTPUT and len(lines) > 10:
        print("\n".join(lines[0:10]))
        print("...output truncated...")
    else:
        print(out)


if __name__ == "__main__":
    run_tests()
