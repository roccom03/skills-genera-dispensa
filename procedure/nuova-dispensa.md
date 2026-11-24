# Come aggiungere una nuova materia

Questo file è **eseguibile**: contiene la procedura completa e il metodo di scrittura usato per la dispensa di Image Processing. Basta farlo eseguire a Claude Code e nasce la cartella della nuova dispensa.

## Come eseguirlo
1. Apri Claude Code **nella cartella della repo** (`skills-genera-dispensa/`).
2. Scrivi `/nuova-dispensa` (o `/nuova-dispensa Nome Materia`). Equivale a: «esegui `procedure/nuova-dispensa.md`».
3. Rispondi alle domande (sotto). Claude crea `corsi/<materia>/` e lavora per fasi.
4. Controlla il PDF e pubblica: `git add corsi/<materia> README.md && git commit && git push`.

---

# ISTRUZIONI PER CLAUDE (esegui in ordine)

## Passo −1 – Ambiente (prima di tutto)
Se manca Python o qualche strumento, esegui il flusso di `/prepara-ambiente`. Esegui **`procedure/ambiente.md`** (Passo A–C): `strumenti/controlla_ambiente.py` rileva da solo Linux/macOS/Windows e ti dice cosa manca. Usa il comando Python che indica al posto di `python3`, e su Windows lavora sui file con Python invece che con i comandi `cp`/`mkdir`.

