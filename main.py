#coding:utf-8
import discord
import io
import lib

#on recup les infos
f=io.open("config.naths","r",encoding="utf-8")
data=f.read().strip().split("\n")
f.close()

config=dict([tuple(d.split(":")) for d in data])
print(config)

#class bot
class Bot(discord.Client):
    def __init__(self):
        super().__init__()
    
        
    async def on_ready(self):
        print("Logged in as ")
        print(self.user.name)
        print(self.user.id)
        print("---------")
        gen=self.get_channel(692779375367553127)
        await gen.send("Ouaah, le bot nathbot est levé, il est pret a vous écouter !")
        
    
    async def on_message(self,msg):
        author=msg.author
        content=msg.content
        if(msg.author == self.user):
            return
        elif(content.startswith(config["prefix"]+"ping")):
            await msg.channel.send("pong")
        elif(content.startswith(config["prefix"]+"exit")):
            #TODO
            #exit()
            pass
        elif(content.startswith(config["prefix"]+"dm")):
            cc=content.split(" ")
            if(len(cc)>=2):
                member=discord.utils.get(msg.guild.members, name=cc[1])
                if member!=None:
                    if(len(cc)>=3): txt=" ".join(cc[2:])
                    else: txt="Hello !"
                    await member.send(txt)
                else:
                    await msg.channel.send("il n'y a personne ayant le nom "+cc[1]+" ici !")
        elif(content.startswith(config["prefix"]+"+")):
            cc=content.split(" ")
            if(len(cc)>=2):
                a,b=None,None
                try:
                    a=int(cc[1])
                    b=int(cc[2])
                    await msg.channel.send(cc[1]+" + "cc[2]+" = "+str(a+b))
                except:
                    await msg.channel.send("Eh Oh ! je ne peux qu'additionner que des nombre !, essaie de faire de l'agebre avec des aptates et des bananes !")
        elif(content.startswith(config["prefix"]+"help")):
            txt=lib.help()
            await msg.send(txt)
            
                

#on lance le programme
if __name__== "__main__":
    bot = Bot()
    bot.run(config["token"])






