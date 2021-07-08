import sqlite3

conn = sqlite3.connect("trivia.db")
c = conn.cursor()

def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS trivia_answers (Question TEXT UNIQUE, Options TEXT NOT NULL, Answer TEXT NOT NULL, Letter TEXT NOT NULL)")
    conn.commit()

def insert():
    c.execute("INSERT INTO trivia_answers VALUES('test question', 'test options', 'test answer', 'test letter')")
    conn.commit()

def delete():
    return

def check():
    c.execute("SELECT * FROM trivia_answers")
    for row in c:
        if row[2] not in row[1]:
            print(str(row) + '\n')


#create_table()
#insert()
#delete()

check()

c.close()
conn.close()
