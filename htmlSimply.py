#FUNCTION: MAKES HTML FILE SIMPLE TEXTFILE EASIER TO PROCESS AND READ

import re,glob,os
'''
glob is like regular expressions in a sense where it finds content without knowing what it will be.
however, it is very simplified. if there was to be different levels of the find function, it would look somewhat like this:
-the find function (ctrl+f)
-glob
-extended glob
-regular expressions
-extended regular expressions
where regex contains many special characters glob only has * ? \ [...] and [!...]
*-match 0 or more of anything, except the escape character (\) to limit in case of directory search
?-match 1 of any character
\-cancel any special effects or create special effects to characters
[...]-match any letters in the box
[!...]-dont match any letters in the box
'''


def cleanup(site): #cleans up html code and returns it
	clpat=re.compile('<.*?>',re.S)
	site=clpat.sub('\n',site)
	
	site=site.replace('&nbsp;',' ')
	site=site.replace('&amp',' ')
	site=site.replace(' Name','name')
	
	blankpat=re.compile('[\n\r]{2,}',re.S)
	site=blankpat.sub('\n',site)
	
	fspcepat=re.compile(' {2,}|\t*',re.M)
	site=fspcepat.sub('',site)
	
	b2pat=re.compile(' ?\n ?',re.S)
	site=b2pat.sub('\n',site)
	
	b3pat=re.compile('\n+',re.S)#'\n{4,}'
	site=b3pat.sub('\n',site)#'\n\n\n'
	
	site=re.sub(r'.*(?=\{behavior:url\(#default#VML\);\})\{behavior:url\(#default#VML\);\}','',site,re.S|re.I|re.M)
			
	ifdelpat=re.compile('(?<=html\n).+?\nif.*else.*?\n',re.S)
	site=ifdelpat.sub('',site)
	
	corrspacepat=re.compile('(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|(?<=\d)(?!comp)(?=[a-zA-Z])',re.S)
	site=corrspacepat.sub(' ',site)
	
	footerpat=re.compile('Match scheduling.*|Data provided by.*|(?:\(Elimination Match Data.*\))?\n\[Results.+\]\n|FIRST&#\d{3,}.+',re.S)#((\(elimination match data.*)?\[results:.*+)#|(?:\(Elimination Match Data.*\))?\n\[Results.+\]\n
	site=footerpat.sub('',site)

	return site



getpath3=os.getcwd().replace('\\','/')+'/opr/web/'
savepath3=os.getcwd().replace('\\','/')+'/opr/result/'

if not os.path.exists(savepath3):
	os.makedirs(savepath3)


for year in xrange(3,14):
	count=1
	ncount=1
	yr= ('0' if year<10 else '') + str(year)+'/'
	yrpath=getfile(yr)
	if not os.path.exists(yrpath.replace('web','result')):
		os.makedirs(yrpath.replace('web','result'))
		
	html=glob.glob(yrpath+'*.html')
	
	for x in html:
		fin=open(x.replace('\\','/'),'r')
		fout=open(x.replace('html','txt').replace('web','result').replace('\\','/'),'w')
		
		site=fin.read()
		
		try:
			clean=cleanup(site)
			fout.write(clean)
			print 'done'+yr+' '+str(count)
			count+=1
		except:
			fout.write('not done')
			print 'nd '+str(ncount)
			ncount+=1

		fin.close()
		fout.close()
		
		
	yrpathc=yrpath+'Championship/'
	
	if not os.path.exists(yrpathc.replace('web','result')):
		os.makedirs(yrpathc.replace('web','result'))
		
	htmlc=glob.glob(yrpathc+'*.html')
	
	for y in htmlc:
		fin=open(y.replace('\\','/'),'r')
		fout=open(y.replace('html','txt').replace('web','result').replace('\\','/'),'w')

		site=fin.read()
			
		try:
			clean=cleanup(site)
			fout.write(clean)
			total[1]+=1
		except:
			fout.write('not done')
		
		fin.close()
		fout.close()