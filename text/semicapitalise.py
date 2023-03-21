#! /usr/bin/python3

# Lowercase unnecessary leading capitals
# Rule 1: Find all proper nouns
# Rule 2: Find lines ending in continuation sentences
# Rule 3: If not in the list of proper nouns, then lowercase it

# Exception to the rule - this is a quote, followed by narrative -
# Genesis 28:6 When Esau saw that Isaac had blessed Jacob, and sent him away to
# Padanaram, to take him a wife from thence; and that as he blessed him he gave
# him a charge, saying, Thou shalt not take a wife of the daughters of Canaan;
# Genesis 28:9 [-then-] {+Then+} went Esau unto Ishmael, and took unto the
# wives which he had Mahalath the daughter of Ishmael Abraham's son, the sister
# of Nebajoth, to be his wife.


import re
import sys

def getpropernouns(fn):
    fd=open(fn,'r')
    propernoun_re=re.compile('[a-z] ([A-Z][a-z]+)')
    pns={}
    for line in fd:
        for m in propernoun_re.findall(line):
            pns[m]=line
    return pns

def decap(fn, fo, propernouns):
    fd=open(fn,'r')
    continuation=False
    continuation_re=re.compile('[:;,]\s*$')
    continuation_bl_re=re.compile('(say|saying|said|written)[a-z ]*[:;,]\s*$') # saying: Quotation
    word_re=re.compile('^(.*:\d+\s+\[?)([A-Z][a-z]+)(.*)',re.S)
    for line in fd:
        if continuation:
            m=word_re.search(line)
            if m and m.group(2) not in propernouns:
                line = m.group(1)+m.group(2).lower()+m.group(3)
        continuation = continuation_re.search(line) and not continuation_bl_re.search(line)
        fo.write(line)

# Get proper nouns
fn='../text/kingjamesbibleonline.txt'
propernouns=getpropernouns(fn)
n='Abialbon Adina Ahi Ahiam Ahinadab Amam Arab Beerah Cretes Dimnah Eliahba Elihoreph Eluzai Hadid Halhul Hallohesh Heleb Hezrai Hezro Hurai Huz Igal Ishmerai Ithai Kenan Machnadebai Magpiash Maharai Malchiram Mishmannah Nohah Non Sallu Shammoth Sibbecai Ummah Uthai Uzzia Vaniah Zenan Hodijah Zelek'
for r in n.split(): propernouns[r]=True
propernouns.pop("The")
propernouns.pop("So")
for k in propernouns: sys.stdout.write(k+' ')
sys.stdout.write('\n')
fo=open('../text/kingjamesbibleonline-semicaps.txt','w')
decap(fn,fo,propernouns)
