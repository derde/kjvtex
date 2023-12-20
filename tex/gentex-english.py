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
    'cxlvi', 'cxlvii', 'cxlviii', 'cxlix', 'cl', 'cli', 'clii', 'cliii',
    'cliv', 'clv', 'clvi', 'clvii', 'clviii', 'clix', 'clx', 'clxi', 'clxii',
    'clxiii', 'clxiv', 'clxv', 'clxvi', 'clxvii', 'clxviii', 'clxix', 'clxx',
    'clxxi', 'clxxii', 'clxxiii', 'clxxiv', 'clxxv', 'clxxvi', 'clxxvii',
    'clxxviii', 'clxxix', 'clxxx', 'clxxxi', 'clxxxii', 'clxxxiii', 'clxxxiv',
    'clxxxv', 'clxxxvi', 'clxxxvii', 'clxxxviii', 'clxxxix', 'cxc', 'cxci',
    'cxcii', 'cxciii', 'cxciv', 'cxcv', 'cxcvi', 'cxcvii', 'cxcviii', 'cxcix',
    'cc',
]

# Unicode smallcaps
smallcaps={ 'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ꜰ', 'g':
'ɢ', 'h': 'ʜ', 'i': 'ɪ', 'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ', 'o':
'ᴏ', 'p': 'ᴘ', 'q': 'ǫ', 'r': 'ʀ', 's': 'ꜱ', 't': 'ᴛ', 'u': 'ᴜ', 'v': 'ᴠ', 'w':
'ᴡ', 'x': 'x', 'y': 'ʏ', 'z': 'ᴢ' }


def unicodesmallcaps(word):
    o=''
    for c in word.lower():
        o+=smallcaps.get(c,c)
    return o

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

class RewriteReference:
    def __init__(self,numberfile):
        self.aftoen={}
        self.entoaf={}
        fd=open(numberfile,'r')
        for line in fd:
            en,af=line.strip().split('\t',1)
            self.aftoen[af]=en
            self.entoaf[en]=af
    def __getitem__(self, key):
        return self.aftoen.get(key,key)

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
    ot=1
    nt=1
    languageindex=1
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
    tabIndexPos = {
        'Genesis':         1,
        'Exodus':          2,
        'Leviticus':       3,
        'Numbers':         4,
        'Deuteronomy':     5,
        'Joshua':          6,
        'Judges':          7,
        'Ruth':            8,
        '1 Samuel':        9,
        '2 Samuel':        10,
        '1 Kings':         11,
        '2 Kings':         12,
        '1 Chronicles':    13,
        '2 Chronicles':    14,
        'Ezra':            15,
        'Nehemiah':        16,
        'Esther':          17,
        'Job':             18,
        'Psalms':          19,
        'Proverbs':        20,
        'Ecclesiastes':    21,
        'Song of Solomon': 22,
        'Isaiah':          23,
        'Jeremiah':        24,
        'Lamentations':    25,
        'Ezekiel':         26,
        'Daniel':          27,
        'Hosea':           28,
        'Joel':            29,
        'Amos':            30,
        'Obadiah':         31,
        'Jonah':           31,
        'Micah':           32,
        'Nahum':           33,
        'Habakkuk':        34,
        'Zephaniah':       35,
        'Haggai':          36,
        'Zechariah':       37,
        'Malachi':         38,
        'Matthew':         5,
        'Mark':            6,
        'Luke':            7,
        'John':            8,
        'Acts':            9,
        'Romans':          11,
        '1 Corinthians':   12,
        '2 Corinthians':   13,
        'Galatians':       14,
        'Ephesians':       15,
        'Philippians':     16,
        'Colossians':      17,
        '1 Thessalonians': 18,
        '2 Thessalonians': 18,
        '1 Timothy':       19,
        '2 Timothy':       20,
        'Titus':           21,
        'Philemon':        21,
        'Hebrews':         23,
        'James':           25,
        '1 Peter':         26,
        '2 Peter':         27,
        '1 John':          28,
        '2 John':          28,
        '3 John':          28,
        'Jude':            29,
        'Revelation':      31,
    }
    def __init__(self,file='english.psalmtitles', numberfile='english.renumbering'):
        self.bookFullnames=self.bookfullnamesEn
        self.oldtestament="THE OLD TESTAMENT"
        self.newtestament="THE NEW TESTAMENT"
        pass
    def prefilter(self,text):
        return text
    def renumberreference(self,ref):
        return ref
    def markuppsalmheadings(self,text,state):
        return text
    def getbookprettyname(self,book):
        return book

