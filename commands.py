#coding:utf-8
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
from essentials import *



#########################

def random_color():
    hexas="0123456789abcdef"
    random_hex="0x"+"".join([random.choice(hexas) for x in range(6)])
    return discord.Colour(int(random_hex, 16))

def create_embed(bot,titre="titre",description="description",color=discord.Colour(int("0x000000",16)),img=""):
    embed=discord.Embed()
    embed.title=titre
    embed.description=description
    embed.colour=color
    if(img!=""):
       embed.set_image(url=img)
    return embed

def channel_is_immunisee(bot,msg):
    return msg.channel.id in bot.channels_immunisees

def save_params(bot):
    txt=""
    #channels d'affichage de logs
    for c in bot.channels_logs:
        txt+=str(c)+bot.cacc
    #channels immunisées a la censure
    for c in bot.channels_immunisees:
        txt+=str(c)+bot.cacc
    #
    f=io.open(bot.file_save,"w",encoding="utf-8")
    f.write(txt)
    f.close()


def load_params(bot):
    f=io.open(bot.file_save,"r",encoding="utf-8")
    data=f.read().split(bot.cac)
    f.close()
    #channels d'affichage de logs
    if len(data)>0:
        bot.channels_logs=list(set([int(c) for c in data[0].split(bot.cacc) if len(c)>1]))
    #channels immunisées
    if len(data)>1:
        bot.channels_immunisees=list(set([int(c) for c in data[1].split(bot.cacc) if len(c)>1]))
    #

async def censure(bot,msg,imun):
    return 0
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



async def sens_image(bot,channel,url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return await channel.send('Could not download file...')
            data = io.BytesIO(await resp.read())
            await channel.send(file=discord.File(data, 'cool_image.png'))



async def senddmmessage(msg,member,txt):
    try:
        await member.send(txt)
    except discord.Forbidden:
        await msg.channel.send("La personne ayant le nom "+cc[1]+" a bloqué ses messages privés !")
    except:
        await msg.channel.send("Il y a eu une erreur :( ")





































