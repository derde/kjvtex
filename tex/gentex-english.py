#! /usr/bin/python3
# coding: utf-8
import os

romannumerals=[ '', 'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix',
    'x', 'xi', 'xii', 'xiii', 'xiv', 'xv', 'xvi', 'xvii', 'xviii', 'xix', 'xx',
    'xxi', 'xxii', 'xxiii', 'xxiv', 'xxv', 'xxvi', 'xxvii', 'xxviii', 'xxix',
    'xxx', 'xxxi', 'xxxii', 'xxxiii', 'xxxiv', 'xxxv', 'xxxvi', 'xxxvii',
    'xxxviii', 'xxxix', 'xl', 'xli', 'xlii', 'xliii', 'xliv', 'xlv', 'xlvi',
    'xlvii', 'xlviii', 'xlix', 'l', 'li', 'lii', 'liii', 'liv', 'lv', 'lvi',
    'lvii', 'lviii', 'lix', 'lx', 'lxi', 'lxii', 'lxiii', 'lxiv', 'lxv', 'lxvi',
    'lxvii', 'lxviii', 'lxix', 'lxx', 'lxxi', 'lxxii', 'lxxiii', 'lxxiv', 'lxxv',
    'lxxvi', 'lxxvii', 'lxxviii', 'lxxix', 'lxxx', 'lxxxi', 'lxxxii', 'lxxxiii',
    'lxxxiv', 'lxxxv', 'lxxxvi', 'lxxxvii', 'lxxxviii', 'lxxxix', 'xc', 'xci',
    'xcii', 'xciii', 'xciv', 'xcv', 'xcvi', 'xcvii', 'xcviii', 'xcix', 'c', 'ci',
    'cii', 'ciii', 'civ', 'cv', 'cvi', 'cvii', 'cviii', 'cix', 'cx', 'cxi', 'cxii',
    'cxiii', 'cxiv', 'cxv', 'cxvi', 'cxvii', 'cxviii', 'cxix', 'cxx', 'cxxi',
    'cxxii', 'cxxiii', 'cxxiv', 'cxxv', 'cxxvi', 'cxxvii', 'cxxviii', 'cxxix',
    'cxxx', 'cxxxi', 'cxxxii', 'cxxxiii', 'cxxxiv', 'cxxxv', 'cxxxvi', 'cxxxvii',
    'cxxxviii', 'cxxxix', 'cxl', 'cxli', 'cxlii', 'cxliii', 'cxliv', 'cxlv',
    'cxlvi', 'cxlvii', 'cxlviii', 'cxlix', 'cl', ]

# DISCLAIMER: this code is torturous, because it is hacked from code for making
# a side-by-side parallel Bible, which needs a lot of bad hacks.  I'm sorry.
# Don't write your own code like this.  Be better.
# 
# And although it's called English, it seems to be doing Afrikaans too now.
# Weird.
#
# Inputs:
#   ../af1953.txt, ../TEXT-PCE-127.txt : source text
#   1526.Pericopes.csv : paragrah division list
#   afrikaans.renumbering: list of verses with variant numbering
#   hebrew-words: list of hebrew words in the text; to replace things like ALEPH. wih the character
#   afrikaans.psalmtitles: list of substrings that represent the psalm titles
# Outputs:
#   english.tex
#   afrikaans.tex
# Processing:
#   Section headings (OT, NT)
#   Chapter headings
#   Afrikaans: lowercase paragraphs
#   Verse numbers
#   Paragraph breaks
#   Italics for [ .. ]  text
#   End notes for books processing
#   Smallcaps for "LORD" (and HERE)

import re
import itertools
import sys,copy

class Hebrew:
    "Hebrew rewrites"
    def __init__(self,file='hebrew-words'):
        fd=open(file,'r')
        self.lookup={}
        self.latin2utf8={}
        for line in fd:
            bits=line.strip().split('\t')
            if len(bits)<4:
                ref=bits[0]
                self.lookup[ref]=None
            else:
                ref,heLatin,uni,heUtf8=bits[:4]
                if not heLatin.endswith(' '): heLatin+=' ';
                self.lookup[ref]={ 'heLatin': heLatin, 'ref':ref, 'heUtf8':heUtf8 }
                self.latin2utf8[heLatin]=heUtf8
    def adjust(self,text,p):
        if p['book'] in ( "Psalms", "Spreuke", "Klaagliedere"):
            if p['sourcereference'] in self.lookup:
                for heLatin,heUtf8 in self.latin2utf8.items():
                    if text.find(heLatin)>=0:
                        text=text.replace(heLatin,r'\hebrewinfix{%s}' % heUtf8)
        return text

