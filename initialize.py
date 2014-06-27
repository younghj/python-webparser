#FUNCTION: EXTRACTS ALL THE URLS OF THE MATCHES

from urllib2 import urlopen #from a library called urllib import into the program a function called urlopen
import re,os #import the regular expressions library and the operating system library

'''
regular expressions (also known as regex) is a tool that we are able to use like a find function on Word/Chrome/WindowsExplorer.
similar to when we type 'a' into the find-tool of chrome, it will return all the parts of the webpage that has the letter 'a'
regular expressions will do the same except you are able to work with variables and
work with words even if you don't know what the specific word is but rather only the general pattern for it

tl;dr:
when I have to be brief, I like to explain regex as 'find' (ctrl+f) on steroids

e.g. if you wanted to pick up on the word calculator and the word calculus, then you can ask regex to search for
'calcul.*' (the dot represents any character and the star means '0 or more'



the operating system library gives you the capability to do the actions that you would be able to do in an os

e.g. make directories, search a directory, etc.
'''

def ap(ls,file): #ap is a function that I made to make the files that have broken links, unbroken. Also to count the number of links
	for x in xrange(0,len(ls)): #from the zero-th element of the list of links to the last. (remember that lists start from 0)
		line=re.sub('(?<=match)[es](?=results?)','',ls[x],re.I) #subs the matching string with '' and it is applied to the x-th element of the list; case-insensitive (re.I)
		line=re.sub('(?<=match)[es](?![resultum])','es',line,re.I)
		file.write(line+'\n') #writes to line. remember to add a \n if there wasn't one to start with
	return len(ls)

savepath=os.getcwd().replace('\\','/')+'/opr/' 
'''os.getcwd() is a os function that gets the current working directory (programmers don't like hard names)
then the string returned from that function is refined through another function called replace
it replaces \ with /, \ is an escape character (which means it will make meaningless(a.k.a. literal) character meaningful
and meaningful characters meaningless.

e.g. if '' was to identify a string then '\' would now be one starting quotation mark
with one quote mark inside the string without the ending quotation mark to pair up with the starting quote mark

if n was just the character n; then \n is now a newline character which will essentially go onto the next line or a new line.
'''

if not os.path.exists(savepath):
	os.makedirs(savepath)
'''
if the directory in the savepath does not exist the, the os.path.exists() function will return a 0,
but in order to enter an if-statement the condition has be true,
so you 'not' the result to reverse the given return value.

and if it doesn't exist then os.makedirs(savepath) makes the directory 'savepath'
'''
	
	
name=lambda x : os.path.join(savepath,x) #'portable' function called name that joins x to savepath

fout = open(name('match.txt'),'w')
fchamp = open(name('matchchamp.txt'),'w')
page= urlopen('http://www.usfirst.org/roboticsprograms/frc/archived-game-documentation-and-event-results').read() #opens and reads the provided website

linkPat=re.compile('https://my\.usfirst\.org/myarea/index\.lasso\?event_type=FRC&amp;year=20(?:0[2-9]|1[0-3])',re.I)
#looks for the link to the result documentation

findLink=re.findall(linkPat,page)
#goes through the source code (NOT the user friendly text on the site) and applies the above pattern
#stores the list of matching patterns into findLink

'''
sample links that need to match:
?page=event_details&amp;eid=1284&amp;-session=myarea:0A7D78870760633C92VthO24F66C
?page=event_details&    eid=1276&    -session=myarea:0A7D78870760633C92VthO24F66C
?page=event_details&    eid=1411&    -session=myarea:0A7D7887075a2385BCvySR1D4D7A
?page=event_details&    eid=1424&    -session=myarea:0A7D7887075a2385BCvySR1D4D7A
?page=event_details&    eid=7681&    -session=myarea:0A7D7887075a2385F8IOLo1D5225

general pattern to match all the links or at least the majority:
"\?page=event_details&(amp;)?eid=\d+&-session=myarea:\w+"
'''

