import os
import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import datetime
from dotenv import load_dotenv  
from transformers import GPTNeoForCausalLM, GPT2Tokenizer
import random

#pip install discord.py requests beautifulsoup4 python-dotenv asyncio transformers

load_dotenv()
token = os.getenv('DISCORD_BOT_TOKEN')
app_key = os.getenv('APP_KEY')

model = GPTNeoForCausalLM.from_pretrained("EleutherAI/gpt-neo-1.3B")
tokenizer = GPT2Tokenizer.from_pretrained("EleutherAI/gpt-neo-1.3B")
tokenizer.pad_token = tokenizer.eos_token



intents = discord.Intents.all()
activity = discord.Game(name="/help")

#i fixed it

client = commands.Bot(case_insensitive=True,
                          command_prefix='/',
                          intents=intents,
                          activity=activity,
                          status=discord.Status.dnd)


@client.event
async def on_ready():
    print("We have logged in as", client.user)




@client.command()
async def news(ctx):

    page = requests.get('https://www.bbc.com/news/topics/cmj34zmwm1zt')
    soup = BeautifulSoup(page.text, 'html.parser')
    news_title_elements = soup.find_all(class_='bvDsJq')
    news_desc_elements = soup.find_all(class_='cNPpME')
    news_date_elements = soup.find_all(class_='dkFuVs')

    #data = []
    desc = 'test'
    formatted = ""
    for i in range(len(news_title_elements)-1):
        title = news_title_elements[i].text
        desc = news_desc_elements[i].text
        date = news_date_elements[i].text
        formatted += f"**{title:<60}** *({date})*\n{desc}\n\n"

    
    
    member = ctx.author
    user = await client.fetch_user(member.id)
    url = member.avatar


    em = discord.Embed(title="Recent Climate Change News",timestamp=datetime.datetime.now(datetime.UTC),description=formatted,color=discord.Color.blurple())
    em.set_footer(text=f"Requested by {user}",
                      icon_url=url)
    await ctx.message.channel.send(embed=em)
    

@client.command()
async def weather(ctx, *, city='Oakville'):
    
    try:
        url = "http://api.weatherapi.com/v1/current.json"
        current = requests.get(url,params={'key':app_key,'q':city})
        data = current.json()

        '''url = "http://api.weatherapi.com/v1/forecast.json"
        forecast = requests.get(url,params={'key':app_key,'q':city,'days':14})
        print(forecast.json())'''

        member = ctx.author
        user = await client.fetch_user(member.id)
        url = member.avatar

        formatted = f"**Location:** {data['location']['name']}, {data['location']['region']} ({data['location']['country']})\n**Local time:** {data['location']['localtime']} "
        em = discord.Embed(title=f"**{data['current']['condition']['text']} **| {data['current']['temp_c']} °C ({data['current']['temp_f']} °F) ",timestamp=datetime.datetime.now(datetime.UTC),description=formatted,color=discord.Color.blurple())

        em.add_field(
                        name="**Feels like**",
                        value=f"{data['current']['feelslike_c']} °C ({data['current']['feelslike_f']} °F) ",
                        inline=False)
        em.add_field(
                        name="**Wind**",
                        value=f"{data['current']['wind_kph']} km/h °C ({data['current']['wind_dir']} °F) ",
                        inline=False)

        em.add_field(
                        name="**Preciptiation**",
                        value=f"{data['current']['precip_mm']} mm ",
                        inline=False)
        em.add_field(
                        name="**Humidity**",
                        value=f"{data['current']['humidity']} % ",
                        inline=False)
        
        em.set_footer(text=f"Requested by {user}",
                        icon_url=url)
        em.set_thumbnail(
                url=f"https:{data['current']['condition']['icon']}"
            )
        await ctx.message.channel.send(embed=em)


    except KeyError:
        await ctx.message.channel.send("Please try again and ensure the city is valid.")


