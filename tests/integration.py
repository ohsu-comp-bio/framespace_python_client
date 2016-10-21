from framespace import Framespace

# The server code is at github.com/ohsu-computational-biology/framespace-ref
# The docs describe how to run a server easily via Docker
# Get the host IP with `docker-machine ip default`
# TODO get this via CLI config, or just run the docker-machine command
server_host = "192.168.99.100"
fsp = Framespace(server_host)

print "list keyspaces"
r = fsp.list_keyspaces()
print r.keyspaces[0].keys[:5]

# TODO seems like list_* functions are just duplicating search_* functions
#      called with no args. The API docs are a little confusing. There are
#      both GET and POST endpoints for things that should maybe only have GET
#fsp.search_keyspaces()

print "list axes"
r = fsp.list_axes()
print r

print "search axes"
r = fsp.search_axes()
print r

print "list dataframes"
r = fsp.list_dataframes()
print r

print "list units"
r = fsp.list_units()
print r

r = fsp.search_axes(names=["sample"])
print r

r = fsp.search_units()
print r

r = fsp.search_units(ids=["580a442e33b0e2aa6b359726"])
print r

# TODO fails hard. keyspace_ids is required param?
# TODO server needs is returning code 200 on error. Should be 500 or consistent
#      error code field should be on response
#r = fsp.search_keyspaces()
#print r

r = fsp.search_keyspaces(keyspace_ids=["1"])
print r

r = fsp.search_dataframes(["1"])
print r
