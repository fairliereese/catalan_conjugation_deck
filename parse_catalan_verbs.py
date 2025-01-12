import pandas as pd

df = pd.read_csv('diccionari.txt',
                 comment='#',
                 sep=' ', header=None,
                 names=['conj_verb', 'inf_verb', 'code'])

# keep only verbal forms
df = df.loc[df.code.str.startswith('V')]

# filter for only the verbs we care about
cat_sp_df = pd.read_csv('spanish_to_catalan_verbs.csv', sep=',',
                        encoding='utf-8')
cat_sp_df = cat_sp_df[['spanish_verb', 'catalan_verb']]
cat_sp_df.rename({'catalan_verb': 'inf_verb'}, axis=1, inplace=True)
df = df.loc[df.inf_verb.isin(cat_sp_df.inf_verb.tolist())]

# region
df['region'] = 'central'
df.loc[df.code.str.endswith('B'), 'region'] = 'balear'
df.loc[df.code.str.endswith('4'), 'region'] = 'balear'

df.loc[df.code.str.endswith('V'), 'region'] = 'valencia'
df.loc[df.code.str.endswith('Z'), 'region'] = 'valencia'
df.loc[df.code.str.endswith('3'), 'region'] = 'balear'

df.loc[df.code.str.endswith('5'), 'region'] = 'valencia,balear'
df.loc[df.code.str.endswith('6'), 'region'] = 'valencia,balear'
df.loc[df.code.str.endswith('7'), 'region'] = 'valencia,balear'

# mood
# I = indicative
# M = imperative
# P = participle
# G = gerund
# N = infinitive
# S = subjunctive

split_char = 'V'
split_offset=1

df['mood'] = df.code.str.split(split_char, n=1, expand=True)[1].str.slice(0+split_offset,1+split_offset)

# this character in the code which, at the very least seems like it
# distinguishes auxilary verbs
df['verb_type']  = df.code.str.split(split_char, n=1, expand=True)[1].str.slice(-1+split_offset,0+split_offset)
# df.loc[(df.inf_verb=='anar')&(df.conj_verb.isin(['vam', 'anem']))]

# gender for participles
df['gender'] = df.code.str.split(split_char, n=1, expand=True)[1].str.slice(4+split_offset,5+split_offset)

# tense
# P = present
# I = past imperfect
# F = future
# S = simple past
# C = conditional
df['tense'] = df.code.str.split(split_char, n=1, expand=True)[1].str.slice(1+split_offset,2+split_offset)

# person (1st 2nd 3rd)
df['person'] = df.code.str.split(split_char, n=1, expand=True)[1].str.slice(2+split_offset,3+split_offset)

# singular or plural
df['sing_or_plural'] = df.code.str.split(split_char, n=1, expand=True)[1].str.slice(3+split_offset,4+split_offset)
df.sing_or_plural.unique()

# keep only central forms
df = df.loc[df.region == 'central']


# remove passat simple 
df = df.loc[df.tense != 'S']

# get rid of participles save for male single because the others serve only as adjectives
# print(len(df.index))
df = df.loc[~((df.mood == 'P') &
              (df.gender == 'F'))]
df = df.loc[~((df.mood == 'P') &
              (df.sing_or_plural == 'P'))]
# print(len(df.index))

# remove auxilary verbs except haver
haver_df = df.loc[df.inf_verb=='haver'].copy(deep=True)
df = df.loc[~(df.verb_type=='A')]
df = pd.concat([haver_df, df], axis=0)
assert len(df.loc[df.inf_verb=='haver']) != 0

# get rid of some weird exceptions that result in duplicates
merge_cols = ['inf_verb', 'mood', 'tense', 'person',
              'sing_or_plural']
temp = df.loc[df.duplicated(subset=merge_cols, keep=False)]
df = df.drop_duplicates(subset=merge_cols, keep=False)

# entès, entés --> keep only central variant
temp = temp.loc[~((temp.inf_verb == 'entendre') &
              (temp.mood == 'P') &
              (temp.gender == 'M') &
              (temp.conj_verb == 'entés'))]

# estat, sigut for ser --> keep only sigut because you can practice estat w/ estar
temp = temp.loc[~((temp.inf_verb == 'ser') &
              (temp.mood == 'P') &
              (temp.gender == 'M') &
              (temp.conj_verb == 'estat'))]