class German:
    ot=1
    nt=1
    languageindex=3
    bookfullnamesDe = {
        'Ge'   : '1. Mose',
        'Ex'   : '2. Mose',
        'Le'   : '3. Mose',
        'Nu'   : '4. Mose',
        'De'   : '5. Mose',
        'Jos'  : 'Josua',
        'Jg'   : 'Richter',
        'Ru'   : 'Ruth',
        '1Sa'  : '1. Samuel',
        '2Sa'  : '2. Samuel',
        '1Ki'  : '1. Könige',
        '2Ki'  : '2. Könige',
        '1Ch'  : '1. Chronik',
        '2Ch'  : '2. Chronik',
        'Ezr'  : 'Esra',
        'Ne'   : 'Nehemia',
        'Es'   : 'Ester',
        'Job'  : 'Hiob',
        'Ps'   : 'Psalmen',
        'Pr'   : 'Sprüche',
        'Ec'   : 'Prediger',
        'Song' : 'Hohelied',
        'Isa'  : 'Jesaja',
        'Jer'  : 'Jeremia',
        'La'   : 'Klagelieder',
        'Eze'  : 'Hesekiel',
        'Da'   : 'Daniel',
        'Ho'   : 'Hosea',
        'Joe'  : 'Joel',
        'Am'   : 'Amos',
        'Ob'   : 'Obadja',
        'Jon'  : 'Jona',
        'Mic'  : 'Micha',
        'Na'   : 'Nahum',
        'Hab'  : 'Habakuk',
        'Zep'  : 'Zephanja',
        'Hag'  : 'Haggai',
        'Zec'  : 'Sacharja',
        'Mal'  : 'Maleachi',
        'Mt'   : 'Matthäus',
        'Mr'   : 'Markus',
        'Lu'   : 'Lukas',
        'Joh'  : 'Johannes',
        'Ac'   : 'Apostelgeschichte',
        'Ro'   : 'Römer',
        '1Co'  : '1. Korinther',
        '2Co'  : '2. Korinther',
        'Ga'   : 'Galater',
        'Eph'  : 'Epheser',
        'Php'  : 'Philipper',
        'Col'  : 'Kolosser',
        '1Th'  : '1. Thessalonicher',
        '2Th'  : '2. Thessalonicher',
        '1Ti'  : '1. Timotheus',
        '2Ti'  : '2. Timotheus',
        'Tit'  : 'Titus',
        'Phm'  : 'Philemon',
        'Heb'  : 'Hebräer',
        'Jas'  : 'Jakobus',
        '1Pe'  : '1. Petrus',
        '2Pe'  : '2. Petrus',
        '1Jo'  : '1. Johannes',
        '2Jo'  : '2. Johannes',
        '3Jo'  : '3. Johannes',
        'Jude' : 'Judas',
        'Re'   : 'Offenbarung',
    }
    def __init__(self,file='de.psalmtitles', numberfile='german.renumbering'):
        self.bookFullnames=self.bookfullnamesDe
        self.oldtestament="DAS ALTE TESTAMENT"
        self.newtestament="DAS NEUE TESTAMENT"
        self.rewritereference=RewriteReference(numberfile)
        self.tabIndexPos={}
    def prefilter(self,text):
        lineformat_re=re.compile('(.*? \d+:\d+ ) *(.*)')
        m=lineformat_re.search(text)
        if m:
            ref,verse=m.groups()
            if verse.startswith('<<'):
                text=ref+verse
                pass
            else:
                text=ref+verse.replace('<<','[').replace('>>',']')
        return text
    def renumberreference(self,ref):
        return self.rewritereference[ref]
    def markuppsalmheadings(self,text,state):
        text=re.sub('([;.?!:])(\w)','\\1 \\2',text)
        return text
    def getbookprettyname(self,book):
        return book
    def renumberreference(self,ref):
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

