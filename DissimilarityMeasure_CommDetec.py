import sqlite3
import networkx as nx
import subprocess
import cairo
import community
import operator
from itertools import combinations

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


db = sqlite3.connect("paper_db")
cursor = db.cursor()
db.row_factory = dict_factory

#To find about db table name
cursor.execute("SELECT * FROM sqlite_master WHERE type='table';")
print "Column Names : " , (cursor.fetchall())

res = db.execute("select * from papers")

#print the col_names
col_name_list = [tuple[0] for tuple in res.description]
print "Column Names: "
print col_name_list

#creating a dictionary with key = 'id' and value = ids in ref_id
mygraph = {}
for row in list(res):
    key = row['id']
    if row['ref_id'] is not u'' or None:
        val = map(int, row['ref_id'].strip().split(";"))
        mygraph[key]  = val
    else:
        mygraph[key]  = row['ref_id']
    
#generating the dendogram
G = nx.from_dict_of_lists(mygraph)
nx.write_adjlist(G, "test.adjlist")
dendo = community.generate_dendogram(G)
comDict = community.partition_at_level(dendo, 3)


resultDict = {}
#Calculating -  Dissimilarity Matrix
#for all pair of vertices find the dissimilarity matrix 
for (key1, val1), (key2, val2) in combinations(mygraph.items(), 2):
    #vertices common to both the vertices key1 and key2 will be
    #in intersection list of its values
    neighbours  = [val for val in val1 if val in val2]
    dissimilarIndx = 0 
    for pair in combinations(neighbours,2):
        for a, b in pair:
            if(  comDict[a] != comDict[b]):
                dissimilarIndx = dissimilarIndx+ 1
            
    dictKey = (val1, val2)
    if dissimilarIndx > 0:
        resultDict[(key1, key2)] = dissimilarIndx


#  --------------Dictionary contains -----------------
#  Key   -  Pair of nodes for which dissimilarity will be calculated
#  value -  value of dissimilarity for given pair of nodes
sorted_dict = sorted(resultDict.items(), key=operator.itemgetter(1))

#Dump the result data to result File
resultData  = open('dissimilarityVal.txt', 'w')
for t in sorted_dict:
    line = ' '.join(str(x) for x in t)
    resultData.write(line + '\n')
resultData.close()







