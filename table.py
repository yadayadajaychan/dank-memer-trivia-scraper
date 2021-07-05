import sqlite3

conn = sqlite3.connect("trivia.db")
c = conn.cursor()

def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS trivia_answers (Question TEXT UNIQUE, Options TEXT NOT NULL, Answer TEXT NOT NULL, Letter TEXT NOT NULL)")

def test():
    c.execute("INSERT INTO trivia_answers VALUES('test question', 'test options', 'test answer', 'test letter')")
    conn.commit()
    c.close()
    conn.close()

create_table()
#test()
