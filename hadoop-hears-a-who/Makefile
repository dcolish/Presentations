OUTPUT=presentation.out presentation.toc presentation.blg 	\
	presentation.run.xml presentation.aux presentation.log 	\
	presentation.snm presentation.bbl presentation-blx.bib 	\
	presentation.pdf presentation.nav


.PHONY: all

all: presentation.pdf

clean: 
	rm -f $(OUTPUT)

%.pdf: %.tex
	pdflatex $<
	bibtex $(subst aux,tex,$(basename $<))
	pdflatex $<
