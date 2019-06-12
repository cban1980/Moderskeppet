#!/usr/bin/env python3
import feedparser 
from bs4 import BeautifulSoup as bs
import re
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot
import discord
import os
import sys
import requests
import json
import wikipedia
from urllib.request import urlopen
import random
import praw
bot = commands.Bot(command_prefix='!')
HOMEDIR = os.path.expanduser('~')
TOKENHOME = "%s/.Moderskeppet/" % (HOMEDIR)

with open(TOKENHOME + "token.txt", "r") as readfile:
    TOKEN = readfile.read().strip()


def cssformat(input):
    return "```css\n" + input + "```"


def htmlformat(input):
    return "```html\n" + input + "```"


@bot.event
async def on_message(message):
    if message.content.lower().startswith('!hjalp'):
        commands={}
        commands['!reddit']='!reddit <nummer> <subreddit> <sökterm>. Hämtar definerat antal matchningar från definerad subreddit.abs'
        commands['!tobbe']='Postar Tobbes veckomeny full med Aioli.'
        commands['!!pproxy']='Random proxy för TPB'
        commands['!eqauc']='!eqauc <nummer> <söktermer>. Sökfunktion för ahungry.com/eqauctions'
        commands['!polis']="!polis <stad>. Hämtar hem registrerade händelser för polisen från det senaste dygnet i <stad>"
        commands['!varn']='Aktuella SMHI varningar.'
        commands['!namnsdag']='Dagens namn.'
        commands['!blocket']='!blocket <område> <nummer> <söktermer>. Sökfunktion för blocket annonser.'
        commands['!bolaget']='!bolaget <nummer> <namn>. Sökfunktion för drycker på systembolaget.'
        commands['!wiki']='!wiki <sökterm>. Sökfunktion för den svenska wikipedian.'
        commands['!spel']='!spel <spel>. Byter Bengts Now Playing.'
        commands['!svt']='Now playing på Svt1.'
        commands['!nt']='!nt <nummer>. Visar nya <nummer> nyheter från NT.se.'
        commands['!mat']='Dagens meny på SMHIs stormkök.' 
        commands['!serverinvite']='Autogenererad invitelänk till Ninjaz servern, skickas i PM.' 
        commands['!namn']='Byter namn på Bengt.'
        commands['!why']='Randomiserad BOFH reason.'
        msg=discord.Embed(title='𝐃𝐢𝐬𝐜𝐨𝐫𝐝𝐛𝐨𝐭𝐞𝐧 𝐁𝐞𝐧𝐠𝐭', color=0x008000)
        for command,description in commands.items():
            msg.add_field(name=command,value=description, inline=False)
        await bot.send_message(message.channel, embed=msg)


@bot.command(name='reddit', pass_context=True)
async def reddit(ctx,arg, arg1, arg2):
    nummer = int(arg)
    subred = arg1
    patter = str(arg2)
    rewdit = praw.Reddit('Bengt', user_agent='Discordboten Bengt')
    for submission in rewdit.subreddit(subred).search("title:" + patter, limit=nummer):
        a = submission.title
        b = submission.url
        c = " ".join([a, b])
        await bot.say(c)

@bot.command(name='why', pass_context=True)
async def why(ctx):
    url_data = requests.get('http://pages.cs.wisc.edu/~ballard/bofh/excuses').text
    soup = bs(url_data, 'html.parser')
    for line in soup:
        soppa = line.splitlines()
    await bot.say(random.choice(soppa))

@bot.command(name='tobbe', pass_context=True)
async def tobbe(ctx):
    url_data = requests.get('http://www.oscarshall.se/empty_8.html').text
    soup = bs(url_data, 'html.parser')
    maten = soup.find("div", class_ = "ParagraphContainer")
    maten = maten.getText().rstrip().lstrip()
    maten = re.sub("(?s)99(.*$)", " ", maten)
    await bot.say(htmlformat(maten))


@bot.command(name='pproxy', pass_context=True)
async def pproxy(ctx):
    url_data = requests.get('https://proxybay.ist/').text
    soup = bs(url_data, 'html.parser')
    sites = []
    for tag in soup.findAll( class_ = "t1", href=True ):
        sites += tag['href'].splitlines()
    await bot.say(random.choice(sites))


