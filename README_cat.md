# Creant la baralla de cartes de conjugació per català

Estic aprenent català com que em vaig mudar a Catalunya gairebé fa un any. Tot i que estic contenta amb el meu progrés al moment, trobo més difícils les formes de conjugació en català i menys naturals que les de castellà (que vaig estudiar 4 anys a l'institut). A més, hi ha certes formes que mai he entès (per exemple, el subjuntiu imperfet). Per tant, volia trobar una solució per ajudar-me de practicar les conjugacions de manera més útil que simplement escrivint les formes verbals en una taula, que al fi, falta el context necessari per aprendre les conjugacions.

Per adquirir el vocabulari, he estat utilitzant [Anki](https://ankiweb.net/), una aplicació de flashcards que fa servir repetició espaiada per optimitzar la retenció del vocabulari. Vaig trobar [aquesta excel·lent baralla de cartes](https://ankiweb.net/shared/info/638411848) que fa exactament allò que vull, però és pel castellà. Per resumir, aquesta baralla de cartes utilitza 72 verbs els quals eren triats per exemplificar cada patró de conjugació tant els regulars i els irregulars, a dins d'una frase. Vaig fer servir aquesta baralla de cartes per crear-ne una equivalent per a català.

## Analitzant la baralla de cartes de conjucacions castellanes

En lloc de tornar a fer tota [la feina per generar la baralla de cartes castellana](https://www.asiteaboutnothing.net/ultimate-spanish-conjugation-verb-set.php), vaig decidir simplement agafar-ne tots els verbs, traduir-los a català, i utilitzar només aquests verbs per formar part de la baralla de cartes catalana. Per tant, primer, vaig descarregar la [baralla de cartes castellana](https://ankiweb.net/shared/info/638411848).

```bash
unzip Ultimate_Spanish_Conjugation_Lisardos_KOFI_Method.apkg
python get_spanish_verbs.py
```

Això farà el fitxer `spanish_verbs.tsv`. A continuació, vaig traduir tots els verbs castellans als seus equivalents catalans, que són al fitxer `spanish_to_catalan_verbs.csv`. Vaig treure uns quants verbs en aquest pas.

## Obtaining Catalan verbal forms

Then, I needed a list of all Catalan verbal forms and metadata about each one. The Catalan speaking and learning community is incredibly lucky to have the [Softcatalà resource](https://www.softcatala.org/), including a [verb conjugator](https://www.softcatala.org/conjugador-de-verbs/). They have a number of computational tools to support this resource on their [GitHub](https://github.com/Softcatala/catalan-dict-tools/).


I obtained the entire dictionary from Softcatalà using their tools.
```bash
git clone https://github.com/Softcatala/catalan-dict-tools.git
cd catalan-dict-tools
bash build-lt.sh
```
This should result in the file `diccionari.txt`, which I include in this repo.

I then parsed the codes from the Softcatalà dictionary to obtain the form information for each conjugated verb (mood, tense, pronoun, etc.). Based on my needs, I had to make some decisions about specific verbal forms to keep, and which to remove.
* Keep only the Central conjugations (ie. remove Valencian and Balearic conjugations)
* Remove the past simple conjugations and replace them with periphrasic past conjugations
* Remove future subjunctive conjugations
* Add negative command conjugations (which are just the present subjunctive)
* From here, for many verbs with multiple valid forms, pick one (this is behavior I'd like to change in the future; ie. by displaying all valid options)

```bash
python parse_catalan_verbs.py
```

This results in the `catalan_verbs_parsed.tsv` table.

## Translating context phrases

Each card contains phrases in order to contextualize the target verb that also needed to be translated to Catalan. I split the notes on each Spanish card using a variety of delimiters and then manually translated them from Spanish to Catalan.

```bash
python get_spanish_context_phrases.py
```

This results in `spanish_context_phrases.tsv`, and the manual translations (with added pronoun translations [ie tú->tu; yo->jo]) are in `spanish_catalan_context_phrases.csv`.

This part is likely the one that resulted in some difficult-to-catch errors, if you see any please contact me or open an issue on this GitHub repo.


## Assembling the final table

I used the tags from the Spanish conjugation deck that defined the verbal forms to merge with the equivalent Catalan verbal forms. I added tags for verb endings, verbal forms, and infinitive for each card. Finally, I replaced the Spanish text (including the context phrases, the infinitive, and the conjugated form) with the Catalan equivalent.

```bash
python get_anki_table.py
```

This results in the `table_to_make_cards.csv` file. All that's left now is to import the cards into Anki!

## Final cards and recommendations

The final `.apkg` file can be downloaded [here](https://github.com/fairliereese/catalan_conjugation_deck/blob/main/catal%C3%A0_conjugaci%C3%B3.apkg) from the GitHub repo. The original author of the Spanish conjugation deck put a lot of work into making a [manual](https://www.asiteaboutnothing.net/w_ultimate_spanish_conjugation.php#how) on how to most effectively use these cards, and I recommend reading it before studying.

## Wishlist

There are a few things that I would like to add in the future:
* For forms with multiple valid conjugations, report all valid forms as answers
* Add `treure` to the table instead of `jeure`
* Add `dur` to the table
* Add `haver-hi` card
* Add past perfect cards to help train the difference between past perfect and periphrasic past, as the distictions are different than they are in English and Latin American Spanish (ie add key words `avui` / `aquest cap de setmana` vs. `ahir` / `l'any passat`)

Again, if you see any errors, as this was done systematically, please feel free to contact me and I will try to make an update!


(Gràcies a les eines de Softcatalà per ajudar-me corregir aquest text)
