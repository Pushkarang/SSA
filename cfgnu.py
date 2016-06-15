# prints cfg used by ssa.py and file 'c' contains cfg with leader as node

import re
f = open("s.ll","r")
ff = open("c","w")
h = "i"
p=""
LL=[]
def insert(x):
    x = x.replace(" ","")
    if x not in LL:
         LL.append(x)

# prints cfg with leader as node
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
#prints cfg in number representation
print len(LL)
f.close()
ff.close()
f = open("c","r")
while True:
    l = f.readline()
    if not l:
        break
    ll = []
    ll = l.split()
    for i in range(len(ll)-1):
        print LL.index(ll[i])+1,"",LL.index(ll[i+1])+1
