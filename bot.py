import discord, logging, os, sqlite3
from dotenv import load_dotenv
from sqlite3 import Error
load_dotenv()
logging.basicConfig(level=logging.INFO)
client = discord.Client()
guild = discord.Guild
uid = os.getenv('id')

def check_non_empty(arg):
    if len(arg.content) == 0:
        return False
    else:
        return True

def send_long_message(arg):
    split_mesg = []
    for row in c:
        arg = arg + str(row) + '\n\n'
        if len(arg) >= 1700:
            split_mesg.append(arg)
            arg = ''
    if arg:
        split_mesg.append(arg)
    split_mesg.append("Done!")
    return split_mesg

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

            descr = str(embed.description).replace('*', '').split('\n')
            
            question = descr[0]
            c.execute("SELECT * FROM trivia_answers WHERE Question=(?)", (question,))
            trivia_answer = c.fetchone()
            if trivia_answer:
                await message.channel.send(f"Answer is {trivia_answer[3]}, {trivia_answer[2]}")
                open("answer.txt", "w").write(trivia_answer[3])

            msg = await client.wait_for('message', check=check, timeout=16)
            dank = await client.wait_for('message', check=answer, timeout=16)
            #await message.channel.send(msg.content)
            #await message.channel.send(dank.content)
            if dank.reference.message_id == msg.id:
                
                
                #await message.channel.send("question: " + question)

                option_a = str(descr[3]).replace('A) ', '').replace('*', '')
                option_b = str(descr[4]).replace('B) ', '').replace('*', '')
                option_c = str(descr[5]).replace('C) ', '').replace('*', '')
                option_d = str(descr[6]).replace('D) ', '').replace('*', '')
                options = option_a + '\n'+ option_b + '\n'+ option_c + '\n'+ option_d
                #await message.channel.send("options: " + options) 
                
                letter = ''
                correct_answer = ''

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
                    else:
                        await message.channel.send("error")
                        return
                elif 'no' in str(dank.content):
                    correct_answer = str(dank.content).split('`')[1].rstrip()
                    if correct_answer == option_a:
                        letter = 'A'
                    elif correct_answer == option_b:
                        letter = 'B'
                    elif correct_answer == option_c:
                        letter = 'C'
                    elif correct_answer == option_d:
                        letter = 'D'
                    else:
                        await message.channel.send("error, not committing to database")
                        return
                else:
                    await message.channel.send("error parsing dankmemer response, not committing answer to database")
                    return

                #await message.channel.send("answer: " + correct_answer)
                #await message.channel.send("letter: " + letter)

                if trivia_answer:
                    if trivia_answer[1] == options and trivia_answer[2] == correct_answer and trivia_answer[3] == letter:
                        return
                    else:
                        await message.channel.send(f"<@{uid}>, discrepancy detected between database and answer")
                else:
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

            if len(bot_input) == 2:
                row_offset = number_of_rows - 10
                c.execute("SELECT * FROM trivia_answers LIMIT (?),10", (row_offset,))
                send_list = 'Total Rows: ' + str(number_of_rows) + '\n\n' 
                for split in send_long_message(send_list):
                    await message.channel.send(split)

            elif len(bot_input) == 3:
                #3rd argument is passed as OFFSET, negative starts from bottom of list
                try:
                    third_arg = int(bot_input[2])
                except ValueError:
                    await message.channel.send("Not an integer!")
                    return
                except:
                    await message.channel.send("Error")
                    return
                if third_arg >= 0:
                    c.execute("SELECT * FROM trivia_answers LIMIT (?),10", (third_arg,))
                    send_list = 'Total Rows: ' + str(number_of_rows) + '\n' + 'Offset: ' + bot_input[2] + '\n\n'
                    for split in send_long_message(send_list):
                        await message.channel.send(split)
                else:
                    row_offset = number_of_rows + third_arg
                    c.execute("SELECT * FROM trivia_answers LIMIT (?),10", (row_offset,))
                    send_list = 'Total Rows: ' + str(number_of_rows) + '\n' + 'Offset: ' + str(row_offset) + '\n\n' 
                    for split in send_long_message(send_list):
                        await message.channel.send(split)

            elif len(bot_input) == 4:
                #3rd arg is offset, 4th is limit
                try:
                    third_arg = int(bot_input[2])                                                                        
                    limit = int(bot_input[3])
                except ValueError:
                    await message.channel.send("Not an integer!")
                    return
                except:
                    await message.channel.send("Error")
                    return
                if third_arg >= 0:
                    c.execute("SELECT * FROM trivia_answers LIMIT (?),(?)", (third_arg, limit))
                    send_list = 'Total Rows: ' + str(number_of_rows) + '\n' + 'Offset: ' + bot_input[2] + '\n' + 'Limit: ' + bot_input[3] + '\n\n'
                    for split in send_long_message(send_list):
                        await message.channel.send(split)
                else:
                    row_offset = number_of_rows + third_arg
                    c.execute("SELECT * FROM trivia_answers LIMIT (?),(?)", (row_offset, limit,))
                    send_list = 'Total Rows: ' + str(number_of_rows) + '\n' + 'Offset: ' + str(row_offset) + '\n' + 'Limit: ' + bot_input[3] + '\n\n'
                    for split in send_long_message(send_list):
                        await message.channel.send(split)

            elif len(bot_input) > 4:
                await message.channel.send("Too many arguments")
        
        elif cmd == '-q' or cmd == '--query':
            if len(bot_input) >= 3:
                full_query = ''
                for arg in bot_input[2:len(bot_input)]:
                    full_query = full_query + arg + ' '
                query = '%' + full_query.rstrip() + '%'
                c.execute("SELECT * FROM trivia_answers WHERE Question LIKE (?)", (query,))
                send_list = ''
                for split in send_long_message(send_list):
                    await message.channel.send(split)
                
            else:
                await message.channel.send("Need to provide search pattern")


            #TODO efficient database calls, empty message, and discord message limit

        elif cmd == '-h' or cmd == '--help':
            help_mesg = "`-h`, `--help`\n    displays help message\n`-l`, `--list`\n    lists entries in database, defaults to last 10 entries\n    optional arguments: OFFSET, LIMIT\n    `OFFSET`: offset to read database from, if only one argument is given, it is assumed to be offset\n    `LIMIT`: maximum number of rows to display\n        negative offset reads from bottom of table\n        negative limit results in no upper bound on number of rows returned\n`-q`, `--query`\n    queries database for question (case insensitive)\n`-s`, `--send`\n    sends current database to chat\n`-i`, `--info`\n    view info about this bot"
            await message.channel.send(help_mesg)

        elif cmd == '-s' or cmd == '--send':
            await message.channel.send(file=discord.File('trivia.db'))

        elif cmd == '-i' or cmd == '--info':
            await message.channel.send("source code for this bot can be viewed at <https://github.com/yadayadajaychan/dank-memer-trivia-scraper>")





token = os.getenv('token')
client.run(token)
