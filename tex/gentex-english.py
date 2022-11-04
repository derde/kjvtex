#! /usr/bin/python3
# coding: utf-8

# DISCLAIMER: this code is torturous, because it is hacked from code for making
# a side-by-side parallel Bible, which needs a lot of bad hacks.  I'm sorry.
# Don't write your own code like this.  Be better.

import re
import itertools
import sys,copy


english='en'
afrikaans='af'

class Hebrew:
    def __init__(self,file='hebrew-words'):
        fd=open(file,'r')
        self.lookup={}
        for line in fd:
            bits=line.split('\t')
            ref,NAME,uni,chars=bits[:4]
            self.lookup[ref]={ 'NAME': NAME, 'ref':ref, 'chars':chars }
    def adjust(self,text,p):
        'Zap the "ALEPH." away, and return the character to use'
        c=''
        if p['book'] == "Psalms" and p['REFERENCE'] in self.lookup:
            r=self.lookup[p['REFERENCE']]
            text=text.replace(r['NAME'],'')
            c=r['chars']
        return text,c

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

    def __init__(self,file):
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
    bookAbbreviationsEN = {
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
    bookAbbreviationsAF={
        'Genesis':           'Genesis',
        'Exodus':            'Exodus',
        'Levitikus':         'Levitikus',
        'Numeri':            'Numeri',
        'Deuteronomium':     'Deuteronomium',
        'Josua':             'Josua',
        'Rigters':           'Rigters',
        'Rut':               'Rut',
        '1 Samuel':          '1 Samuel',
        '2 Samuel':          '2 Samuel',
        '1 Konings':         '1 Konings',
        '2 Konings':         '2 Konings',
        '1 Kronieke':        '1 Kronieke',
        '2 Kronieke':        '2 Kronieke',
        'Esra':              'Esra',
        'Nehemia':           'Nehemia',
        'Ester':             'Ester',
        'Job':               'Job',
        'Psalms':            'Psalms',
        'Spreuke':           'Spreuke',
        'Prediker':          'Prediker',
        'Hooglied':          'Hooglied',
        'Jesaja':            'Jesaja',
        'Jeremia':           'Jeremia',
        'Klaagliedere':      'Klaagliedere',
        'Esegiel':           'Esegiel',
        'Daniel':            'Daniel',
        'Hosea':             'Hosea',
        'Joel':              'Joel',
        'Amos':              'Amos',
        'Obadja':            'Obadja',
        'Jona':              'Jona',
        'Miga':              'Miga',
        'Nahum':             'Nahum',
        'Habakuk':           'Habakuk',
        'Sefanja':           'Sefanja',
        'Haggai':            'Haggai',
        'Sagaria':           'Sagaria',
        'Maleagi':           'Maleagi',
        'Mattheus':          'Mattheus',
        'Markus':            'Markus',
        'Lukas':             'Lukas',
        'Johannes':          'Johannes',
        'Handelinge':        'Handelinge',
        'Romeine':           'Romeine',
        '1 Korinthiers':     '1 Korinthiers',
        '2 Korinthiers':     '2 Korinthiers',
        'Galasiers':         'Galasiers',
        'Efesiers':          'Efesiers',
        'Filippense':        'Filippense',
        'Kolossense':        'Kolossense',
        '1 Thessalonicense': '1 Thessalonicense',
        '2 Thessalonicense': '2 Thessalonicense',
        '1 Timotheus':       '1 Timotheus',
        '2 Timotheus':       '2 Timotheus',
        'Titus':             'Titus',
        'Filemon':           'Filemon',
        'Hebreers':          'Hebreers',
        'Jakobus':           'Jakobus',
        '1 Petrus':          '1 Petrus',
        '2 Petrus':          '2 Petrus',
        '1 Johannes':        '1 Johannes',
        '2 Johannes':        '2 Johannes',
        '3 Johannes':        '3 Johannes',
        'Judas':             'Judas',
        'Openbaring':        'Openbaring',
    }

    def __init__(self,language,file):
        self.language=language;
        self.state={
            'book': '',
            'chapter': '',
            'chapter': '', }
        self.language=language
        if language==english:
            self.bookAbbreviations=self.bookAbbreviationsEN
            self.oldtestament="OLD TESTAMENT"
            self.newtestament="NEW TESTAMENT"
        elif language==afrikaans:
            self.bookAbbreviations=self.bookAbbreviationsAF
            self.oldtestament="OU TESTAMENT"
            self.newtestament="NUWE TESTAMENT"
        self.paragraphdivisions=paragraphdivisions('1526.Pericopes.csv')
        self.markheading=r'\markright';
        self.fd=file
        self.shortnames={}
        for k,v in self.bookAbbreviations.items():
            self.shortnames[v]=k

    def booktochapters(self):
        '''Read in the bible file, and parse to book, chapter, verse and text'''
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
        o+=r'\bibldropcapschapter{'+chapter+'}' + '%\n' 
        # o+=self.verseheading('1') + '%\n'
        return o

    def verseheading(self,verse):
        # r+=  r'\verse{'+verse+'}'  
        cmd='\\verse'
        if verse=='1': cmd=r'\versei'
        elif verse=='2': cmd=r'\verseii'
        else: cmd=r'\verse'
        return r' '+cmd+'{'+verse+'}{'+str(self.state['index'])+'}'

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
        'Written to folks by writer'
        # return '\par{\em ' + m.group(1) + '}'
        return r'\biblepistleattribution{em ' + m.group(1) + '}'
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
        dontsmallcapsnt=['AEnas','JESUS','For David himself said by the Holy Ghost','KING OF','TO THE UNKNOWN GOD','MYSTERY'];
        if re.search('|'.join(dontsmallcapsnt),text): 
            return text
        text=re.sub(r"([A-Z]{2,}'?S?)(\s*)", self.sub_format_smallcaps, text)
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
        self.state['index']=26
        self.state['shortbook']=''
        newbook=True
        hebrew=Hebrew()
        yield r'\biblbeforeoldtestament' % self.state +'%\n'
        yield (r'\biblnewsection{'+self.oldtestament+'}') % self.state +'%\n'
        for book,chapter,verse,text in self.booktochapters():
            ostate=copy.copy(self.state)
            self.state['book']=book
            self.state['book_s']=self.singular(self.state['book'])  # singular
            self.state['BOOK']=self.singular(book.upper())
            self.state['short']=self.shortnames[book]
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
                yield ( r'\biblendchapter{%(book_s)s %(chapter)s}{%(index)s}' % ostate ) + '%\n'
            if newbook and ostate['book']:
                yield ( r'\biblendbook{%(book)s}' % ostate ) + '%\n'
            if newbook and book.startswith('Matthe'): # matthew/matteus
                yield ( r'\biblbeforenewtestament' % self.state ) + '%\n'
                yield ( (r'\biblnewsection{'+self.newtestament+'}') % self.state ) + '%\n'
            if newbook:
                self.state['index']=(self.state['index']+1) % 66
                yield r'\biblbookheading{%(book)s}' % self.state+'%\n';
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
            text,aleph=hebrew.adjust(text,self.state)
            if aleph:
                t += '\hebrewprefix{'+aleph+'} '
            t += self.verseheading(verse)
            t += r'\biblnewreference{%(REFERENCE)s}{%(index)s}' % self.state
            text=re.sub(r'<<\[(.*?)\]>>*',self.sub_format_epistleattribution,text)
            text=re.sub(r'<<([^a-z]*?)>>',self.sub_format_sectionsep,text)
            text=re.sub(r'<<(.*?)>>',self.sub_format_psalmheading,text)
            text=re.sub(r'\[(.*?)\]',self.sub_format_italics,text)
            t += self.reformat_smallcaps(text)
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
src_dst = [
    (english,   '../TEXT-PCE-127.txt', 'english.tex'),
    (afrikaans, '../af1953.txt', 'afrikaans.tex'), ]

for language,srcfile,dstfile in src_dst:
    src=open(srcfile,'r')
    outfd=open(dstfile,'w')
    #src=os.popen('grep ^Ps < ../TEXT-PCE-127.txt','r')
    for splurge in iteratechapters(language,src):
        outfd.write( splurge )
    outfd.close()


# 2 Kings 1:43 And he walked in all the ways of Asa his father; he turned not aside from it, doing that which was right in the eyes of the LORD : nevertheless the high places were not taken away; for the people offered and burnt incense yet in the high places.
# 43 En hy het geheel en al in die weg van sy vader Asa gewandel — daarvan het hy nie afgewyk nie — deur te doen wat reg was in die oë van die HERE.
# 44 Net die hoogtes is nie afgeskaf nie; die volk het nog op die hoogtes geoffer en rook laat opgaan.

