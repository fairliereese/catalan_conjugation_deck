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

## Obtenint les formes verbals catalanes

A continuació, necessitava una llista de totes les formes verbals catalanes i metadades de cadascuna. Les comunitats de catalanoparlants i aprenents de català tenen molta sort de disposar del [recurs de Softcatalà](https://www.softcatala.org/), incloent-hi un [conjugador de verbs](https://www.softcatala.org/conjugador-de-verbs/). Tenen una pila d'eines computationals que li donen suport a aquest recurs al seu [GitHub](https://github.com/Softcatala/catalan-dict-tools/).

Vaig obtenir el diccionari sencer de Softcatalà fent servir les seves eines.
```bash
git clone https://github.com/Softcatala/catalan-dict-tools.git
cd catalan-dict-tools
bash build-lt.sh
```

Això farà el fitxer `diccionari.txt`, el qual incloc en aquest repo.

Després, vaig analitzar els codis del diccionari Softcatalà per adquirir la informació de la forma per cada verb conjugat. Basat en allò que necessitava, havia de prendre algunes decisions sobre quines d'agafar-ne i quines d'eliminar.

* Mantenir només les conjugacions centrals (eliminar les valencianes i balears)
* Eliminar les conjugacions de passat simple i substituir-les amb el passat perifràstic
* Afegir les formes imperatives negatives (les quals només són del subjuntiu present)
* D'aquí, hi havia uns quants verbs amb diverses formes vàlides, triar-ne una

```bash
python parse_catalan_verbs.py
```

Això crea la taula `catalan_verbs_parsed.tsv`.

## Traduint les frases de context

Cada carta disposa de frases per afegir context al verb, les quals també calia traduir a català. Vaig dividir les notes a cada carta castellana fent servir uns quants delimitadors i després traduir-les de castellà a català.

```bash
python get_spanish_context_phrases.py
```

Això genera el fitxer `spanish_context_phrases.tsv`, i les traduccions (també amb traduccions dels pronoms [per exemple tú->tu; yo->jo]) són al fitxer `spanish_catalan_context_phrases.csv`.

Aquest part és la més probable d'haver introduït uns errors difícils de trobar. Si en veus algun si us plau avisa'm o obri un issue en [aquest GitHub repo](https://github.com/fairliereese/catalan_conjugation_deck).

## Construïnt la taula final

Vaig fer servir els tags de la baralla de cartes de conjugació castellana que va definir les formes verbals per unir-les amb les equivalents de català. Vaig afegir tags per les terminacions verbals, les formes verbals, i l'infinitiu per a cada carta. Per fi, vaig substituir el text castellà (incloent-hi les frases de context, l'infinitiu i la forma conjugada) amb l'equivalent català.


```bash
python get_anki_table.py
```

Això fa el fitxer `table_to_make_cards.csv`. L'única cosa que ens queda és afegir les cartes a Anki!

## Les cartes finals i recomanacions

El fitxer `.apkg` fitxer es pot descarregar [aquí](https://github.com/fairliereese/catalan_conjugation_deck/blob/main/catal%C3%A0_conjugaci%C3%B3.apkg) del GitHub repo. L'autor original de la baralla de cartes castellana va fer molta feina per fer un [manual](https://www.asiteaboutnothing.net/w_ultimate_spanish_conjugation.php#how) sobre com s'hauria de fer servir les cartes de manera efectiva, i us recomano llegir-lo abans d'estudiar.

## Llista de desitjos

Hi queden unes quantes coses que m'agradarien afegir al futur:
* Per a formes amb unes quantes conjugacions vàlides, mostrar-ne totes com a respostes
* Afegir-hi `treure` en lloc de `jeure`
* Afegir-hi `dur`
* Afegir-hi `haver-hi`
* Afegir cartes de la forma passat perfet per ajudar de practicar la diferència entre el passat perfet i passat perifràstic, com que les distincions són diferents que són en l'anglès o el castellà de Amèrica Llatina (per exemple, afegir paraules claus `avui` / `aquest cap de setmana` vs. `ahir` / `l'any passat`)

Altre cop, si veus algun error, com que tota aquesta feina vaig fer sistemàticament, si us plau avisa'm i intentaré fer una actualització.

(Gràcies a les eines de Softcatalà per ajudar-me corregir aquest text)
