#! /usr/bin/python3
# coding: utf-8

# DISCLAIMER: this code is torturous, because it is hacked from code for making
# a side-by-side parallel Bible, which needs a lot of bad hacks.  I'm sorry.
# Don't write your own code like this.  Be better.

import re
import itertools
import sys

class Renumbering:
    def __init__(self,file):
        self.ltor={}
        self.rtol={}
        if not file: return
        fd=open(file,'r')
        for line in fd:
            m=re.search('(.*) (\d+:\d+) \((\d+:\d+)\)',line)
            if not m: continue
            book,L,R=m.group(1),m.group(2),m.group(3)
            self.ltor[book+' '+L]=book+' '+R
            self.rtol[book+' '+R]=book+' '+L
    def tokjv(self,ref):
        return self.rtol.get(ref,ref)
    def tomasoretic(self,ref):
        return self.ltor.get(ref,ref)

            
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

    def __init__(self,file,renumbering):
        self.renumbering=renumbering
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
        chapverse = m.group(2)
        ref1 = self.bookmaplookup(0,1,m.group(1))+' '+chapverse
        #if ref1.startswith('Psalms'): ref1='Psalm '+ref1.split()[-1]
        self.paragraphs[ref1] = True
        # if nref1!=ref1 or nref2!=ref2: print(ref1,ref2,"=>",nref1,nref2)

    def isnewparagraph(self,ref):
        return ref in self.paragraphs
        

