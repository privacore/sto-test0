#!/usr/bin/env python
from __future__ import print_function
import xml.etree.ElementTree
import os
import argparse
import sys


parser = argparse.ArgumentParser(description="STO splitter")
parser.add_argument("outdir",type=str,help="Output directory")
parser.add_argument("conflict_handling",choices=["overwrite","abort","skip"],default="skip")
parser.add_argument("input_file",type=str,help="Input XML file",nargs='+')

args=parser.parse_args()

if not os.path.isdir(args.outdir):
	print("%s is not a directory"%args.outdir,file=sys.stderr)
	sys.exit(1)

for input_file_name in args.input_file:
	if not os.access(input_file_name,os.R_OK):
		print("%s is not readable"%input_file_name,file=sys.stderr)
		sys.exit(1)



#turn xml subtree into a pretty-indented one. Overrides all nodes' .text and .tail
def prettify(elem, level=0, is_last_child=False):
	if len(elem):
		elem.text = "\n" + "\t"*(level+1)
		for i in range(0,len(elem)):
			prettify(elem[i], level+1, i+1==len(elem))
	if is_last_child:
		elem.tail = "\n" + "\t"*(level-1)
	else:
		elem.tail = "\n" + "\t"*level


def dump_fragment(lexicalentry,full_output_file_name):
	prettify(lexicalentry)
	fragment_tree = xml.etree.ElementTree.ElementTree()
	fragment_tree._setroot(lexicalentry)
	fragment_tree.write(full_output_file_name,encoding="utf-8")



#so far so good
for input_file_name in args.input_file:
	print("Opening and parsing %s"%(input_file_name))
	tree = xml.etree.ElementTree.parse(input_file_name)
	root = tree.getroot()
	lexicon=root.find("Lexicon")
	total_entry_count=0
	total_wordform_count=0
	for lexicalentry in lexicon.findall("LexicalEntry"):
		id=None
		pos=None
		for feat in lexicalentry.findall("feat"):
			att=feat.attrib["att"]
			val=feat.attrib["val"]
			if att=="id":
				id=val
			if att=="partOfSpeech":
				pos=val
		
		output_file_name = id
		if output_file_name[0:4]=="GMU_":
			output_file_name = output_file_name[4:]
		output_file_name = output_file_name.lower()
		output_file_name = output_file_name.replace("/","_")
		
		if pos=="commonNoun":
			subdir="noun/"+output_file_name[0]
			if not os.path.exists(args.outdir+"/"+subdir):
				subdir="noun/rest"
		elif pos=="properNoun":
			subdir="propernoun"
		elif pos[-7:]=="Pronoun":
			subdir="pronoun"
		elif pos=="mainVerb" or pos=="deponentVerb":
			subdir="verb"
		elif pos=="adjective" or pos=="ordinalAdjective":
			subdir="adj"
		else:
			subdir="rest"
		
		full_output_file_name = args.outdir + "/" + subdir + "/" + output_file_name + ".xml"
		print("Generating %s"%full_output_file_name)
		if os.path.exists(full_output_file_name):
			if args.conflict_handling=="skip":
				print("\tskipping")
				continue
			elif args.conflict_handling=="abort":
				print("%s already exists"%full_output_file_name,file=sys.stderr)
				sys.exit(1)
			elif args.conflict_handling=="overwrite":
				print("\toverwriting")
		dump_fragment(lexicalentry,full_output_file_name)
	print("Handled %s"%(input_file_name))
