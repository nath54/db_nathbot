#coding:utf-8
import random,io

debug=True

loadblgs=True
loadcmps=True
loadcens=True
loadcits=True

fichsb=["dj1.nath"]
fichsc=["cmp1.nath"]
fichcens=["motspasbiens.nath"]
fichscits=["cits1.nath"]

blgs=[]
cmps=[]
cens=[]
cits=[]

phrases_arrivees=["Mais qui est-ce ?","Nous avons un nouveau soldat !","Un nouvel état est déclaré !","Une nouvelle recrue a été recrutée !"]

nbs="0123456789"
lets="abcdefghiklmnopqrstuvwxyzéèçàêôûîöïûüëäâù"
ope="/*-+%"
par="()"

def load_blagues():
    global blgs
    blgs=[]
    for ff in fichsb:
        f=io.open(ff,"r",encoding="utf-8")
        blgs=list(set(blgs+[bb for bb in f.read().split("|||||") if len(bb)>3 ]))
        f.close()

def load_compliments():
    global cmps
    cmps=[]
    for ff in fichsc:
        f=io.open(ff,"r",encoding="utf-8")
        cmps+=[cc for cc in f.read().split("|||||") if len(cc)>3]
        f.close()

def load_citations():
    global cits
    cits=[]
    for ff in fichscits:
        f=io.open(ff,"r",encoding="utf-8")
        cits+=[cc for cc in f.read().split("|||||") if len(cc)>3]
        f.close()

def load_censure():
    global cens
    cens=[]
    for ff in fichcens:
        f=io.open(ff,"r",encoding="utf-8")
        cens=list(set(cens+[cc for cc in f.read().split("\n") if len(cc)>=1 ]))
        f.close()
    cc=[]
    for c in cens: cc.append(c+"s")
    cens+=cc
    cens.sort(key=lambda item:len(item))
    cens=cens[::-1]

def load_reponses():
    f=io.open("reps.nath","r",encoding="utf-8")
    data=f.read().strip().split("\n")
    f.close()
    bot_reponses=[tuple(d.split(":")) for d in data]
    if debug: print(bot_reponses)    
    return bot_reponses

#
print("Chargement des infos du bot...")
if loadblgs: load_blagues()
if loadcmps: load_compliments()
if loadcits: load_citations()
if loadcens: load_censure()
print("Infos du bot chargées.")
    
#
def help(prefix="n)"):
	txt="""
Voici une petite liste des commandes de ce bot :
    GESTION SERVER
        - `"""+prefix+"""dm pseudo msg` : message privés
        - `"""+prefix+"""invite` : crée une invitation
        - `"""+prefix+"""delinvites` : détruit tts les invitations
        - `"""+prefix+"""censure` : canal texte censuré
        - `"""+prefix+"""stop censure` : canal texte plus censuré
    FUN
        - `"""+prefix+"""complimente moi` : vous complimente
        - `"""+prefix+"""blague` : blague
        - `"""+prefix+"""morejokes` : blague (anglais)
        - `"""+prefix+"""tirer une carte` : carte aléatoire
        - `"""+prefix+"""citation` : citation célèbre
    MATHS
        - `"""+prefix+"""nbalea`:
            -0 arguments : nombre entre 1 et 10
            -1 argument : nombre entre 1 et le nombre donné
            -2 arguments : nombre entre les deux nombres donnés
        - `"""+prefix+"""calcul expression` : calcule l'expression
            ATTENTION !, il y a des problemes de priorités de calcul
    LANGUES
        - `"""+prefix+"""trans <destination> texte a traduire`
        ou bien `"""+prefix+"""trans <src> <destination> texte a traduire`: traduit le texte avec google trad
    MUSIC
        - `"""+prefix+"""join` :le bot rejoint le salon vocal
        - `"""+prefix+"""leave` : le bot quitte le salon vocal
        - `"""+prefix+"""play_url url youtube de la musique` : joue de la musique
                    ATTENTION, ne donnez pas une musique trop longue, sinon, elle prendra du temps a charger
        - `"""+prefix+"""pause` : met en pause la musique
        - `"""+prefix+"""resume` : remet en route la musique
        - `"""+prefix+"""stop music` : arrete la musique
    NE SERT A RIEN
        - `"""+prefix+"""compter nombre [lent,moyen,rapide]` : Compte jusque nombre
    AUTRE
        - `"""+prefix+"""help` : affiche l'aide
    
	"""
	return txt

def blague():
    global blgs
    if not loadblgs: load_blaquges()
    ######################################
    txt=random.choice(blgs)
    return txt
	
def citation(search):
    global cits
    if not loadcits: load_citations()
    ######################################
    if search=="": txt=random.choice(cits)
    else:
        search=search.lower().strip()
        citts=[]
        for c in cits:
            ccc=c.lower().split(search)
            if len(ccc)>=2: citts.append(c) #and all([len(cccc)>1 for cccc in ccc]): citts.append(c)
        if len(citts)>0:
            txt=random.choice(citts)
        else:
            txt="Il n'y a pas de résultats"
    return txt
	
def compliment(n):
    global cmps
    if not loadcmps: load_compliments()
    ######################################
    c=random.choice(cmps)
    txt=n.join(c.split("@nom"))
    return txt



def testmotspasbiens(content):
    global cens
    #print("Test ",content)
    if not loadcens: load_censure()
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