class English:
    bookfullnamesEn = {
        'Ge'   : 'Genesis',
        'Ex'   : 'Exodus',
        'Le'   : 'Leviticus',
        'Nu'   : 'Numbers',
        'De'   : 'Deuteronomy',
        'Jos'  : 'Joshua',
        'Jg'   : 'Judges',
        'Ru'   : 'Ruth',
        '1Sa'  : '1 Samuel',
        '2Sa'  : '2 Samuel',
        '1Ki'  : '1 Kings',
        '2Ki'  : '2 Kings',
        '1Ch'  : '1 Chronicles',
        '2Ch'  : '2 Chronicles',
        'Ezr'  : 'Ezra',
        'Ne'   : 'Nehemiah',
        'Es'   : 'Esther',
        'Job'  : 'Job',
        'Ps'   : 'Psalms',
        'Pr'   : 'Proverbs',
        'Ec'   : 'Ecclesiastes',
        'Song' : 'Song of Solomon',
        'Isa'  : 'Isaiah',
        'Jer'  : 'Jeremiah',
        'La'   : 'Lamentations',
        'Eze'  : 'Ezekiel',
        'Da'   : 'Daniel',
        'Ho'   : 'Hosea',
        'Joe'  : 'Joel',
        'Am'   : 'Amos',
        'Ob'   : 'Obadiah',
        'Jon'  : 'Jonah',
        'Mic'  : 'Micah',
        'Na'   : 'Nahum',
        'Hab'  : 'Habakkuk',
        'Zep'  : 'Zephaniah',
        'Hag'  : 'Haggai',
        'Zec'  : 'Zechariah',
        'Mal'  : 'Malachi',
        'Mt'   : 'Matthew',
        'Mr'   : 'Mark',
        'Lu'   : 'Luke',
        'Joh'  : 'John',
        'Ac'   : 'Acts',
        'Ro'   : 'Romans',
        '1Co'  : '1 Corinthians',
        '2Co'  : '2 Corinthians',
        'Ga'   : 'Galatians',
        'Eph'  : 'Ephesians',
        'Php'  : 'Philippians',
        'Col'  : 'Colossians',
        '1Th'  : '1 Thessalonians',
        '2Th'  : '2 Thessalonians',
        '1Ti'  : '1 Timothy',
        '2Ti'  : '2 Timothy',
        'Tit'  : 'Titus',
        'Phm'  : 'Philemon',
        'Heb'  : 'Hebrews',
        'Jas'  : 'James',
        '1Pe'  : '1 Peter',
        '2Pe'  : '2 Peter',
        '1Jo'  : '1 John',
        '2Jo'  : '2 John',
        '3Jo'  : '3 John',
        'Jude' : 'Jude',
        'Re'   : 'Revelation',
    }
    def __init__(self,file='english.psalmtitles', numberfile='english.renumbering'):
        self.bookFullnames=self.bookfullnamesEn
        self.oldtestament="THE OLD TESTAMENT"
        self.newtestament="THE NEW TESTAMENT"
        pass
    def renumberreference(self,ref):
        return ref
    def markuppsalmheadings(self,text,state):
        return text
    def getbookprettyname(self,book):
        return book

