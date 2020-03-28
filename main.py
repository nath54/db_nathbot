#coding:utf-8

print("Démarage...")

import discord
import io
import lib
import random
import time
import quickpoll
import eval_expr
#import openjson

print("Librairies chargées.")

print("Chargement des infos du bot...")
#
debug=True

#on recup les infos
f=io.open("config.naths","r",encoding="utf-8")
data=f.read().strip().split("\n")
f.close()
config=dict([tuple(d.split(":")) for d in data])
if debug: print(config)

f=io.open("color.nath","r",encoding="utf-8")
data=f.read().strip().split("\n")
f.close()
colors=dict([tuple(  [d.split(":")[0],discord.Colour( int(d.split(":")[1], 16) )] ) for d in data])
if debug: print(colors)

print("Infos du bot chargées.")

#
async def senddmmessage(msg,member,txt):
    try:
        await member.send(txt)
    except discord.Forbidden:
        await msg.channel.send("La personne ayant le nom "+cc[1]+" a bloqué ses messages privés !")
    except:
        await msg.channel.send("Il y a eu une erreur :( ")


#class bot
class Bot(discord.Client):
    def __init__(self):
        super().__init__()
    
    
    def random_color(self):
        hexas="0123456789abcdef"
        random_hex="0x"+"".join([random.choice(hexas) for x in range(6)])
        return discord.Colour(int(random_hex, 16))
    
    def create_embed(self,titre="titre",description="description",color=discord.Colour(int("0x000000",16)),img=""):
        embed=discord.Embed()
        embed.title=titre
        embed.description=description
        embed.colour=color
        if(img!=""):
            embed.set_image(url=img)
        return embed
    
    def censure_on_this_server(self,msg):
        #TODO
        return True
    
    
    async def on_ready(self):
        actt=["Vous répondre"]
        await self.change_presence(activity=discord.Game(name=actt[0]))
        #await self.change_presence(activity=discord.CustomActivity(name=actt[0]))
        print("Logged in as ")
        print(self.user.name)
        print(self.user.id)
        print("---------")
        for ic in [692779375367553127,693088240722378772]:
            gen=self.get_channel(ic) #get le general du server de test
            await gen.send("Ouaah, le bot nathbot est levé, il est pret a vous écouter !")
    
    async def on_new_user_in_server(self,p):
        for ic in [693029376341573722]:
            gen=self.get_channel(ic) #get le general du server de test
            await gen.send(embed=create_embed(self,titre=random.choice(lib.phrases_arrivees),description=p.name+" est arrivé sur ce serveur !",color=discord.Colour(int("0x000000",16)),img=p.avatar_url))
                
    
    async def on_message(self,msg):
        author=msg.author
        content=msg.content
        imun=False
        for r in msg.author.roles:
            if r.name in ["immunisé a nathbot"]: imun=True
        try:
            if(msg.author == self.user):
                return
            ############################################### PETITES FUTILITES #####################################
            
            if not imun:
                if(content.lower().startswith("bonjour")): await msg.channel.send("Bonjour <@!"+str(msg.author.id)+"> !")
                elif(content.lower().startswith("salut")): await msg.channel.send("Salut <@!"+str(msg.author.id)+"> !")
                elif(content.lower().startswith("aurevoir")): await msg.channel.send("Aurevoir <@!"+str(msg.author.id)+"> !")
                elif(content.lower().startswith("yo")): await msg.channel.send("Yo <@!"+str(msg.author.id)+"> !")
                elif(content.lower().startswith("hello")): await msg.channel.send("Hello <@!"+str(msg.author.id)+"> !")
                elif(content.lower().startswith("hi")): await msg.channel.send("Hi <@!"+str(msg.author.id)+"> !")
                elif(content.lower().startswith("oui")): await msg.channel.send("non !")
                elif(content.lower().startswith("non")): await msg.channel.send("oui !")
                elif(content.lower().startswith("si")): await msg.channel.send("nan !")
                elif(content.lower().startswith("nan")): await msg.channel.send("si !")
            
            ############################################### PING ###############################################
            if(content.startswith("ping")):
                await msg.channel.send("pong")
                
            ############################################### EXIT ###############################################
            elif(content.startswith(config["prefix"]+"exit")):
                #TODO
                await self.logout()
                exit()
                pass
                
            ############################################### MESSAGES PRIVES ###############################################
            elif(content.startswith(config["prefix"]+"dm")):
                cc=content.split(" ")
                if(len(cc)>=2): 
                    if(len(cc)>=3): txt=" ".join(cc[2:])
                    else: txt="Hello !"
                    if cc[1]!="all":
                        member=discord.utils.get(msg.guild.members, name=cc[1])
                        if member!=None:
                            try:
                                await member.send(txt)
                                if debug: print("Envoyé a : "+member.name)
                            except discord.Forbidden:
                                await msg.channel.send("La personne ayant le nom "+cc[1]+" a bloqué ses messages privés !")
                            except:
                                await msg.channel.send("Il y a eu une erreur lors de l'envoi du message à "+member.name+" :( ")
                        else:
                            await msg.channel.send("il n'y a personne ayant le nom "+cc[1]+" ici !")
                    elif cc[1]=="all":
                        for member in msg.guild.members:
                            if member!=self.user:
                                try:
                                    await member.send(txt)
                                    if debug: print("Envoyé a : "+member.name)
                                except discord.Forbidden:
                                    await msg.channel.send("La personne ayant le nom "+cc[1]+" a bloqué ses messages privés !")
                                except:
                                    await msg.channel.send("Il y a eu une erreur lors de l'envoi du message à "+member.name+" :( ")
                                
            ############################################### ADDITION ###############################################
            elif(content.startswith(config["prefix"]+"+")):
                cc=content.split(" ")
                if(len(cc)>=2):
                    try:
                    #if 1:
                        liste=[float(el) for el in cc[1:]]
                        listte=[str(el) for el in liste]
                        await msg.channel.send(" + ".join(listte)+" = "+str(sum(liste)))
                    except:
                    #else:
                        await msg.channel.send("Eh Oh ! je ne peux qu'additionner que des nombre !, essaie de faire de l'algebre avec des patates et des bananes !")
                        
            ############################################### MULTIPLICATION ###############################################
            elif(content.startswith(config["prefix"]+"*")):
                cc=content.split(" ")
                if(len(cc)>=2):
                    try:
                    #if 1:
                        liste=[float(el) for el in cc[1:]]
                        listte=[str(el) for el in liste]
                        r=1
                        for l in liste: r*=l
                        await msg.channel.send(" * ".join(listte)+" = "+str(r))
                    except:
                    #else:
                        await msg.channel.send("Eh Oh ! je ne peux qu'additionner que des nombre !, essaie de faire de l'algebre avec des carotte et des chou-fleurs !")
                        
            ############################################### BLAGUE ###############################################                    
            elif(content.startswith(config["prefix"]+"blague")): 
                await msg.channel.send( lib.blague() )
                
            ############################################### BLAGUE ###############################################                    
            elif(content.startswith(config["prefix"]+"complimente moi")): 
                nom=str(msg.author.name)
                await msg.channel.send( lib.compliment(nom) )
                
            ############################################### NB ALEATOIRE ###############################################                    
            elif(content.startswith(config["prefix"]+"nbalea")):
                cc=content.split(" ")
                if len(cc)>=3:
                    try:
                        await msg.channel.send( str( random.randint( int(cc[1]) , int(cc[2]) ) ) )
                    except:
                        await msg.channel.send("il y a eu une erreur, as-tu bien donné un nombre en argument et est-ce que ton premier nombre est bien inférieur au deuxieme nombre ?")
                    
                elif len(cc)>=2:
                    try:
                        await msg.channel.send( str(random.randint(1,int(cc[1]))) )
                    except:
                        await msg.channel.send("il y a eu une erreur, as-tu bien donné un nombre en argument ?")
                else:
                    try:
                        await msg.channel.send( str(random.randint(1,10)) )
                    except:
                        await msg.channel.send("il y a eu une erreur, mais qu'a tu encore fait comme bêtise ?")
            
            ############################################### AIDE ###############################################                    
            elif(content.startswith(config["prefix"]+"embed")):
                author=msg.author
                image=author.avatar_url
                couleur=self.random_color()
                description=" ".join(content.split(" ")[1:])
                titre=author.name
                print("titre : ",titre," description : ",description," couleur : ",couleur," image : ",image)
                embed=self.create_embed(titre=titre,description=description,color=couleur,img=image)
                await msg.channel.send(embed=embed)
                
            ############################################### INVITATIONS ###############################################                    
            elif(content.startswith(config["prefix"]+"invite")): 
                invite = await msg.channel.create_invite(unique=False)
                await msg.channel.send(invite.url)
                
            ############################################### INVITATIONS ###############################################                    
            elif(content.startswith(config["prefix"]+"delinvites")): 
                invites = await msg.guild.invites()
                for i in invites:
                    await i.delete()
                await msg.channel.send("Toutes les invitations ont bien été supprimées")
                
            ############################################### COMPTER ###############################################                    
            elif(content.startswith(config["prefix"]+"compter")):
                cc=content.split(" ")
                if len(cc)>=2:
                    if True:
                        vitesse=0.5
                        if len(cc)>=3:
                            if " ".join(cc[2:])=="très lent": vitesse=2
                            elif " ".join(cc[2:])=="lent": vitesse=1
                            elif " ".join(cc[2:])=="moyen": vitesse=0.5
                            elif " ".join(cc[2:])=="rapide": vitesse=0.3
                            elif " ".join(cc[2:])=="très rapide": vitesse=0.1
                        mes = await msg.channel.send("0")
                        arg1=int(cc[1])
                        for x in range(0,arg1+1):
                            await mes.edit(content="Je compte jusqu'à "+str(arg1)+ ": "+str(x))
                            time.sleep(vitesse)
                    else:
                        await msg.channel.send("Eh, il faut un nombre positif pour que cette commande fonctionne !")
                else:
                    await msg.channel.send("Eh, il faut un nombre positif pour que cette commande fonctionne !")
            ############################################### AIDE ###############################################                    
            elif(content.startswith(config["prefix"]+"calcul ")):
                expr=content[len(config["prefix"]+"calcul "):]
                e=eval_expr.convert(expr)
                ne=eval_expr.traite1(e)
                res=eval_expr.f(ne,{})
                await msg.channel.send("Le résultat du calcul est : "+str(res))
            ############################################### AIDE ###############################################                    
            elif(content.startswith(config["prefix"]+"help")):
                txt=lib.help()
                await msg.channel.send(txt)
                
            ############################################### CENSURE ###################################################
            if(self.censure_on_this_server(msg)):
                bien,newmes,vulgarites=lib.testmotspasbiens(msg.content)
                if not imun:
                    if not bien and False:
                        await msg.delete()
                        mes = await msg.channel.send("Eh Oh ! Ce n'est vraiment pas bien ce que tu viens de dire la "+str(msg.author)+" !")
                        #
                        time.sleep(3)
                        #
                        await mes.edit(content="autodestruction...")
                        time.sleep(0.5)
                        await mes.delete()
                        
                    if not bien and True:
                        mes = await msg.channel.send("Pas de vulgarités !")
                        await msg.channel.send("<@!"+str(msg.author.id)+"> a dit : "+newmes)
                        await msg.delete()
                        #
                        time.sleep(3)
                        #
                        await mes.edit(content="autodestruction...")
                        time.sleep(0.5)
                        await mes.delete()
                        #await msg.edit(content=newmes)
                else:
                    if not bien:
                        mes = await msg.channel.send("Vous avez de la chance d'être immunisé, car vous avez dit des mots vulgaires : "+str(vulgarites))
                        #
                        time.sleep(3)
                        #
                        await mes.edit(content="autodestruction...")
                        time.sleep(0.5)
                        await mes.delete()
        except Exception as e:
            msg.channel.send("Error : "+str(e))                
            
                

print("Démarage du bot...")
#on lance le programme
if __name__== "__main__":
    bot = Bot()
    bot.run(config["token"])
    quickpoll.setup(bot)





