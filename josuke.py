import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import sys, os, psutil
from gtts import gTTS
from discord import FFmpegPCMAudio
from discord.utils import get

CLIENT = discord.Client()
client = commands.Bot(command_prefix='+')
blackList = []
langList = """Language List:
      af: Afrikaans
      ar: Arabic
      bn: Bengali
      bs: Bosnian
      ca: Catalan
      cs: Czech
      cy: Welsh
      da: Danish
      de: German
      el: Greek
      en-au: English (Australia)
      en-ca: English (Canada)
      en-gb: English (UK)
      en-gh: English (Ghana)
      en-ie: English (Ireland)
      en-in: English (India)
      en-ng: English (Nigeria)
      en-nz: English (New Zealand)
      en-ph: English (Philippines)
      en-tz: English (Tanzania)
      en-uk: English (UK)
      en-us: English (US)
      en-za: English (South Africa)
      en: English
      eo: Esperanto
      es-es: Spanish (Spain)
      es-us: Spanish (United States)
      es: Spanish
      et: Estonian
      fi: Finnish
      fr-ca: French (Canada)
      fr-fr: French (France)
      fr: French
      gu: Gujarati
      hi: Hindi
      hr: Croatian
      hu: Hungarian
      hy: Armenian
      id: Indonesian
      is: Icelandic
      it: Italian
      ja: Japanese
      jw: Javanese
      km: Khmer
      kn: Kannada
      ko: Korean
      la: Latin
      lv: Latvian
      mk: Macedonian
      ml: Malayalam
      mr: Marathi
      my: Myanmar (Burmese)
      ne: Nepali
      nl: Dutch
      no: Norwegian
      pl: Polish
      pt-br: Portuguese (Brazil)
      pt-pt: Portuguese (Portugal)
      pt: Portuguese
      ro: Romanian
      ru: Russian
      si: Sinhala
      sk: Slovak
      sq: Albanian
      sr: Serbian
      su: Sundanese
      sv: Swedish
      sw: Swahili
      ta: Tamil
      te: Telugu
      th: Thai
      tl: Filipino
      tr: Turkish
      uk: Ukrainian
      ur: Urdu
      vi: Vietnamese
      zh-cn: Chinese (Mandarin/China)
      zh-tw: Chinese (Mandarin/Taiwan)"""
langCodes = """ af
      ar
      bn
      bs
      ca
      cs
      cy
      da
      de
      el
      en-au
      en-ca
      en-gb
      en-gh
      en-ie
      en-in
      en-ng
      en-nz
      en-ph
      en-tz
      en-uk
      en-us
      en-za
      en
      eo
      es-es
      es-us
      es
      et
      fi
      fr-ca
      fr-fr
      fr
      gu
      hi
      hr
      hu
      hy
      id
      is
      it
      ja
      jw
      km
      kn
      ko
      la
      lv
      mk
      ml
      mr
      my
      ne
      nl
      no
      pl
      pt-br
      pt-pt
      pt
      ro
      ru
      si
      sk
      sq
      sr
      su
      sv
      sw
      ta
      te
      th
      tl
      tr
      uk
      ur
      vi
      zh-cn
      zh-tw"""

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    
@client.command(pass_context=True)
async def languageDict(ctx):
    await ctx.send(langList)
    
@client.command(pass_context=True)
async def hello(ctx):
    await ctx.send("Hey " + ctx.message.author.name + "!")
    
@client.command(pass_context=True)
async def summon(ctx):
    x = ctx.message.author.name
    await ctx.send("What do you need " + x + "?")
    
@client.command(pass_context=True)
async def repetez(ctx):
    message = ctx.message.content
    await ctx.send(message[8:])

@client.command(pass_context=True)
async def blacklist(ctx, member:discord.User):
    userID = (discord.utils.get(client.get_all_members(), name=ctx.message.author.name, discriminator= ctx.message.author.discriminator).id)
    if userID == 195350037142700032:
        try:
            blackList.index(member.name)
            await ctx.send(member.name + " is already on the blacklist.")
        except:
            blackList.append(member.name)
            await ctx.send(member.name + " has been blacklisted")
    else:
        await ctx.send("You do not have permission to edit the blacklist.")
        return
    
