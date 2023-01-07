PDFDEPS=hyph-en.tex \
	hyph-af.tex\
	bibldefault.tex \
	biblayout.tex \
	kjvtopics.tex \
	kjvwordlist.tex \
	english.tex
PDF=largeprint.pdf a5x800.pdf english0.pdf waterproof.pdf giftandaward.pdf africa.pdf
FONTS=GrazeShort-Bold.otf    GrazeShorter-BoldItalic.otf    GrazeShorter-Italic.otf    GrazeShorter.otf  \
      GrazeShort-Bold.woff2  GrazeShorter-BoldItalic.woff2  GrazeShorter-Italic.woff2  GrazeShorter.woff2 \

FONTS_GRAZESHORTER=\
	GrazeShorter.otf \
	GrazeShorter-Bold.otf \
	GrazeShorter-BoldItalic.otf \
	GrazeShorter-Italic.otf 
FONTSW_GRAZESHORTER=\
	GrazeShorter.woff2 \
	GrazeShorter-Bold.woff2 \
	GrazeShorter-BoldItalic.woff2 \
	GrazeShorter-Italic.woff2 
FONTS_GRAZESHORTERNARROW=\
	GrazeShorterNarrow.otf \
	GrazeShorterNarrow-Bold.otf \
	GrazeShorterNarrow-BoldItalic.otf \
	GrazeShorterNarrow-Italic.otf 
FONTSW_GRAZESHORTERNARROW=\
	GrazeShorterNarrow.woff2 \
	GrazeShorterNarrow-Bold.woff2 \
	GrazeShorterNarrow-BoldItalic.woff2 \
	GrazeShorterNarrow-Italic.woff2 

default: $(PDF)

.NOTINTERMEDIATE: meh

%.pdf : %.tex $(PDFDEPS) $(FONTS_GRAZESHORTER)
	xelatex $< </dev/null 
	grep myrearmatter -A3 < $< | grep -P '^\s*\\mypageiii' || xelatex $< </dev/null  # just run it again, for the TOC, because CPU is cheap

%.txt : %.pdf
	pdftotext -layout $<
	@grep -5 LATEX $@
	@echo "Hypehation: ` grep -P '[-]' $@ | grep -vw page | grep -Po '[-]' | wc -l `"

english.tex: gentex-english.py
	./gentex-english.py english.tex

clean:
	find . -maxdepth 1 '(' -name '*.aux' -o -name '*.pages' -o -name '*.section' -o -name '*.log' -o -name '*.toc' -o -name '*.dvi' -o -name '*.ps' ')' -print0 | xargs -0 rm

generated.tex: gentex.py
	./gentex.py generated.tex

bibl2.pdf: bibl2.tex generated.tex
	xelatex bibl2.tex < /dev/null

bibl.pdf: bibl.tex
	xelatex bibl.tex < /dev/null

# Make book signatures - the 28 here is 28 x 1/72" ≅ 10mm
# See also https://softwarerecs.stackexchange.com/questions/438/software-to-put-pages-of-a-pdf-file-in-book-order
%-book.pdf: %.pdf
	# pdfbook2 --no-crop --paper=a4paper --outer-margin=28 --inner-margin=0 --top-margin=0 --bottom-margin=0 --signature=40 $<
	pdfbook2 --no-crop --paper=a4paper --outer-margin=18 --inner-margin=0 --top-margin=15 --bottom-margin=14 --signature=4 $<
	# pdfbook2 --paper=a4paper --outer-margin=18 --inner-margin=0 --top-margin=15 --bottom-margin=14 --signature=4 $<

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
	pdfbook2 --no-crop --paper=a4paper --outer-margin=10 --inner-margin=0 --top-margin=8 --bottom-margin=7 --signature=32 $(basename $<)-u.pdf


fonts: $(FONTS)

%.woff2: %.sfd
	fontforge -c 'open(argv[1]).generate(argv[2])' $< $@
%.otf: %.sfd
	fontforge -c 'open(argv[1]).generate(argv[2])' $< $@

%.ttf: %.sfd
	fontforge -c 'open(argv[1]).generate(argv[2])' $< $@

# Deploy the font on the X server (cool way to crash programs)
fontinst: $(FONTS_GRAZESHORTER) $(FONTS_GRAZESHORTERNARROW)
	rsync --info=stats0,flist1 -av $(FONTS_GRAZESHORTER) $(FONTS_GRAZESHORTERNARROW) $(HOME)/.fonts/ 
	fc-cache -f $(HOME)/.fonts

otf: $(FONTS_GRAZESHORTER) $(FONTS_GRAZESHORTERNARROW) 

woff2: $(FONTSW_GRAZESHORTER) $(FONTSW_GRAZESHORTERNARROW) 

fonts: fontzip

fontzip: GrazeShorter.zip GrazeShorterNarrow.zip

GrazeShorter.zip: $(FONTSW_GRAZESHORTER) $(FONTS_GRAZESHORTER) README.fonts copyright
	zip $@ $(FONTS_GRAZESHORTER) $(FONTSW_GRAZESHORTER) README.fonts copyright

GrazeShorterNarrow.zip: $(FONTSW_GRAZESHORTERNARROW) $(FONTS_GRAZESHORTERNARROW) README.fonts copyright
	zip $@ $(FONTS_GRAZESHORTERNARROW) $(FONTSW_GRAZESHORTERNARROW) README.fonts copyright

.PRECIOUS: %.pdf