class Afrikaans:
    af_lowercase={
        '??': '??',
        '??': '??',
        '??': '??',
        '??': '??',
        '??': '??',
        '??': '??',
        '??': '??',
        '??': '??',
    }
    af_wordmap={
        'D??T'        :   'D??t',
        'GESE??ND'    :   'Gese??nd',
        'JEHISK??A'   :   'Jehisk??a',
        'JOS??A'      :   'Jos??a',
        'L??'         :   'L??',
        'N??'         :   'N??',
        'NASAR??NER'  :   'Nasar??ner',
        'SAMAR??A'    :   'Samar??a',
        'SEDEK??A'    :   'Sedek??a',
        'S??MEON'     :   'S??meon',
        'SJIGGAJ??N'  :   'Sjiggaj??n',
        'VANWE??'     :   'Vanwe??',
    }
    bookFullnamesAf={
        'Gn'   :  'Genesis',
        'Ex'   :  'Exodus',
        'Lv'   :  'Levitikus',
        'Nu'   :  'Numeri',
        'Dt'   :  'Deuteronomium',
        'Jos'  :  'Josua',
        'Rgt'  :  'Rigters',
        'Rut'  :  'Rut',
        '1Sa'  :  '1 Samuel',
        '2Sa'  :  '2 Samuel',
        '1Ko'  :  '1 Konings',
        '2Ko'  :  '2 Konings',
        '1Kr'  :  '1 Kronieke',
        '2Kr'  :  '2 Kronieke',
        'Esr'  :  'Esra',
        'Neh'  :  'Nehemia',
        'Est'  :  'Ester',
        'Job'  :  'Job',
        'Ps'   :  'Psalms',
        'Spr'  :  'Spreuke',
        'Prd'  :  'Prediker',
        'Hgl'  :  'Hooglied',
        'Js'   :  'Jesaja',
        'Je'   :  'Jeremia',
        'Klg'  :  'Klaagliedere',
        'Es'   :  'Esegiel',
        'Dn'   :  'Daniel',
        'Hs'   :  'Hosea',
        'Jl'   :  'Joel',
        'Am'   :  'Amos',
        'Ob'   :  'Obadja',
        'Jna'  :  'Jona',
        'Mg'   :  'Miga',
        'Nh'   :  'Nahum',
        'Hb'   :  'Habakuk',
        'Sf'   :  'Sefanja',
        'Hg'   :  'Haggai',
        'Sg'   :  'Sagaria',
        'Ml'   :  'Maleagi',
        'Mt'   :  'Mattheus',
        'Mk'   :  'Markus',
        'Lk'   :  'Lukas',
        'Jo'   :  'Johannes',
        'Hnd'  :  'Handelinge',
        'Rom'  :  'Romeine',
        '1Ko'  :  '1 Korinthiers',
        '2Ko'  :  '2 Korinthiers',
        'Gal'  :  'Galasiers',
        'Ef'   :  'Efesiers',
        'Fil'  :  'Filippense',
        'Kol'  :  'Kolossense',
        '1Th'  :  '1 Thessalonicense',
        '2Th'  :  '2 Thessalonicense',
        '1Ti'  :  '1 Timotheus',
        '2Ti'  :  '2 Timotheus',
        'Tit'  :  'Titus',
        'Flm'  :  'Filemon',
        'Heb'  :  'Hebreers',
        'Jak'  :  'Jakobus',
        '1Pt'  :  '1 Petrus',
        '2Pt'  :  '2 Petrus',
        '1Jo'  :  '1 Johannes',
        '2Jo'  :  '2 Johannes',
        '3Jo'  :  '3 Johannes',
        'Jud'  :  'Judas',
        'Opn'  :  'Openbaring',
    }
    booknamesAccented ={
        'Genesis'              : ['G??NESIS'            ,'G??nesis'             ],
        'Exodus'               : ['EXODUS'             ,'Exodus'              ],
        'Levitikus'            : ['LEV??TIKUS'          ,'Lev??tikus'           ],
        'Numeri'               : ['N??MERI'             ,'N??meri'              ],
        'Deuteronomium'        : ['DEUTERON??MIUM'      ,'Deuteron??mium'       ],
        'Josua'                : ['JOSUA'              ,'Josua'               ],
        'Rigters'              : ['RIGTERS'            ,'Rigters'             ],
        'Rut'                  : ['RUT'                ,'Rut'                 ],
        '1 Samuel'             : ['I SAMUEL'           ,'I Samuel'            ],
        '2 Samuel'             : ['II SAMUEL'          ,'II Samuel'           ],
        '1 Konings'            : ['I KONINGS'          ,'I Konings'           ],
        '2 Konings'            : ['II KONINGS'         ,'II Konings'          ],
        '1 Kronieke'           : ['I KRONIEKE'         ,'I Kronieke'          ],
        '2 Kronieke'           : ['II KRONIEKE'        ,'II Kronieke'         ],
        'Esra'                 : ['ESRA'               ,'Esra'                ],
        'Nehemia'              : ['NEHEM??A'            ,'Nehem??a'             ],
        'Ester'                : ['ESTER'              ,'Ester'               ],
        'Job'                  : ['JOB'                ,'Job'                 ],
        'Psalms'               : ['PSALMS'             ,'Psalms'              ],
        'Spreuke'              : ['SPREUKE'            ,'Spreuke'             ],
        'Prediker'             : ['PREDIKER'           ,'Prediker'            ],
        'Hooglied'             : ['HOOGLIED'           ,'Hooglied'            ],
        'Jesaja'               : ['JESAJA'             ,'Jesaja'              ],
        'Jeremia'              : ['JEREMIA'            ,'Jeremia'             ],
        'Klaagliedere'         : ['KLAAGLIEDERE'       ,'Klaagliedere'        ],
        'Esegiel'              : ['ES??GI??L'            ,'Es??gi??l'             ],
        'Daniel'               : ['DANI??L'             ,'Dani??l'              ],
        'Hosea'                : ['HOS??A'              ,'Hos??a'               ],
        'Joel'                 : ['JO??L'               ,'Jo??l'                ],
        'Amos'                 : ['AMOS'               ,'Amos'                ],
        'Obadja'               : ['OB??DJA'             ,'Ob??dja'              ],
        'Jona'                 : ['JONA'               ,'Jona'                ],
        'Miga'                 : ['MIGA'               ,'Miga'                ],
        'Nahum'                : ['NAHUM'              ,'Nahum'               ],
        'Habakuk'              : ['H??BAKUK'            ,'H??bakuk'             ],
        'Sefanja'              : ['SEF??NJA'            ,'Sef??nja'             ],
        'Haggai'               : ['HAGGAI'             ,'Haggai'              ],
        'Sagaria'              : ['SAGAR??A'            ,'Sagar??a'             ],
        'Maleagi'              : ['MALE??GI'            ,'Male??gi'             ],
        'Mattheus'             : ['MATTH????S'           ,'Matth????s'            ],
        'Markus'               : ['MARKUS'             ,'Markus'              ],
        'Lukas'                : ['LUKAS'              ,'Lukas'               ],
        'Johannes'             : ['JOHANNES'           ,'Johannes'            ],
        'Handelinge'           : ['HANDELINGE'         ,'Handelinge'          ],
        'Romeine'              : ['ROMEINE'            ,'Romeine'             ],
        '1 Korinthiers'        : ['I KORINTHI??RS'      ,'I Korinthi??rs'       ],
        '2 Korinthiers'        : ['II KORINTHI??RS'     ,'II Korinthi??rs'      ],
        'Galasiers'            : ['GAL??SI??RS'          ,'Gal??si??rs'           ],
        'Efesiers'             : ['EF??SI??RS'           ,'Ef??si??rs'            ],
        'Filippense'           : ['FILIPPENSE'         ,'Filippense'          ],
        'Kolossense'           : ['KOLOSSENSE'         ,'Kolossense'          ],
        '1 Thessalonicense'    : ['I THESSALONICENSE'  ,'I Thessalonicense'   ],
        '2 Thessalonicense'    : ['II THESSALONICENSE' ,'II Thessalonicense'  ],
        '1 Timotheus'          : ['I TIM??THE??S        ','I Tim??the??s         '],
        '2 Timotheus'          : ['II TIM??THE??S'       ,'II Tim??the??s'        ],
        'Titus'                : ['TITUS'              ,'Titus'               ],
        'Filemon'              : ['FIL??MON'            ,'Fil??mon'             ],
        'Hebreers'             : ['HEBRE??RS'           ,'Hebre??rs'            ],
        'Jakobus'              : ['JAKOBUS'            ,'Jakobus'             ],
        '1 Petrus'             : ['I PETRUS'           ,'I Petrus'            ],
        '2 Petrus'             : ['II PETRUS'          ,'II Petrus'           ],
        '1 Johannes'           : ['I JOHANNES'         ,'I Johannes'          ],
        '2 Johannes'           : ['II JOHANNES'        ,'II Johannes'         ],
        '3 Johannes'           : ['III JOHANNES'       ,'III Johannes'        ],
        'Judas'                : ['JUDAS'              ,'Judas'               ],
        'Openbaring'           : ['OPENBARING'         ,'Openbaring'          ],
    }

    def __init__(self,file='afrikaans.psalmtitles', numberfile='afrikaans.renumbering'):
        # Hebrew letter, prefix, capitalised-word
        self.titlecasewl=re.compile(r"^([A-Z][a-z]+\. )?(???n |O |O, )?([-A-Z????????????????]{2,})(.*)")
        self.titlecasebl=re.compile(r"^([A-Z][a-z]+\. )?(???n |O, )?(HERE)")
        self.bookFullnames=self.bookFullnamesAf
        self.oldtestament="DIE OU TESTAMENT"
        self.newtestament="DIE NUWE TESTAMENT"
        fd=open(file,'r')
        splitreftext_re=re.compile('(^[^:]*:[^ ]*) (.*)')
        self.titles={}
        for line in fd:
            m=splitreftext_re.search(line)
            if not m: continue
            self.titles[m.group(1)]=m.group(2)

        self.aftoen={}
        self.entoaf={}
        fd=open(numberfile,'r')
        for line in fd:
            en,af=line.strip().split('\t',1)
            self.aftoen[af]=en
            self.aftoen[en]=af
    def getbookprettyname(self,book):
        return self.booknamesAccented[book][1]
    def renumberreference(self,ref):
        # Rewrite references
        ref= self.aftoen.get(ref,ref)
        return ref
    def paragraphcapstotitlecase(self,text):
        '''Convert capitals to titlecase'''
        m=self.titlecasewl.search(text)
        if m and not self.titlecasebl.search(text):
            # Change to titlecase - UTF8 stuff just works, it seems:
            text=''
            if m.group(1): text+=m.group(1)
            if m.group(2): text+=m.group(2)
            text+=m.group(3).title()+m.group(4)
        return text
    def markuppsalmheadings(self,text,state):
        ref=state['sourcereference'];
        if ref in self.titles:
            heading=self.titles[ref]
            text=text.replace(heading,r'\biblepsalmheading{'+self.paragraphcapstotitlecase(heading)+'}')
        else:
            text=self.paragraphcapstotitlecase(text)
        return text

