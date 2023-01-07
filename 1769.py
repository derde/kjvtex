#! /usr/bin/python3

import re

class Errata:
  def __init__(self,fn):
    fd=open(fn,'r')
    self.verse={}
    for line in fd:
      m=re.search('^(.*?\d+:\d+)',line)
      if not m: continue
      ref=m.group(1)
      self.verse[ref]=line
  def erratum(self,line):
    m=re.search('^(.*?\d+:\d+)',line)
    ref=m.group(1)
    return self.verse.get(ref,line)
      
errata = Errata('1769.errata')
titles = Errata('1769.titles')
fi = open('1769.txt','r')
fo = open('1769.fix','w')
fo.write('Source: 1769 from textus-receptus-bibles, with errata fixed\n');
for line in fi:
    line=errata.erratum(line)
    title=titles.erratum(line)
    if title!=line:
        line_m=re.search("^(.*\d+:\d+) (.*)",line)
        ref,text=line_m.groups()
        m=re.search('(<<.*>>)',title)
        thetitle=m.group(1)
        if line.startswith("Psalm"):
           line=ref+' '+thetitle+' '+text+'\r\n'
        else:
           line=ref+' '+text+' '+thetitle+'\r\n'

    fo.write(line)
fo.close()
