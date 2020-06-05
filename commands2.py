#coding:utf-8
import discord
import lib
import time
from commands import *
from commands_music import *
from googletrans import Translator
gtrans=Translator()

################################################################################ MSGS REPS ################################################################################
async def mess_reps(bot,msg,imun,isbot):
    content=msg.content 
    if not imun and not isbot:
        for r in bot.bot_reponses:
            if(content.lower().startswith(r[0])) and r[2]!="b":
                rr=str("<@!"+str(msg.author.id)+">").join(r[1].split("@nom"))
                await msg.channel.send(rr) 
################################################################################ TEST_HELP ################################################################################
async def test_help(bot,msg,imun,isbot):
    content=msg.content 
    try:
        if not isbot and len(content.split("<@&"+str(bot.user.id)+">"))>=2 or len(content.split("<@!"+str(bot.user.id)+">"))>=2:
            await msg.channel.send("Vous m'avez mentionné ?\nAussi, voici une commande qui peut vous aider ;) `"+config["prefix"]+"help`")
    except Exception as e:
        print(e)
################################################################################ PING ################################################################################
async def ping(bot,msg):
    content=msg.content 
    if(content.lower().startswith("ping")): await msg.channel.send("pong")
################################################################################ DM ################################################################################
async def dm(bot,msg):
    content=msg.content 
    cc=content.split(" ")
    if(len(cc)>=2): 
        if(len(cc)>=3): txt=" ".join(cc[2:])
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
                if member!=bot.user:
                    try:
                        await member.send(txt)
                        if debug: print("Envoyé a : "+member.name)
                    except discord.Forbidden:
                        await msg.channel.send("La personne ayant le nom "+cc[1]+" a bloqué ses messages privés !")
                    except:
                        await msg.channel.send("Il y a eu une erreur lors de l'envoi du message à "+member.name+" :( ")
################################################################################ NBALEA ################################################################################
async def nbalea(bot,msg):
    content=msg.content 
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
################################################################################ COMPTER ################################################################################
async def compter(bot,msg):
    content=msg.content 
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
################################################################################ TRANS ################################################################################
async def trans(bot,msg):
    content=msg.content 
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
    if txtt!="" and destination!="" and source!="":
        t=gtrans.translate(txtt,src=source,dest=destination)
        await msg.channel.send("Traduction : "+t.text)
    elif txtt!="" and destination!="":
        t=gtrans.translate(txtt,dest=destination)
        await msg.channel.send("Traduction : "+t.text)
    else:
        await msg.channel.send("Vous utilisez mal la commande !")
################################################################################ IMMUNISE CHANNEL ################################################################################
async def immunise_channel(bot,msg):
    if True:#msg.author.server_permissions.mannage_channels:
        if not msg.channel.id in bot.channels_immunisees:
            bot.channels_immunisees.append(msg.channel.id)
            await msg.channel.send("Ce canal texte est maintenant immunisé à nathbot.")
        else:
            await msg.channel.send("Ce canal texte est déjà immunisé à nathbot !")
    else:
        await msg.channel.send("Vous n'avez pas les permissions d'effectuer une telle tache, sous fifre !")
    save_params(bot)
################################################################################ STOP IMMUNISE CHANNEL ################################################################################
async def stop_immunise_channel(bot,msg):
    if True:#msg.author.server_permissions.mannage_channels:
        if not msg.channel.id in bot.channels_immunisees:
            await msg.channel.send("Ce canal texte n'est pas immunisé à nathbot !")
        else:
            del(bot.channels_immunisees[bot.channels_immunisees.index(msg.channel.id)])
            await msg.channel.send("Ce canal texte n'est maintenant plus immunisé à nathbot.")
    else:
        await msg.channel.send("Vous n'avez pas les permissions d'effectuer une telle tache, sous fifre !")
    save_params(bot)
