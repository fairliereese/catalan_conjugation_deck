import sqlite3
import pandas as pd

conn = sqlite3.connect('collection.anki21')
cursor = conn.cursor()

# spanish <-> catalan verbs
cat_sp_df = pd.read_csv('spanish_to_catalan_verbs.csv', sep=',',
                        encoding='utf-8')
cat_sp_df = cat_sp_df[['spanish_verb', 'catalan_verb']]
cat_sp_df.rename({'catalan_verb': 'inf_verb'}, axis=1, inplace=True)

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

# get rid of vos
# print(len(df.index))
# df = df.loc[~((df.tags.str.contains(' tú_vos '))&
#             ~(df.tags.str.contains(' tú ')))]
df = df.loc[~((df.tags.str.contains(' vos ')))]
# print(len(df.index))

# get rid of subjunctive future
# print(len(df.index))
df = df.loc[~df.tags.str.contains(' subjuntivo_futuro ')]
# print(len(df.index))

# remove hay
df = df.loc[~df.tags.str.contains('idiom')]

# tags I care about that I can merge on

# 1, 2, 3rd person
person_map = {'yo': '1',
              'tú': '2',
              'tú_vos': '2',
              'él_ella_usted': '3',
              'nosotros': '1',
              'vosotros': '2',
              'ellos_ellas_ustedes': '3'}
df['person'] = '0'
for key, item in person_map.items():
    thing = ' '+key+' '
    df.loc[df.tags.str.contains(thing), 'person'] = person_map[key]

# singular or plural
sing_or_plural_map = {'yo': 'S',
              'tú': 'S',
              'tú_vos': 'S',
              'él_ella_usted': 'S',
              'nosotros': 'P',
              'vosotros': 'P',
              'ellos_ellas_ustedes': 'P'}
df['sing_or_plural'] = '0'
for key, item in sing_or_plural_map.items():
    thing = ' '+key+' '
    df.loc[df.tags.str.contains(thing), 'sing_or_plural'] = sing_or_plural_map[key]
df.loc[df.tags.str.contains(' participio '), 'sing_or_plural'] = 'S'

# mood
mood_map = {'presente': 'I',
           'imperfecto': 'I',
           'indefinido': 'I',
           'futuro': 'I',
           'condicional': 'I',
           'subjuntivo_presente': 'S',
           'subjuntivo_pasado': 'S',
           'imperativo': 'M',
           'negative_imperativo': 'M',
           'gerundio': 'G',
           'participio': 'P'}
df['mood'] = '0'
for key, item in mood_map.items():
    thing = ' '+key+' '
    df.loc[df.tags.str.contains(thing), 'mood'] = mood_map[key]

# tense
tense_map = {'presente': 'P',
           'imperfecto': 'I',
           'indefinido': 'passat_perifrastic',
           'futuro': 'F',
           'condicional': 'C',
           'subjuntivo_presente': 'P',
           'subjuntivo_pasado': 'I'}
df['tense'] = '0'
for key, item in tense_map.items():
    thing = ' '+key+' '
    df.loc[df.tags.str.contains(thing), 'tense'] = tense_map[key]

# pos_neg_cmd
pos_neg_map = {'imperativo': 'pos',
               'negative_imperativo': 'neg'}
df['pos_neg_cmd'] = '0'
for key, item in pos_neg_map.items():
    thing = ' '+key+' '
    df.loc[df.tags.str.contains(thing), 'pos_neg_cmd'] = pos_neg_map[key]

# get rid of imperative haver
df = df.loc[~((df.mood=='M')&(df.inf_verb=='haver'))]

merge_cols = ['inf_verb', 'mood', 'tense', 'person',
              'sing_or_plural', 'pos_neg_cmd']
df.loc[df.duplicated(subset=merge_cols, keep=False)].sort_values(by=merge_cols).head()

# TODO add a version of the past using "ahir"
# for the passat simple (ie he anat)

# translated spanish to cat. phrases to stick on the cards
trans_df = pd.read_csv('spanish_catalan_context_phrases.csv', sep=',',
                        encoding='utf-8')

# replace all translated df stuff w/ catalan
df['cast_note'] = df.note.tolist()
for ind, entry in trans_df.iterrows():
    sp = entry.spanish_phrase
    ca = entry.catalan_phrase
    df.note = df.note.str.replace(sp, ca)

merge_cols = ['inf_verb', 'mood', 'tense', 'person',
              'sing_or_plural', 'pos_neg_cmd']

df.loc[df.duplicated(subset=merge_cols, keep=False)].sort_values(by=merge_cols).head()