# sent, essent for ser --> keep only sent because I don't like how essent looks
# print(len(temp.index))
temp = temp.loc[~((temp.inf_verb == 'ser') &
              (temp.mood == 'G') &
              (temp.conj_verb == 'essent'))]

# ser --> remove pre-2017 sóc
temp = temp.loc[~((temp.inf_verb == 'ser') &
              (temp.mood == 'I') &
              (temp.conj_verb == 'sóc'))]

# anar --> remove pre-2017 vés
temp = temp.loc[~((temp.inf_verb == 'anar') &
              (temp.mood == 'M') &
              (temp.conj_verb == 'ves'))]

# donar --> remove pre-2017 vés
temp = temp.loc[~((temp.inf_verb == 'donar') &
              (temp.mood == 'M') &
              (temp.conj_verb == 'dóna'))]

# anir<> vs ir<> for anar --> keep only anar-based because IDK
temp = temp.loc[~((temp.inf_verb=='anar') &\
              (temp.tense=='F')&\
              (temp.conj_verb.str.startswith('i')))]
temp = temp.loc[~((temp.inf_verb=='anar') &\
              (temp.tense=='C')&\
              (temp.conj_verb.str.startswith('i')))]

# haver -- keep conditional w/o gs
temp = temp.loc[~((temp.inf_verb=='haver') &\
              (temp.tense=='C')&\
              (temp.conj_verb.str.contains('g')))]


# caure, creure, dir, fer, somriure imperfect --> keep obert (è) for 
# vosaltres and nosaltres
temp = temp.loc[~((temp.inf_verb.isin(['caure', 'creure', 'dir', 'fer',
                                 'jeure', 'veure', 'somriure', 
                                 'riure', 'predir'])) &
              (temp.tense == 'I') &
              (temp.sing_or_plural == 'P') &
              (temp.person=='1')&\
              (temp.mood=='I')&
              (temp.conj_verb.str.contains('é')))]
temp = temp.loc[~((temp.inf_verb.isin(['caure', 'creure', 'dir', 'fer',
                                 'jeure', 'veure', 'somriure', 
                                 'riure', 'predir'])) &
              (temp.tense == 'I') &
              (temp.sing_or_plural == 'P') &
              (temp.person=='2')&\
              (temp.mood=='I')&
              (temp.conj_verb.str.contains('é')))]

# donar present indicative --> keep non-accented form (o)
# previous versions of 2nd / 3rd person singular had ó
# pre-2017 orth. changes, which are not reflected in the code afaik
temp = temp.loc[~((temp.inf_verb.isin(['donar'])) &
              (temp.tense == 'P') &
              (temp.conj_verb.str.contains('ó')))]

# jeure present indiccative and subjunctive; and imperative --> keep forms 
# beginning with ja instead of je
temp = temp.loc[~((temp.inf_verb.isin(['jeure'])) &
              (temp.tense == 'P') &
              (temp.mood.isin(['I', 'S']))&
              (temp.conj_verb.str.startswith('je')))]
temp = temp.loc[~((temp.inf_verb.isin(['jeure'])) &
              (temp.mood.isin(['M']))&
              (temp.conj_verb.str.startswith('je')))]

# veure imperative: use form without g for tu and vosaltres
temp = temp.loc[~((temp.inf_verb.isin(['veure'])) &
              (temp.mood.isin(['M']))&
              (temp.person=='2')&
              (temp.conj_verb.str.contains('g')))]

# venir -- get rid of present indicative accented forms, which use 
# old orthorraph
temp = temp.loc[~((temp.inf_verb.isin(['venir'])) &
              (temp.mood.isin(['I']))&
              (temp.conj_verb.str.contains('é')))]

# ser --> conditional, only keep seria etc. 
temp = temp.loc[~((temp.inf_verb.isin(['ser'])) &
              (temp.mood.isin(['I']))&
              (temp.conj_verb.str.startswith('f')))]

# tenir --> imperatives are messed uppp
temp = temp.loc[~((temp.inf_verb.isin(['tenir'])) &
              (temp.mood.isin(['M']))&
              (temp.conj_verb.isin(['tingues', 'té', 'tingueu'])))]

