# Creating the Catalan conjugation Anki deck

I am learning Catalan as I moved to Catalunya almost a year ago. While I'm happy with my progress thus far, I've found the conjugation patterns of verbs in Catalan more challenging and less natural than in Spanish (which I studied for 4 years in high school). Moreover, in neither language have I been good at using certain forms (such as imperfect subjunctive). Thus, I wanted to find a solution to help me drill conjugations in a way more meaningful than simply writing verb forms out in a table, which ultimately is missing the context needed to internalize the conjugations in a meaningful way.

For vocabulary acquisition, I've been using [Anki](https://ankiweb.net/), which is a highly-customizable flashcards platform that employs spaced repetition to optimize retention. I found [this excellent deck](https://ankiweb.net/shared/info/638411848) which does exactly what I want, but for Spanish. In summary, this deck uses 72 verbs which were picked to exemplify all possible regular and irregular conjugation patterns for all verbal forms within the context of a sentence. I used this deck as a template to create an equivalent deck for Catalan.

## Parsing the Spanish conjugation deck

Instead of re-implementing all [the work done to generate the Spanish deck](https://www.asiteaboutnothing.net/ultimate-spanish-conjugation-verb-set.php), I decided to simply take all the verbs from the original Spanish deck, translate them to Catalan, and use just those verbs to form the basis of the Catalan deck. Thus, first I downloaded the [Spanish conjugation deck](https://ankiweb.net/shared/info/638411848).

```bash
unzip Ultimate_Spanish_Conjugation_Lisardos_KOFI_Method.apkg
python get_spanish_verbs.py
```

This will give the `spanish_verbs.tsv` file. I then manually translated all the Spanish verbs to the Catalan equivalents, which are in the `spanish_to_catalan_verbs.csv` file. I did remove a few verbs at this stage.

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
