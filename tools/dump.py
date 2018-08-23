#!/usr/bin/python
import Lexicon
import LexiconIO
import argparse
import sys

#hack to make utf-8 values work
import sys
reload(sys)
sys.setdefaultencoding("utf_8")


parser = argparse.ArgumentParser(description="STO dumper - dumps STO entries to stdout")
parser.add_argument("lexicon_dir",type=str,help="Lexicon directory")
parser.add_argument("dump_part",choices=["id","lemma","wordform"],default="lemma",help="Which part to dump. If 'wordform' you should specify --wfa too")
parser.add_argument("-p","--pos",action="append",help="POS filter ('commonNoun', 'mainVerb', ...)")
parser.add_argument("--wfa",action="append",help="WordForm 'att' filter in the form of att=val, eg. degree=positive")
parser.add_argument("-o","--output_file",type=argparse.FileType('w'),default=sys.stdout,help="Destination file, default stdout")
args=parser.parse_args()

req_wfa={}
if args.wfa:
	for wfa in args.wfa:
		e = wfa.split('=')
		if len(e)==2:
			req_wfa[e[0]] = e[1]
		else:
			print >>sys.stderr, "WFA '%s' must have an equal sign"%wfa
			sys.exit(2)

lexicon = LexiconIO.load_lexicon_from_dir(args.lexicon_dir)

for (source,le) in lexicon.all_entries():
	if args.pos and le.feat.get("partOfSpeech") not in args.pos:
		continue
	if args.dump_part=="id":
		print >>args.output_file, le.id
	elif args.dump_part=="lemma":
		for r in le.lemma.representations:
			print >>args.output_file, r.get("writtenForm")
	elif args.dump_part=="wordform":
		for wf in le.wordforms:
			matches=True
			for (att,val) in req_wfa.iteritems():
				if not wf.feat.has(att,val):
					matches = False
					break
			if matches:
				for r in wf.representations:
					print >>args.output_file, r.get("writtenForm")

sys.exit(0)
