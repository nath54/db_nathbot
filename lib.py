#coding:utf-8
import random,io

loadblgs=True
loadcmps=True
loadcens=True

fichsb=["dj1.nath"]
fichsc=["cmp1.nath"]
fichcens=["motspasbiens.nath"]

blgs=[]
cmps=[]
cens=[]

phrases_arrivees=["Mais qui est-ce ?","Nous avons un nouveau soldat !","Un nouvel état est déclaré !","Une nouvelle recrue a été recrutée !"]

#
if loadblgs:
    blgs=[]
    for ff in fichsb:
        f=io.open(ff,"r",encoding="utf-8")
        blgs=list(set(blgs+[bb for bb in f.read().split("|||||") if len(bb)>3 ]))
        f.close()

if loadcmps:
    cmps=[]
    for ff in fichsc:
        f=io.open(ff,"r",encoding="utf-8")
        cmps+=[cc for cc in f.read().split("|||||") if len(cc)>3]
        f.close()

if loadcens:
    cens=[]
    for ff in fichcens:
        f=io.open(ff,"r",encoding="utf-8")
        cens=list(set(cens+[cc for cc in f.read().split("\n") if len(cc)>=1 ]))
        f.close()
    cens.sort(key=lambda item:len(item))
    cens=cens[::-1]
#
def help():
	txt="""
Voici une petite liste de commandes :
    - `n)help` : affiche l'aide
    - `n)dm pseudo msg` : le bot envoie un message privé au pseudo
    - `n)+ a b c ...` : additionne a b c ...
    - `n)* a b c ...` : multiplie a b c ...
    - `n)complimente moi` : vous complimente
    - `n)blague` : fait une blague
    - `n)nbalea`:
        -0 arguments : renvoie un nombre entre 1 et 10
        -1 argument : renvoie un nombre entre 1 et le nombre donné
        -2 arguments : renvoie un nombre entre les deux nombres donnés
    - `n)invite` : crée une invitation
    - `n)delinvites` : détruit toutes les invitations
    - ``
	"""
	return txt

def blague():
    global blgs
    if not loadblgs:
        blgs=[]
        for ff in fichsb:
            f=io.open(ff,"r",encoding="utf-8")
            bblgs=list(set(blgs+[bb for bb in f.read().split("|||||") if len(bb)>3 ]))
            f.close()
    ######################################
    txt=random.choice(blgs)
    return txt
	
def compliment(n):
    global cmps
    if not loadcmps:
        cmps=[]
        for ff in fichsc:
            f=io.open(ff,"r",encoding="utf-8")
            cmps+=[cc for cc in f.read().split("|||||") if len(cc)>3]
            f.close()
    ######################################
    c=random.choice(cmps)
    txt=n.join(c.split("@nom"))
    return txt

def testmotspasbiens(content):
    global cens
    #print("Test ",content)
    if not loadcens:
        cens=[]
        for ff in fichcens:
            f=io.open(ff,"r",encoding="utf-8")
            cens=list(set(cens+[cc for cc in f.read().split("\n") if len(cc)>=1 ]))
            f.close()
    #####################################
    newmes=content
    bien=True
    vulgarites=[]
    if False: #methode 1
        cont=content.split(" ")
        for c in cont:
            #print(c)
            if c.lower().strip() in cens:
                vulgarites.append(c)
                #print("mot pas bien détécté : ",c)
                bien=False
                nt="".join(["*" for lettre in c])
                newmes=nt.join(newmes.split(c))
                #print("new message : ",newmes)
    elif True: #methode 2
        cont=content.lower()
        for c in cens:
            if len(cont.split(c))>=2:
                #print(c)
                vulgarites.append(c)
                bien=False
                nt="".join(["#" for lettre in c])
                #print(nt)
                newmes=nt.join(cont.split(c))
                cont=newmes
                #print(newmes)
    return bien,newmes,vulgarites

