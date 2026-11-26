# Come tradurre e riprogettare un pacco di slide

Questo file è **eseguibile**: contiene la procedura per ottenere, da un pacco di slide in lingua straniera, un nuovo PDF di slide **in italiano** con grafica rinnovata.

## Come eseguirlo
1. Apri Claude Code **nella cartella della repo**.
2. Scrivi `/traduci-slide` (o `/traduci-slide Nome Corso`).
3. Rispondi alle domande. Claude crea `corsi/<corso>/slide-<lingua>/` e lavora per fasi. Ogni pacco di slide dà un PDF a sé, chiamato come il titolo del pacco tradotto (es. `Tecniche-di-modulazione-digitale.pdf`); per aggiungere altri pacchi a un corso già fatto rilancia `/traduci-slide` (vedi «Aggiungere un pacco a un corso già fatto»).
4. Controlla il PDF e pubblica: `git add corsi/<corso> README.md && git commit && git push`.

Per una dispensa discorsiva (teoria, dimostrazioni, esempi) usa invece `/nuova-dispensa`.

---

# ISTRUZIONI PER CLAUDE (esegui in ordine)

## Passo −1 – Ambiente (prima di tutto)
Se manca Python o qualche strumento, esegui il flusso di `/prepara-ambiente`. Esegui **`procedure/ambiente.md`** (Passo A–C): `strumenti/controlla_ambiente.py` rileva da solo Linux/macOS/Windows e ti dice cosa manca. Usa il comando Python che indica al posto di `python3`, e su Windows lavora sui file con Python invece che con i comandi `cp`/`mkdir`.

