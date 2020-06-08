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


async def join(bot,msg):
    channel=msg.author.voice.channel
    voice = get(bot.voice_clients, guild=msg.guild)
    
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


async def leave(bot,msg):
    channel=msg.author.voice.channel
    voice = get(bot.voice_clients, guild=msg.guild)
    if not msg.guild in bot.states_bot_music.keys() :
        bot.states_bot_music[msg.guild]="waiting for music"
    if voice and voice.is_connected():
        voice.stop()
        await voice.disconnect()
        if debug: print(f"The bot has left {channel}\n")
        await msg.channel.send(f"The bot has left {channel}\n")
    else:
        if debug: print(f"Bot was not in {channel}\n")
        await msg.channel.send(f"Bot was not in {channel}\n")


async def after_playing_song(bot,msg,fich):
    voice = get(bot.voice_clients, guild=msg.guild)
    if not msg.guild in bot.states_bot_music.keys() :
        bot.states_bot_music[msg.guild]="waiting for music"
    if voice==None:
        await msg.channel.send("Not connected...")
        return
    voice.stop()
    bot.states_bot_music[msg.guild]="stoped"
    if len(os.listdir("songs/"))>1: os.remove(fich)
    del(bot.playlists_guilds[msg.guild][0])
    if len(bot.playlists_guilds[msg.guild])>0:
        await play_current(bot,msg,aff=False,fich=bot.playlists_guilds[msg.guild][0])


async def play_current(bot,msg,aff=True,fich=None):
    if fich==None:
        if len(os.listdir("songs/")) > 1:
            fich="songs/"+random.choice(os.listdir("songs/"))
        else:
            await msg.channel.send("I don't find you songs to play :(")
            return 
        
    voice = get(bot.voice_clients, guild=msg.guild)
    if not msg.guild in bot.states_bot_music.keys() :
        bot.states_bot_music[msg.guild]="waiting for music"
    if voice==None:
        await msg.channel.send("Not connected...")
        return
    if not bot.states_bot_music[msg.guild] in ["playing","resumed"] or True:
        song_there=os.path.isfile(fich)
        if voice and voice.is_connected():
            if song_there:
                if debug: print("Playing ",fich)
                #if fich.ends=="song.mp3": await msg.channel.send("Playing last song downloaded")
                else: await msg.channel.send(f"Playing {fich}")
                if msg.guild in bot.playlists_guilds.keys():  bot.playlists_guilds[msg.guild].append(fich)
                else:    bot.playlists_guilds[msg.guild]=[fich]
                bot.states_bot_music[msg.guild]="playing"
                dismus=discord.FFmpegPCMAudio(source=fich)
                voice.play( dismus )
                voice.source=discord.PCMVolumeTransformer(voice.source)
                voice.source.volume=0.35
            else:
                if aff: await msg.channel.send("There are not song currently downloaded :(")
        else:
            await msg.channel.send("I'm not connected !")
    else:
        await msg.channel.send("Already playing music, added song to playlist")
        if msg.guild in bot.playlists_guilds.keys():    bot.playlists_guilds[msg.guild].append(fich)
        else:         bot.playlists_guilds[msg.guild]=[fich]

async def play_url(bot,msg,url,quality="100",formate="bestaudio"):
    voice = get(bot.voice_clients, guild=msg.guild)
    if not msg.guild in bot.states_bot_music.keys() :
        bot.states_bot_music[msg.guild]="waiting for music"
    if voice==None:
        await msg.channel.send("Not connected...")
        return
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
            await play_current(bot,msg,aff=False,fich=nname)
        else:
            await msg.channel.send("I'm not connected !")
    except Exception as e:
        await msg.channel.send("Error playing music : "+str(e))
        print("error ",e)
                
            
async def stop_playing(bot,msg):
    voice = get(bot.voice_clients, guild=msg.guild)
    if not msg.guild in bot.states_bot_music.keys() :
        bot.states_bot_music[msg.guild]="waiting for music"
    if voice==None:
        await msg.channel.send("Not connected...")
        return
    voice.stop()
    bot.states_bot_music[msg.guild]="stoped"
    await msg.channel.send("Music has been stoped")
    bot.playlists_guilds[msg.guild]=[]

async def pause_playing(bot,msg):
    voice = get(bot.voice_clients, guild=msg.guild)
    if not msg.guild in bot.states_bot_music.keys() :
        bot.states_bot_music[msg.guild]="waiting for music"
    if voice==None:
        await msg.channel.send("Not connected...")
        return
    if not voice.is_paused() or not bot.states_bot_music[msg.guild]=="paused":
        voice.pause()
        bot.states_bot_music[msg.guild]="paused"
        await msg.channel.send("Music has been paused")
    else:
        await msg.channel.send("Music is already paused")

async def resume_playing(bot,msg):
    voice = get(bot.voice_clients, guild=msg.guild)
    if not msg.guild in bot.states_bot_music.keys() :
        bot.states_bot_music[msg.guild]="waiting for music"
    if voice==None:
        await msg.channel.send("Not connected...")
        return
    if voice.is_paused() or bot.states_bot_music[msg.guilf]=="paused":
        voice.resume()
        bot.states_bot_music[msg.guild]="resumed"
        await msg.channel.send("Music has been resumed")
    else:
        await msg.channel.send("Music is already playing")
        
async def skip_playing(bot,msg):
    voice=get(bot.voice_clients, guild=msg.guild)
    if not msg.guild in bot.states_bot_music.keys() :
        bot.states_bot_music[msg.guild]="waiting for music"
    if voice==None:
        await msg.channel.send("Not connected...")
        return
    if len(bot.playlists_guilds[msg.guild])>0:
        fich=bot.playlists_guilds[msg.guild][0]
        after_playing_song(bot,msg,fich)

async def show_playlist(bot,msg):
    await msg.channel.send("Votre playlist : "+",".join(bot.playlists_guilds[msg.guild]))


