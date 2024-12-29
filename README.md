Inspired by the [spanish conjugation deck](https://www.asiteaboutnothing.net/w_ultimate_spanish_conjugation.php).

Download and generate the dictionary that softcatala uses.

```bash
git clone https://github.com/Softcatala/catalan-dict-tools.git
bash build-lt.sh
```

Get one verb to play with:
```bash
grep esquitxar /Users/fairliereese/Documents/catala/catalan-dict-tools/resultats/lt/diccionari.txt > esquitxar_example.txt
```

`dev.ipynb`

.apkg database format: https://github.com/ankidroid/Anki-Android/wiki/Database-Structure

Using the unzipped .anki21 file from the linked spanish conjucation deck

`dev_sqlite.py`
