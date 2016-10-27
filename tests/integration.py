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
    output(fsp.search_keyspaces())

    ksid = "580a440433b0e2aa6b3596d5"
    example("Search keyspaces by ID = " + ksid)
    output(fsp.search_keyspaces(keyspace_ids=[ksid]))

    example("Get all axes")
    output(fsp.search_axes())

    ksid = "580a440433b0e2aa6b3596d3"
    example("List dataframes for keyspace ID = " + ksid)
    output(fsp.search_dataframes([ksid]))

    example("Get all units")
    output(fsp.search_units())

    example("Search axes by name = sample")
    output(fsp.search_axes(names=["sample"]))

    uid = "580a442e33b0e2aa6b359726"
    example("Search units by ID = " + uid)
    output(fsp.search_units(ids=[uid]))

    dfid = "57912977105a6c0d293bbe8e"
    example("Slice dataframe")
    fsp.slice_dataframe(dfid)


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
