import sqlite3
import networkx as nx
import subprocess
import cairo
import community

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

subprocess.call("cls", shell=True)
db = sqlite3.connect("paper_db")
cursor = db.cursor()
db.row_factory = dict_factory

#To find about db table name
cursor.execute("SELECT * FROM sqlite_master WHERE type='table';")
print "Column Names : "
print(cursor.fetchall())

res = db.execute("select * from papers")

#print the col_names
col_name_list = [tuple[0] for tuple in res.description]
print "Column Names: "
print col_name_list

#creating a dictionary with given where key = 'id' and value = ids in ref_id
mygraph = {}
for row in list(res):
    key = row['id']
    if row['ref_id'] is not u'' or None:
        val = map(int, row['ref_id'].strip().split(";"))
        mygraph[key]  = val
    else:
        mygraph[key]  = row['ref_id']
    
print "graph prep"
G = nx.from_dict_of_lists(mygraph)

nx.write_adjlist(G, "test.adjlist")

print "generate dendogram"
dendo = community.generate_dendogram(G)


print "Length of dendogram"
print len(dendo)

print "parition at level"
comDict = community.partition_at_level(dendo, 3)

if isinstance(comDict, dict):
    print "Dictionary type"

for the_key, the_value in comDict.iteritems():
    print the_key, 'corresponds to', the_value










