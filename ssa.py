import re
f = open("s.ll","r")
h = "i:"
IR ={}
# IR is a dictionary with leader having instructions belongs to that basic block as its value

IR["dummy:"]= ""
IR[h] = ""
while True:
    l = f.readline()
    if not l:
        break
    k = re.search("^[a-zA-Z]+[0-9]*:",l)
    if(k):
    	h = l[k.start():k.end()]
    	IR[h] = ""
    else:
	    k = re.search("goto",l)
	    if(k):
	    	IR[h] = IR[h] + l[:k.start()]
	    	continue
	    IR[h] = IR[h]+l

f.close()

# run python cfgnu.py first to genetate file c

f = open("s.ll","r")
ff = open("c","w")
h = "i"
p=""
LL=["dummy"]
def insert(x):
    x = x.replace(" ","")
    if x not in LL:
         LL.append(x)

# LL is list of all basic block leaders
flag = 0
insert(h)
while True:
    l = f.readline()
    if not l:
        break
    k = re.search("^[a-zA-Z]+[0-9]*:",l)
    if(k):
        h = l[k.start():k.end()-1]
        if(flag==0):
            ff.write(p+" "+h+"\n")
            insert(h)
        flag =0
        continue
    else:
        k = re.search("goto",l)
        if(k):
            flag =1
            ff.write(h+" "+l[k.end():-1]+"\n")
            insert(l[k.end():-1])
            continue
    
    p = str(h)


# a.txt contains cfg 
f = open("a.txt","r")
node = f.readline()
node =int(node)
node =node+1
a = [[0 for x in range(node)] for x in range(node)] 
for l in f:
    r=l.split()
    a[int(r[0])][int(r[1])]=1
doms = [set() for _ in xrange(node)]
D = [set() for _ in xrange(node)]

for i in range(node):
    for j in range(i):
        doms[i].add(j)
for i in range(node):
    if(i!=0):
        tmp1=set()
        l=[]
        for j in range(node):
            if(a[j][i]==1):
                l.append(j)
    
        
        T = []
        for k in l:
            T.append(doms[k])
        p = set()
        if(len(T)>0):
            p = set.intersection(*T)
        doms[i] = set()
        doms[i].add(i)
        doms[i] =set.union(p,doms[i])
# doms is set of dominators
pre = "0"
III=[]
SSS=[]
DD = set()
for j in range(node):
	for i in sorted(doms[j]):
		if(i in DD):
			pre = i
			DD.add(i)
		else:
			III.append(pre)
			SSS.append(i)
			DD.add(i);
			pre=i
def isDom(x,y):
    if(x in doms[y]):
        return True
    else:
        return False

def predec(x):
    p=[]
    for i in range(node):
        if(i >0):
            if(a[i][x]==1):
                p.append(i)

    return p
DomF=[[]]
for i in range(node):
    if(i>0):
        df=[]
        nsd=[i]
        for j in range(node):
            if(j>0):
                if(not isDom(i,j)):
                    nsd.append(j)
        for j in nsd:
            pp = predec(j)
            for k in pp:
                if(isDom(i,k)):
                    df.append(j)
        DomF.append(df)
origin=[]
# DomF contains dominator frontiers
for i in LL:
	origin.append([])

var = set()
#USE function returns list of use variables in x statement
def USE(x):
	use=[]
	k = re.search("=",x)
	if(k):
		u = x[k.end():]
		k = re.findall("[a-zA-Z]+[0-9]*",u)
		if(k):
			for U in k:
				use.append(U)
				continue
	k = re.search("if",x)
	if(k):
		u = x[k.end():]
		k = re.findall("[a-zA-Z]+[0-9]*",u)
		if(k):
			for U in k:
				use.append(U)
				continue

	return use

# DEF returns definations in x statement

def DEF(x):
	kk= re.search("[a-zA-Z]+[0-9]*[a-zA-Z]*[ ]*=",x)
	if(kk):
		k = re.findall("[a-zA-Z]+[0-9]*",x[kk.start():kk.end()])
		return k
		#This  is culprit
	kk= re.search("[a-zA-Z]+[0-9]*[a-zA-Z]*[ ]*<- ",x)
	if(kk):
		k = re.findall("[a-zA-Z]+[0-9]*",x[kk.start():kk.end()])
		return k

	return []

for k in IR.keys():
	v = []
	s = str(IR[k])
	ss = s.split("\n")
	for s in ss:
		kk= re.search("[a-zA-Z]+[0-9]*[a-zA-Z]*[ ]*=",s)
		if(kk):
			v.append(s[kk.start():kk.end()-1].replace(" ",""))
			var.add(s[kk.start():kk.end()-1])
	origin[LL.index(k.replace(":",""))] = v