@client.command()
async def forecast(ctx, *, city='Oakville'):
    
    try:
        url = "http://api.weatherapi.com/v1/forecast.json"
        forecast = requests.get(url,params={'key':app_key,'q':city,'days':6})
        data = forecast.json()
        print(data)


        member = ctx.author
        user = await client.fetch_user(member.id)
        url = member.avatar


        formatted = f"**Location:** {data['location']['name']}, {data['location']['region']} ({data['location']['country']})\n**Local time:** {data['location']['localtime']}\n\nForecast for the next 5 days:"
        em = discord.Embed(title=f"**{data['current']['condition']['text']} **| {data['current']['temp_c']} °C ({data['current']['temp_f']} °F) ",timestamp=datetime.datetime.now(datetime.UTC),description=formatted,color=discord.Color.blurple())

        temp = []
        for i in range(1,6):
            print(i)
            temp = data['forecast']['forecastday'][i]['date'].split('-')
            date = f"{temp[1]}/{temp[2]}"
            
            willitrain = data['forecast']['forecastday'][i]['day']['daily_will_it_rain']
            precipitation = data['forecast']['forecastday'][i]['day']['totalprecip_mm']
            maxtemp = data['forecast']['forecastday'][i]['day']['maxtemp_c']
            mintemp = data['forecast']['forecastday'][i]['day']['mintemp_c']
            avgtemp = data['forecast']['forecastday'][i]['day']['avgtemp_c']
            conditiontext = data['forecast']['forecastday'][i]['day']['condition']['text']

            if willitrain == 1:
                willitrain = 'Yes'
                
            else:
                willitrain = 'No'
            
            em.add_field(
                        name=f"**👈 {date}:** {avgtemp}°C & {conditiontext}",
                        value=f"Precipitation: {willitrain} ({precipitation} mm)\nMax Temp: {maxtemp} °C\nMin Temp: {mintemp} °C",
                        inline=False)
            
        em.set_footer(text=f"Requested by {user}",
                        icon_url=url)
        
        em.set_thumbnail(
                url=f"https:{data['current']['condition']['icon']}"
            )
        await ctx.message.channel.send(embed=em)


    except KeyError:
        await ctx.message.channel.send("Please try again and ensure the city is valid.")



@client.command()
async def advice(ctx):

    # Generate a piece of advice
    await ctx.message.reply('Response loading...')
    
    # Define prompt
    prompt = "Generate one sentence of advice for how to reduce energy consumption."

    # Tokenize input prompt
    input_ids = tokenizer(prompt, return_tensors="pt", padding=True).input_ids
    
    # Generate the attention mask
    attention_mask = input_ids.ne(tokenizer.pad_token_id).long()

    outputs = model.generate(
        input_ids,
        attention_mask=attention_mask,  # Pass the attention mask
        max_length=110,
        do_sample=True,
        temperature=0.5,
        top_p=0.9,
        top_k=50,
        repetition_penalty=1.2,  
        pad_token_id=tokenizer.eos_token_id,  # Avoid repetition by setting eos_token_id
        num_return_sequences=1  # Generate only one sequence
    )
    
    # Decode and return the generated text
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
    
    advice = generated_text
    advice = advice[71:]

    # Reply with the generated advice
    await ctx.message.reply(advice)


@client.command()
async def ecochallenge(ctx):
    challenges = ["🥩 Meatless Mondays: I dare you to spend one day per week on a vegetarian diet!",
                  "💡 Turn-off Tuesdays: I dare you to spend one day per week shutting off all technology and devices that use electricity for one hour!",
                  "🚶 Walking Wednesdays: I dare you to spend one day per week commuting on foot!",
                  "🚯 Trashless Thursdays: I dare you to spend one day per week only using reusable items and generating no trash!",
                  "🥪 Foodie Fridays: I dare you to spend one day per week paying attention to what you eat and only eating organic/locally sourced produce!",
                  "🌍 Sustainable Saturday: I dare you to spend one day per week using only sustainable items!",
                  "🌱 Seedling Sunday: I dare you to spend one day per week planting/taking care of a plant!"]
    
    random_number = random.randint(0,6)
    await ctx.message.reply(challenges[random_number])
    

@client.command(description="Returns the ping of the bot")
async def ping(ctx):
    embed = discord.Embed(title="Testing ping...")
    import time
    start = time.time()
    msg = await ctx.message.channel.send(embed=embed)
    end = time.time()
    embed = discord.Embed(title="Pong!")
    embed.add_field(name="> Bot Latency",
                    value=f"``{round((end -  start) * 1000)}ms``",
                    inline=False)
    embed.add_field(name="> API Latency",
                    value=f"``{round(client.latency * 1000)}ms``",
                    inline=False)
    return await msg.edit(embed=embed)




client.run(token)
