# Printable KJV

The general goal of this project is to provide a framework for a compact printed KJV.  Having the framework allows various printings of the Bible, tuned for economy and printing constraints (e.g. larger margin for perfect binding).  

The project consists of these components:

* xelatex layout files
* python script to parse Bible text and add latex markup.
* custom fonts (Graze Shorter, based on Charis SIL)
* Makefile
* Downloadable PDFs

Goals:
 * all text and no commentary (no tendentious notes, etc)
 * minimum cost: ie. most efficient use of page space, fewest number of pages
 * made for reading: i.e. the fewest possible intrusions into the text.

Specific features to reduce length and print cost:
* Verses continue on the same line.  This reflects the form of the original (no verse divisions), and encourages regular reading over proof-texting.
*  Over 31k verses with random lengths, this shortens the print by around 14k lines, and at 110 lines per page, that's 127 pages or so saved. * Embedded verse numbers (these are printed in a smaller font, and raised, so that they are visually distinct.
* No paragraph headings: these both tend to be tendentious (adj. having or showing a definite tendency, bias, or purpose), and take up print space
* Chapter numbers use drop-caps
* New books of the Bible start on same page as the previous book ended (66 books that don't start on a new page should save around 30 pages)
*  no maps (yes, those are indeed on the end papers, but you don't have to print them, you know, and not printing saves)
* Acrostic psalms (ps 119) has just the Hebrew letter.

Other features:
* No paragraph titles (same as headings: they tend to be wrong and unhelpfil)
* Print table of contents block down outer margin to identify signature selection errors. This is a nondescript little black block ... a shade of grey might be better ...

## Tradeoffs in printing:

Margins
 * 7mm all around is about as small as you can go.
 * The inner margin must be bigger if the binding is not flat
 * TODO: It would be nice to make the inner margin 7mm on the left page, and the inner margin 10mm on the left page, to make use of the ragged right, which generally does not reach the end of the block

Page size
 * Larger page size means fewer pages, therefore less binding, fewer headers
 * Larger page size means longer line, therefore more efficiency in wrapping
 * Wider than A5 page size starts to become unwieldy
> The largest practical paper size should be used








Text size
 * 10pt seems nice, but it seems that 8.5pt might be an acceptable minimum
 > This is very subjective

Inter-line spacing
 * For the Charis SIL font, reducing the inter-line spacing to 90% of the point size makes the capitals run into the descenders of the letters **ypjq** that hang down from the line
 * Generally having the point size the same as the line spacing works best. (That's at least with the Charis SIL font).  
 * Generally the space between the words should be the same as the height of the letters with no tails, acemnorsuvwxz
 > Minimum line spacing

Ragged vs justified
 * Ragged seems to turn off hyphenation, so it is a small loss in efficiency
 * Justified makes a block that needs a column separation of 1.5em, or a line.  With ragged you can do 1em colum separation.
 > Ragged seems nicer

Kerning
 * If the font is not kerned for lower case letters, then it's best to edit the font.  Adjusting the inter-character space is crude, and it works, but it's not ideal.


## METRICS OF OTHER BIBLES

### KJV Hard cover
    pages=1357 (genesis to revelation)
    top-margin=14mm 
    heading-height=3mm
    outer-margin=9mm
    inner-margin=10mm
    bottom-margin=9mm
    ragged-right
    psalms-blank-lines
    lines-per-page=47
    text-height=157mm
    line-spacing=157/47mm=9.5pt
    # height-of-ph-to-inter-line-spacing=39:27
    height-of-ph-to-inter-line-spacing=37:44
    text-height-p-h=9.5pt/44*37=8.0pt (8.5pt declared)

### ESV soft cover
    pages=1042 (genesis to revelation)
    top-space=16mm (from top of page to main text)
    top-margin=9mm (from top of page to heading printing)
    heading-height=3mm (height of heading)
    outer-margin=9mm
    inner-margin=13mm
    bottom-space=7mm (footnotes on every page)
    bottom-margin=13mm (footnotes on every page)
    footnote-height=1.5mm 
    ragged-right
    psalms-blank-lines
    lines-per-page=53
    text-height=185mm
    line-spacing=185/53mm=9.9pt
    height-of-ph-to-inter-line-spacing=38:49
    text-height-p-h=7.7pt (font size)

### Christian art large print
    pages=1739 (genesis to revelation)
    page-height=245mm
    page-width=132mm
    top-space=16mm (from top of page to main text)
    top-margin=7mm (from top of page to heading printing)
    heading-height=3mm (height of heading)
    outer-margin=8mm
    inner-margin=9mm
    bottom-space=14mm (footnotes on every page)
    bottom-margin=6mm (footnotes on every page)
    footnote-height=2mm 
    justified
    psalms-verse-per-line
    lines-per-page=38
    text-height=182mm
    line-spacing=182/38mm=13.5pt
    height-of-ph-to-inter-line-spacing=40:44
    text-height-ph=12.2pt (font size)

### Christian art standard print
    pages=985 (genesis to revelation)
    page-height=220mm
    page-width=133mm
    top-space=18 (from top of page to main text)
    top-margin=14mm (from top of page to heading printing)
    heading-height=3mm (height of heading)
    outer-margin=6mm
    inner-margin=9mm
    bottom-space=14mm (no footnotes)
    bottom-margin=14mm (no footnotes)
    footnote-height=0mm 
    justified
    verse-per-line
    lines-per-page=59
    text-height=177mm
    line-spacing=177/59=3mm=8.5pt
    height-of-ph-to-inter-line-spacing=22:24
    text-height-ph=7.8pt (font size)
    little-o-aspect-ratio=10:11

### Holman Gift & Award
    pages=759
    page-height=216mm
    page-width=135mm
    top-space=10mm (from top of page to main text)
    top-margin=6mm (from top of page to heading printing)
    heading-height=2mm (height of heading)
    outer-margin=5mm
    inner-margin=10mm
    bottom-space=8mm
    bottom-margin=0mm (no footnotes)
    footnote-height=0mm (no footnotes)
    psalms-verse-per-line
    lines-per-page=73
    text-height=mm
    line-spacing=193/73mm==7.5pt
    height-of-ph-to-inter-line-spacing=20:21
    text-height-ph=7.1pt (font size)
    justified
    perfect-binding
    endless-headings

### Africa marked edition 
(generous spacing, large margins)
    pages=1147=878+269 (OT+NT)
    page-height=200mm
    page-width=135mm
    top-space=15mm (from top of page to main text)
    top-margin=10mm (from top of page to heading printing)
    heading-height=3mm (height of heading)
    outer-margin=13mm
    inner-margin=15mm
    bottom-space=15mm
    bottom-margin=11mm
    footnote-height=4mm (page number)
    psalms-verse-per-line
    lines-per-page=59
    text-height=167mm
    line-spacing=167mm/59==8.02pt
    height-of-ph-to-inter-line-spacing=37:40
    text-height-ph=7.4pt (font size)
    justified
    perfect-binding
    header-topics
    ragged-right
    column-separation=2mm (incl line)

### Waterproof bible
For this paper size and similar margins, we can do 707 pages: CharisSIL 9.0pt text, line spacing 9.5pt, scaled 0.86

    pages=705
    page-height=221mm
    page-width=148mm
    top-space=13mm (from top of page to main text)
    top-margin=7mm (from top of page to heading printing)
    heading-height=3mm (height of heading, incl line)
    outer-margin=7mm 
    inner-margin=15mm
    bottom-space=8mm
    bottom-margin=8mm
    footnote-height=0mm (no footer)
    psalms-verse-per-line
    lines-per-page=74
    text-height=201mm
    line-spacing=201mm/74==7.7pt 
    height-of-ph-to-inter-line-spacing=34:36
    text-height-ph=7.27pt (font size)
    justified
    perfect-binding
    no-italics
    column-separation=3mm (no line)

## ERRATA:
 * DONE: Handling of Psalm 119 ALEPH to TETH to JOD - replace with hebrew letters?  Give own line, italics?
 * Handling if 2nd verse indent for PSALMS (not done: just cancelled indent) (DONE)

## Checklist after layout adjustment:
*    Psalm 119: check that paragraph breaks and Hebrew names appear
*    Psalm 121: check psalm title and first verse are distinct (check italics, indent/ line break)
*    Table of contents: check that it appears (run xelatex twice)
*        Check that "Song of Solomon" and "2 Thessalonians" don't look ugly (e.g. wrapped badly)
### Layout:
* Verse numbering: check for collision with descender (e.g. g and j), or below top of ascender
* Check for "overfull vbox" in xelatex log file for the job, and inspect each page and neighbouring pages for every report
### Fonts:
*        Check font kerning: "Avith" in 1 Chronicles 1:46 - A and V should kern. Charis SIL does not include kerning, unless you edit it!
*        Check that bold fonts do appear (verse numbers, headings)
*        Check that italic fonts do appear (italicised words)
### Appearance:
* Check register-true (text on front and back of page should be on the same line)
### Layout:
* After psalm title indentation
* Verse 2 of psalms indentation

# Afrikaans

The 1953 edition of the Afrikaans Bible is derived from the Dutch Staatenvertaling, and thereby on the received text.  While it does include some poor original scholarship, it is currently the best Afrikaans translation.  Also, it is out of copyright.  **af.tex** and **af.pdf** are an 800 page large print (giant print?) Bible that you can print on a duplex printer with spiral binding.

## Afrikaans-specific checklist:

These are the specific additional check items for Afrikaans:

* Font overruns on accented letters, especially capitals in 1 Chronicles.  Add 0.5pt to 1pt to line spacing to resolve.
* Font kerning, for words like "Kyk"
* Handling of CAPITAL leading verse
* Psalm titles in italics
* Alef. Bet. rewritten (or handled) in Lamentations, Proverbs and Psalms

