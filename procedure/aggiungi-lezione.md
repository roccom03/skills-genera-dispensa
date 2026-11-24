# Come aggiungere una lezione a una dispensa

Questo file è **eseguibile**: unisce le fonti di una lezione in un capitolo LaTeX ben organizzato e lo aggiunge alla dispensa del corso (creandola se non esiste). Le fonti possono essere **qualsiasi combinazione** di: **slide** della lezione (PDF, PPTX, DOCX…), **appunti** e **trascrizione** della lezione, questi ultimi **scritti a mano** (foto, scansioni, PDF di scansioni) oppure **digitali** (testo, DOCX, PDF con testo), oppure una **registrazione audio/video** della lezione (in questo caso la trascrizione la fai tu con whisper, vedi Passo 2). Ne basta una; più sono, più la sintesi è completa.

## Come eseguirlo
1. Apri Claude Code nella cartella della repo (o usa il comando globale, vedi `README.md`).
2. Scrivi `/aggiungi-lezione` (o `/aggiungi-lezione Nome Corso`).
3. Indica dove sono appunti e trascrizione e rispondi alle domande.
4. Controlla il PDF e pubblica: `git add corsi/<corso> && git commit && git push`.

---

# ISTRUZIONI PER CLAUDE (esegui in ordine)

## Ruolo
Agisci da **professore universitario esperto** e da **tipografo professionista in LaTeX**: l'obiettivo è una dispensa di studio perfetta, chiara e accademica.

## Passo −1 – Ambiente
Esegui `procedure/ambiente.md` (Passo A–C) e `strumenti/controlla_ambiente.py`. Usa il comando Python che indica; su Windows niente `cp`/`mkdir -p`.

