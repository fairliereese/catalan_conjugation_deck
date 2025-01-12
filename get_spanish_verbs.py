import sqlite3
import pandas as pd

conn = sqlite3.connect('collection.anki21')
cursor = conn.cursor()

# first, just get all the verbs
cursor.execute("SELECT sfld FROM notes")
rows = cursor.fetchall()
notes = []
verbs = []
for row in rows:
    if row[0].startswith("El verbo en"):
        notes.append(row[0])
        verbs.append(row[0].split('{{c1::')[1].split('}}')[0])
        
assert len(notes) == 72

df = pd.DataFrame(data=verbs, columns=['spanish_verb'])
df.to_csv('spanish_verbs.tsv', sep='\t')