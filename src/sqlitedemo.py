#import sqlite3

#fens = splite3.connect(':memory:')
#fens = sqlite3.connect('fens.db')

#c = fens.cursor()

#c.execute("""CREATE TABLE IF NOT EXISTS fens (
#  name text,
#  number integer,
#  notation text
#  )""")

#c.execute("INSERT INTO fens VALUES ('Position 1',1,'rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2')")
#c.execute("INSERT INTO fens VALUES (?,?,?)", (val1,val2,val3))
#c.execute("INSERT INTO fens VALUES (:name,:number,:notation)", {'name':val1,'number':val2,'notation':val3})
#c.execute("SELECT * FROM fens WHERE number = 1")
#print(c.fetchone()) #fetchmany and fetchall works too
#fens.commit()

#fens.close()

# used to store puzzles / save and load games using FEN