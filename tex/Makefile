PDF=largeprint.pdf a5x800.pdf english0.pdf waterproof.pdf giftandaward.pdf africa.pdf
FONTS=CharisShort-Bold.otf    CharisShorter-Bold.otf    CharisShorter-Italic.otf    CharisShorter.otf    CharisShort-Italic.otf    CharisShort.otf \
      CharisShort-Bold.woff2  CharisShorter-Bold.woff2  CharisShorter-Italic.woff2  CharisShorter.woff2  CharisShort-Italic.woff2  CharisShort.woff2

default: $(PDF)

%.pdf : %.tex english.tex biblayout.tex
	xelatex $< </dev/null 
	xelatex $< </dev/null  # just run it again, for the TOC, because CPU is cheap

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

# Make book signatures - the 28 here is 28 x 1/72" ≅ 10mm
# See also https://softwarerecs.stackexchange.com/questions/438/software-to-put-pages-of-a-pdf-file-in-book-order
%-book.pdf: %.pdf
	pdfbook2 --no-crop --paper=a4paper --outer-margin=28 --inner-margin=0 --top-margin=0 --bottom-margin=0 --signature=32 $<

# Make book signatures - but move the 1st four pages to the tail first
%-u-book.pdf: %.pdf
	# Take off 4 page header from the front, and put it at the back, to get proper signatures
	pdfseparate $< tmp/$(basename $<)-%04d.pdf
	mv tmp/$(basename $<)-0001.pdf tmp/$(basename $<)-z0001.pdf
	mv tmp/$(basename $<)-0002.pdf tmp/$(basename $<)-z0002.pdf
	mv tmp/$(basename $<)-0003.pdf tmp/$(basename $<)-z0003.pdf
	mv tmp/$(basename $<)-0004.pdf tmp/$(basename $<)-z0004.pdf
	pdfunite tmp/$(basename $<)-*.pdf $(basename $<)-u.pdf
	rm tmp/$(basename $<)-*.pdf
	pdfbook2 --no-crop --paper=a4paper --outer-margin=28 --inner-margin=0 --top-margin=0 --bottom-margin=0 --signature=32 $(basename $<)-u.pdf


fonts: $(FONTS)

%.woff2: %.sfd
	fontforge -c 'open(argv[1]).generate(argv[2])' $< $@
%.otf: %.sfd
	fontforge -c 'open(argv[1]).generate(argv[2])' $< $@

