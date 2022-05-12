import sqlite3
import model.data as data

con = sqlite3.connect('MegaDataBase.db')
cur = con.cursor()

data.setup(cur)

con.commit()
con.close()