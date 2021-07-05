import discord, logging, os, sqlite3
from dotenv import load_dotenv
from sqlite3 import Error
load_dotenv()
logging.basicConfig(level=logging.INFO)
client = discord.Client()
guild = discord.Guild

def check_non_empty(arg):
    if len(arg.content) == 0:
        return False
    else:
        return True

conn = sqlite3.connect("trivia.db")
c = conn.cursor()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    #TODO: Query database command
    #if message.content.startswith('jhetto'):
        #async for msg in message.channel.history(limit=20):
        #    if msg.author != client.user:
        #        if check_non_empty(msg):
        #            sendmsg = 'Message content: ' + str(msg.content) + '\n' + 'Message author: ' + str(msg.author.name) + '\n' + 'Message sent: ' + str(msg.created_at) + '\n' + str(msg)
        #            await message.channel.send(sendmsg)

    for embed in message.embeds:
        if "trivia question" in str(embed.author):

            def check(m):
                if m.channel == message.channel:
                    mesg_content = str(m.content).upper()
                    if mesg_content == 'A' or mesg_content == 'B' or mesg_content == 'C' or mesg_content == 'D': 
                        return True
            def answer(m):
                if m.channel == message.channel and m.author.id == 270904126974590976:
                    return True

            msg = await client.wait_for('message', check=check, timeout=30)
            dank = await client.wait_for('message', check=answer, timeout=30)
            #await message.channel.send(msg.content)
            #await message.channel.send(dank.content)
            if dank.reference.message_id == msg.id:
                descr = str(embed.description).replace('*', '').split('\n')
                question = descr[0]
                #await message.channel.send("question: " + question)

                option_a = str(descr[3]).replace('A) ', '').replace('*', '')
                option_b = str(descr[4]).replace('B) ', '').replace('*', '')
                option_c = str(descr[5]).replace('C) ', '').replace('*', '')
                option_d = str(descr[6]).replace('D) ', '').replace('*', '')
                options = option_a + '\n'+ option_b + '\n'+ option_c + '\n'+ option_d
                #await message.channel.send("options: " + options) 
                
                global letter
                global correct_answer

                if 'coin' in str(dank.content):
                    letter = str(msg.content).upper()
                    if letter == 'A':
                        correct_answer = option_a
                    elif letter == 'B':
                        correct_answer = option_b
                    elif letter == 'C':
                        correct_answer = option_c
                    elif letter == 'D':
                        correct_answer = option_d
                elif 'no' in str(dank.content):
                    correct_answer = str(dank.content).split('`')[1]
                    if correct_answer == option_a:
                        letter = 'A'
                    elif correct_answer == option_b:
                        letter = 'B'
                    elif correct_answer == option_c:
                        letter = 'C'
                    elif correct_answer == option_d:
                        letter = 'D'
                else:
                    await message.channel.send("error parsing dankmemer response, not committing answer to database")
                    return None

                #await message.channel.send("answer: " + correct_answer)
                #await message.channel.send("letter: " + letter)

                #TODO: Sanitize database inputs
                c.execute("INSERT INTO trivia_answers (Question, Options, Answer, Letter) VALUES (?, ?, ?, ?)", (question, options, correct_answer, letter))
                conn.commit()

token = os.getenv('token')
client.run(token)