## Passo −1b – Repo aggiornata (`git fetch`)
Esegui **`procedure/aggiorna-repo.md`** (sezione «All'inizio»): `git fetch origin`, controllo dei commit nuovi sul remoto e, se ce ne sono, integrazione con `git pull --rebase` (albero di lavoro pulito) **prima di scrivere**. Controlla anche che la materia non sia già stata creata altrove (cartella `corsi/<materia>/` arrivata dal remoto).

## Passo 0 – Domande (prima di fare qualsiasi altra cosa)
Chiedi, una alla volta o con `AskUserQuestion`:
1. **Nome della materia** (cartella in `kebab-case`) e **nome del docente**.
2. **Slide**: percorso del file o della cartella dei PDF (anche più file).
3. **Codici di partenza** (opzionale): MATLAB/Python, dataset, note del docente, tracce d'esame.
4. **Lingua**: italiano, inglese o entrambe.
5. **Libro di riferimento**, se i docenti dicono che le slide non bastano.
6. **Livello di partenza dello studente**, per calibrare il Capitolo 0.

Riassumi in 5 righe e **aspetta la conferma**.


### Controllo `.gitignore` (ogni volta)
Prima di copiare o leggere materiale del docente, apri `.gitignore` e assicurati che ci siano `**/materiali/` e `**/slide-da-tradurre/`, più ogni altra cartella/file con slide, appunti, trascrizioni o zip che l'utente ha indicato dentro la repo (aggiungi le righe mancanti). Verifica con `git check-ignore -v <percorso>` e `git status`; nel riepilogo finale elenca le righe aggiunte. In git vanno solo PDF, codici e ciò che serve ai comandi.

## Passo 1 – Crea la cartella
```
cp -r template/dispensa corsi/<materia>
mkdir corsi/<materia>/materiali      # copia qui slide e codici (la cartella è in .gitignore, non va su GitHub)
```
Sostituisci i segnaposto (`NOME-DISPENSA` in `latexmkrc`, titolo/corso/docente in `main.tex`, README della materia). Il preambolo in `template/dispensa/sorgenti/preambolo.tex` è quello di Image Processing: ambienti già pronti `esempio`, `attenzione`, `riquadro`, `prerequisiti`, `riassunto`, `definizione/teorema/proposizione/lemma/proprieta` (in riquadro), macro `\serve{}` e `\slidefig[larghezza]{pagina}{didascalia}{etichetta}`, listati MATLAB, `cleveref`. Non inventarne altri se bastano questi.

Albero finale:
```
corsi/<materia>/
├── README.md
├── <Nome-Dispensa>.pdf
├── materiali/                 # solo locale
└── sorgenti/
    ├── main.tex  preambolo.tex  latexmkrc  CHANGELOG.md
    ├── capitoli/  (000_prerequisiti.tex, 00_introduzione.tex, 01_….tex, …)
    ├── figure/    (immagini estratte/ritagliate dalle slide, grafici)
    └── codice/    (script, dati, processa_slide.py)
```

## Passo 2 – Mappa delle slide, a blocchi (obbligatoria, anche per poche slide)
La finestra di contesto è limitata: **non leggere mai più di un blocco di pagine alla volta** e non caricare i PDF interi. Usa `sorgenti/codice/processa_slide.py` (stato in `materiali/avanzamento.json`, fuori da git):
```
cd corsi/<materia>/sorgenti
python3 codice/processa_slide.py init ../materiali/slide.pdf|.pptx|.docx [altri ...] --blocco 10   # i file Office sono convertiti in automatico
python3 codice/processa_slide.py prossimo      # testo + immagini a bassa risoluzione del blocco
# ... scrivi il .tex di quel blocco ...
python3 codice/processa_slide.py fatto "argomento; file .tex scritto; punti dubbi"
```
Ripeti `prossimo` → scrivi → `fatto` **fino a «Tutti i blocchi sono completati»**, anche per 700 pagine (70 giri), senza chiedere conferma a ogni blocco. Regole:
- La nota di `fatto` deve bastare a riprendere il lavoro (argomento, file scritto, notazione/termini scelti, dubbi): `prossimo` ripropone le ultime 3 note.
- **Dopo un azzeramento del contesto** o all'inizio di una sessione: `stato`, poi `prossimo`. Non rifare i blocchi chiusi.
- Apri le immagini in `materiali/render/` solo per le pagine senza testo o con formule/schemi. Le build ripetute si contano una volta.
- `mappa` stampa la tabella *pagine → argomento* (ricostruiscila nel CHANGELOG).
- Se un argomento attraversa due blocchi, chiudi il primo con la nota «continua in…» e completa la sezione nel blocco successivo.

Il **Passo 3** (scrittura) avviene dentro lo stesso ciclo: un capitolo per blocco di slide, scritto subito dopo `prossimo`.

## Passo 3 – Metodo di scrittura (quello di Image Processing)
Un capitolo `.tex` per blocco di slide, **nell'ordine delle slide**. In ogni capitolo:
- **Riquadro `prerequisiti`** in apertura, con rimandi mirati al Capitolo 0 (`\S\ref{p:…}`).
- **Stile discorsivo**: spiega, non elencare. Niente frasi «da slide». Elenchi puntati solo per sequenze di passaggi o confronti. Termini chiave in `\textbf{}`, senza abusarne.
- **Ogni formula importante ha la sua dimostrazione** (ambiente `proof`), che in ripasso si può saltare; enunciati in `teorema`/`proposizione`/`lemma`/`definizione`, con `\label` e `\cref`.
- **Esempi numerici svolti in tutti i passaggi** (ambiente `esempio`), tipici da esame; `attenzione` per errori comuni e per punti in cui le slide usano convenzioni diverse; `riassunto` («In sintesi») a fondo capitolo.
- **Figure**: dalle slide con `\slidefig[larghezza]{file}{didascalia}{etichetta}` (permesso del docente per uso di studio, indica la fonte se esterna nella didascalia). `processa_slide.py prossimo` **estrae da solo** le immagini incorporate del blocco in `figure/` e le elenca; per quelle vettoriali o trasparenti usa `processa_slide.py ritaglia file.pdf PAGINA x0 y0 x1 y1` (coordinate in % della pagina). **Non saltare le figure**: ogni figura delle slide che serve alla comprensione va inclusa o ridisegnata. Le figure matematiche semplici (grafici, curve) in TikZ/pgfplots. Le formule contenute nei ritagli non restano immagini: coprile con `ritaglia ... --bianco X0 Y0 X1 Y1` (in % del ritaglio) e scrivile in LaTeX nel testo. Larghezza 0,5–0,85 della pagina: mai figure minuscole o tagliate.
- **Codice**: ogni script in `codice/`, incluso con `\lstinputlisting` e **spiegato** (cosa fa, cosa osservare, cosa variare). Se l'utente ha dato codici di partenza, usali come base e riportali nel testo. Non dichiarare «eseguito» ciò che non hai potuto eseguire.
- Se i docenti indicano libri di riferimento, citane i capitoli nel testo.
- Il testo va riscritto **con parole proprie**, non copiato dalle slide.

## Passo 4 – Capitolo 0 «Prerequisiti» (sempre in testa)
1. Elenca i concetti che il testo dà per scontati (matematica, segnali, fisica, statistica… secondo la materia).
2. Scrivi per ciascuno una **mini-lezione**, non un riassunto né un glossario:
   - *perché esiste* e a cosa serve;
   - spiegazione **passo-passo** partendo dalle basi, con linguaggio discorsivo;
   - **almeno un'analogia o un esempio svolto** per ogni concetto;
   - definizioni e formule in `\begin{riquadro}{…}`; sequenze di passaggi in elenchi;
   - in chiusura `\serve{…}`: «Perché ci serve in questo corso», con rimandi ai capitoli.
3. Ordina dal più elementare al più specifico; chiudi con una tabella *capitolo → prerequisiti*.
4. **Niente appendice di richiami duplicata**: dentro i capitoli i richiami vengono tolti e sostituiti da un rimando al Capitolo 0 (aggiungi al Cap. 0 ciò che mancava prima di togliere).

## Passo 5 – Integrazioni successive
Se l'utente fornisce slide aggiunte dopo: **non stravolgere** la struttura. Individua il punto esatto in cui ogni novità si inserisce, iniettala arricchendo il testo esistente senza cancellarne il nucleo, aggiungi i prerequisiti nuovi al Cap. 0 e registra tutto nel `CHANGELOG.md`. **Prima di riscrivere il testo, mostra un Changelog a punti**: (a) concetti inclusi nel Cap. 0; (b) capitoli/sezioni dove hai inserito le integrazioni e cosa.

## Passo 6 – Riordino cronologico
L'ordine di capitoli e sezioni deve ricalcare esattamente le slide; il Cap. 0 resta in testa. È **solo taglia-e-incolla**, senza riscrivere. Prima di spostare stampa un **«Piano di Riordino»** (capitoli attuali → nuova posizione, con le pagine di slide) e **aspetta la conferma**. Se una sezione non si può spostare senza spezzarla, segnalalo e lascia com'è.

## Passo 7 – Revisione tipografica per la stampa
Nessuna modifica al contenuto. Controlla:
- formule `\[…\]`, `equation`, `align` (mai `$$…$$`);
- figure `[htbp]` + `\centering` + larghezza ragionevole + `\caption` + `\label`;
- riquadri non spezzabili tra due pagine, titoli non isolati a fondo pagina (`\Needspace`), niente righe orfane;
- listati e tabelle entro i margini (righe lunghe a capo);
- spazio sopra/sotto i riquadri e tra titoli di paragrafo e riquadri.

**Verifica visiva di tutte le pagine**: `pdftoppm -r 55`, fogli di 8 pagine, e un controllo automatico dei margini con `pdftotext -bbox-layout`. Una figura tagliata o piccola si ritaglia di nuovo dalla slide originale. Resta un po' di bianco a fondo pagina quando un riquadro non entra: è normale, segnalalo.

## Passo 8 – Chiusura
1. `latexmk -pdf` senza errori né riferimenti mancanti; copia il PDF nella cartella della materia con il nome definitivo.
2. Aggiungi la riga alla tabella del `README.md` principale e compila il README della materia (link a PDF, sorgenti, script, `CHANGELOG.md`).
3. Dichiara cosa **non** hai potuto verificare (script senza toolbox, formule lette da immagini, ricostruzioni da confermare col docente).
4. Rifai `git fetch origin` (`procedure/aggiorna-repo.md`, sezione «Alla fine») e mostra `git status -sb`; se il remoto è avanti, integra e ricompila prima di proporre il commit. **Commit e push solo se l'utente lo chiede**; non chiedere mai token o password in chat.

## Regole sempre valide
- `materiali/` non va mai su GitHub (slide, note, tracce d'esame sono del docente; uso riservato agli iscritti). Avvisa che le figure estratte restano nel PDF: se la repo è pubblica, valuta di renderla privata.
- Non riscrivere testo già approvato quando fai riordino o impaginazione.
- Ogni `\label` mancante o `\cref` rotto è un errore da correggere.
- Un `CHANGELOG.md` per materia: concetti del Cap. 0, integrazioni, riordini, correzioni grafiche.