class bibleformatter:
    paragraph_wl_re=re.compile("^('n )?[A-Z]{2,}")
    paragraph_bl_re=re.compile("^HERE ")
    # These are the particular things that appear in the AFrikaans
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
    bookAbbreviations = {
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

    def __init__(self,file, is_afrikaans=False):
        self.state={
            'book': '',
            'chapter': '',
            'chapter': '', }
        if is_afrikaans:
            this_renumbering=Renumbering('afrikaans.renumbering')
        else:
            this_renumbering=Renumbering(None)
        self.paragraphdivisions=paragraphdivisions('1526.Pericopes.csv',this_renumbering)
        if is_afrikaans:
            self.reformat=self.reformat_afrikaans
            self.markheading=r'\markleft';
        else:
            self.reformat=self.reformat_english
            self.markheading=r'\markright';
        self.fd=open(file,'r')
        self.shortnames={}
        for k,v in self.bookAbbreviations.items():
            self.shortnames[v]=k

    def booktochapters(self):
        lineformat_re=re.compile('(.*?) (\d+):(\d+) (.*)')
        for line in self.fd:
            m=lineformat_re.search(line.strip())
            book,chapter,verse,text=m.groups()
            book=self.bookAbbreviations.get(book,book)
            text=text.replace('’',"'")
            yield book,chapter,verse,text

    def chapternumber(self,book,chapter, one_chapter=False):
        # Generate  chapter numbers for each book
        o='';
        if chapter=='1':
            if book in ('Obadiah','Philemon','2 John','3 John','Jude'):
                return o+self.verseheading('1') #  + '\n';
        o+=self.verseheading('1') +  \
            r'\bibldropcapschapter{'+chapter+'}' + '%\n' 
        return o

    def verseheading(self,verse):
        r= self.setverseforheading()
        # r+=  r'\verse{'+verse+'}'  
        if verse!='1': r+=  r' \verse{'+verse+'}'  
        return r

    def setverseforheading(self):
        ref = '%(book)s %(chapter)s:%(verse)s' % self.state
        # return self.markheading+'{'+ref+'}' ;
        return '' # r'\markright{%s}' % (ref)
        # return r'\markboth{%s}{%s}' % (ref,ref)

    def isnewparagraph(self,book,chapter,verse,text):
        # Afrikaans text has capital words indicating new paragraphs
        #if book.startswith('Psa'):
        #    return True;
        #isnew = self.paragraph_wl_re.search(text) and not self.paragraph_bl_re.search(text)
        # FIXME: Afrikaans books need verse number adjustments
        # if book.startswith("Psalm"): return True
        ref = book+' '+chapter+':'+verse
        isnew = verse!='2' and verse!='3' and self.paragraphdivisions.isnewparagraph(ref)
        if isnew:
            # print("DEBUG: NEW PARAGRAPH: "+ref)
            pass
        return isnew

    def sub_format_smallcaps(self,m):
        if m.span(1)[0]==0:
            return m.group(1)+m.group(2)
        word=m.group(1)
        smallcapsd=word[0]+r'{\myfootnotefont '+word[1:]+'}'
        # smallcapsd= r'\textsc{'+m.group(1).title()+'}'
        whitespace=m.group(2)
        # if not whitespace: whitespace='%\n'
        return smallcapsd+whitespace

    def sub_format_italics(self,m):
        smallcapsd='{\em ' + m.group(1) + '}'
        return smallcapsd
    def sub_format_epistleattribution(self,m):
        return '\par{\em ' + m.group(1) + '}'
    def sub_format_sectionsep(self,m):
        return '\par{\em ' + m.group(1) + '}'
    def sub_format_psalmheading(self,m):
        return '{\em ' + m.group(1) + '}\\biblsyntheticparii%\n'
    def sub_format_italics_bracketquote(self,m):
        # FIXME: for psalms, the <<< >>> is followed by paragraph break
        # FIXME: for NT book notes, the <<[ ]>> is preceded by paragraph break
        return self.sub_format_italics(m)+r'\biblsyntheticparii'+'%\n'

    def reformat_english(self,text):
        # Rewrite CAPITALISED WORDS as smallcaps .. this might do the wrong thing in the new testament and odd places
        dontsmallcapsnt=['AEnas','JESUS','For David himself said by the Holy Ghost','KING OF','TO THE UNKNOWN GOD','MYSTERY'];
        if re.search('|'.join(dontsmallcapsnt),text): 
            return text
        text=re.sub(r"([A-Z]{2,}'?S?)(\s*)", self.sub_format_smallcaps, text)
        return text

    def afrikaans_titlecase(self,m):
        indefinitearticle=''
        if m.group(1): indefinitearticle=m.group(1)
        word=m.group(2)
        if word=='HERE':
            return word
        return indefinitearticle+word[0]+word[1:].lower()  # .title() does the wrong thing for DRIE-EN-TWINTIG

    def reformat_afrikaans(self,text):
        # Rewrite paragraph capitalisation
        for k,v in list(self.af_wordmap.items()):
            text=text.replace(k,v);
        utext=text # .decode('utf-8')
        utext=re.sub(r"(^[’']n )?([A-Z-]{2,})", self.afrikaans_titlecase, utext, 1) # DRIE-EN-TWINTIG VYF-EN-TWINTIG EEN-EN-TWINTIG
        utext=re.sub(r"([A-Z]{2,})(\s*)", self.sub_format_smallcaps, utext)
        text=utext # .encode('utf-8')
        # hyphenate_regexes = (
        #     re.compile('([a-z])(honderd|duisend|miljoen)') , re.compile(r'(skrif)(geleerde)') )
        # hyphenwords=('skrif-geleerde', 'ge-reg-tig-heid', 'Goeder-tieren-heid',
        #     'Egipte-naars', 'eers-ge-borenes', 'goeder-tieren-heid',
        #     'ver-slaan','ver-plet-ter', 'lank-moedig-heid','lyd-saam-heid',
        #     'on-der-tussen', 'oop-ge-sny', 'familie-hoofde', 'dubbel-draad',
        #     'tent-doeke', 'tent-doek', 'purper-rooi', 'bloed-rooi',)
        # for regex in hyphenate_regexes:
        #     text=regex.sub(r'\1\\-\2',text)
        # for word in hyphenwords:
        #     text=text.replace(word.replace('-',''),word.replace('-','\\-'))
        return text

    def singular(self, book):
        if book=='Psalms': return 'Psalm'
        if book=='PSALMS': return 'PSALM'
        return book

    def booktoparagraphs(self):
        '''Parse the book, and return paragraphs'''
        index=26
        obook=''
        ochapter=''
        chaptertext=[]
        self.state['paragraph']=0
        newbook=True
        newsection=True
        for book,chapter,verse,text in self.booktochapters():
            self.state['book']=book
            self.state['BOOK']=self.singular(book.upper())
            self.state['short']=self.shortnames[book]
            self.state['chapter']=chapter
            self.state['verse']=verse
            self.state['text']=text
            self.state['index']=index
            self.state['shortbook']=( book in ('Obadiah','Philemon','2 John','3 John','Jude') )
            versetmpl = {True: '%(BOOK)s %(verse)s',
                        False: '%(BOOK)s %(chapter)s:%(verse)s' }
            self.state['REFERENCE']=versetmpl[self.state['shortbook']] % self.state
            if ( chapter!=ochapter or book!=obook ):
                if ochapter:
                    self.state['paragraph']+=1
                    yield { 'index': index, 'newsection': newsection, 'newbook': newbook, 'book':obook, 'short': self.shortnames[obook], 'chapter': ochapter, 'paragraph': self.state['paragraph'], 'chaptertext': ''.join(chaptertext), }
                    newbook=False
                    newsection=False
                    self.state['paragraph']=0
                    chaptertext=[]
                if book!=obook:
                    newsection=newsection or book.startswith('Matthew')
                    newbook=True
                    index=(index+1) % 66
                    self.state['index']=index
                chaptertext.append(self.chapternumber(book,chapter))
            if verse!='1':
                if self.isnewparagraph(book,chapter,verse,text):
                    if verse=='2':
                        chaptertext.append(r'\biblsyntheticparii'+'%\n')  # just shove in a synthetic paragraph break, since real \par breaks drop-caps number
                    else:
                        self.state['paragraph']+=1
                        yield { 'index':index, 'newsection': newsection, 'newbook': newbook, 'book':obook, 'short': self.shortnames[obook], 'chapter': ochapter, 'paragraph': self.state['paragraph'], 'chaptertext': ''.join(chaptertext), }
                        newbook=False
                        newsection=False
                        chaptertext=[];
                        # chaptertext.append(r'\par'+'\n');
                chaptertext.append(self.verseheading(verse))
            text=re.sub(r'<<\[(.*?)\]>>*',self.sub_format_epistleattribution,text)
            text=re.sub(r'<<([^a-z]*?)>>',self.sub_format_sectionsep,text)
            text=re.sub(r'<<(.*?)>>',self.sub_format_psalmheading,text)
            text=re.sub(r'\[(.*?)\]',self.sub_format_italics,text)
            chaptertext.append('\\biblnewreference{%(REFERENCE)s}{%(index)s}' % self.state)
            chaptertext.append(self.reformat(text)+'');
            chaptertext.append('\\biblendreference{%(REFERENCE)s}{%(index)s}' % self.state)
            obook = book
            ochapter = chapter
        self.state['paragraph']+=1
        yield { 'index':index, 'newsection': False, 'newbook': newbook, 'book':obook, 'short':self.shortnames[obook], 'chapter': ochapter, 'paragraph': self.state['paragraph'], 'chaptertext': ''.join(chaptertext), }
        newbook=False
        self.state['paragraph']=0

def iteratechapters(src):
    en=bibleformatter(src)
    ochapter=''
    obook=''
    oparagraph=None
    bookindex=0
    for paragraph in en.booktoparagraphs():
        paragraph['book_s']=en.singular(paragraph['book'])  # singular
        if not oparagraph: oparagraph=paragraph
        o = '';
        # End previous chapter?
        chapter = '{%(book_s)s %(chapter)s}' % paragraph
        if ochapter and chapter!=ochapter:
            o += r'\biblendchapter{%(book_s)s %(chapter)s}{%(index)s}' % oparagraph + '%\n'
        # End previous book?
        if paragraph['newbook']:
            if obook:
                o += r'\biblendbook{'+obook+'}{'+str(paragraph['index'])+'}%\n'
            # yield r'\biblchapter{'+paragraph['book']+' / ' + right['book']+'}\n'  # TeX chapter, which is a book of the Bible

        if paragraph['newsection']:
            o += r'\biblnewsection'+'%\n'

        if paragraph['newbook']:
            o+=r'\biblbookheading{'+paragraph['book']+'}%\n';
            o+= r'\biblnewbook{'+paragraph['book'] + '}{'+paragraph['short']+'}{'+str(bookindex)+'}%\n' 
            bookindex+=1
            obook=paragraph['book']
    
        # Print current chapter
        if chapter!=ochapter:
            if paragraph['book'] in ('Obadiah','Philemon','2 John','3 John','Jude'):
                o += r'\biblnewchapter{%(book_s)s}' % paragraph + '%\n' # omit chapter from heading for 1-heading book
            else:
                o += r'\biblnewchapter{%(book_s)s %(chapter)s}' % paragraph + '%\n'
            ochapter=chapter
        elif (chapter==ochapter):
            o+=r'\biblsyntheticpar'+'%\n'
        o+=paragraph['chaptertext'].strip()+'%\n';  # /par ?
        yield o
        oparagraph=paragraph

outfd=sys.stdout
if len(sys.argv)>1:
    outfd=open(sys.argv[1],'w')
src='../1769.txt'
src='../TEXT-PCE-127.txt'
for splurge in iteratechapters(src):
    outfd.write( splurge )



# 2 Kings 1:43 And he walked in all the ways of Asa his father; he turned not aside from it, doing that which was right in the eyes of the LORD : nevertheless the high places were not taken away; for the people offered and burnt incense yet in the high places.
# 43 En hy het geheel en al in die weg van sy vader Asa gewandel — daarvan het hy nie afgewyk nie — deur te doen wat reg was in die oë van die HERE.
# 44 Net die hoogtes is nie afgeskaf nie; die volk het nog op die hoogtes geoffer en rook laat opgaan.