class French:
    ot=1
    nt=1
    languageindex=4
    bookfullnamesFr = {
        'Ge'   : 'Genèse',
        'Ex'   : 'Exode',
        'Le'   : 'Lévitique',
        'Nu'   : 'Nombres',
        'De'   : 'Deutéronome',
        'Jos'  : 'Josué',
        'Jg'   : 'Juges',
        'Ru'   : 'Ruth',
        '1Sa'  : '1 Samuel',
        '2Sa'  : '2 Samuel',
        '1Ki'  : '1 Rois',
        '2Ki'  : '2 Rois',
        '1Ch'  : '1 Chroniques',
        '2Ch'  : '2 Chroniques',
        'Ezr'  : 'Esdras',
        'Ne'   : 'Néhémie',
        'Es'   : 'Esther',
        'Job'  : 'Job',
        'Ps'   : 'Psaumes',
        'Pr'   : 'Proverbes',
        'Ec'   : 'Ecclésiaste',
        'Song' : 'Cantique des Cantiques',
        'Isa'  : 'Ésaïe',
        'Jer'  : 'Jérémie',
        'La'   : 'Lamentations',
        'Eze'  : 'Ézéchiel',
        'Da'   : 'Daniel',
        'Ho'   : 'Osée',
        'Joe'  : 'Joël',
        'Am'   : 'Amos',
        'Ob'   : 'Abdias',
        'Jon'  : 'Jonas',
        'Mic'  : 'Michée',
        'Na'   : 'Nahum',
        'Hab'  : 'Habacuc',
        'Zep'  : 'Sophonie',
        'Hag'  : 'Aggée',
        'Zec'  : 'Zacharie',
        'Mal'  : 'Malachie',
        'Mt'   : 'Matthieu',
        'Mr'   : 'Marc',
        'Lu'   : 'Luc',
        'Joh'  : 'Jean',
        'Ac'   : 'Actes',
        'Ro'   : 'Romains',
        '1Co'  : '1 Corinthiens',
        '2Co'  : '2 Corinthiens',
        'Ga'   : 'Galates',
        'Eph'  : 'Éphésiens',
        'Php'  : 'Philippiens',
        'Col'  : 'Colossiens',
        '1Th'  : '1 Thessaloniciens',
        '2Th'  : '2 Thessaloniciens',
        '1Ti'  : '1 Timothée',
        '2Ti'  : '2 Timothée',
        'Tit'  : 'Tite',
        'Phm'  : 'Philémon',
        'Heb'  : 'Hébreux',
        'Jas'  : 'Jacques',
        '1Pe'  : '1 Pierre',
        '2Pe'  : '2 Pierre',
        '1Jo'  : '1 Jean',
        '2Jo'  : '2 Jean',
        '3Jo'  : '3 Jean',
        'Jude' : 'Jude',
        'Re'   : 'Révélation',
    }
    def __init__(self,file='de.psalmtitles', numberfile='de.renumbering'):
        self.bookFullnames=self.bookfullnamesFr
        self.oldtestament="L'ANCIEN TESTAMENT"
        self.newtestament="LE NOVEAU TESTAMENT"
        self.tabIndexPos={}
        pass
    def prefilter(self,text):
        lineformat_re=re.compile('(.*? \d+:\d+ ) *(.*)')
        m=lineformat_re.search(text)
        if m:
            ref,verse=m.groups()
            if verse.startswith('<<'):
                text=ref+verse
                pass
            else:
                text=ref+verse.replace('<<','[').replace('>>',']')
        return text
    def renumberreference(self,ref):
        return ref
    def markuppsalmheadings(self,text,state):
        text=re.sub('([;.?!:])(\w)','\\1 \\2',text)
        return text
    def getbookprettyname(self,book):
        return book
    def renumberreference(self,ref):
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

