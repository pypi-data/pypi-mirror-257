import sys, os, json

sys.path.insert(0, os.path.abspath(os.path.join( os.path.dirname(__file__), "../"))) # Use local grew lib

from grewpy import Graph, CorpusDraft, Request, Corpus, request_counter

ud_folder = "/Users/guillaum/resources/ud-treebanks-v2.13/"
treebanks = os.listdir(ud_folder)

# print (treebanks)
NA = Request.parse ("pattern { N -[amod]-> A; N << A }")
AN = Request.parse ("pattern { N -[amod]-> A; A << N }")
print ("Treebank\tNA\tAN")
for tb in treebanks:
	corpus = Corpus(ud_folder + tb)
	print (f"{tb}\t{corpus.count(NA)}\t{corpus.count(AN)}")