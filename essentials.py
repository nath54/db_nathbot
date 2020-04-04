#coding:utf-8
import io
import random
import discord

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