class Afrikaans:
    ot=1
    nt=1
    tabIndexPos={}
    languageindex=2
    af_lowercase={
        'Á': 'á',
        'É': 'é',
        'Ê': 'ê',
        'Ë': 'ë',
        'Í': 'í',
        'Ó': 'ó',
        'Ú': 'ú',
        'Ō': 'ō',
    }
    af_wordmap={
        'DÍT'        :   'Dít',
        'GESEËND'    :   'Geseënd',
        'JEHISKÍA'   :   'Jehiskía',
        'JOSÍA'      :   'Josía',
        'LÊ'         :   'Lê',
        'NÁ'         :   'Ná',
        'NASARÉNER'  :   'Nasaréner',
        'SAMARÍA'    :   'Samaría',
        'SEDEKÍA'    :   'Sedekía',
        'SÍMEON'     :   'Símeon',
        'SJIGGAJŌN'  :   'Sjiggajōn',
        'VANWEË'     :   'Vanweë',
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
        'Genesis'              : ['GÉNESIS'            ,'Génesis'             ],
        'Exodus'               : ['EXODUS'             ,'Exodus'              ],
        'Levitikus'            : ['LEVÍTIKUS'          ,'Levítikus'           ],
        'Numeri'               : ['NÚMERI'             ,'Númeri'              ],
        'Deuteronomium'        : ['DEUTERONÓMIUM'      ,'Deuteronómium'       ],
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
        'Nehemia'              : ['NEHEMÍA'            ,'Nehemía'             ],
        'Ester'                : ['ESTER'              ,'Ester'               ],
        'Job'                  : ['JOB'                ,'Job'                 ],
        'Psalms'               : ['PSALMS'             ,'Psalms'              ],
        'Spreuke'              : ['SPREUKE'            ,'Spreuke'             ],
        'Prediker'             : ['PREDIKER'           ,'Prediker'            ],
        'Hooglied'             : ['HOOGLIED'           ,'Hooglied'            ],
        'Jesaja'               : ['JESAJA'             ,'Jesaja'              ],
        'Jeremia'              : ['JEREMIA'            ,'Jeremia'             ],
        'Klaagliedere'         : ['KLAAGLIEDERE'       ,'Klaagliedere'        ],
        'Esegiel'              : ['ESÉGIËL'            ,'Eségiël'             ],
        'Daniel'               : ['DANIËL'             ,'Daniël'              ],
        'Hosea'                : ['HOSÉA'              ,'Hoséa'               ],
        'Joel'                 : ['JOËL'               ,'Joël'                ],
        'Amos'                 : ['AMOS'               ,'Amos'                ],
        'Obadja'               : ['OBÁDJA'             ,'Obádja'              ],
        'Jona'                 : ['JONA'               ,'Jona'                ],
        'Miga'                 : ['MIGA'               ,'Miga'                ],
        'Nahum'                : ['NAHUM'              ,'Nahum'               ],
        'Habakuk'              : ['HÁBAKUK'            ,'Hábakuk'             ],
        'Sefanja'              : ['SEFÁNJA'            ,'Sefánja'             ],
        'Haggai'               : ['HAGGAI'             ,'Haggai'              ],
        'Sagaria'              : ['SAGARÍA'            ,'Sagaría'             ],
        'Maleagi'              : ['MALEÁGI'            ,'Maleági'             ],
        'Mattheus'             : ['MATTHÉÜS'           ,'Matthéüs'            ],
        'Markus'               : ['MARKUS'             ,'Markus'              ],
        'Lukas'                : ['LUKAS'              ,'Lukas'               ],
        'Johannes'             : ['JOHANNES'           ,'Johannes'            ],
        'Handelinge'           : ['HANDELINGE'         ,'Handelinge'          ],
        'Romeine'              : ['ROMEINE'            ,'Romeine'             ],
        '1 Korinthiers'        : ['I KORINTHIËRS'      ,'I Korinthiërs'       ],
        '2 Korinthiers'        : ['II KORINTHIËRS'     ,'II Korinthiërs'      ],
        'Galasiers'            : ['GALÁSIËRS'          ,'Galásiërs'           ],
        'Efesiers'             : ['EFÉSIËRS'           ,'Efésiërs'            ],
        'Filippense'           : ['FILIPPENSE'         ,'Filippense'          ],
        'Kolossense'           : ['KOLOSSENSE'         ,'Kolossense'          ],
        '1 Thessalonicense'    : ['I THESSALONICENSE'  ,'I Thessalonicense'   ],
        '2 Thessalonicense'    : ['II THESSALONICENSE' ,'II Thessalonicense'  ],
        '1 Timotheus'          : ['I TIMÓTHEÜS        ','I Timótheüs         '],
        '2 Timotheus'          : ['II TIMÓTHEÜS'       ,'II Timótheüs'        ],
        'Titus'                : ['TITUS'              ,'Titus'               ],
        'Filemon'              : ['FILÉMON'            ,'Filémon'             ],
        'Hebreers'             : ['HEBREËRS'           ,'Hebreërs'            ],
        'Jakobus'              : ['JAKOBUS'            ,'Jakobus'             ],
        '1 Petrus'             : ['I PETRUS'           ,'I Petrus'            ],
        '2 Petrus'             : ['II PETRUS'          ,'II Petrus'           ],
        '1 Johannes'           : ['I JOHANNES'         ,'I Johannes'          ],
        '2 Johannes'           : ['II JOHANNES'        ,'II Johannes'         ],
        '3 Johannes'           : ['III JOHANNES'       ,'III Johannes'        ],
        'Judas'                : ['JUDAS'              ,'Judas'               ],
        'Openbaring'           : ['OPENBARING'         ,'Openbaring'          ],
    }

    def __init__(self,file='afrikaans.psalmtitles', numberfile='afrikaans.renumbering', ot=1, nt=1):
        self.ot=ot
        self.nt=nt
        # Hebrew letter, prefix, capitalised-word
        self.titlecasewl=re.compile(r"^([A-Z][a-z]+\. )?(’n |O |O, )?([-A-ZÁÉÊËÍÓŌÚ]{2,})(.*)")
        self.titlecasebl=re.compile(r"^([A-Z][a-z]+\. )?(’n |O, )?(HERE)")
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

        self.rewritereference=RewriteReference(numberfile)
        #self.aftoen={}
        #self.entoaf={}
        #fd=open(numberfile,'r')
        #for line in fd:
        #    en,af=line.strip().split('\t',1)
        #    self.aftoen[af]=en
        #    self.aftoen[en]=af
    def prefilter(self,text):
        return text
    def getbookprettyname(self,book):
        return self.booknamesAccented[book][1]
    def renumberreference(self,ref):
        # Rewrite references
        return self.rewritereference[ref]
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
    def __init__(self,file,language):
        self.language=language
        self.languageindex=language.languageindex
        self.staticdata()
        self.bookmap=[]
        for line in self.bookmapdata.split('\n'):
            bits=re.split(' *: *',line.strip())
            if len(bits)>3:
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

    def staticdata(self):
        self.paragraphs={}
        self.bookmapdata='''\
pericope  1=english           2=afrikaans         3=german            4=french
GEN      : Genesis         :  Genesis           : 1. Mose           : Genèse
EXOD     : Exodus          :  Exodus            : 2. Mose           : Exode
LEV      : Leviticus       :  Levitikus         : 3. Mose           : Lévitique
NUM      : Numbers         :  Numeri            : 4. Mose           : Nombres
DEUT     : Deuteronomy     :  Deuteronomium     : 5. Mose           : Deutéronome
JOSH     : Joshua          :  Josua             : Josua             : Josué
JUDG     : Judges          :  Rigters           : Richter           : Juges
RUTH     : Ruth            :  Rut               : Ruth              : Ruth
1SAM     : 1 Samuel        :  1 Samuel          : 1. Samuel         : 1 Samuel
2SAM     : 2 Samuel        :  2 Samuel          : 2. Samuel         : 2 Samuel
1KGS     : 1 Kings         :  1 Konings         : 1. Könige         : 1 Rois
2KGS     : 2 Kings         :  2 Konings         : 2. Könige         : 2 Rois
1CHRON   : 1 Chronicles    :  1 Kronieke        : 1. Chronik        : 1 Chroniques
2CHRON   : 2 Chronicles    :  2 Kronieke        : 2. Chronik        : 2 Chroniques
EZRA     : Ezra            :  Esra              : Esra              : Esdras
NEH      : Nehemiah        :  Nehemia           : Nehemia           : Néhémie
ESTH     : Esther          :  Ester             : Ester             : Esther
JOB      : Job             :  Job               : Hiob              : Job
PS       : Psalms          :  Psalms            : Psalmen           : Psaumes
PROV     : Proverbs        :  Spreuke           : Sprüche           : Proverbes
ECC      : Ecclesiastes    :  Prediker          : Prediger          : Ecclésiaste
SONG     : Song of Solomon :  Hooglied          : Hohelied          : Cantique des Cantiques
ISA      : Isaiah          :  Jesaja            : Jesaja            : Ésaïe
JER      : Jeremiah        :  Jeremia           : Jeremia           : Jérémie
LAM      : Lamentations    :  Klaagliedere      : Klagelieder       : Lamentations
EZEK     : Ezekiel         :  Esegiel           : Hesekiel          : Ézéchiel
DAN      : Daniel          :  Daniel            : Daniel            : Daniel
HOSEA    : Hosea           :  Hosea             : Hosea             : Osée
JOEL     : Joel            :  Joel              : Joel              : Joël
AMOS     : Amos            :  Amos              : Amos              : Amos
OBAD     : Obadiah         :  Obadja            : Obadja            : Abdias
JONAH    : Jonah           :  Jona              : Jona              : Jonas
MICAH    : Micah           :  Miga              : Micha             : Michée'
NAHUM    : Nahum           :  Nahum             : Nahum             : Nahum
HAB      : Habakkuk        :  Habakuk           : Habakuk           : Habacuc
ZEPH     : Zephaniah       :  Sefanja           : Zephanja          : Sophonie
HAG      : Haggai          :  Haggai            : Haggai            : Aggée
ZECH     : Zechariah       :  Sagaria           : Sacharja          : Zacharie
MAL      : Malachi         :  Maleagi           : Maleachi          : Malachie
MATT     : Matthew         :  Mattheus          : Matthäus          : Matthieu
MARK     : Mark            :  Markus            : Markus            : Marc
LUKE     : Luke            :  Lukas             : Lukas             : Luc
JOHN     : John            :  Johannes          : Johannes          : Jean
ACTS     : Acts            :  Handelinge        : Apostelgeschichte : Actes
ROM      : Romans          :  Romeine           : Römer             : Romains
1COR     : 1 Corinthians   :  1 Korinthiers     : 1. Korinther      : 1 Corinthiens
2COR     : 2 Corinthians   :  2 Korinthiers     : 2. Korinther      : 2 Corinthiens
GAL      : Galatians       :  Galasiers         : Galater           : Galates
EPH      : Ephesians       :  Efesiers          : Epheser           : Éphésiens
PHIL     : Philippians     :  Filippense        : Philipper         : Philippiens
COL      : Colossians      :  Kolossense        : Kolosser          : Colossiens
1THES    : 1 Thessalonians :  1 Thessalonicense : 1. Thessalonicher : 1 Thessaloniciens
2THES    : 2 Thessalonians :  2 Thessalonicense : 2. Thessalonicher : 2 Thessaloniciens
1TIM     : 1 Timothy       :  1 Timotheus       : 1. Timotheus      : 1 Timothée
2TIM     : 2 Timothy       :  2 Timotheus       : 2. Timotheus      : 2 Timothée
TITUS    : Titus           :  Titus             : Titus             : Tite
PHILEM   : Philemon        :  Filemon           : Philemon          : Philémon
HEB      : Hebrews         :  Hebreers          : Hebräer           : Hébreux
JAS      : James           :  Jakobus           : Jakobus           : Jacques
1PET     : 1 Peter         :  1 Petrus          : 1. Petrus         : 1 Pierre
2PET     : 2 Peter         :  2 Petrus          : 2. Petrus         : 2 Pierre
1JOHN    : 1 John          :  1 Johannes        : 1. Johannes       : 1 Jean
2JOHN    : 2 John          :  2 Johannes        : 2. Johannes       : 2 Jean
3JOHN    : 3 John          :  3 Johannes        : 3. Johannes       : 3 Jean
JUDE     : Jude            :  Judas             : Judas             : Jude
REV      : Revelation      :  Openbaring        : Offenbarung       : Révélation
'''

    def bookmaplookup(self,srccol,dstcol,value):
        for r in self.bookmap:
            if r[srccol]==value: return r[dstcol]
        return ''

    def addparagraph(self,refs):
        '''Add to the list'''
        m=re.search('(\S+) (\d+:\d+)',refs)
        chapterandverse = m.group(2)
        book = self.bookmaplookup(0,self.languageindex,m.group(1))
        # e.g. Song of Songs 4:12
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
    paragraph_wl_re=re.compile(r"^([A-Z][a-z]+\. )?(’n |O |O, )?([-A-ZÁÉÊËÍÓŌÚ]{2,})(.*)")
    paragraph_bl_re=re.compile(r"\bHERE\b")
    # These are the particular things that appear in the AFrikaans: we don't actually like that leading capital
    # python seems to have these already ... not sure what we're doing here ...
    def __init__(self,language,file):
        self.language=language;
        self.ot=language.ot
        self.nt=language.nt
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
            line=self.language.prefilter(line)
            m=lineformat_re.search(line.strip())
            if m:
                book,chapter,verse,text=m.groups()
                book=self.language.bookFullnames.get(book,book)
                yield book,chapter,verse,text
            else:
                print('G3021 '+line.strip())

    def chapternumber(self,book,chapter, one_chapter=False):
        # Generate  chapter numbers for each book
        o='';
        if chapter=='1':
            if book in ('Obadiah','Philemon','2 John','3 John','Jude'):
                return o+self.verseheading('1') #  + '\n';
        o+=r'\bibldropcapschapter{'+chapter+'}' + '%\n' 
        # o+=self.verseheading('1') + '%\n'
        return o

    def verseheading(self,verse,insert):
        # r+=  r'\verse{'+verse+'}'  
        cmd='\\verse'
        if verse=='1':
            cmd=r'\versei' # no space before 1st verse
        elif verse=='2': cmd=r'\verseii' # space before 2nd verse
        else: cmd=r'\verse' # space before verses 3 and on
        return r''+cmd+'{'+verse+insert+'}{'+str(self.state['index'])+'}'

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
        whitespace=m.group(2)
        return r'{\mysmallcaps{'+word[0]+'}{'+word[1:]+'}{'+unicodesmallcaps(word[1:])+'}}'+whitespace

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

        text=re.sub(r"([A-ZÁÉÊËÍÓŌÚ]{2,}'?S?)(\s*)", self.sub_format_smallcaps, text)
        return text

    def singular(self, book):
        if book=='Psalms': return 'Psalm'
        if book=='PSALMS': return 'PSALM'
        return book

    def reftoroman(self,book,chapter,verse,cmd):
        book=book.replace(' ','').lower();
        book=book.replace('1','i')
        book=book.replace('2','ii')
        book=book.replace('3','iii')
        book=book.lower().replace(' ','')
        return cmd+ book + \
            'q'+romannumerals[int(chapter)]+\
            'q'+romannumerals[int(verse)];

    def reftoconditional(self,book,chapter,verse,cmd):
        c = self.reftoroman(book,chapter,verse,cmd)
        if not c: return ''
        return r'\ifdefined'+c+c+r'\fi{}'

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
        self.state['index']=1
        self.state['shortbook']=''
        newbook=True
        emit = 0
        if self.ot:
            emit = 1
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
                # ostate['sbook']=ostate['book'].replace(' ','').lower().replace('1','i').replace('2','ii').replace('3','iii')
                ostate['sbook']=bookiii(ostate['book'])
                ostate['romanchapter']=romannumerals[int(ostate['chapter'])]
                if emit: yield ( r'\ifdefined\biblendchapter%(sbook)s%(romanchapter)s{\biblendchapter%(sbook)s%(romanchapter)s}\fi' % ostate ) + '%\n'
                if emit: yield ( r'\biblendchapter{%(book_s)s %(chapter)s}{%(index)s}' % ostate ) + '%\n'
            if newbook and ostate['book']:
                ostate['sbook']=bookiii(ostate['book'])
                if emit: yield ( r'\ifdefined\biblendbook%(sbook)s{\biblendbook%(sbook)s}\fi' % ostate ) + '%\n'
                if emit: yield ( r'\biblendbook{%(book)s}' % ostate ) + '%\n'
            if newbook and book.startswith('Matth'): # matthew/matteus
                if self.nt:
                    emit=1
                if emit: yield ( r'\biblbeforenewtestament' % self.state ) + '%\n'
                if emit: yield ( (r'\biblnewsection{'+self.language.newtestament+'}') % self.state ) + '%\n'
            if newbook:
                if self.state['book'] not in ('2 John','3 John','2 Peter', '2 Timothy', '2 Thessalonians'):
                    self.state['index']=((self.state['index']) % 61 )+1
                    i=self.language.tabIndexPos.get(self.state['book'])
                    if i:
                        self.state['index']=i
                self.state['prettyname']=self.language.getbookprettyname(self.state['book'])
                if emit: yield r'\biblbookheading{%(prettyname)s}' % self.state+'%\n';
                if emit: yield r'\biblnewbook{%(book)s}{%(short)s}' % self.state + '%\n'
            if newchapter:
                if self.state['shortbook']:
                    if emit: yield r'\biblnewchapter{%(book_s)s}' % self.state + '%\n' # omit chapter from heading for 1-heading book
                else:
                    if emit: yield r'\biblnewchapter{%(book_s)s %(chapter)s}' % self.state + '%\n'
                    if emit: yield r'\bibldropcapschapter{%(chapter)s}' % self.state + '%\n' 
            if self.state['isnewparagraph']:
                if verse=='1':
                    pass # meh .. it might be new, but we don't want to print it
                elif verse=='2':
                    if emit: yield r'\biblsyntheticparii' % self.state + '%\n'
                else:
                    if emit: yield r'\biblnewparagraph' % self.state + '%\n'
            t=''
            if self.state['verse']!='1':
                t+=' ';
            t += self.reftoconditional(self.state['book'],self.state['chapter'],self.state['verse'],'\\q')
            text = self.language.markuppsalmheadings(text,self.state)
            text=text.replace('’',"'") # weird unicode is weird
            text = self.hebrew.adjust(text,self.state)
            firstletter = text[:1]
            if firstletter in ('A'):
                insert = '\\versehskipa'
            else:
                insert = '\\versehskip'
            t += self.verseheading(verse,insert)
            t += r'\biblnewreference{%(REFERENCE)s}{%(index)s}' % self.state
            # each verse has a prefix that can be defined
            text=re.sub(r'<<\[(.*?)\]>>*',self.sub_format_epistleattribution,text)
            text=re.sub(r'<<([^a-z]*?)>>',self.sub_format_sectionsep,text)
            text=re.sub(r'<<(.*?)>>',self.sub_format_psalmheading,text)
            text=re.sub(r'\[(.*?)\]',self.sub_format_italics,text)
            text=re.sub(r'AEneas','Æneas',text)
            text= self.reformat_smallcaps(text)
            t += r'\bibl{'+text+'}'  # final wrap for text
            t += r'\biblendreference{%(REFERENCE)s}{%(index)s}' % self.state 
            t += '\n'
            if emit: yield t
        if emit: yield ( r'\biblendchapter{%(book_s)s %(chapter)s}{%(index)s}' % self.state ) + '%\n'
        if emit: yield ( r'\biblendlastbook{%(book)s}' % self.state ) + '%\n'
        if emit: yield ( r'\biblafternewtestament' % self.state ) + '%\n'

