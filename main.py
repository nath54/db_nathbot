#coding:utf-8
import discord
import io
import lib
import random

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
    
    async def on_ready(self):
        print("Logged in as ")
        print(self.user.name)
        print(self.user.id)
        print("---------")
        for ic in [692779375367553127]:
            gen=self.get_channel(ic) #get le general du server de test
            await gen.send("Ouaah, le bot nathbot est levé, il est pret a vous écouter !")
    
    async def on_new_user_in_server(self,p):
        for ic in [693029376341573722]:
            gen=self.get_channel(ic) #get le general du server de test
            await gen.send(embed=create_embed(self,titre=random.choice(lib.phrases_arrivees),description=p.name+" est arrivé sur ce serveur !",color=discord.Colour(int("0x000000",16)),img=p.avatar_url))
                
    
    async def on_message(self,msg):
        author=msg.author
        content=msg.content
        if(msg.author == self.user):
            return
        ############################################### PING ###############################################
        elif(content.startswith(config["prefix"]+"ping")):
            await msg.channel.send("pong")
        ############################################### EXIT ###############################################
        elif(content.startswith(config["prefix"]+"exit")):
            #TODO
            #exit()
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
            invites = await message.guild.invites()
            for i in invites:
                await i.delete()
            
        ############################################### AIDE ###############################################                    
        elif(content.startswith(config["prefix"]+"help")):
            txt=lib.help()
            await msg.channel.send(txt)
            
                

#on lance le programme
if __name__== "__main__":
    bot = Bot()
    bot.run(config["token"])