@client.command(pass_context=True)
async def unblacklist(ctx, member:discord.User):
    userID = (discord.utils.get(client.get_all_members(), name=ctx.message.author.name, discriminator= ctx.message.author.discriminator).id)
    if userID == 195350037142700032:
        try:
            blackList.remove(member.name)
            await ctx.send(member.name + " has been removed from the blacklist")
        except:
            await ctx.send(member.name + " is not on the blacklist.")
    else:
        await ctx.send("You do not have permission to edit the blacklist.")
        return
    
@client.command(pass_context=True)
async def viewBlacklist(ctx):
    blist = ""
    await ctx.send("Blacklist: ")
    for x in blackList:
         blist += x + "\n" 
    await ctx.send(blist)
    
@client.command(pass_context=True)
async def die(ctx):
    await ctx.send("Goodbye cruel world...")
    for process in (process for process in psutil.process_iter() if process.name()=="pythonw.exe"):
        process.kill()

@client.command(pass_context=True)
async def speak(ctx):
    unrefined = ctx.message.content
    startIndex = 10
    language = ctx.message.content[7:9]
    if ctx.message.content[9] == "-":
        startIndex = 13
        language = ctx.message.content[7:12]
    print("Language: " + language)
    refined = unrefined[startIndex:]
    print("Message: " + refined)
    try:
        rec = gTTS(text= refined, lang=language, slow=False)
        rec.save("discord.mp3")
        await ctx.send("Successfully converted!")
        if ctx.message.author.voice is None:
            await ctx.send("You are not connected to a voice channel!")
            return
        voice = get(client.voice_clients, guild=ctx.guild)
        channel = ctx.message.author.voice.channel
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
        source = FFmpegPCMAudio('discord.mp3')
        player = voice.play(source)
    except:
        await ctx.send("Oops! The language you have chosen doesn't exist or was spelled incorrectly. Use +languageDict to view the list of languages supported by this bot. :)")
        return

@client.command(pass_context=True)
async def leave(ctx):
    try:
        server = ctx.message.guild.voice_client
        await server.disconnect()
    except:
        await ctx.send("I'm currently not in any voice channel. Call me into one!")

@client.command(pass_context=True)
async def kick(ctx, userName: discord.User):
    if ctx.message.author.top_role.name is "admin":
        try:
            await ctx.kick(userName)
            await ctx.send("DORADORADORADORADORA:fist:")
        except:
            await ctx.send("Your stand lacks the required power:laughing::laughing::laughing:")
        
#UNDER CONSTRUCTION#
@client.command(pass_context=True)
async def lyrics(ctx):
    id = ctx.message.id
    try:
        url = 'https://www.google.com/search?ei=fvXlXOC8LM_UsAXtvJK4BQ&q=' + songs[id][0] + ' lyrics'
        r = requests.get(url)
        text = r.text
        start = '>Lyrics</span></span></div><div class="NJM3tb"></div><div><div><div><div class="xpc"><div class="jfp3ef"><div><div><span class="hwx"><div class="BNeawe tAd8D AP7Wnd">'
        end = '</div></span></div><div><span class="hwx"></span><span class="hwc">'
        lyric = text[text.find(start)+len(start):text.find(end)]
        
        if ("meta" in lyric):
            
            url = 'https://www.google.com/search?ei=fvXlXOC8LM_UsAXtvJK4BQ&q=' + songs[id][0]
            r = requests.get(url)
            text = r.text
            start = '>Lyrics</span></span></div><div class="NJM3tb"></div><div><div><div><div class="xpc"><div class="jfp3ef"><div><div><span class="hwx"><div class="BNeawe tAd8D AP7Wnd">'
            end = '</div></span></div><div><span class="hwx"></span><span class="hwc">'
            lyric = text[text.find(start)+len(start):text.find(end)]

            if ("meta" in lyric):
                x = 5/0
        
        await client.say("__***Lyrics for " + songs[id][0] + ":***__")
        while (len(lyric) > 2000):
            await client.say(lyric[0:1999])
            lyric = lyric[1999:]
        await client.say(lyric)
    except:
        
        try:
            if (songs[id][0] == ""):
                await client.say("Nothing is playing in the server")
            else:
                await client.say("Unable to find lyrics for " + songs[id][0] + "")
            
        except:
            await client.say("Nothing is playing in the server")
            
client.run('NjQ1MTUzNDI2MTkxMjg2MzE3.Xc-dnw.8GR5rdMOGisP5_Ufe9_uh4QMiQo')