for n in IR.keys():
	s = str(IR[n])
	S = s.split("\n")
	for s in S:
		k = re.search("phi",s)
		if(not k):
			use = USE(s)
			for u in use:
				var.add(u)
		deff = (DEF(s))
		for d in deff:
			var.add(d)

defsites={}
for v in var:
	defsites[v] = ""

for v in var:
	ln=[]
	ind=0
	for o in origin:
		for e in o:
			if(str(v)==str(e)):
				ln.append(ind)
		ind = ind + 1
	defsites[v] = ln


		
phi={}

# insertion of phi funtion generating phi list
for v in var:
	phi[v]=[]
for v in var:
	W = defsites[v]
	while(len(W)>0):
		n = W.pop()
		for y in DomF[n]:
			if(y not in phi[v]):
				phi[v].append(y)
				if(v not in origin[y]):
					W.append(y)



f = open("a.txt","r")
l = f.readline()
I = []
SS=[]
while True:
    l = f.readline()
    if not l:
        break
    l=l.strip()
    k = re.search(" ",l)
    if(k):
    	I.append((l[k.end()+1:]))
    	SS.append(l[:k.start()])

def NoPre(x):
	return(I.count(x))
def Succ(X):
	x = LL.index(X.replace(":",""))

	succ=[]
	c=0
	for i in SS:
		if(int(i)==int(x)):

			succ.append(LL[int(I[c])])
		c = c+1
	return succ
def PRE(X):

	x = LL.index(X.replace(":",""))
	succ=[]
	c=0
	for i in I:
		if(int(i)==int(x)):

			succ.append(LL[int(SS[c])])
		c = c+1
	return succ	


def child(X):
	x = LL.index(X.replace(":",""))

	chi=[]
	c=0
	for i in III:
		if(int(i)==int(x)):
			chi.append(LL[int(SSS[c])])
		c = c+1
	return chi

# phi function insertion into IR
for i in phi.keys():
	for node in phi[i]:
		ss = (i+",")*NoPre(str(node))
		if(NoPre(str(node))>=2):
			IR[LL[node]+":"] = i+"<- phi ("+ss+")\n"+IR[LL[node]+":"]		


#Renaming

count={}
stack={}


for v in var:
	v = v.replace(" ","")
	count[v]=0
	stack[v]=[]
	stack[v].append(0)

def isphi(x):
	k = re.search("<- phi [(]",x)
	if(k):
		return True
	else:
		return False

def Rename(n):
	s = IR[n]
	S = s.split("\n")
	ir = ""
	originals = S
	for s in S:
		if(not isphi(s)):
			eachuse = USE(s)
			for eu in eachuse:
				k= re.search("=",s)
				if(k):	
					i = len(stack[eu])
					i = stack[eu][i-1]
					tmps = s[k.end():]
					mods = tmps.replace(eu,eu+"["+str(i)+"]")
					mods = s[:k.end()]+mods
					s=mods
				else:
					i = len(stack[eu])
					i = stack[eu][i-1]
					s = s.replace(eu,eu+"["+str(i)+"]")


		for a in DEF(s):
			count[a] = count[a] + 1
			i = count[a]
			stack[a].append(i)
			k = re.search("=",s)
			if(not k):
				k = re.search("<- phi [(]",s)
			if(k):
				tmps = s[:k.start()]
				mods = tmps.replace(a,a+"["+str(i)+"]")
				s = mods+s[k.start():]

		ir = ir+"\n"+s
	IR[n] = ir
	su = Succ(n)
	for Y in su:
		pp = PRE(Y)
		j = pp.index(n.replace(":",""))
		ir = ""
		ys = IR[Y+":"]
		yS = ys.split("\n")
		for ys in yS:
			if(isphi(ys)):
				k = re.search("[(].*[)]",ys)
				listphi = ys[k.start()+1:k.end()-1].split(",")
				i = len(stack[listphi[j]])
				i = stack[listphi[j]][i-1]
				listphi[j] = listphi[j]+"["+str(i)+"]"
				ys = ys[:k.start()]+"("+",".join(listphi)+")"
			ir = ir+"\n"+ys 
		IR[Y+":"] = ir

	for chil in child(n):
		Rename(chil+":")
	for s in originals:
		dd = DEF(s)
		for ddd in dd:
			stack[ddd].pop()

Rename("i:")

print "digraph struct {"
for i in IR.keys():
	if(not i=="dummy:"):
		print i.replace(":","")+"[label=\""
		print IR[i]
		print "\"]"
c=0
for i in SS:
	print LL[int(i)]+"->"+LL[int(I[c])]
	c = c+1
print "}"