print len(findLink) #debugging purposes: doesn't need to be in the program for the program to work
print '\n' #debugging purposes

total=0 #debugging purposes

for i in xrange(0,len(findLink)): #run this loop number of times equal to the number of years matched in the first link
    findLink[i]=findLink[i].replace('amp;','') #you need to look out for things in the source code that 'mess up' the link
    print findLink[i] #debugging purposes

    yearPage=urlopen(findLink[i]).read() #open and read the link that goes to each of the individual years list of competitions
    yearPat=re.compile('\?page=event_details&(?:amp;)?eid=\d*&(?:amp;)?-session=myarea:\w+',re.I) #look for the regional/champ competitions
    findYear=re.findall(yearPat,yearPage) #store all the links matched from the opened webpage in 'yearPage' into a list 'findYear'


    for j in xrange(0,len(findYear)): #run this loop number of times equal to the number of regional/champ matches found in that year
		findYear[j]='https://my.usfirst.org/myarea/index.lasso'+findYear[j].replace('amp;','') 
		#since the pattern matched from the previous search wasn't a link, this makes it a link

		gamePage=urlopen(findYear[j]).read() #opens and reads
		regPat=re.compile('http://www2\.usfirst\.org/\d{4}comp/[Ee]vents/(?!CMP)[A-Z]+(?:\d)?/[mM]atch[Rresultum]*\.html') #differentiate regional competitions
		champPat=re.compile('http://www2\.usfirst\.org/\d{4}comp/[eE]vents/(?:\w[a-z]*|CMP)/[Mm]atch[Rresultum]*\.html') #differentiate championship compettions
		
		findReg=re.findall(regPat,gamePage) #match regPat in gamePage and store all matched values into a list findReg
		findChamp=re.findall(champPat,gamePage) #same as above with different variables

		total+=ap(findReg,fout) #partially debugging purposes: don't need to total the return value
		total+=ap(findChamp,fchamp) #partially debugging purposes
		
    


print total #debugging purposes
totalsub=total #debugging purposes

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

six=urlopen('http://www.usfirst.org/roboticsprograms/frc/2006-event-results').read() #no pattern just the link open and read
five=urlopen('http://www.usfirst.org/roboticsprograms/frc/2005-frc-regional-and-championship-results').read() #same as above

sixPat=re.compile('http://www2\.usfirst\.org/2006comp/[Ee]vents/(?!CURIE)[A-Z]{1,5}(?:\d)?/(?:bak\.)?[Mm]atch[Rresultum]*\.html')
sixchampPat=re.compile('http://www2\.usfirst\.org/2006comp/[Ee]vents/(?:(?=CURIE)\w{5}|\w{6,})/(?:bak\.)?[Mm]atch[Rresultum]*\.html')

fivePat=re.compile('http://www2\.usfirst\.org/2005comp/[Ee]vents/[A-Z]+(?:\d)?/(?:bak\.)?[Mm]atch[Rresultum]*\.html')
fivechampPat=re.compile('http://www2\.usfirst\.org/2005comp/[Ee]vents/\w[a-z]+/(?:bak\.)?[Mm]atch[Rresultum]*\.html')

#patterns of the links to the regional and championship matches in the 2006 and 2005 years, respectively

sixLs=re.findall(sixPat,six)
sixChampLs=re.findall(sixchampPat,six)
fiveLs=re.findall(fivePat,five)
fiveChampLs=re.findall(fivechampPat,five)
#apply the patterns to the respective pages and store separately

total+=ap(sixLs,fout)#partially debugging purposes
total+=ap(sixChampLs,fchamp)#partially debugging purposes
total+=ap(fiveLs,fout)#partially debugging purposes
total+=ap(fiveChampLs,fchamp)#partially debugging purposes

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

print total-totalsub #debugging purposes
print total #debugging purposes

fout.close()
fchamp.close()