Inspired by the [spanish conjugation deck](https://www.asiteaboutnothing.net/w_ultimate_spanish_conjugation.php).

Download and generate the dictionary that softcatala uses.

```bash
git clone https://github.com/Softcatala/catalan-dict-tools.git
bash build-lt.sh
```

Get one verb to play with:
```bash
grep esquitxar diccionari.txt > esquitxar_example.txt
```

`dev.ipynb`

.apkg database format: https://github.com/ankidroid/Anki-Android/wiki/Database-Structure

Using the unzipped .anki21 file from the linked spanish conjucation deck

`get_spanish_verbs.ipynb`

Edit `spanish_verbs.tsv` to manually add the catalan translations

Format and choose catalan conjugations form the softcatala catalogue

`parse_cat_verbs.ipynb`

Create table with all new card content

`dev_sqlite.ipynb`


# Wishlist
* add treure because f that verdb (have jeure as a model but treure would def be more useful)
* add dur because also f that verb
* add haver-hi card (hi ha bla bla bla) (tagged in the kofi deck as "idiom")
* add past tense cards to help train the difference between passat perfet and passat perifrastic (ie by adding an avui, or aquest cap de setmana for simple or ahir, or l'any passat for the passat perifrastic)