class paragraphdivisions:
    def staticdata(self):
        self.paragraphs={}
        self.bookmapdata='''\
GEN      : Genesis         :  Genesis 
EXOD     : Exodus          :  Exodus 
LEV      : Leviticus       :  Levitikus 
NUM      : Numbers         :  Numeri 
DEUT     : Deuteronomy     :  Deuteronomium 
JOSH     : Joshua          :  Josua 
JUDG     : Judges          :  Rigters 
RUTH     : Ruth            :  Rut 
1SAM     : 1 Samuel        :  1 Samuel 
2SAM     : 2 Samuel        :  2 Samuel 
1KGS     : 1 Kings         :  1 Konings 
2KGS     : 2 Kings         :  2 Konings 
1CHRON   : 1 Chronicles    :  1 Kronieke 
2CHRON   : 2 Chronicles    :  2 Kronieke 
EZRA     : Ezra            :  Esra 
NEH      : Nehemiah        :  Nehemia 
ESTH     : Esther          :  Ester 
JOB      : Job             :  Job 
PS       : Psalms          :  Psalms 
PROV     : Proverbs        :  Spreuke 
ECC      : Ecclesiastes    :  Prediker 
SONG     : Song of Solomon :  Hooglied 
ISA      : Isaiah          :  Jesaja 
JER      : Jeremiah        :  Jeremia 
LAM      : Lamentations    :  Klaagliedere 
EZEK     : Ezekiel         :  Esegiel 
DAN      : Daniel          :  Daniel 
HOSEA    : Hosea           :  Hosea 
JOEL     : Joel            :  Joel 
AMOS     : Amos            :  Amos 
OBAD     : Obadiah         :  Obadja 
JONAH    : Jonah           :  Jona 
MICAH    : Micah           :  Miga 
NAHUM    : Nahum           :  Nahum 
HAB      : Habakkuk        :  Habakuk 
ZEPH     : Zephaniah       :  Sefanja 
HAG      : Haggai          :  Haggai 
ZECH     : Zechariah       :  Sagaria 
MAL      : Malachi         :  Maleagi 
MATT     : Matthew         :  Mattheus 
MARK     : Mark            :  Markus 
LUKE     : Luke            :  Lukas 
JOHN     : John            :  Johannes 
ACTS     : Acts            :  Handelinge 
ROM      : Romans          :  Romeine 
1COR     : 1 Corinthians   :  1 Korinthiers 
2COR     : 2 Corinthians   :  2 Korinthiers 
GAL      : Galatians       :  Galasiers 
EPH      : Ephesians       :  Efesiers 
PHIL     : Philippians     :  Filippense 
COL      : Colossians      :  Kolossense 
1THES    : 1 Thessalonians :  1 Thessalonicense 
2THES    : 2 Thessalonians :  2 Thessalonicense 
1TIM     : 1 Timothy       :  1 Timotheus 
2TIM     : 2 Timothy       :  2 Timotheus 
TITUS    : Titus           :  Titus 
PHILEM   : Philemon        :  Filemon 
HEB      : Hebrews         :  Hebreers 
JAS      : James           :  Jakobus 
1PET     : 1 Peter         :  1 Petrus 
2PET     : 2 Peter         :  2 Petrus 
1JOHN    : 1 John          :  1 Johannes 
2JOHN    : 2 John          :  2 Johannes 
3JOHN    : 3 John          :  3 Johannes 
JUDE     : Jude            :  Judas 
REV      : Revelation      :  Openbaring'''

    def __init__(self,file,language):
        self.language=language
        self.staticdata()
        self.bookmap=[]
        for line in self.bookmapdata.split('\n'):
            bits=re.split(' *: *',line.strip())
            if len(bits)==3:
                self.bookmap.append(bits)

        self.refs={}
        fd=open(file,'r')
        line1=fd.readline()
        self.headings=line1.strip('\n').split('\t')
        verse_range_i = self.headings.index('Verse Range')
        for line in fd:
            if line.startswith("#"): continue
            bits=line.strip('\n').split('\t')
            if len(bits)==1:
                r=bits[0].split()
                book=r[0]
                chapter=r[1].split(':')[0]
                for ref in r[1:]:
                    verse=ref.split(':')[-1]
                    self.addparagraph('dummy '+book+' '+chapter+':'+verse)
            else:
                self.addparagraph(bits[verse_range_i])

    def bookmaplookup(self,srccol,dstcol,value):
        for r in self.bookmap:
            if r[srccol]==value: return r[dstcol]
        return ''

    def addparagraph(self,refs):
        '''Add to the list'''
        m=re.search('(\S+) (\d+:\d+)',refs)
        chapterandverse = m.group(2)
        book = self.bookmaplookup(0,1,m.group(1))
        ref1 = book+' '+chapterandverse
        #if ref1.startswith('Psalms'): ref1='Psalm '+ref1.split()[-1]
        ref1 = self.language.renumberreference(ref1)
        self.paragraphs[ref1] = True
        # Make it a paragraph for all the other forms and languages too:
        
        for mapentry in self.bookmapdata:
            if book in (mapentry):
                for b in mapentry:
                    self.paragraphs[book+' '+chapterandverse] = True

        # if nref1!=ref1 or nref2!=ref2: print(ref1,ref2,"=>",nref1,nref2)

    def isparagraphdivision(self,ref):
        return ref in self.paragraphs
        

