import sqlite3
import pandas as pd

# spanish <-> catalan verbs
cat_sp_df = pd.read_csv('spanish_to_catalan_verbs.csv', sep=',',
                        encoding='utf-8')
cat_sp_df = cat_sp_df[['spanish_verb', 'catalan_verb']]
cat_sp_df.rename({'catalan_verb': 'inf_verb'}, axis=1, inplace=True)

conn = sqlite3.connect('collection.anki21')
cursor = conn.cursor()

# get the tags and notes for each card
cursor.execute("SELECT sfld, tags FROM notes")
rows = cursor.fetchall()
notes = []
tags = []
intro_phrases = ["El verbo en",
                 "Before",
                 "During",
                 "Grammar",
                 "For ", 
                 "I hesitated",
                 "If you see"]
for row in rows:
    if row[0].startswith(intro_phrases[0]): pass
    elif row[0].startswith(intro_phrases[1]): pass
    elif row[0].startswith(intro_phrases[2]): pass
    elif row[0].startswith(intro_phrases[3]): pass
    elif row[0].startswith(intro_phrases[4]): pass
    elif row[0].startswith(intro_phrases[5]): pass
    elif row[0].startswith(intro_phrases[6]): pass
    else:
        notes.append(row[0])
        tags.append(row[1])
        
# make into a df
df = pd.DataFrame(data=notes,
                  columns=['note'])
df['tags'] = tags

# get the base verb and add catalan equivalent
# (inner merge to get rid of verbs I didn't add equivalents for)
df['spanish_verb'] = df['note'].str.split('::…', expand=True)[1].str.split('…}}', expand=True)[0]
df = df.merge(cat_sp_df,
              how='inner',
              on='spanish_verb')

# context phrases to translate
df['context_phrase' ] = df.note.str.split('(', expand=True)[1].str.split(')', expand=True)[0]
temp = pd.DataFrame(data=df.context_phrase.unique().tolist(), columns=['spanish_phrase'])
temp.to_csv('spanish_context_phrases.tsv', sep='\t', index=False)