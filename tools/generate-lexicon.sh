#!/bin/bash

if [ $# -ne 1 ]; then
	echo "Usage: `basename $0` <output-lexicon-file>" >&2
	echo "Example: `basename $0` sto.xml" >&2
	exit 1
fi

destination_file="$1"

dn=`dirname $0`
basedir=`dirname $dn`
entries_dir=$basedir/entries
head_file=$basedir/lmf-resources/lexicon-head.xml.snippet
tail_file=$basedir/lmf-resources/lexicon-tail.xml.snippet

if [ ! -d $entries_dir ]; then
	echo "Source directory $entries_dir doesn't exist" >&2
	exit 2
fi

if [ ! -r $head_file ]; then
	echo "Required helper file $head_file doesn't exist" >&2
	exit 2
fi
if [ ! -r $tail_file ]; then
	echo "Required helper file $tail_file doesn't exist" >&2
	exit 2
fi


echo "entries_dir=$entries_dir"
cp $head_file $destination_file || exit

find $entries_dir -type f -name \*.xml -print0 |xargs -0 cat >>$destination_file || exit

cat $tail_file >> $destination_file || exit

exit 0
