import sys, os, json

sys.path.insert(0, os.path.abspath(os.path.join( os.path.dirname(__file__), "../"))) # Use local grew lib

from grewpy import Graph, CorpusDraft, Request, Corpus, request_counter

tb10 = ["UD_Ancient_Greek-Perseus", "UD_Arabic-PADT", 
				"UD_Chinese-GSDSimp", "UD_English-GUM", 
				"UD_English-LinES", "UD_French-GSD", 
				"UD_French-Sequoia", "UD_Indonesian-GSD", 
				"UD_Japanese-GSD", "UD_Turkish-IMST"
			]

ud_folder = "/Users/guillaum/resources/ud-treebanks-v2.13/"
treebanks = os.listdir(ud_folder)

# print (treebanks)
PV = Request.parse ("pattern { V -[obj]-> O; O[upos=PRON]; O << V }")
VP = Request.parse ("pattern { V -[obj]-> O; O[upos=PRON]; V << O }")
NV = Request.parse ("pattern { V -[obj]-> O; O[upos=NOUN|PROPN]; O << V }")
VN = Request.parse ("pattern { V -[obj]-> O; O[upos=NOUN|PROPN]; V << O }")

print ("Treebank\tPV\tVP\tNV\tVN")
for tb in treebanks:
	corpus = Corpus(ud_folder + tb)
	print (f"{tb}\t{corpus.count(PV)}\t{corpus.count(VP)}\t{corpus.count(NV)}\t{corpus.count(VN)}")
	corpus.clean()