@bot.command(name='eqauc', pass_context=True)
async def eqauc(ctx, arg1, *, arg2):
    argu = re.sub(' ', '+', arg2)
    adressen = 'http://ahungry.com/action/eq/item-detail/%s' % (argu)
    url_output = requests.get(adressen).text
    soup = bs(url_output, 'html5lib')
    auctions = soup.find_all(class_="item-detail-auctions")
    g = ""
    for i in auctions[0:int(arg1)]:
        g += i.getText().rstrip()
    g = re.sub('auctions,', '', g)
    await bot.say(ctx.message.author.mention + " -> 🇷<200b>🇪<200b>🇸<200b>🇺<200b>🇱<200b>🇹<200b>🇸<200b>" "```css\n" + g + "```")


@bot.command(name='namnsdag', pass_context=True)
async def namnsdag():
    namn = requests.get("https://www.dagensnamn.nu").text
    soup = bs(namn, 'html.parser')
    dagens = soup.find('h1').getText()
    await bot.say(dagens)


@bot.command(name='polis', pass_context=True)
async def polis(ctx, *, arg): 
    url_data = 'https://polisen.se/api/events?locationname=%s' % (arg)
    data = requests.get(url_data).json()
    for i in data:
        name = i['name']
        sum = i['summary']
        await bot.say("%s %s" % (name, sum))


@bot.command(name='varn', pass_context=True)
async def varn(ctx):
    adress = 'https://opendata-download-warnings.smhi.se/api/version/2/messages.json'
    output = requests.get(adress).json()
    output = json.dumps(output)
    await bot.say(htmlformat(output['message']['text']))


@bot.command(name='blocket', pass_context=True)
async def blocket(ctx, arg, arg1, *,  arg2):
    arg2 = re.sub(' ', '+', arg2) 
    adressen = 'https://blocket.nyh.name/%s?q=%s' % (arg, arg2)
    d = feedparser.parse(adressen)
    for post in d.entries[0:int(arg1)]:
      await  bot.say(post.title + ": " + post.link + "") 


@bot.command(name='bolaget', pass_context=True)
async def bolaget(ctx, arg1, *, arg2):
    adressen = 'https://bolaget.io/v1/products?search=%s&limit=%s' % (arg2, arg1)
    adressen = adressen.replace('"', '')
    input = requests.get(adressen).json()
    for i in input:
        alc = i['alcohol']
        namn = i['name']
        addnamn = i['additional_name']
        pris = i['price']['amount']
        await bot.say(cssformat(( "%s - %s - %s - %s SEK" % ( namn, addnamn, alc, pris))))


@bot.command(name='wiki', pass_context=True)
async def wiki(ctx, *, arg):
    wikipedia.set_lang("sv")
    w = wikipedia.summary(arg)
    await bot.say(w)


@bot.command(name='spel', pass_context=True)
async def spel(context, *, arg):
    playing = arg
    await  bot.change_presence(game=discord.Game(name=arg))


@bot.command(name='nt', pass_context=True)
async def nt(context, arg):
    d = feedparser.parse('https://www.nt.se/nyheter/norrkoping/rss/')
    for post in d.entries[0:int(arg)]:
        await bot.say(post.title + ": " + post.link + "")


@bot.command(name='svt1', pass_context=True)
async def svt1(context):
    svt1 = urlopen("https://www.svtplay.se/kanaler").read().decode("utf-8")
    soup = bs(svt1, 'html.parser')
    meny = soup.find(class_="play_guide-page-program-list-schedule__link").getText()
    time = soup.find(class_="play_guide-page-program-list-schedule__time").getText()
    meny = meny[5:]
    await bot.say("%s %s" % (time, meny))


@bot.command(name='mat', pass_context=True)
async def mat(context):
    storm = urlopen("http://www.stormkoket.se").read().decode("utf-8")
    soup = bs(storm, 'html.parser')
    meny1 = soup.find(class_="panel-pane pane-todays-menu").getText()
    meny2 = re.sub('Visa menyn för denna vecka', '', meny1)
    await bot.say( htmlformat(meny2))


@bot.command(name='serverinvite', pass_context=True)
async def inv(context):
    invite = await bot.create_invite(context.message.server, max_uses=1, xkcd=True)
    await bot.send_message(context.message.author, "Inbjudningsurlen är {}".format(invite.url))
    await bot.say("Inbjudningslänk genererad! kolla i pm! ")


@bot.command(pass_context=True)
async def rename(ctx, *, name):
    await bot.edit_profile(username=name)


@bot.event
async def on_ready():
    print('Inloggad som: ' + bot.user.name)
    url_data = requests.get('http://www.fortunecookiemessage.com/').text
    soup = bs(url_data, 'html.parser')
    cookie = soup.find(class_="cookie-link").getText()
    await bot.change_presence(game=discord.Game(name=cookie))


bot.run(TOKEN)