## Passo −1b – Repo aggiornata (`git fetch`)
Esegui **`procedure/aggiorna-repo.md`** (sezione «All'inizio»): `git fetch origin`, controllo dei commit nuovi sul remoto e, se ce ne sono, integrazione con `git pull --rebase` (albero di lavoro pulito) **prima di scrivere**. Controlla anche che il pacco o il corso non siano già stati creati altrove (cartelle arrivate dal remoto).

## Passo 0 – Domande (prima di fare qualsiasi altra cosa)
Chiedi, una alla volta o con `AskUserQuestion`:
1. **Corso** (cartella in `kebab-case`; se esiste già, `slide-<lingua>/` va dentro) e **docente**.
2. **Slide**: percorso di file o cartella (PDF, PPTX, DOCX o altri formati Office). **Ogni file/pacco di slide è un pacco a sé** e produce un PDF a sé: se l'utente ne carica più d'uno, chiedi (o ricava dal frontespizio) il **titolo originale di ciascun pacco** e non unirli mai in un unico PDF, a meno che l'utente lo chieda esplicitamente. Più file che sono parti dello stesso pacco (es. «lezione 3a» e «3b») vanno uniti solo se l'utente lo conferma.
3. **Lingua di partenza** e **lingua richiesta** (default italiano; il codice, es. `it`, dà il nome della cartella `slide-it`).
4. **Stile grafico**, a scelta tra quelli in `template/slide/sorgenti/stili/`: **classico** (blu, sans), **sobrio** (grigio e bordeaux, serif; predefinito), **colorato** (verde acqua e arancio, barra del titolo piena), **accademico** (verde e oro, serif, striscia laterale). **topology** (grigio chiaro, blu notte e verde acqua, sans, fregi a diagonali: ispirato al tema Slidesgo «Topology»), **circuito** (fondo blu notte, testo chiaro, accenti ciano e viola, linee di circuito: ispirato a «Computer Science College Major», adatto a presentazioni più che a studio su carta). Mostra l'anteprima `template/slide/anteprima-stili.png` (con `SendUserFile`, se disponibile) e accetta anche ritocchi a colori e font o uno stile nuovo.
5. **Varianti di build** (stessa slide ripetuta con piccole aggiunte): accorparle in una slide o mantenerle.

Riassumi in 5 righe (elencando i pacchi e il nome del PDF di ciascuno) e **aspetta la conferma**.

### Nome dei pacchi e dei PDF
Il nome di ogni PDF è il **titolo originale (inglese) del pacco, tradotto nella lingua richiesta**: «Digital Modulation Techniques» → `Tecniche-di-modulazione-digitale.pdf`. Regole: parole separate da trattini, niente spazi né accenti né apostrofi (l'apostrofo diventa trattino: `Introduzione-all-Internet-of-Things`), maiuscola solo alla prima parola e ai nomi propri/sigle. Il titolo si legge dal frontespizio del pacco, non dal nome del file; se non c'è un titolo chiaro **chiedilo all'utente**. Lo slug della cartella delle sezioni è lo stesso nome in minuscolo (`tecniche-modulazione-digitale`).

### Controllo `.gitignore` (ogni volta)
Prima di copiare o leggere materiale del docente, apri `.gitignore` e assicurati che ci siano `**/materiali/` e `**/slide-da-tradurre/`, più ogni altra cartella/file con slide, appunti, trascrizioni o zip che l'utente ha indicato dentro la repo (aggiungi le righe mancanti). Verifica con `git check-ignore -v <percorso>` e `git status`; nel riepilogo finale elenca le righe aggiunte. In git vanno solo PDF, codici e ciò che serve ai comandi.

## Passo 1 – Crea la cartella
```
mkdir -p corsi/<corso>/slide-<lingua>
cp -r template/slide/sorgenti corsi/<corso>/slide-<lingua>/sorgenti      # solo se la cartella non esiste già
mkdir corsi/<corso>/slide-<lingua>/materiali      # slide originali (in .gitignore)
```
Imposta lo **stile scelto** nella riga `\input{stili/<stile>}` di `sorgenti/preambolo.tex` (uno stile per corso, uguale per tutti i pacchi; la cartella `stili/` resta nel corso per poterlo cambiare). Per **ogni pacco**: rinomina `sorgenti/Titolo-Pacco-Tradotto.tex` con il nome del pacco (`Nome-Del-Pacco.tex`: il PDF prende lo stesso nome, `latexmkrc` compila tutti i `.tex` della cartella tranne `preambolo.tex`), rinomina `sezioni/nome-pacco/` con lo slug e imposta titolo, corso, docente e anno nel `.tex`. Se il corso ha già dei pacchi, **copia** il `.tex` di un pacco esistente e crea una nuova cartella in `sezioni/`: `preambolo.tex`, `GLOSSARIO.md` e `codice/` sono comuni a tutti i pacchi e non si toccano. PPTX/PPT/ODP, DOC/DOCX/ODT/RTF e XLS/XLSX/ODS li converte da solo `processa_slide.py init` (serve LibreOffice; per Keynote `.key` chiedi all'utente di esportare in PDF).

## Passo 2 – Mappa e traduzione a blocchi (obbligatoria, anche per poche slide)
La finestra di contesto è limitata: **non leggere mai più di un blocco di pagine alla volta** e non caricare i PDF interi. Usa `sorgenti/codice/processa_slide.py` (stato in `materiali/avanzamento.json`, fuori da git):
```
cd corsi/<corso>/slide-<lingua>/sorgenti
python3 codice/processa_slide.py --pacco <slug> init ../materiali/slide.pdf --blocco 10
python3 codice/processa_slide.py --pacco <slug> prossimo      # testo + immagini a bassa risoluzione del blocco
# ... scrivi il .tex di quel blocco ...
python3 codice/processa_slide.py --pacco <slug> fatto "argomento; file .tex scritto; punti dubbi"
```
`--pacco <slug>` tiene uno stato separato per ogni pacco (`materiali/avanzamento-<slug>.json`): aggiungere un pacco nuovo **non** cancella né sovrascrive lo stato degli altri. Elabora i pacchi uno alla volta, ciascuno fino a «Tutti i blocchi sono completati». Con un solo pacco `--pacco` si può omettere. Nei comandi seguenti sottintendilo.
Ripeti `prossimo` → scrivi → `fatto` **fino a «Tutti i blocchi sono completati»**, anche per 700 pagine (70 giri), senza chiedere conferma a ogni blocco. Regole:
- La nota di `fatto` deve bastare a riprendere il lavoro (argomento, file scritto, notazione/termini scelti, dubbi): `prossimo` ripropone le ultime 3 note.
- **Dopo un azzeramento del contesto** o all'inizio di una sessione: `stato`, poi `prossimo`. Non rifare i blocchi chiusi.
- Apri le immagini in `materiali/render/` solo per le pagine senza testo o con formule/schemi. Le build ripetute si contano una volta.
- `mappa` stampa la tabella *pagine → argomento* (ricostruiscila nel CHANGELOG).
- Se un argomento attraversa due blocchi, chiudi il primo con la nota «continua in…» e completa la sezione nel blocco successivo.

Il **Passo 3** (traduzione) avviene dentro lo stesso ciclo: una sezione `.tex` per blocco, scritta subito dopo `prossimo`. Il glossario si aggiorna a ogni blocco; consultalo prima di tradurre, per restare coerente anche dopo un azzeramento del contesto.

## Passo 3 – Traduzione
Una sezione `sezioni/<slug-pacco>/NN_argomento.tex` per blocco (numerazione da 01 per ogni pacco) di slide, **nello stesso ordine delle originali**.
- Traduzione fedele nel contenuto, ma in italiano naturale e con parole proprie, non letterale.
- **Glossario** in `sorgenti/GLOSSARIO.md` (termine originale → italiano) e terminologia coerente in tutto il deck. Alla prima occorrenza il termine inglese va tra parentesi.
- **Non aggiungere né togliere contenuto**: niente dimostrazioni o esempi nuovi. Se una slide è ambigua o sbagliata, segnalalo in un commento `% NOTA:` e nel riepilogo finale.
- Formule sempre riscritte in LaTeX (mai come immagini).
- **Le figure vanno sempre portate nelle slide, mai saltate né sostituite da una descrizione a parole.** `processa_slide.py prossimo` estrae da solo le immagini incorporate delle pagine del blocco in `sorgenti/figure/` (esclusi loghi e icone ripetuti) e le elenca per pagina: includile con `\slidefig[larghezza]{figure/<file>}{Fonte: slide del corso, p.~N}` accanto al testo (`columns`) o su una slide a sé. Le figure **vettoriali** (nessuna immagine incorporata) o che appaiono nere perché trasparenti: `processa_slide.py ritaglia file.pdf PAGINA x0 y0 x1 y1` (coordinate in % della pagina, 220 dpi), poi apri il risultato e controlla che la figura sia **intera e leggibile**, altrimenti allarga il riquadro. **Le formule non restano mai come immagine**: se un ritaglio contiene formule (equazioni, mappature come «A₁ = +1,5», legende con R_b, T_s…) copri quelle zone di bianco con `--bianco X0 Y0 X1 Y1` (in % del ritaglio, serve Pillow) oppure ritaglia solo la parte di grafico, e scrivi le formule **in LaTeX** nel testo della slide o in una didascalia. Le etichette di assi e curve restano parte della figura.
- Ridisegna in TikZ (etichette in italiano) solo gli schemi semplici (poche scatole e frecce, grafici elementari) o quando la figura contiene testo da tradurre; tienine l'originale come ripiego. Se una figura con testo non tradotto resta com'è, segnalalo in `% NOTA:` e nel riepilogo. Solo se la figura è illeggibile alla massima risoluzione puoi descriverla a parole, e va detto nel riepilogo con il numero di pagina.
- Codice: i commenti si traducono, gli identificatori no.

## Passo 4 – Restyling
- Una idea per slide, niente muri di testo: se una slide originale è troppo fitta, dividila in due.
- `block` per definizioni e teoremi, `alertblock` per avvertenze, `columns` per testo accanto a figura.
- Stile solo in `preambolo.tex` e nei file di `stili/` (colori, font, footer). Non ripetere formattazioni dentro le sezioni. Per cambiare stile a un corso già fatto basta cambiare il nome nella riga `\input{stili/…}` e ricompilare, poi ricontrolla visivamente: i font con grazie occupano più spazio e qualche slide può richiedere un testo più piccolo o una divisione.
- Ogni sezione ha un titolo (`\section`) per l'indice.

## Passo 5 – Revisione
`latexmk -pdf` in `sorgenti/`: zero errori, zero riferimenti mancanti, zero *Overfull* rilevanti.
**Controllo figure**: per ogni pagina delle slide originali con una figura (elenco di `prossimo`, `pdfimages -list`, immagini di `materiali/render/`) verifica che la figura compaia nel PDF finale; riporta nel riepilogo quelle mancanti e il motivo.
**Verifica visiva di tutte le slide di ogni PDF**: `pdftoppm -r 40`, fogli da 12 slide (montaggio con `codice/` o Pillow). Controlla testo che esce dai margini o dal fondo della slide, figure tagliate o piccole, formule illeggibili. Un testo tagliato **non** passa mai la revisione: l'overfull verticale (`Overfull \vbox`) nei log di Beamer vuol dire che la slide non entra nel quadro, quindi dividila in due o riduci il contenuto (vedi Passo 4). Riconsegna solo dopo aver ricontrollato le slide corrette.

## Passo 6 – Chiusura
1. Copia **ogni** PDF in `corsi/<corso>/slide-<lingua>/` con il nome del pacco tradotto (uno per pacco, mai un file unico).
2. Aggiungi al `README.md` principale la riga del corso con un link per ogni PDF e crea/aggiorna il README breve della cartella (un elenco puntato: titolo originale → PDF).
3. Dichiara cosa **non** hai potuto verificare (figure con testo non tradotto, formule lette da immagini, punti dubbi delle slide).
4. Rifai `git fetch origin` (`procedure/aggiorna-repo.md`, sezione «Alla fine») e mostra `git status -sb`; se il remoto è avanti, integra e ricompila prima di proporre il commit. **Commit e push solo se l'utente lo chiede**.

## Aggiungere un pacco a un corso già fatto
Quando l'utente carica altri pacchi di slide per un corso che ha già `slide-<lingua>/`: **non** ricreare la cartella e **non** toccare i pacchi esistenti. Fai solo: nome del pacco (sopra) → Passo 1 «Per ogni pacco» → Passi 2–5 con `--pacco <slug>` → Passo 6 (nuovo PDF, nuova riga di README). Il glossario si estende, non si riscrive. Se una slide ripete contenuto di un altro pacco, traducila comunque ma segnalalo con `% NOTA:`.

## Regole sempre valide
- `materiali/` non va mai su GitHub.
- Le slide appartengono al docente: uso di studio riservato agli iscritti; indica la fonte nel frontespizio.
- Non riscrivere testo già approvato quando fai correzioni grafiche.
