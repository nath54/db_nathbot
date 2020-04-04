#coding:utf-8

#print("Démarage...")

from commands2 import *

#print("Librairies chargées.")

#print("Chargement des infos du bot...")
#



#print("Infos du bot chargées.")

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
        load_params(self)
        self.bot_reponses=lib.load_reponses()
        voice=None
        self.playlists_guilds={}
        self.states_bot_music={}
    
    
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
        await message_on(self,msg)            

print("Démarage du bot...")
#on lance le programme
if __name__== "__main__":
    bot = Bot()
    bot.run(config["token"])