# add the catalan conjugations
cat_conj_df = pd.read_csv('catalan_verbs_parsed.tsv', sep='\t', encoding='utf-8')
# cat_conj_df.loc[cat_conj_df.duplicated(subset=merge_cols, keep=False)].sort_values(by=merge_cols)


for c in merge_cols:
    df[c] = df[c].astype(str)
    cat_conj_df[c] = cat_conj_df[c].astype(str)
df = df.merge(cat_conj_df,
              how='left',
              on=merge_cols)

l = len(df.loc[df.duplicated(subset=merge_cols, keep=False)].sort_values(by=merge_cols))
assert l == 0

# fix context text for estar
# singular
inds = df.loc[(df.inf_verb=='estar')&(df.note.str.contains('Cadis'))&(df.sing_or_plural=='S')].index.tolist()
df.loc[inds, 'note'] = df.loc[inds].note.str.replace('a Cadis', 'feliç')

# plural
inds = df.loc[(df.inf_verb=='estar')&(df.note.str.contains('Cadis'))&(df.sing_or_plural=='P')].index.tolist()
df.loc[inds, 'note'] = df.loc[inds].note.str.replace('a Cadis', 'feliços')

# replace inf verb and conj verb in note
df['note1'] = df.note.str.split('{{', expand=True)[0]
df['note2'] = df.note.str.split('}}', expand=True)[1]
df['cat_note'] = df.note1+'{{c1::'+df.conj_verb+'::…'+\
                 df.inf_verb+'…}}'+df.note2
df.cat_note[0]

# add neg. commands for everything by just sticking a no everywhere in the pos. cmds
# remove old negative imperatiu
# print(len(df.index))
df = df.loc[~df.tags.str.contains('negative_imperativo')]
# print(len(df.index))

imp_df = df.loc[df.mood=='M'].copy(deep=True)
imp_df['cat_note'] = imp_df.note1+'no {{c1::'+imp_df.conj_verb+'::…'+\
                     imp_df.inf_verb+'…}}'+imp_df.note2
imp_df.pos_neg_cmd = 'neg'
# print(len(df.index))
df = pd.concat([df, imp_df], axis=0)
# print(len(df.index))

# tags for tense
d = {'P': 'present',
     'I': 'imperfet',
     'passat_perifrastic': 'passat_perifrastic',
     'F': 'futur',
     'C': 'condicional',
     '0': ''}
df['tense_tag'] = df.tense.map(d)

# tags for mood
d = {'G': 'gerundi',
     'P': 'participi',
     'I': 'indicatiu',
     'S': 'subjuntiu',
     'M': 'imperatiu'}
df['mood_tag'] = df.mood.map(d)

# neg. imperative
df.loc[(df.mood=='M')&
       (df.pos_neg_cmd=='neg'), 'mood_tag'] = 'imperatiu_negatiu'

# tags for ending
df['ending_tag'] = ''
df.loc[df.inf_verb.str.endswith('ir'), 'ending_tag'] = '-ir'
df.loc[df.inf_verb.str.endswith('re'), 'ending_tag'] = '-re'
df.loc[df.inf_verb.str.endswith('ar'), 'ending_tag'] = '-ar'
df.loc[df.inf_verb.str.endswith('er'), 'ending_tag'] = '-er'

# tags for personal pronoun

df['pronoun_tag'] = ''

# jo
df.loc[(df.sing_or_plural=='S')&
       (df.person=='1'), 'pronoun_tag'] = 'jo'

# tu
df.loc[(df.sing_or_plural=='S')&
       (df.person=='2'), 'pronoun_tag'] = 'tu'

# ell/ella/vostè
df.loc[(df.sing_or_plural=='S')&
       (df.person=='3'), 'pronoun_tag'] = 'ell/ella/vostè'

# nosaltres
df.loc[(df.sing_or_plural=='P')&
       (df.person=='1'), 'pronoun_tag'] = 'nosaltres'

# vosaltres
df.loc[(df.sing_or_plural=='P')&
       (df.person=='2'), 'pronoun_tag'] = 'vosaltres'

# ells/elles/vostès
df.loc[(df.sing_or_plural=='P')&
       (df.person=='3'), 'pronoun_tag'] = 'ells/elles/vostès'

df['cat_tags'] = ' '+df['tense_tag']+\
                 ' '+df['mood_tag']+\
                 ' '+df['ending_tag']+\
                 ' '+df['pronoun_tag']+\
                 ' '+df['inf_verb']+' '
df.cat_tags = df.cat_tags.str.replace('  ', ' ')
df.cat_tags = df.cat_tags.str.replace('  ', ' ')
df.cat_tags = df.cat_tags.str.replace('  ', ' ')
df.loc[df.cat_tags.str.contains('  ')]

# add new tags
df.to_csv('table_to_make_cards.csv', sep='|', index=False)