def iteratechapters(language,src):
    en=bibleformatter(language,src)
    for line in en.booktolatex():
        yield line

def bookiii(name):
    name=name.replace(' ','').\
        lower().\
        replace('.','').\
        replace('1','i').\
        replace('2','ii').\
        replace('3','iii')
    name=re.sub('[^a-z]+','x',name) # replace accents with x
    return name
#import os
#src=os.popen('sed 1,23145d < ../TEXT-PCE-127.txt','r')
#src=os.popen('sed "/^\(Joh\|Ro\) / p; d" < ../TEXT-PCE-127.txt','r')
#src=open('../1769.txt','r')
english=English() # 1
afrikaans=Afrikaans() # 2
afrikaansnt=Afrikaans(ot=0,nt=1) # 2
german=German() # 3
french=French() # 4
src_dst = [
    # (english,   '../text/TEXT-PCE-127.txt', 'english.tex'), # don't like this one any more
    (english,   '../text/kingjamesbibleonline.txt', 'english.tex'), # like this one more
    (english,   '../text/kingjamesbibleonline-sc.txt', 'en.tex'), # like this one more
    (afrikaans, '../text/af1953.txt', 'afrikaans.tex'), 
    (afrikaansnt, '../text/af1953.txt', 'afrikaans-nt.tex'), 
    (german, '../text/sch2000.txt', 'sch2000.tex'), 
    (french, '../text/fr.ostervald2018', 'ostervald2018.tex'), ]

for language,srcfile,dstfile in src_dst:
    if not os.path.exists(srcfile):
        continue
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
# 43 En hy het geheel en al in die weg van sy vader Asa gewandel — daarvan het hy nie afgewyk nie — deur te doen wat reg was in die oë van die HERE.
# 44 Net die hoogtes is nie afgeskaf nie; die volk het nog op die hoogtes geoffer en rook laat opgaan.

