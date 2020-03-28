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

nbs="0123456789"
lets="abcdefghiklmnopqrstuvwxyzéèçàêôûîöïûüëäâù"
ope="/*-+%"
par="()"

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
    - `n)compter nombre vitesse` : Compte jusqu'au nombre positif que vous avez mis à la vitesse que vous avez mit. (pas très utile, mais bon)
            ATTENTION ! : il faut que la vitesse soit parmis la liste ci-dessus, sinon, il va prendre par défaut moyen
            -liste: très lent, lent, moyen, rapide, très rapide
    - `n)calcul expression` : calcule l'expression
            ATTENTION !, faites bien attention à l'écriture de l'expression !
            Il faut bien mettre des parenthèses.
            Car il y a des problemes de priorités de calcul
    - `n)help` : affiche l'aide
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
            cond=True
            ctc=cont.split(c)
            if len(ctc)>=2:
                #print(c)
                for x in range(len(ctc)-1):
                    c1=ctc[x]
                    if c1!="" and c1[-1] in lets:
                        #print("c1 : ",c1)
                        cond=False
                    if x<len(ctc)-2:
                        c2=ctc[x+1]
                        if c2[0] in lets:
                            #print("c2 : ",c2)
                            cond=False
                    
                
            if len(ctc)>=2 and cond:
                #print(c)
                vulgarites.append(c)
                bien=False
                nt="".join(["#" for lettre in c])
                #print(nt)
                newmes=nt.join(cont.split(c))
                cont=newmes
                #print(newmes)
    return bien,newmes,vulgarites

