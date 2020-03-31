#coding:utf-8

nbs="0123456789"
lets="abcdefghiklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
ope="/*-+%"
par="()"


def convert(stringe):
    stringe.replace("[","(")
    stringe.replace("]",")")
    expr,pa,niv=[],[],0
    for c in stringe:
        if c=="(":
            temp=expr
            for p in pa:
                if(pa.index(p))<niv:
                    if type(temp[p])==list:  temp=temp[p]
                    else:     break
            if len(temp)==0:     pa.append(0)
            else:   pa[len(pa)-1]+=1
            niv+=1
            temp.append([])
        elif c==")":
            del(pa[len(pa)-1])
            niv-=1
        else:
            temp=expr
            for p in pa:
                if(pa.index(p))<niv:
                    if type(temp[p])==list:    temp=temp[p]
                    else:          break
            if len(temp)==0: pa.append(0)
            else:  pa[len(pa)-1]+=1
            temp.append(c)
    return expr
  
def traite1(exp):
    nexp=[]
    if type(exp)==list:
        i=0
        innt=False
        debint=0
        for c in exp:
            if type(c)==list:
                if innt:
                    innt=False
                    nexp.append(int("".join(exp[debint:i])))
                nexp.append(traite1(c))
            elif type(c)==str:
                if not c in nbs:
                    if innt:
                        innt=False
                        nexp.append(int("".join(exp[debint:i])))
                    nexp.append(c)
                elif c in nbs:
                    if not innt:
                        innt=True
                        debint=i
                    
            i+=1            
        if innt:
            nexp.append(int("".join(exp[debint:i])))
    return nexp


def ff(v1,v2,op,vals):
    r=0
    #traite v1
    if type(v1) in [int,float]: pass
    elif type(v1) in [tuple,list]: v1=f(v1,vals)
    elif type(v1)==str:
        if v1 in vals.keys(): v1=vals[v1]
        else: v1=0
    else: v1=0
    #traite v2
    if type(v2) in [int,float]: pass
    elif type(v2) in [tuple,list]: v2=f(v2,vals)
    elif type(v2)==str:
        if v2 in vals.keys(): v2=vals[v2]
        else: v2=0
    else: v2=0
    #op
    if op == "-": r=v1-v2
    elif op=="+": r=v1+v2
    elif op=="*": r=v1*v2
    elif op=="/": r=v1/v2
    elif op=="^": r=v1**v2
    elif op=="//": r=v1//v2
    elif op=="%": r=v1%v2
    return r

def f(expr,vals):
    r=0
    if type(expr) in [tuple,list]:
        e=list(expr)
        liste_calculs=[]
        if len(e)>3:
            """
            while len(e)>=3:
               v1=e[0]
               v2=e[2]
               op=e[1]
               liste_calculs.append([v1,v2,op])
            
            for c in liste_calculs:
                if c[1]=="/":
                    c[1]="*"
                    c[2]=[1,"/",c[2]]
            """    
            
            while len(e)>=3:
                #v1=e[0]
                #v2=e[2]
                #op=e[1]
                #r=ff(v1,v2,op,vals)
                r=f([e[0],e[1],e[2]],vals)
                e=[r]+e[3:]
        elif len(e)==3:
            v1=e[0]
            v2=e[2]
            op=e[1]
            r=ff(v1,v2,op,vals)
        elif len(e)==2 and e[0]=="-":
            r=ff(0,e[1],"-",vals)
        elif len(e)==1:
            r=f(e[0],vals)
    elif type(expr) in [int,float]:
        r=expr
    return r
        
            
    


