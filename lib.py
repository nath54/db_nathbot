#coding:utf-8
import random,io

loadblgs=True
loadcmps=True

fichsb=["dj1.nath"]
fichsc=["cmp1.nath"]

blgs=[]
cmps=[]

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


