#coding:utf-8

print("Démarage...")

import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os
import io
import lib
import random
import time
import eval_expr
import openjson
import aiohttp
from googletrans import Translator
gtrans=Translator()

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
        self.channels_logs=[]
        self.channels_immunisees=[]
        self.file_save="save.nath"
        self.cac="\n"
        self.ccac="|||||"
        self.cacc="@@@@@"
        self.data_cartes=[
                    ["as de coeur","c_as.png"],["2 de coeur","c_2.png"],["3 de coeur","c_3.png"],["4 de coeur","c_4.png"],["5 de coeur","c_5.png"],["6 de coeur","c_6.png"],["7 de coeur","c_7.png"],["8 de coeur","c_8.png"],["9 de coeur","c_9.png"],["10 de coeur","c_10.png"],["valet de coeur","c_j.png"],["dame de coeur","c_q.png"],["roi de coeur","c_k.png"],
                    ["as de carreaux","cc_as.png"],["2 de carreaux","cc_2.png"],["3 de carreaux","cc_3.png"],["4 de carreaux","cc_4.png"],["5 de carreaux","cc_5.png"],["6 de carreaux","cc_6.png"],["7 de carreaux","cc_7.png"],["8 de carreaux","cc_8.png"],["9 de carreaux","cc_9.png"],["10 de carreaux","cc_10.png"],["valet de carreaux","cc_j.png"],["dame de carreaux","cc_q.png"],["roi de carreaux","cc_k.png"],
                    ["as de pique","p_as.png"],["2 de pique","p_2.png"],["3 de pique","p_3.png"],["4 de pique","p_4.png"],["5 de pique","p_5.png"],["6 de pique","p_6.png"],["7 de pique","p_7.png"],["8 de pique","p_8.png"],["9 de pique","p_9.png"],["10 de pique","p_10.png"],["valet de pique","p_j.png"],["dame de pique","p_q.png"],["roi de pique","p_k.png"],
                    ["as de trèfle","t_as.png"],["2 de trèfle","t_2.png"],["3 de trèfle","t_3.png"],["4 de trèfle","t_4.png"],["5 de trèfle","t_5.png"],["6 de trèfle","t_6.png"],["7 de trèfle","t_7.png"],["8 de trèfle","t_8.png"],["9 de trèfle","t_9.png"],["10 de trèfle","t_10.png"],["valet de trèfle","t_j.png"],["dame de trèfle","t_q.png"],["roi de trèfle","t_k.png"],
        ]
        #self.cartes_tarot=tarot_sign
        self.load_params()
        self.bot_reponses=lib.load_reponses()
        voice=None
        self.playlists_guilds={}
    
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
    
    def channel_is_immunisee(self,msg):
        return msg.channel.id in self.channels_immunisees
    
    def save_params(self):
        txt=""
        #channels d'affichage de logs
        for c in self.channels_logs:
            txt+=str(c)+self.cacc
        #channels immunisées a la censure
        for c in self.channels_immunisees:
            txt+=str(c)+self.cacc
        #
        f=io.open(self.file_save,"w",encoding="utf-8")
        f.write(txt)
        f.close()
    
    def load_params(self):
        f=io.open(self.file_save,"r",encoding="utf-8")
        data=f.read().split(self.cac)
        f.close()
        #channels d'affichage de logs
        if len(data)>0:
            self.channels_logs=list(set([int(c) for c in data[0].split(self.cacc) if len(c)>1]))
        #channels immunisées
        if len(data)>1:
            self.channels_immunisees=list(set([int(c) for c in data[1].split(self.cacc) if len(c)>1]))
        #
    
    async def censure(self,msg,imun):
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
    
    async def sens_image(self,channel,url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return await channel.send('Could not download file...')
                data = io.BytesIO(await resp.read())
                await channel.send(file=discord.File(data, 'cool_image.png'))
    
    ######################################### JOIN #########################################
    async def join(self,msg):
        channel=msg.author.voice.channel
        voice = get(self.voice_clients, guild=msg.guild)
        
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
        """
        #a cause d'un bug :
        await voice.disconnect()
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
            if debug: print(f"The bot is connected to {channel}\n")
        """
        await msg.channel.send(f"The bot is connected to {channel}\n")
    
    ######################################### LEAVE #########################################
    async def leave(self,msg):
        channel=msg.author.voice.channel
        voice = get(self.voice_clients, guild=msg.guild)
        if voice and voice.is_connected():
            voice.stop()
            await voice.disconnect()
            if debug: print(f"The bot has left {channel}\n")
            await msg.channel.send(f"The bot has left {channel}\n")
        else:
            if debug: print(f"Bot was not in {channel}\n")
            await msg.channel.send(f"Bot was not in {channel}\n")
    ########################################### del #################################################
    async def after_playing_song(self,msg,fich):
        voice = get(self.voice_clients, guild=msg.guild)
        voice.stop()
        if len(os.listdir("songs/"))>1: os.remove(fich)
        del(self.playlists_guilds[msg.guild][0])
        if len(self.playlists_guilds[msg.guild])>0:
            await self.play_current(msg,aff=False,fich=self.playlists_guilds[msg.guild][0])
    ######################################### play current #########################################
    async def play_current(self,msg,aff=True,fich="songs/"+random.choice(os.listdir("songs/"))):
        voice = get(self.voice_clients, guild=msg.guild)
        if not voice.is_playing:
            song_there=os.path.isfile(fich)
            if voice and voice.is_connected():
                if song_there:
                    if debug: print("Playing ",nname)
                    if name=="song.mp3": await msg.channel.send("Playing last song downloaded")
                    else: await msg.channel.send(f"Playing {nname}")
                    dismus=discord.FFmpegPCMAudio(source="song.mp3")
                    if msg.guild in self.playlists_guilds.keys():  self.playlists_guilds[msg.guild].append(fich)
                    else:    self.playlists_guilds[msg.guild]=[fich]
                    voice.play( dismus , after=lambda msg,fich:self.after_playing_song )
                    voice.source=discord.PCMVolumeTransformer(voice.source)
                    voice.source.volume=0.27
                else:
                    if aff: await msg.channel.send("There are not song currently downloaded :(")
            else:
                await msg.channel.send("I'm not connected !")
        else:
            await msg.channel.send("Already playing music, added song to playlist")
            if msg.guild in self.playlists_guilds.keys():    self.playlists_guilds[msg.guild].append(fich)
            else:         self.playlists_guilds[msg.guild]=[fich]
    ######################################### play url #########################################
    async def play_url(self,msg,url,quality="100",formate="bestaudio"):
        voice = get(self.voice_clients, guild=msg.guild)
        song_there=os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
                if debug: print("Removed song.mp3")
        except Exception as e:
            if debug: print("error while removing song.mp3 : ",e)
            await msg.channel.send("Error")
            return
        
        ydl_opts={
            "format":formate,
            "postprocessors":[{
                "key":"FFmpegExtractAudio",
                "preferredcodec":"mp3",
                "preferredquality":quality,
            }],
        }
        
        try:
            if voice and voice.is_connected():
                name="song.mp3"
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    await msg.channel.send("Downloading music...")
                    ydl.download([url])
                
                for fich in os.listdir("./"):
                    if fich.endswith(".mp3"):
                        name=fich
                        os.rename(name,"songs/"+name)
                nname="songs/"+name
                await self.play_current(msg,aff=False,fich=nname)
            else:
                await msg.channel.send("I'm not connected !")
        except Exception as e:
            await msg.channel.send("Error playing music : "+str(e))
            print("error ",e)
                
            
    async def stop_playing(self,msg):
        voice = get(self.voice_clients, guild=msg.guild)
        voice.stop()
        voice.is_playing=False
        await msg.channel.send("Music has been stoped")
        self.playlists_guilds[msg.guild]=[]
    
    async def pause_playing(self,msg):
        voice = get(self.voice_clients, guild=msg.guild)
        if not voice.is_paused():
            voice.pause()
            await msg.channel.send("Music has been paused")
        else:
            await msg.channel.send("Music is already paused")
    
    async def resume_playing(self,msg):
        voice = get(self.voice_clients, guild=msg.guild)
        if voice.is_paused():
            voice.resume()
            await msg.channel.send("Music has been resumed")
        else:
            await msg.channel.send("Music is already playing")
            
    async def skip_playing(self,msg):
        voice=get(self.voice_clients, guild=msg.guild)
        if len(self.playlists_guilds[msg.guild])>0:
            fich=self.playlists_guilds[msg.guild][0]
            self.after_playing_song(msg,fich)
    
    def show_playlist(self,msg):
        await msg.channel.send("Votre playlist : "+",".join(self.playlists_guilds[msg.guild]))
    
    ######################################### ON READY #########################################
    async def on_ready(self):
        actt=["Vous répondre"]
        await self.change_presence(activity=discord.Game(name=actt[0]))
        #await self.change_presence(activity=discord.CustomActivity(name=actt[0]))
        print("Logged in as ")
        print(self.user.name)
        print(self.user.id)
        print("---------")
        for ic in self.channels_logs:
            gen=self.get_channel(ic) #get le general du server de test
            if gen!=None:
                await gen.send("Ouaah, le bot nathbot est levé, il est pret a vous écouter !")
    
    async def on_new_user_in_server(self,p):
        for ic in [693029376341573722]:
            gen=self.get_channel(ic) #get le general du server de test
            await gen.send(embed=create_embed(self,titre=random.choice(lib.phrases_arrivees),description=p.name+" est arrivé sur ce serveur !",color=discord.Colour(int("0x000000",16)),img=p.avatar_url))
    
    async def on_message_edit(self,amsg,msg):
        #print("\n\n author : ",msg.author," content : ",msg.content)
        author=msg.author
        content=msg.content
        ############# test imunisation au bot ##############
        imun=self.channel_is_immunisee(msg)
        try:
            for r in msg.author.roles:
                if r.name in ["immunisé a nathbot"]: imun=True
        except:
            imun=True
        
        isbot=False
        try:
            if(msg.author == self.user):
                isbot=True
                
            if(not imun):
                await self.censure(msg,imun)

        except Exception as e:
            await msg.channel.send("Error : "+str(e))                
            print(e)
    
    async def on_message(self,msg):
        #print("\n\n author : ",msg.author," content : ",msg.content)
        author=msg.author
        content=msg.content
        ############# test imunisation au bot ##############
        imun=self.channel_is_immunisee(msg)
        try:
            for r in msg.author.roles:
                if r.name in ["immunisé a nathbot"]: imun=True
        except:
            imun=True
        
        isbot=False
        if True:
        #try:
            if(msg.author == self.user):
                isbot=True
            ############################################### PETITES FUTILITES #####################################
            
            if not imun and not isbot:
                ############################################### PING ###############################################
                for r in self.bot_reponses:
                    if(content.lower().startswith(r[0])) and r[2]!="b":
                        rr=str("<@!"+str(msg.author.id)+">").join(r[1].split("@nom"))
                        await msg.channel.send(rr) 

                """
                elif(content.lower().startswith("bonjour")): await msg.channel.send("Bonjour <@!"+str(msg.author.id)+"> !")
                elif(content.lower().startswith("salut")): await msg.channel.send("Salut <@!"+str(msg.author.id)+"> !")
                elif(content.lower().startswith("aurevoir")): await msg.channel.send("Aurevoir <@!"+str(msg.author.id)+"> !")
                elif(content.lower().startswith("au revoir")): await msg.channel.send("Au revoir <@!"+str(msg.author.id)+"> !")
                elif(content.lower().startswith("yo")): await msg.channel.send("Yo <@!"+str(msg.author.id)+"> !")
                elif(content.lower().startswith("hello")): await msg.channel.send("Hello <@!"+str(msg.author.id)+"> !")
                elif(content.lower().startswith("hi")): await msg.channel.send("Hi <@!"+str(msg.author.id)+"> !")
                elif(content.lower().startswith("oui")): await msg.channel.send("non !")
                elif(content.lower().startswith("non")): await msg.channel.send("oui !")
                elif(content.lower().startswith("si")): await msg.channel.send("nan !")
                elif(content.lower().startswith("nan")): await msg.channel.send("si !")
                elif(content.lower().startswith("ah")): await msg.channel.send("B")
                elif(content.lower().startswith("hein")): await msg.channel.send("deux")
                elif(content.lower().startswith("ok")): await msg.channel.send("google !")
                elif(content.lower().startswith("salam")): await msg.channel.send("Hummm, COUSCOUS MIAM MIAM !")
                elif(content.lower().startswith("xd")): await msg.channel.send("AHHHH, c'est drole, HEEEEEEEEIIIIINNNNNN ??????")
                """
                
            
            ############################################### GET HELP ##############################################
            
            #print(content)
            try:
                if not isbot and len(content.split("<@&"+str(self.user.id)+">"))>=2 or len(content.split("<@!"+str(self.user.id)+">"))>=2:
                    await msg.channel.send("Vous m'avez mentionné ?\nAussi, voici une commande qui peut vous aider ;) `"+config["prefix"]+"help`")
            except Exception as e:
                print(e)
            
            ##### PING ###
            if(content.lower().startswith("ping")): await msg.channel.send("pong")
            ############################################### MESSAGES PRIVES ###############################################
            if(content.startswith(config["prefix"]+"dm") and not isbot):
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
            elif(content.startswith(config["prefix"]+"+") and not isbot):
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
            elif(content.startswith(config["prefix"]+"*") and not isbot):
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
            elif(content.startswith(config["prefix"]+"blague") and not isbot): 
                await msg.channel.send( lib.blague() )
            
            ############################################### CITATION ###############################################                    
            elif(content.startswith(config["prefix"]+"citation") and not isbot): 
                await msg.channel.send( lib.citation(content[len(config["prefix"]+"citation"):]) )
            
            ############################################### BLAGUE ###############################################                    
            elif(content.startswith(config["prefix"]+"complimente moi") and not isbot): 
                nom="<@!"+str(msg.author.id)+">"
                await msg.channel.send( lib.compliment(nom) )
                
            ############################################### NB ALEATOIRE ###############################################                    
            elif(content.startswith(config["prefix"]+"nbalea") and not isbot):
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
            ############################################### carte ALEATOIRE ###############################################   
            elif(content.startswith(config["prefix"]+"tirer une carte") and not isbot):
                c=random.choice(self.data_cartes)
                await msg.channel.send(c[0],file=discord.File("./imgs/cartes/"+c[1]))
            ############################################### AIDE ###############################################                    
            elif(content.startswith(config["prefix"]+"embed")):
                author=msg.author
                image=author.avatar_url
                couleur=self.random_color()
                description=" ".join(content.split(" ")[1:])
                titre=author.name
                #print("titre : ",titre," description : ",description," couleur : ",couleur," image : ",image)
                embed=self.create_embed(titre=titre,description=description,color=couleur,img=image)
                await msg.channel.send(embed=embed)
                
            ############################################### INVITATIONS ###############################################                    
            elif(content.startswith(config["prefix"]+"invite") and not isbot): 
                invite = await msg.channel.create_invite(unique=False)
                await msg.channel.send(invite.url)
                
            ############################################### del INVITATIONS ###############################################                    
            elif(content.startswith(config["prefix"]+"delinvites") and not isbot): 
                invites = await msg.guild.invites()
                for i in invites:
                    await i.delete()
                await msg.channel.send("Toutes les invitations ont bien été supprimées")
                
            ############################################### COMPTER ###############################################                    
            elif(content.startswith(config["prefix"]+"compter") and not isbot):
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
            ############################################### calcul ###############################################                    
            elif(content.startswith(config["prefix"]+"calcul ") and not isbot):
                expr=content[len(config["prefix"]+"calcul "):]
                e=eval_expr.convert(expr)
                ne=eval_expr.traite1(e)
                res=eval_expr.f(ne,{})
                await msg.channel.send("Le résultat du calcul est : "+str(res))
            ############################################### more jokes ###############################################                    
            elif(content.startswith(config["prefix"]+"morejokes")):
                t,b,a=openjson.more_jokes()
                if a=="reddit":
                    cl=colors["orange"]
                else:
                    cl=self.random_color()
                description=b+"\n -from "+a
                titre=t
                embed=self.create_embed(titre=titre,description=description,color=cl)
                await msg.channel.send(embed=embed)
            ############################################### more jokes ###############################################                    
            elif(content.startswith(config["prefix"]+"trans")):
                arg1=""
                arg2=""
                source=""
                destination=""
                txtt=""
                
                i1=content.find("<")+1
                #print("i1 : ",i1)
                if i1!=-1:
                    i2=content.find(">",i1)
                    #print("i2 : ",i2)
                    if i2!=-1:
                        arg1=content[i1:i2]
                        txtt=content[i2+1:]
                        i3=content.find("<",i2)+1
                        #print("i3 : ",i3)
                        if i3!=-1:
                            i4=content.find(">",i3)
                            #print("i4 : ",i4)
                            if i4!=-1:
                                arg2=content[i3:i4]
                                txtt=content[i4+1:]
                if arg1!="" and arg2=="":
                    destination=arg1
                elif arg1!="" and arg2!="":
                    source=arg1
                    destination=arg2
                #print("arg1 : ",arg1)
                #print("arg2 : ",arg2)
                #print("source : ",source)
                #print("destination : ",destination)
                #print("txtt : ",txtt)
                if txtt!="" and destination!="" and source!="":
                    t=gtrans.translate(txtt,src=source,dest=destination)
                    await msg.channel.send("Traduction : "+t.text)
                elif txtt!="" and destination!="":
                    t=gtrans.translate(txtt,dest=destination)
                    await msg.channel.send("Traduction : "+t.text)
                else:
                    await msg.channel.send("Vous utilisez mal la commande !")
            ############################################### join ###############################################                    
            elif(content.startswith(config["prefix"]+"join") and not isbot):
                await self.join(msg)
            ############################################### join ###############################################                    
            elif(content.startswith(config["prefix"]+"leave") and not isbot):
                await self.leave(msg)
            ############################################### play url ###############################################                    
            elif(content.startswith(config["prefix"]+"play_url") and not isbot):
                url=msg.content[len(config["prefix"]+"play_url"):].strip()
                print(url)
                await self.play_url(msg,url)
            ############################################### play current ###############################################                    
            elif(content.startswith(config["prefix"]+"play_current") and not isbot):
                await self.play_current(msg)
            ############################################### stop ###############################################                    
            elif(content.startswith(config["prefix"]+"stop") and not isbot):
                await self.stop_playing(msg)
            ############################################### pause ###############################################                    
            elif(content.startswith(config["prefix"]+"pause") and not isbot):
                await self.pause_playing(msg)
            ############################################### resume ###############################################                    
            elif(content.startswith(config["prefix"]+"resume") and not isbot):
                await self.resume_playing(msg)
            ############################################### show playlist ###############################################                    
            elif(content.startswith(config["prefix"]+"show playlist") and not isbot):
                await self.show_playlist(msg)
            ############################################### IMMUNISE ###############################################                    
            elif(content.startswith(config["prefix"]+"immunise channel") and not isbot):
                if True:#msg.author.server_permissions.mannage_channels:
                    if not msg.channel.id in self.channels_immunisees:
                        self.channels_immunisees.append(msg.channel.id)
                        await msg.channel.send("Ce canal texte est maintenant immunisé à nathbot.")
                    else:
                        await msg.channel.send("Ce canal texte est déjà immunisé à nathbot !")
                else:
                    await msg.channel.send("Vous n'avez pas les permissions d'effectuer une telle tache, sous fifre !")
                self.save_params()
            ############################################### IMMUNISE ###############################################                    
            elif(content.startswith(config["prefix"]+"stop immunise channel")):
                if True:#msg.author.server_permissions.mannage_channels:
                    if not msg.channel.id in self.channels_immunisees:
                        await msg.channel.send("Ce canal texte n'est pas immunisé à nathbot !")
                    else:
                        del(self.channels_immunisees[self.channels_immunisees.index(msg.channel.id)])
                        await msg.channel.send("Ce canal texte n'est maintenant plus immunisé à nathbot.")
                else:
                    await msg.channel.send("Vous n'avez pas les permissions d'effectuer une telle tache, sous fifre !")
                self.save_params()
            ############################################### save ###############################################                    
            elif(content.startswith(config["prefix"]+"debuginfos")):
                if msg.author.name=="nath54":
                    await msg.channel.send("channels immunisees : "+str(self.channels_immunisees))
                    await msg.channel.send("channels logs : "+str(self.channels_logs))
            ############################################### save ###############################################                    
            elif(content.startswith(config["prefix"]+"save")):
                if msg.author.name=="nath54":
                    self.save_params()
                    await msg.channel.send("Les paramètres du bot ont été sauvegardés")
            ############################################### save ###############################################                    
            elif(content.startswith(config["prefix"]+"load")):
                if msg.author.name=="nath54":
                    self.load_params()
                    await msg.channel.send("Les paramètres du bot ont été chargés")
            ############################################### AIDE ###############################################                    
            elif(content.startswith(config["prefix"]+"load_datas")):
                if msg.author.name=="nath54":
                    lib.load_blagues()
                    lib.load_compliments()
                    lib.load_citations()
                    lib.load_censure()
                    self.bot_reponses=lib.load_reponses()
            ############################################### AIDE ###############################################                    
            elif(content.startswith(config["prefix"]+"help")):
                txt=lib.help(config["prefix"])
                await msg.channel.send(txt)
            ############################################### EXIT ###############################################
            elif(content.startswith(config["prefix"]+"exit")):
                if msg.author.name=="nath54":
                    for ic in self.channels_logs:
                        gen=self.get_channel(ic) #get le general du server de test
                        if gen!=None:
                            await gen.send("Catastrophe ! le bot nathbot va se rendormir, espérons qu'il va vite revenir parmis nous !")
                    
                    await self.logout()
                    await self.close()
                    #exit()
                else:
                    await msg.channel.send("Eh, vous ne pouvez pas éteindre le bot comme ca, y a que son créateur qui peut le faire !")
                    
                
            ############################################### CENSURE ###################################################
            if(not imun):
                await self.censure(msg,imun)

        #except Exception as e:
        else:
            await msg.channel.send("Error : "+str(e))                
            print(e)
            
                

print("Démarage du bot...")
#on lance le programme
if __name__== "__main__":
    bot = Bot()
    bot.run(config["token"])