class bibleformatter:
    paragraph_wl_re=re.compile(r"^([A-Z][a-z]+\. )?(???n |O |O, )?([-A-Z????????????????]{2,})(.*)")
    paragraph_bl_re=re.compile(r"\bHERE\b")
    # These are the particular things that appear in the AFrikaans: we don't actually like that leading capital
    # python seems to have these already ... not sure what we're doing here ...
    def __init__(self,language,file):
        self.language=language;
        self.hebrew=Hebrew()
        self.state={
            'book': '',
            'chapter': '',
            'chapter': '', }
        self.paragraphdivisions=paragraphdivisions('1526.Pericopes.csv', self.language)
        self.markheading=r'\markright';
        self.fd=file
        self.shortnames={}
        for k,v in self.language.bookFullnames.items():
            self.shortnames[v]=k

    def booktochapters(self):
        '''Read in the bible file, and parse to book, chapter, verse and text'''
        lineformat_re=re.compile('(.*?) (\d+):(\d+) (.*)')
        for line in self.fd:
            if line.startswith("Source:"): continue
            m=lineformat_re.search(line.strip())
            book,chapter,verse,text=m.groups()
            book=self.language.bookFullnames.get(book,book)
            yield book,chapter,verse,text

    def chapternumber(self,book,chapter, one_chapter=False):
        # Generate  chapter numbers for each book
        o='';
        if chapter=='1':
            if book in ('Obadiah','Philemon','2 John','3 John','Jude'):
                return o+self.verseheading('1') #  + '\n';
        o+=r'\bibldropcapschapter{'+chapter+'}' + '%\n' 
        # o+=self.verseheading('1') + '%\n'
        return o

    def verseheading(self,verse):
        # r+=  r'\verse{'+verse+'}'  
        cmd='\\verse'
        if verse=='1': cmd=r'\versei' # no space before 1st verse
        elif verse=='2': cmd=r' \verseii' # space before 2nd verse
        else: cmd=r' \verse' # space before verses 3 and on
        return r''+cmd+'{'+verse+'}{'+str(self.state['index'])+'}'

    def isnewparagraph(self,book,chapter,verse,text):
        # Afrikaans text has capital words indicating new paragraphs
        #if book.startswith('Psa'):
        #    return True;
        # FIXME: Afrikaans books need verse number adjustments
        # if book.startswith("Psalm"): return True
        ref = book+' '+chapter+':'+verse
        if verse in ('1','2','3'): return False
        isnew=False
        if self.language==afrikaans:
            isnew = isnew or (self.paragraph_wl_re.search(text) and not self.paragraph_bl_re.search(text))
        isnew = isnew or self.paragraphdivisions.isparagraphdivision(ref)
        if isnew:
            # print("DEBUG: NEW PARAGRAPH: "+ref)
            pass
        return isnew

    def sub_format_smallcaps(self,m):
        # This would exclude matches as the first word in the text:
        #if m.span(1)[0]==0:
        #    return m.group(1)+m.group(2)
        word=m.group(1)
        smallcapsd=word[0]+r'{\mysmallcapsfont '+word[1:]+'}'
        # smallcapsd= r'\textsc{'+m.group(1).title()+'}'
        whitespace=m.group(2)
        # if not whitespace: whitespace='%\n'
        return smallcapsd+whitespace

    def sub_format_italics(self,m):
        smallcapsd='{\em ' + m.group(1) + '}'
        return smallcapsd
    def sub_format_epistleattribution(self,m):
        'Written to folks by writer'
        # return '\par{\em ' + m.group(1) + '}'
        return r'\biblepistleattribution{' + m.group(1) + '}'
    def sub_format_sectionsep(self,m):
        'END OF THE PROPHETS. stuff'
        # return r'\par\null\par{\em ' + m.group(1) + '}'
        return r'\biblsectionseparator{' + m.group(1) + '}'
    def sub_format_psalmheading(self,m):
        # FIXME return \biblpsalmheading
        return r'\biblpsalmheading{' + m.group(1) + '}%\n'

    def reformat_smallcaps(self,text):
        # Rewrite CAPITALISED WORDS as smallcaps .. 
        # This might do the wrong thing in the new testament and odd places, so exceptions apply:
        dontsmallcapsnt=['AEnas',
            'AEneas',
            'JESUS',
            'For David himself said by the Holy Ghost',
            'And David himself saith in the book',
            'For David is not ascended into the heavens:',
            'KING OF',
            'TO THE UNKNOWN GOD',
            'MYSTERY',
            'thy footstool\\?'];
        if re.search('|'.join(dontsmallcapsnt),text): 
            return text

        text=re.sub(r"([A-Z????????????????]{2,}'?S?)(\s*)", self.sub_format_smallcaps, text)
        return text

    def singular(self, book):
        if book=='Psalms': return 'Psalm'
        if book=='PSALMS': return 'PSALM'
        return book

    def booktolatex(self):
        '''Parse the book, and return paragraphs'''
        self.state['paragraph']=0
        self.state['REFERENCE']=''
        self.state['book']=''
        self.state['BOOK']=''
        self.state['short']=''
        self.state['chapter']=''
        self.state['verse']=''
        self.state['text']=''
        self.state['index']=21
        self.state['shortbook']=''
        newbook=True
        yield r'\biblbeforeoldtestament' % self.state +'%\n'
        yield (r'\biblnewsection{'+self.language.oldtestament+'}') % self.state +'%\n'
        for book,chapter,verse,text in self.booktochapters():
            ostate=copy.copy(self.state)
            self.state['sourcereference']=book+' '+chapter+':'+verse
            self.state['book']=book
            self.state['book_s']=self.singular(self.state['book'])  # singular
            self.state['BOOK']=self.singular(book.upper())
            self.state['short']=self.shortnames.get(book,book)
            self.state['chapter']=chapter
            self.state['verse']=verse
            self.state['text']=text
            self.state['shortbook']=( book in ('Obadiah','Philemon','2 John','3 John','Jude') )
            self.state['isnewparagraph'] = self.isnewparagraph(book,chapter,verse,text)
            versetmpl = {True: '%(BOOK)s %(verse)s',
                        False: '%(BOOK)s %(chapter)s:%(verse)s' }
            self.state['REFERENCE']=versetmpl[self.state['shortbook']] % self.state
            newbook = ostate['book']!=self.state['book']
            newchapter = ostate['chapter']!=self.state['chapter'] or newbook
            if newchapter and ostate['book']:
                ostate['sbook']=ostate['book'].replace(' ','').lower().replace('1','i').replace('2','ii').replace('3','iii')
                ostate['romanchapter']=romannumerals[int(ostate['chapter'])]
                yield ( r'\ifdefined\biblendchapter%(sbook)s%(romanchapter)s{\biblendchapter%(sbook)s%(romanchapter)s}\fi' % ostate ) + '%\n'
                yield ( r'\biblendchapter{%(book_s)s %(chapter)s}{%(index)s}' % ostate ) + '%\n'
            if newbook and ostate['book']:
                ostate['sbook']=ostate['book'].replace(' ','').lower().replace('1','i').replace('2','ii').replace('3','iii')
                yield ( r'\ifdefined\biblendbook%(sbook)s{\biblendbook%(sbook)s}\fi' % ostate ) + '%\n'
                yield ( r'\biblendbook{%(book)s}' % ostate ) + '%\n'
            if newbook and book.startswith('Matthe'): # matthew/matteus
                yield ( r'\biblbeforenewtestament' % self.state ) + '%\n'
                yield ( (r'\biblnewsection{'+self.language.newtestament+'}') % self.state ) + '%\n'
            if newbook:
                if self.state['book'] not in ('2 John','3 John','2 Peter', '2 Timothy', '2 Thessalonians'):
                    self.state['index']=(self.state['index']+1) % 61
                self.state['prettyname']=self.language.getbookprettyname(self.state['book'])
                yield r'\biblbookheading{%(prettyname)s}' % self.state+'%\n';
                yield r'\biblnewbook{%(book)s}{%(short)s}' % self.state + '%\n'
            if newchapter:
                if self.state['shortbook']:
                    yield r'\biblnewchapter{%(book_s)s}' % self.state + '%\n' # omit chapter from heading for 1-heading book
                else:
                    yield r'\biblnewchapter{%(book_s)s %(chapter)s}' % self.state + '%\n'
                    yield r'\bibldropcapschapter{%(chapter)s}' % self.state + '%\n' 
            if self.state['isnewparagraph']:
                if verse=='1':
                    pass # meh .. it might be new, but we don't want to print it
                elif verse=='2':
                    yield r'\biblsyntheticparii' % self.state + '%\n'
                else:
                    yield r'\biblnewparagraph' % self.state + '%\n'
            t=''
            text = self.language.markuppsalmheadings(text,self.state)
            text=text.replace('???',"'") # weird unicode is weird
            text = self.hebrew.adjust(text,self.state)
            t += self.verseheading(verse)
            t += r'\biblnewreference{%(REFERENCE)s}{%(index)s}' % self.state
            text=re.sub(r'<<\[(.*?)\]>>*',self.sub_format_epistleattribution,text)
            text=re.sub(r'<<([^a-z]*?)>>',self.sub_format_sectionsep,text)
            text=re.sub(r'<<(.*?)>>',self.sub_format_psalmheading,text)
            text=re.sub(r'\[(.*?)\]',self.sub_format_italics,text)
            text=re.sub(r'AEneas','??neas',text)
            text= self.reformat_smallcaps(text)
            t += text
            t += r'\biblendreference{%(REFERENCE)s}{%(index)s}' % self.state 
            t += '\n'
            yield t
        yield ( r'\biblendchapter{%(book_s)s %(chapter)s}{%(index)s}' % self.state ) + '%\n'
        yield ( r'\biblendlastbook{%(book)s}' % self.state ) + '%\n'
        yield ( r'\biblafternewtestament' % self.state ) + '%\n'