################################################################################ MESSAGE_ON ################################################################################
async def message_on(bot,msg):
    author=msg.author
    content=msg.content 
    if True:
    #try:
        ############# test imunisation au bot ##############
        imun=channel_is_immunisee(bot,msg)
        try:
            for r in msg.author.roles:
                if r.name in ["immunisé a nathbot"]: imun=True
        except:
            imun=True
        ############# test est le bot ##############
        isbot=False
        if(msg.author == bot.user):  isbot=True
        ############# messages reponses auto ##############
        await mess_reps(bot,msg,imun,isbot)
        ############# test demande help ##############
        await test_help(bot,msg,imun,isbot)
        ############# ping ##############
        await ping(bot,msg)
        ############# messages privés ##############
        if(content.startswith(config["prefix"]+"dm") and not isbot):
            await dm(bot,msg)
        ############# blagues ##############
        elif(content.startswith(config["prefix"]+"blague") and not isbot):
            await msg.channel.send( lib.blague() )
        ############# citations ##############
        elif(content.startswith(config["prefix"]+"citation") and not isbot):
            await msg.channel.send( lib.citation(content[len(config["prefix"]+"citation"):]) )
        ############# compliments ##############
        elif(content.startswith(config["prefix"]+"complimente moi") and not isbot): 
            nom="<@!"+str(msg.author.id)+">"
            await msg.channel.send( lib.compliment(nom) )
        ############# nombres aléatoires ##############
        elif(content.startswith(config["prefix"]+"nbalea") and not isbot):
            await nbalea(bot,msg)
        ############# tirer une carte ##############
        elif(content.startswith(config["prefix"]+"tirer une carte") and not isbot):
            c=random.choice(bot.data_cartes)
            await msg.channel.send(c[0],file=discord.File("./imgs/cartes/"+c[1]))
        ############# creer embed ##############
        elif(content.startswith(config["prefix"]+"embed")):
            embed=create_embed(bot,titre=msg.author.name,description=" ".join(content.split(" ")[1:]),color=random_color(),img=author.avatar_url)
            await msg.channel.send(embed=embed)
         ############# creer invitation ##############
        elif(content.startswith(config["prefix"]+"invite") and not isbot): 
            invite = await msg.channel.create_invite(unique=False)
            await msg.channel.send(invite.url)
        ############# supprimer toutes les invitations ##############
        elif(content.startswith(config["prefix"]+"delinvites") and not isbot): 
            invites = await msg.guild.invites()
            for i in invites: await i.delete()
            await msg.channel.send("Toutes les invitations ont bien été supprimées")
        ############# compter ##############
        elif(content.startswith(config["prefix"]+"compter") and not isbot):
            await compter(bot,msg)
        ############# calcul ##############
        elif(content.startswith(config["prefix"]+"calcul ") and not isbot):
            res=eval_expr.f(eval_expr.traite1(eval_expr.convert(content[len(config["prefix"]+"calcul "):])),{})
            await msg.channel.send("Le résultat du calcul est : "+str(res))
        ############# plus de blagues (anglais) ##############
        elif(content.startswith(config["prefix"]+"morejokes")):
            t,b,a=openjson.more_jokes()
            if a=="reddit":  cl=colors["orange"]
            else:  cl=bot.random_color()
            embed=create_embed(bot, titre=t , description=b+"\n -from "+a , color=cl)
            await msg.channel.send(embed=embed)
        elif(content.startswith(config["prefix"]+"trans")):
            await trans(bot,msg)
        ############# MUSIC : join vocal channel ##############             
        elif(content.startswith(config["prefix"]+"join") and not isbot):
            await join(bot,msg)
        ############# MUSIC : leave vocal channel ##############
        elif(content.startswith(config["prefix"]+"leave") and not isbot):
            await leave(bot,msg)
        ############# MUSIC : play url youtube ##############
        elif(content.startswith(config["prefix"]+"play_url") and not isbot):
            url=msg.content[len(config["prefix"]+"play_url"):].strip()
            await play_url(bot,msg,url)
        ############# MUSIC : play current ##############
        elif(content.startswith(config["prefix"]+"play_current") and not isbot):
            await play_current(bot,msg)
        ############# MUSIC : stop playing music ##############
        elif(content.startswith(config["prefix"]+"stop music") and not isbot):
            await stop_playing(bot,msg)
        ############# MUSIC : pause music ##############
        elif(content.startswith(config["prefix"]+"pause") and not isbot):
            await pause_playing(bot,msg)
        ############# MUSIC : resume music ##############
        elif(content.startswith(config["prefix"]+"resume") and not isbot):
            await resume_playing(bot,msg)
        ############# MUSIC : show playlist ##############
        elif(content.startswith(config["prefix"]+"show playlist") and not isbot):
            await show_playlist(bot,msg)
        ############# IMMUNISE #############                    
        elif(content.startswith(config["prefix"]+"immunise channel") and not isbot):
            await immunise_channel(bot,msg)
        ############# STOP IMMUNISE #############                    
        elif(content.startswith(config["prefix"]+"stop immunise channel")):
            await stop_immunise_channel(bot,msg)
        ############# debug infos #############                    
        elif(content.startswith(config["prefix"]+"debuginfos")):
            if msg.author.name=="nath54":
                await msg.channel.send("channels immunisees : "+str(bot.channels_immunisees))
                await msg.channel.send("channels logs : "+str(bot.channels_logs))
        ############# save #############                    
        elif(content.startswith(config["prefix"]+"save")):
            if msg.author.name=="nath54":
                save_params(bot)
                await msg.channel.send("Les paramètres du bot ont été sauvegardés")
        ############# load #############                    
        elif(content.startswith(config["prefix"]+"load")):
            if msg.author.name=="nath54":
                load_params(bot)
                await msg.channel.send("Les paramètres du bot ont été chargés")
        ############# LOAD DATAS #############                    
        elif(content.startswith(config["prefix"]+"load_datas")):
            if msg.author.name=="nath54":
                lib.load_blagues()
                lib.load_compliments()
                lib.load_citations()
                lib.load_censure()
                bot.bot_reponses=lib.load_reponses()
        ############# AIDE #############                    
        elif(content.startswith(config["prefix"]+"help")):
            txt=lib.help(config["prefix"])
            print(len(txt))
            await msg.channel.send(txt)
        ############# EXIT #############
        elif(content.startswith(config["prefix"]+"exit")):
            if msg.author.name=="nath54":
                for ic in bot.channels_logs:
                    gen=bot.get_channel(ic) #get le general du server de test
                    if gen!=None:
                        await gen.send("Catastrophe ! le bot nathbot va se rendormir, espérons qu'il va vite revenir parmis nous !")
                
                await bot.logout()
                await bot.close()
                #exit()
            else:
                await msg.channel.send("Eh, vous ne pouvez pas éteindre le bot comme ca, y a que son créateur qui peut le faire !")
        ############# CENSURE #############
        if(not imun):
            await censure(bot,msg,imun)
    #except Exception as e:
    else:
        await msg.channel.send("Error : "+str(e))                
        print(e)








