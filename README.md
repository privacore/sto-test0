(English below)
# Dette repository indeholder et dansk lexikon oprindelig afledt af STO
STO (SprogTeknisk Ordbog) er udviklet af CST (https://cst.ku.dk/) som del af et EU-projekt (MetaNord), og brugte delvist leksikale resourcer lavet i et tidligere project (PAROLE), og andre kilder, så som RO (https://dsn.dk/ro) og DDO (https://ordnet.dk/ddo). STO-projektet er afsluttet.

Dette repository er en omformatering af STO fra LMF (Lexical Markup Framework) til et format, hvor hvert LexicalEntry er i sin egen fil, hvilket gør nogle opgaver nemmere.

De oprindelige filer i LMF-format kan hentes på CLARIN https://repository.clarin.dk/repository/xmlui/handle/20.500.12115/22

Licens: CC BY-SA 4.0

# This repository contains a Danish lexicon originally derived from STO.

STO was developed by CST (https://cst.ku.dk/) as part of a EU project, and partially used lexical resources created in an earlier project (PAROLE), and other sources sich as RO (https://dsn.dk/ro) and DDO (https://ordnet.dk/ddo). The STO project finished.

This repository contains an import of STO in an easier-to-maintain format. The original STO is in the LMF format. This repository has split each LexicalEntry into a separate file, which makes it easier to track changes in git.

License: CC BY-SA 4.0

## Structure of repository

	entries/
		noun
			a
			b
			c
			...
		verb
		adj
		pronoun
		propernoun
		rest
		...
	
	trash-entries/

	tools/
		import-sto.sh
		generate-lexicon.sh
	
	lmf-resources/
		DTD_LMF_REV_16-strict.dtd
		lexicon-example.xml
		lexicon-head.xml.snippet
		lexicon-tail.xml.snippet

"entries" contains the lexical entries. One <LexicalEntry> per file. It is further subdivided into subdirectories (nouns, verbs, ..) so we don't have 83.000 entries in a single directory.

"trash-entries"" directory is for deleted entries from entries/. STO relied partially on PAROLE data, and there were a few dubious and incorrect entries from there. To avoid re-introducing them in a mass-import later on we keep the entries but in the separate trash-entries directory.

"tools" contains various tools. Eg. for importing STO (if a new version is available) and generating a proper LMF lexicon file.

"lmf-resources" contains a few files for generating an LMF lexicon and also example of what such a beast might look like.

## Modifying entries

New entries should have a "originalSource" <feat> attribute with an appropriate value.

Updated or deleted entries should have a "updatedBy" <feat> attribute with appropriate value. That attribute can be put either on the whole lexical entry, or in the FormRepresentation.

The subdirectory 'tools' has a check_file_structure.py that checks if a file has the correct structure