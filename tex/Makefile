PDF=africa.pdf english0.pdf

default: $(PDF)

%.pdf : %.tex english.tex biblayout.tex
	xelatex $< </dev/null 

english.tex: gentex-english.py
	./gentex-english.py english.tex

clean:
	rm *.{aux,log,toc,dvi,ps}

generated.tex: gentex.py
	./gentex.py generated.tex

bibl2.pdf: bibl2.tex generated.tex
	xelatex bibl2.tex < /dev/null

bibl.pdf: bibl.tex
	xelatex bibl.tex < /dev/null

