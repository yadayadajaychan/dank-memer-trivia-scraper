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

                c.execute("INSERT INTO trivia_answers (Question, Options, Answer, Letter) VALUES (?, ?, ?, ?)", (question, options, correct_answer, letter))
                conn.commit()

    if message.content.startswith('db'):
        bot_input = message.content.lower().split()
        if len(bot_input) > 1:
            cmd = bot_input[1]
        else:
            cmd = "--help"

        if cmd == '-l' or cmd == '--list':
            c.execute("SELECT COUNT(*) FROM trivia_answers")
            number_of_rows = c.fetchone()[0]
            row_offset = number_of_rows - 10
            c.execute("SELECT * FROM trivia_answers LIMIT (?),10", (row_offset,))
            send_list = ''
            for row in c.fetchall():
                send_list = send_list + str(row) + '\n' 
            await message.channel.send(send_list)






token = os.getenv('token')
client.run(token)
