#FUNCTION: DOWNLOADS ALL THE URLS FROM GETHTTP.PY IN HTML FORMAT

from urllib2 import urlopen
import re
import os

savepath2=os.getcwd().replace('\\','/')+'/opr/web/' #location of http pages saved
savefile2=lambda x : os.path.join(savepath2,x)

if not os.path.exists(savepath2):
	os.makedirs(savepath2)

getpath2=os.getcwd().replace('\\','/')+'/opr/' #location of the txt with list of websites
getfile=lambda x : os.path.join(getpath2,x)

counter=[0]*11

fin=open(getfile('match.txt'),'r')
finC=open(getfile('matchchamp.txt'),'r')

foutF=open(savefile2('error.txt'),'w')

for url in fin.readlines(): #for each line of fin
	store=re.findall('(?:.*)(20(?:0[2-9]|1[0-3]))(?:comp.*)',url,re.I) #identify what year the specific competition was and stores year into array called store
	store=store[0] #array called store[0] is simplified to variable 'store'
	counter[int(store)-2003]+=1 #keep track of number of elements per year
	
	fpath=savefile2(str(store.replace('20',''))) #organizes each year into individual years
	
	if not os.path.exists(fpath):
		os.makedirs(fpath)
		
	matchname=fpath+'/'+str(store)+' match '+str(counter[int(store)-2003])+'.html' #names the html file, in order of processing "<year> match (1..n).html"
	
	fout=open(matchname,'w')
	fout.write(url)
	try: #try to the following and go to 'except' if it fails
		site= urlopen(url).read() #store contents of the html page in 'site'
		fout.write(site)
	except:
		fout.write("404 Error: Page was not found")
		foutF.write(url)
	
	fout.close()
	
#same except for championship
counter=[0]*11
foutF.write('\n')

for url in finC.readlines():
	print url
	store=re.findall('(?:.*)(20(?:0[2-9]|1[0-3]))(?:comp.*)',url,re.I)
	store=store[0]
	counter[int(store)-2003]+=1
	
	fpath=savefile2(str(store.replace('20',''))+'/Championship')
	
	if not os.path.exists(fpath):
		os.makedirs(fpath)
	
	matchnameC=fpath+'/'+str(store)+' champmatch '+str(counter[int(store)-2003])+'.html'
	
	foutC=open(matchnameC,'w')
	foutC.write(url)
	try:
		site= urlopen(url).read()
		foutC.write(site)
		print 'done'
	except:
		foutC.write("404 Error: Page was not found")
		foutF.write(url)
	
	foutC.close()

fin.close()
finC.close()