def iteratechapters(language,src):
    en=bibleformatter(language,src)
    for line in en.booktolatex():
        yield line

#import os
#src=os.popen('sed 1,23145d < ../TEXT-PCE-127.txt','r')
#src=os.popen('sed "/^\(Joh\|Ro\) / p; d" < ../TEXT-PCE-127.txt','r')
#src=open('../1769.txt','r')
english=English()
afrikaans=Afrikaans()
src_dst = [
    # (english,   '../TEXT-PCE-127.txt', 'english.tex'), # don't like this one any more
    (english,   '../kingjamesbibleonline.txt', 'english.tex'), # like this one more
    (afrikaans, '../af1953.txt', 'afrikaans.tex'), ]

for language,srcfile,dstfile in src_dst:
    md5=os.popen('md5sum %s' % srcfile,'r').readline().split()[0]
    src=open(srcfile,'r')
    outfd=open(dstfile,'w')
    outfd.write('\\def\\srcmdsum{%s}\n' % md5)
    outfd.write('\\def\\srcfilename{%s}\n' % srcfile.split('/')[-1])
    #src=os.popen('grep ^Ps < ../TEXT-PCE-127.txt','r')
    for splurge in iteratechapters(language,src):
        outfd.write( splurge )
    outfd.close()


# 2 Kings 1:43 And he walked in all the ways of Asa his father; he turned not aside from it, doing that which was right in the eyes of the LORD : nevertheless the high places were not taken away; for the people offered and burnt incense yet in the high places.
# 43 En hy het geheel en al in die weg van sy vader Asa gewandel ??? daarvan het hy nie afgewyk nie ??? deur te doen wat reg was in die o?? van die HERE.
# 44 Net die hoogtes is nie afgeskaf nie; die volk het nog op die hoogtes geoffer en rook laat opgaan.

