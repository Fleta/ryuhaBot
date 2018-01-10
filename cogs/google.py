import aiohttp
import datetime
import discord
import json

from discord.ext import commands
from lxml import etree
from urllib.parse import parse_qs
from utils.support import edit, permEmbed

class Google:
    def __init__(self, bot):
        self.bot = bot

    def parseGoogleC(self, node):
        if node is None:
            return None

        e = discord.Embed(color=discord.Color.red())

        calculator = node.find(".//table/tr/td/span[@class='nobr']/h2[@class='r']")
        if calculator is not None:
            e.title = 'Calculator'
            e.description = ''.join(calculator.itertext())
            return e

        parent = node.getparent()

        unit = parent.find(".//ol//div[@class='_Tsb']")
        if unit is not None:
            e.title = 'Unit Conversion'
            e.description = ''.join(''.join(n.itertext()) for n in unit)
            return e

        currency = parent.find(".//ol/table[@class='std _tLi']/tr/td/h2")
        if currency is not None:
            e.title = 'Currency Conversion'
            e.description = ''.join(currency.itertext())
            return e

        release = parent.find(".//div[@id='_vBb']")
        if release is not None:
            try:
                e.description = ''.join(release[0].itertext()).strip()
                e.title = ''.join(release[1].itertext()).strip()
                return e
            except:
                return None

        words = parent.find(".//ol/div[@class='g']/div/h3[@class='r']/div")
        if words is not None:
            try:
                definition_info = words.getparent().getparent()[1]
            except:
                pass
            else:
                try:
                    e.title = words[0].text
                    e.description = words[1].text
                except:
                    return None
                for row in definition_info:
                    if len(row.attrib) != 0:
                        break
                    try:
                        data = row[0]
                        lexical_category = data[0].text
                        body = []
                        for index, definition in enumerate(data[1], 1):
                            body.append('%s. %s' % (index, definition.text))
                        e.add_field(name=lexical_category, value='\n'.join(body), inline=False)
                    except:
                        continue
                return e

        words = parent.find(".//ol/div[@class='g']/div/table/tr/td/h3[@class='r']")
        if words is not None:
            e.title = 'Google Translate'
            e.add_field(name='Input', value=words[0].text, inline=True)
            e.add_field(name='Out', value=words[1].text, inline=True)
            return e

        time_in = parent.find(".//ol//div[@class='_Tsb _HOb _Qeb']")
        if time_in is not None:
            try:
                time_place = ''.join(time_in.find("span[@class='_HOb _Qeb']").itertext()).strip()
                the_time = ''.join(time_in.find("div[@class='_rkc _Peb']").itertext()).strip()
                the_date = ''.join(time_in.find("div[@class='_HOb _Qeb']").itertext()).strip()
            except:
                return None
            else:
                e.title = time_place
                e.description = '%s\n%s' % (the_time, the_date)
                return e

        weather = parent.find(".//ol//div[@class='e']")
        if weather is None:
            return None

        location = weather.find('h3')
        if location is None:
            return None
        e.title = ''.join(location.itertext())

        table = weather.find('table')
        if table is None:
            return None

        try:
            tr = table[0]
            img = tr[0].find('img')
            category = img.get('alt')
            image = 'https:' + img.get('src')
            temperature = tr[1].xpath("./span[@class='wob_t']//text()")[0]
        except:
            return None
        else:
            e.set_thumbnail(url=image)
            e.description = '*%s*' % category
            e.add_field(name='Temperature', value=temperature)

        try:
            wind = ''.join(table[3].itertext()).replace('Wind: ', '')
        except:
            return None
        else:
            e.add_field(name='Wind', value=wind)

        try:
            humidity = ''.join(table[4][0].itertext()).replace('Humidity: ', '')
        except:
            return None
        else:
            e.add_field(name='Humidity', value=humidity)

        return e

    async def getGoogleEntry(self, query):
        params = {
            'q' : query,
            'h1' : 'en'
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64)'
        }
        entries = []
        card = None
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.google.com/search', params=params, headers=headers) as res:
                if res.status != 200:
                    raise RuntimeError('Failed to Respond')

                root = etree.fromstring(await res.text(), etree.HTMLParser())
                cNode = root.find(".//div[@id='topstuff']")
                card = self.parseGoogleC(cNode)
                search_nodes = root.findall(".//div[@class='g']")
                for node in search_nodes:
                    urlNode = node.find('.//h3/a')
                    if urlNode is None:
                        continue
                    url = urlNode.attrib['href']
                    if not url.startswith('/url?'):
                        continue
                    url = parse_qs(url[5:])['q'][0]
                    entries.append(url)
        return card, entries

    @commands.command(aliases=['google', 'Google'])
    async def g(self, ctx, *, query):
        """구글 검색을 할 수 있음 !"""
        try:
            card, entries = await self.getGoogleEntry(query)
        except RuntimeError as e:
            await edit(ctx, content=str(e), ttl=5)
        else:
            if card:
                value = '\n'.join(entries[:3])
                if value:
                    card.add_field(name='Search results', value=value, inline=False)
                return await edit(ctx, embed=card)
            if len(entries) == 0:
                return await edit(ctx, content='검색결과 없음', ttl=5)
            next_two = entries[1:3]
            before = entries[0]
            before = before[:-1] + '%29' if before[-1] == ')' else before

            e = discord.Embed(colour=discord.Color.blue(), timestamp=datetime.datetime.now())
            e.set_author(name="Google Search", url="https://www.google.com/search?q=" + query.replace(" ", "+"),
                         icon_url="https://cdn.discordapp.com/attachments/278603491520544768/300645219626647564/Google-logo-2015-G-icon.png")
            if next_two:
                formatted = '\n'.join(map(lambda x: '<%s>' % x, next_two))
                e.add_field(name="Search result", value=before)
                e.add_field(name="More", value=formatted, inline=False)
            else:
                e.add_field(name="Search result", value=before)
            await edit(ctx, embed=e)

def setup(bot):
    bot.add_cog(Google(bot))