## Passo −1b – Repo aggiornata (`git fetch`)
Esegui **`procedure/aggiorna-repo.md`** (sezione «All'inizio»): `git fetch origin`, controllo dei commit nuovi sul remoto e, se ce ne sono, integrazione con `git pull --rebase` (albero di lavoro pulito) **prima di scrivere**. Dopo l'integrazione rileggi indice e titoli dei capitoli (Passo 1): la lezione potrebbe essere già in dispensa e la numerazione dei capitoli potrebbe essere cambiata.

## Passo 0 – Domande (prima di scrivere)
Chiedi, una alla volta o con `AskUserQuestion`:
1. **Corso** (cartella `corsi/<corso>/`; se esiste già `sorgenti/main.tex` si **aggiorna** la dispensa, altrimenti si crea) e **argomento/titolo** della lezione.
2. **Data** della lezione.
3. **Quali fonti hai** (almeno una) e dove sono: **slide**, **appunti**, **trascrizione**, oppure una **registrazione audio/video**. Per ognuna: percorso di file o cartella e se è **a mano** (foto JPG/PNG/HEIC, PDF di scansioni), **digitale** (testo, DOCX, PDF con testo, slide) o una **registrazione** (in quel caso chiedi anche la lingua/le lingue parlate dal docente, per impostare whisper).
5. Solo se la dispensa va creata: titolo, docente, anno accademico.

Riassumi in 5 righe e **aspetta la conferma**. Elenca le fonti che userai. Copia i file originali in `corsi/<corso>/materiali/lezioni/<NN-argomento>/` (in `.gitignore`).


### Controllo `.gitignore` (ogni volta)
Prima di copiare o leggere materiale del docente, apri `.gitignore` e assicurati che ci siano `**/materiali/` e `**/slide-da-tradurre/`, più ogni altra cartella/file con slide, appunti, trascrizioni o zip che l'utente ha indicato dentro la repo (aggiungi le righe mancanti). Verifica con `git check-ignore -v <percorso>` e `git status`; nel riepilogo finale elenca le righe aggiunte. In git vanno solo PDF, codici e ciò che serve ai comandi.

## Passo 1 – Dispensa nuova o esistente
- **Nuova**: copia `template/dispensa/sorgenti` in `corsi/<corso>/sorgenti/`, imposta titolo/docente/anno in `main.tex` e `NOME-DISPENSA` in `latexmkrc`, elimina i capitoli segnaposto (`000_prerequisiti`, `00_introduzione`, `01_primo_argomento`) e le relative `\include`.
- **Esistente**: leggi `main.tex`, l'elenco dei capitoli e i **titoli di capitoli e sezioni** (non rileggere interi i capitoli) e il `CHANGELOG.md`. Se `preambolo.tex` non ha la macro `\figuralezione`, copiala dal template (fine di `template/dispensa/sorgenti/preambolo.tex`).

## Passo 2 – Lettura delle fonti (a blocchi)
La finestra di contesto è limitata: **non leggere mai più di un blocco alla volta**. Leggi ogni fonte con il metodo adatto:
- **Slide** (e documenti digitali con pagine): `codice/processa_slide.py --pacco <NN-argomento> init|prossimo|fatto` (blocchi da ~10 pagine, stato in `materiali/avanzamento-<NN-argomento>.json`, come in `procedure/traduci-slide.md` Passo 2). Per ogni blocco scrivi la lettura in `lettura-slide.md` (punti chiave, formule in LaTeX, figure da riprodurre) e chiudi con `fatto`. Se `sorgenti/codice/` non c'è, copialo da `template/dispensa/sorgenti/codice/`.
- **Trascrizione digitale** (`.txt`/`.docx`/PDF con testo, di solito **rumorosa**, cioè da riconoscimento vocale): **prima di tutto** crea il file della lezione pulita (vedi «Passo 2a»). Non la sintetizzi mai direttamente dal testo grezzo.
- **Registrazione audio o video** (nessuna trascrizione pronta): la trascrivi tu con **whisper** (`whisper`, installato in un ambiente dedicato) prima di qualunque altro passo.
  1. Copia la registrazione in `corsi/<corso>/materiali/lezioni/<NN-argomento>/` (**mai** lasciarla solo nello scratchpad: una pulizia di `/tmp` o un riavvio la cancella insieme a tutto l'output di whisper già pronto).
  2. Se è un video, estrai prima l'audio con `ffmpeg -i video.ext -vn -ac 1 -ar 16000 -c:a pcm_s16le audio.wav` (più leggero e veloce da processare). **Non limitarti all'audio**: le immagini mostrate nel video (slide condivise, demo dal vivo, schemi disegnati, oggetti ripresi dalla telecamera) sono fonte a tutti gli effetti e vanno portate in dispensa come le figure delle slide (vedi «Figure» nelle regole sempre valide del `CLAUDE.md` del progetto).
     - Estrai i fotogrammi ai cambi di scena, non ogni frame: `ffmpeg -i video.ext -vf "select='gt(scene,0.12)',showinfo" -vsync vfr -q:v 1 frames/frame_%04d.png` (regola la soglia se escono troppi/pochi frame).
     - Se sono molti, **non aprirli uno a uno**: costruisci dei fogli di contatto (griglie di miniature numerate, con Pillow) per scorrerli velocemente e scegliere solo quelli utili.
     - **Scarta** i fotogrammi senza contenuto didattico: schermate di videoconferenza con griglia dei partecipanti, webcam di volti (docente o studenti), interfacce di sistema irrilevanti. Se la lezione è su una piattaforma di videoconferenza (Teams, Zoom, Meet...) e un fotogramma utile include comunque la cornice dell'app (barra dei partecipanti, nomi, webcam), **ritaglialo** per tenere solo il contenuto (con uno script Python/Pillow locale, non online): nomi e volti di persone terze non vanno mai in dispensa.
     - Associa ogni fotogramma scelto al punto della trascrizione/lezione pulita a cui si riferisce (annotalo in `lezione-pulita.md`), così la sintesi (Passo 3) sa dove inserirlo con `\figuralezione` e la didascalia giusta.
  3. Lancia whisper **in background** (`run_in_background`, mai in foreground: su CPU, senza GPU, un'ora di lezione richiede indicativamente 1–2 ore) con output nella **stessa cartella della repo**, non in `/tmp`: `whisper audio.wav --model medium --task transcribe --output_dir corsi/<corso>/materiali/lezioni/<NN-argomento>/whisper-raw --output_format all --fp16 False --verbose False`. Modello `medium` di norma; sali a `large-v3` solo se la qualità non basta (più lento).
  4. **Lingua**: se il docente parla una sola lingua, impostala con `--language`; se mescola più lingue (es. italiano/inglese/dialetto), **non forzare `--language`** e lascia il rilevamento automatico, avvisando che il testo richiederà più pulizia manuale nei tratti in lingua diversa da quella principale.
  5. Mentre whisper gira **non restare bloccato ad aspettare**: continua con le altre fonti disponibili (appunti, slide) o altro lavoro richiesto; se l'utente chiede un controllo di avanzamento, leggi l'output del task in background. Su richiesta esplicita dell'utente puoi anche avviare un controllo automatico periodico (ogni 10 minuti) che scrive lo stato in un file di log nella stessa cartella della repo.
  6. A fine trascrizione tratta l'output come una **trascrizione digitale rumorosa**: crea comunque `lezione-pulita.md` (Passo 2a) prima di qualsiasi sintesi.
- **Altro testo digitale** (appunti `.txt`/`.docx`/PDF con testo): leggi a pezzi di ~300 righe e ricopia in `lettura-appunti.md` solo ciò che serve alla sintesi.
- **Scritto a mano** (appunti, trascrizione): al massimo **4–5 immagini/pagine alla volta**, come sotto.
- Per i PDF: `pdftoppm -r 110 -png -f A -l B file.pdf materiali/render/p` e apri le immagini (a 60 dpi la grafia non è leggibile). Per le foto: aprile direttamente.
- Dopo ogni blocco **scrivi la lettura grezza** in `corsi/<corso>/materiali/lezioni/<NN-argomento>/lettura-appunti.md` e `lettura-trascrizione.md` (testo ricopiato, formule in LaTeX), uno per fonte, poi passa al blocco successivo. Dopo un azzeramento del contesto (`stato`, poi `prossimo`) riparti dall'ultimo blocco scritto, senza rileggere i precedenti.
- **Grafia incerta**: non indovinare in silenzio. Segna la parola o la formula dubbia con `[?]` nella lettura e con `% NOTA: lettura incerta` nel `.tex`; elenca tutti i punti incerti nel riepilogo finale. Per le formule controlla la coerenza dimensionale e con il resto della lezione.
- Disegni e schemi a mano: descrivili nella lettura (cosa mostrano, etichette) per poterli ridisegnare o cercare un'immagine equivalente.

## Passo 2a – Pulizia della trascrizione (prima di tutto il resto)
Per **ogni lezione con trascrizione** crea, **prima** della sintesi e di qualunque altro passo sul contenuto, un file di **lezione pulita**: `corsi/<corso>/materiali/lezioni/<NN-argomento>/lezione-pulita.md` (uno per lezione, es. `Lezione1.txt` → `01-…/lezione-pulita.md`). Lavora a pezzi di ~300 righe, scrivendo il file in modo incrementale (stato: riprendi dall'ultimo pezzo scritto dopo un azzeramento del contesto) e usa le slide della lezione (se presenti) per correggere termini tecnici, sigle e nomi.
- **Elimina il rumore**: intercalari e false partenze («ehm», «cioè», «allora», ripetizioni), frasi interrotte o ripetute, saluti, appelli, questioni organizzative (esami, orari, audio, microfono), battute, chiacchiere e digressioni **che non c'entrano con il contesto** della lezione, domande e risposte fuori tema.
- **Correggi gli errori di trascrizione**: parole sentite male, termini tecnici storpiati, sigle e nomi propri (controllali con le slide), punteggiatura e frasi spezzate male. Se una parola resta ambigua, **non indovinare in silenzio**: segnala `[?]`.
- **Conserva tutto il contenuto didattico**: spiegazioni, definizioni, esempi, numeri, formule (in LaTeX), aneddoti utili a capire, risposte del docente alle domande pertinenti, indicazioni su cosa è importante per l'esame. Non aggiungere nulla che il docente non abbia detto e non riassumere: il file resta il parlato, ripulito e ben scritto in italiano (se la lezione è in un'altra lingua, mantieni la lingua originale; la traduzione è del Passo 3).
- Dove il docente rimanda a una slide, indica il riferimento (`[slide N]`) quando è chiaro.
- Organizza il testo in paragrafi e, dove il discorso cambia argomento, con intestazioni `##` che seguono la lezione.
- Alla fine di ogni file elenca, in coda, i **tagli sostanziali** (cosa è stato scartato e perché, in una riga ciascuno) e i punti con `[?]`.
**Aspetta il via dell'utente** sui file puliti (mostra un breve riepilogo: righe prima/dopo, tagli, punti incerti) prima di passare al Passo 3. Da qui in avanti la «trascrizione» è **solo** `lezione-pulita.md`; il file grezzo non si rilegge più.

## Passo 3 – Sintesi e rielaborazione
Con le **slide** come base e la **lezione pulita** (Passo 2a)/gli appunti come spiegazione, il capitolo segue l'ordine logico della lezione; le figure delle slide **vanno portate nel capitolo**: `processa_slide.py prossimo` le estrae in `figure/` (per quelle vettoriali usa `processa_slide.py ritaglia`) e si includono con `\slidefig` (con la fonte) invece di cercarne altre su Internet.
**Solo trascrizione (niente slide)**: la struttura del capitolo la dà la `lezione-pulita.md` (le intestazioni `##` diventano `\section`); poiché non ci sono slide per verificare termini e sigle, controllali con la dispensa esistente e, se serve, con una ricerca web, segnando `[?]` ciò che resta dubbio. Le figure non arrivano dalle slide: per ciò che il docente descrive o disegna a parole applica il Passo 5 (ricerca immagini con fonte e licenza). Non inventare contenuti per "completare" ciò che le slide avrebbero contenuto: se la lezione è lacunosa, segnalalo nel riepilogo.
Unisci tutte le fonti disponibili (slide, appunti, trascrizione) in un unico testo:
- elimina le ripetizioni, correggi gli errori tipici del parlato, riorganizza in un flusso **logico, chiaro e accademico**;
- **non omettere nessun concetto fondamentale** di nessuna fonte; se le fonti si contraddicono (es. slide e parlato del docente: di norma vale ciò che dice la lezione, ma segnalalo), segnalalo con `% NOTA:` senza scegliere in silenzio;
- se la lezione ripete concetti già presenti nella dispensa, **non ripeterli**: rimanda alla sezione con `\cref` (aggiungi la `\label` mancante senza modificare il testo).

## Passo 4 – Scrittura LaTeX
Un file `capitoli/NN_argomento.tex` per lezione (numerazione progressiva), con **`\chapter`** per la lezione e sotto `\section`, `\subsection`, `\subsubsection` per gerarchizzare.
- `itemize` ed `enumerate` per facilitare lo studio; **`\textbf`** per parole chiave e definizioni; box dell'ambiente del template (`riquadro`, `esempio`, `attenzione`, `riassunto`) dove servono. Chiudi il capitolo con `riassunto`.
- Formule: `equation` (o `\[ \]`) per le formule display, `$…$` per quelle inline; mai come immagini.
- Aggiungi `\include{capitoli/NN_argomento}` in `main.tex` nel punto corretto. Se la lezione **amplia o corregge** un capitolo già scritto, applica il Passo 5 di `procedure/nuova-dispensa.md` (Changelog a punti prima di toccare il testo esistente, niente cancellazioni del nucleo).
- Registra tutto nel `CHANGELOG.md` (data, lezione, capitoli/sezioni toccati).

## Passo 5 – Immagini (le cerca Claude)
Quando la spiegazione trarrebbe forte beneficio da un'immagine, uno schema o un grafico:
1. **Cerca** con `WebSearch` (preferisci Wikimedia Commons e fonti con licenza libera: CC0, CC BY, CC BY-SA, pubblico dominio) e **scarica** il file in `corsi/<corso>/sorgenti/figure/` con nome descrittivo (es. `domanda_offerta_equilibrio.png`), con `curl` (o `WebFetch`). Non usare link remoti.
2. **Verifica** che il file sia davvero un'immagine (`file`) e **aprilo** per controllare che mostri ciò che serve e sia leggibile.
3. Inseriscila con `\figuralezione[0.8]{nome-file.png}{didascalia dettagliata che spiega il concetto illustrato}{fig:etichetta}`, con in `\caption` anche la fonte, e aggiungi sopra il commento `% IMMAGINE: ricerca «…» – URL – autore – licenza`.
4. Registra file, URL, autore e licenza in `sorgenti/figure/FONTI.md`.
5. **Se non trovi nulla di adatto**, la licenza non è chiara o la rete è bloccata: per schemi semplici ridisegna in TikZ/PGFPlots; altrimenti lascia `\figuralezione` con il nome del file mancante (il PDF mostra un riquadro) e il commento `% SUGGERIMENTO RICERCA IMMAGINE: [cosa cercare su Google Immagini o Pinterest]`. Elenca questi casi nel riepilogo.
Non inserire immagini con licenza non libera o non verificabile.

## Passo 6 – Revisione
1. `latexmk -pdf` in `sorgenti/`: zero errori, zero riferimenti mancanti (`\ref`/`\cref`), zero *Overfull* rilevanti. Se la lezione è nuova per la dispensa, controlla anche indice e numerazione.
2. **Verifica visiva** delle pagine nuove (`pdftoppm -r 40`, fogli da 12): testo tagliato, figure fuori pagina, formule illeggibili, box spezzati male. Correggi e ricontrolla.
3. **Controllo di completezza**: rileggi le tue `lettura-*.md` (slide, appunti) e `lezione-pulita.md` (trascrizione) e verifica che ogni concetto compaia nel capitolo.

## Passo 7 – Chiusura
1. Copia il PDF nella cartella del corso con il nome definitivo; aggiorna il `README.md` della materia (e la riga del `README.md` principale se è nuova).
2. **Riepilogo**: capitolo aggiunto, concetti già presenti richiamati con `\cref`, immagini inserite (con licenze), immagini da trovare a mano, punti di grafia incerti, contraddizioni tra le fonti.
3. Mostra il **codice LaTeX** del nuovo capitolo in un unico blocco per il copia-incolla, se l'utente lo chiede.
4. Rifai `git fetch origin` (`procedure/aggiorna-repo.md`, sezione «Alla fine») e mostra `git status -sb`; se il remoto è avanti, integra e ricompila prima di proporre il commit. **Commit e push solo se l'utente lo chiede.**

## Regole sempre valide
- `materiali/` non va mai su GitHub (slide, appunti e trascrizioni sono personali o del docente; le immagini originali restano fuori).
- Non riscrivere testo già approvato quando integri o impagini.
- Ogni `\label` mancante o `\cref` rotto è un errore.
