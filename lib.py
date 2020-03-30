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
def help(prefix="n)"):
	txt="""
Voici une petite liste des commandes de ce bot :
    GESTION SERVER
        - `"""+prefix+"""dm pseudo msg` : le bot envoie un message privé au pseudo
        - `"""+prefix+"""invite` : crée une invitation
        - `"""+prefix+"""delinvites` : détruit toutes les invitations
        - `"""+prefix+"""immunise channel` : immunise le canal texte à la censure de vulgarité de nathbot
        - `"""+prefix+"""stop immunise channel` : n'immunise plus le canal texte à la censure de vulgarité de nathbot
    FUN
        - `"""+prefix+"""complimente moi` : vous complimente
        - `"""+prefix+"""blague` : fait une blague
        - `"""+prefix+"""morejokes` : Renvoie une blague , c'est en anglais, mais il y a bcp plus de blagues qu'en francais.
        - `"""+prefix+"""tirer une carte` : Tire une carte aléatoire parmis un jeu de 52 cartes
    MATHS
        - `"""+prefix+"""+ a b c ...` : additionne a b c ...
        - `"""+prefix+"""* a b c ...` : multiplie a b c ...
        - `"""+prefix+"""nbalea`:
            -0 arguments : renvoie un nombre entre 1 et 10
            -1 argument : renvoie un nombre entre 1 et le nombre donné
            -2 arguments : renvoie un nombre entre les deux nombres donnés
        - `"""+prefix+"""calcul expression` : calcule l'expression
            ATTENTION !, faites bien attention à l'écriture de l'expression !
            Il faut bien mettre des parenthèses.
            Car il y a des problemes de priorités de calcul
    LANGUES
        - `"""+prefix+"""trans <destination> texte a traduire`
        ou bien `"""+prefix+"""trans <src> <destination> texte a traduire`: Utilise l'API google traduction pour traduire votre texte
    NE SERT A RIEN
        - `"""+prefix+"""compter nombre vitesse` : Compte jusqu'au nombre positif que vous avez mis à la vitesse que vous avez mit. (pas très utile, mais bon)
            ATTENTION ! : il faut que la vitesse soit parmis la liste ci-dessus, sinon, il va prendre par défaut moyen
            -liste: très lent, lent, moyen, rapide, très rapide
    AUTRE
        - `"""+prefix+"""help` : affiche l'aide
    
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
    if True:
        cont=content.lower()
        for c in cens:
            if c!=cont:
                cond=False
                ctc=cont.split(c)
                if len(ctc)>=2:
                    #print("cont : ",cont)
                    #print("c : ",c)
                    for x in range(len(ctc)-1):
                        cc=True
                        c1=ctc[x]
                        #print("c1 : '"+c1+"'")
                        if c1!="" and c1[-1] in lets:
                            cc=False
                        if (x+1)<=len(ctc)-1:
                            c2=ctc[x+1]
                            #print("c2 : '"+c2+"'")
                            if c2!="" and c2[0] in lets:
                                cc=False
                        if cc: cond=True
                    
            if (len(ctc)>=2 and cond) or c==cont:
                #print(c)
                vulgarites.append(c)
                bien=False
                nt="".join(["#" for lettre in c])
                #print(nt)
                newmes=nt.join(cont.split(c))
                cont=newmes
                #print(newmes)
    return bien,newmes,vulgarites

