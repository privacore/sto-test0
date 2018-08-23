#!/bin/bash

if [ $# -ne 2 ]; then
	echo "Usage: `basename $0` <STO-original-file-directory> <output-directory>" >&2
	echo "Example:" >&2
	echo "   `basename $0` ~/dl/STO-MORF-LMF-final/ ../entries" >&2
	exit 1
fi


dn=`dirname $0`
split_sto_files=$dn/split_sto_files.py

mkdir -p $2/noun
for l in a b c d e f g h i j k l m n o p q r s t u w x y z æ ø å rest; do
	mkdir -p $2/noun/$l || exit
done
mkdir -p $2/propernoun $2/pronoun $2/verb $2/adj $2/rest

for f in $1/*.xml; do
	case $f in
		*_noun_*|*_adj_*|*_pronoun_*|*_rest_*|*_verb_*)
			$split_sto_files $2/ abort $f || exit
			;;
		*_extract_*)
			;;
		*)
			echo "Unknown file(type): $f" >&2
			exit 2
			;;
	esac
done

exit 0