# lluir --> keep 'eix' versions of verb in non nosaltres / vosaltres forms
# also make decisions on the imperative forms and subjunctive
temp = temp.loc[~((temp.inf_verb.isin(['lluir'])) &
              (temp.mood.isin(['I']))&
              (temp.tense=='P')&\
              (temp.conj_verb.isin(['lluu', 'lluo', 'lluen', 'llus', 'llu', 'lluus'])))]
temp = temp.loc[~((temp.inf_verb.isin(['lluir'])) &
              (temp.mood.isin(['M']))&
              (temp.conj_verb.isin(['lluu', 'llu', 'lluï', 'lluïn'])))]
temp = temp.loc[~((temp.inf_verb.isin(['lluir'])) &
              (temp.mood.isin(['S']))&
              (temp.tense=='P')&
              (temp.conj_verb.isin(['lluï', 'lluïn', 'lluïs'])))]
temp = temp.loc[~((temp.inf_verb.isin(['lluir'])) &
              (temp.mood.isin(['S']))&
              (temp.tense=='P')&
              (temp.conj_verb.isin(['lluï', 'lluïn', 'lluïs'])))]


# haver --> remove the persent indicative versions I don't use
temp = temp.loc[~((temp.inf_verb.isin(['haver'])) &
              (temp.mood.isin(['I']))&
              (temp.tense=='P')&\
              (temp.conj_verb.isin(['haig', 'haveu', 'havem'])))]

df = pd.concat([df, temp], axis=0)

# negative command -- just the subjunctive present
neg_cmd_df = df.loc[(df.mood=='S')&(df.tense=='P')]
neg_cmd_df['pos_neg_cmd'] = 'neg'
neg_cmd_df['mood'] = 'M'
neg_cmd_df['tense'] = '0'

# add positive / neg designations for commands
df['pos_neg_cmd'] = '0'
df.loc[df.mood=='M', 'pos_neg_cmd'] = 'pos'

# now add 
df = pd.concat([df, neg_cmd_df], axis=0)

# add perfet, passat perifrastic, negative command
# by looping through each infinitive verb
for infinitive in df.inf_verb.unique().tolist():
    
    # perfet
    haver = [['he', '1', 'S', 'I', 'perfet'],
             ['has', '2', 'S', 'I', 'perfet'],
             ['ha', '3', 'S', 'I', 'perfet'],
             ['hem', '1', 'P', 'I', 'perfet'],
             ['heu', '2', 'P', 'I', 'perfet'],
             ['han', '3', 'P', 'I', 'perfet']]
    haver_df = pd.DataFrame(data=haver,
                            columns=['haver_verb',
                                     'person', 
                                     'sing_or_plural', 
                                     'mood',
                                     'tense'])
    participle = df.loc[(df.inf_verb==infinitive)&\
                        (df.mood=='P')&\
                        (df.gender=='M')&\
                        (df.sing_or_plural=='S')].conj_verb.unique()
    try:
        assert len(participle) == 1
    except:
        print(infinitive)
        print(participle)
    participle = participle[0]
    
    haver_df['conj_verb'] = haver_df.haver_verb+' '+participle
    haver_df['inf_verb'] = infinitive
    df = pd.concat([df, haver_df], axis=0)
    
    # passat perifrastic
    anar = [['vaig', '1', 'S', 'I', 'passat_perifrastic'],
             ['vas', '2', 'S', 'I', 'passat_perifrastic'],
             ['va', '3', 'S', 'I', 'passat_perifrastic'],
             ['vam', '1', 'P', 'I', 'passat_perifrastic'],
             ['vau', '2', 'P', 'I', 'passat_perifrastic'],
             ['van', '3', 'P', 'I', 'passat_perifrastic']]
    anar_df = pd.DataFrame(data=anar,
                            columns=['anar_verb',
                                     'person', 
                                     'sing_or_plural', 
                                     'mood',
                                     'tense'])
    anar_df['conj_verb'] = anar_df.anar_verb+' '+infinitive
    anar_df['inf_verb'] = infinitive
    df = pd.concat([df, anar_df], axis=0)
df['pos_neg_cmd'] = df['pos_neg_cmd'].fillna('0')

# other synthetic tenses?
# plusquamperfet, passat anterior, passat anterior preifrastic, 
# futur perfet... etc.

df.to_csv('catalan_verbs_parsed.tsv', sep='\t', index=False)