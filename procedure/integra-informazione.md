# Come verificare e correggere una lezione già scritta

Questo file è **eseguibile**: quando per una lezione hai **nuove fonti** (slide, appunti, trascrizione, libro, articoli: a mano o digitali), Claude **confronta la dispensa già scritta con le nuove fonti**, cerca **informazioni mancanti** ed **errori** e **corregge la dispensa**.

## Come eseguirlo
1. Apri Claude Code nella cartella della repo (o usa il comando globale, vedi `README.md`).
2. Scrivi `/integra-informazione` (o `/integra-informazione Nome Corso`).
3. Indica quale lezione/capitolo e dove sono le nuove fonti; rispondi alle domande.
4. Leggi il rapporto di verifica, controlla il PDF e pubblica: `git add corsi/<corso> && git commit && git push`.

Per **aggiungere** una lezione nuova usa `/aggiungi-lezione`; qui si lavora su un capitolo che esiste già.

---

# ISTRUZIONI PER CLAUDE (esegui in ordine)

## Ruolo
Agisci da **professore universitario esperto** (verifichi correttezza e completezza) e da **tipografo LaTeX** (modifichi con interventi minimi, senza stravolgere la dispensa).

## Passo −1 – Ambiente
Esegui `procedure/ambiente.md` (Passo A–C) e `strumenti/controlla_ambiente.py`. Usa il comando Python che indica; su Windows niente `cp`/`mkdir -p`.

## Passo −1b – Repo aggiornata (`git fetch`)
Esegui **`procedure/aggiorna-repo.md`** (sezione «All'inizio»): `git fetch origin`, controllo dei commit nuovi sul remoto e, se ce ne sono, integrazione con `git pull --rebase` (albero di lavoro pulito) **prima di scrivere**. Dopo l'integrazione rileggi i capitoli da verificare (Passo 1): potrebbero essere stati modificati altrove.

## Passo 0 – Domande (prima di toccare qualsiasi file)
Chiedi, una alla volta o con `AskUserQuestion`:
1. **Corso** e **capitolo/lezione** da verificare (se non lo sa, mostra l'elenco dei capitoli di `main.tex` e fai scegliere; può essere più di uno).
2. **Nuove fonti**: tipo (slide, appunti, trascrizione, libro, articolo), percorso di file o cartella, e se sono **a mano** (foto, scansioni) o **digitali**.
3. **Affidabilità** delle fonti, se non è ovvia (di norma: libro/articolo e slide del docente > spiegazione del docente > appunti personali; una trascrizione è la più soggetta a errori di ascolto).
4. **Che cosa fare dei dubbi**: di default le correzioni **certe** e le aggiunte si applicano subito, i punti **dubbi o in conflitto** si segnalano senza toccare il testo (puoi cambiare idea).

Riassumi in 5 righe e **aspetta la conferma**. Copia le nuove fonti in `corsi/<corso>/materiali/lezioni/<NN-argomento>/verifica-<AAAA-MM-GG>/` (in `.gitignore`).

## Passo 1 – Cosa c'è già nella dispensa
- Leggi il capitolo da verificare **a sezioni** (mai più di ~10 pagine di PDF o ~300 righe di `.tex` alla volta) e prepara un **elenco dei concetti** già trattati: definizioni, formule, valori numerici, esempi, figure, con la sezione in cui compaiono.
- Leggi `CHANGELOG.md` e, se esistono, le vecchie letture `lettura-*.md` in `materiali/lezioni/<NN-argomento>/`: ti dicono da quali fonti nasce il testo, così non le rileggi.
- Se il capitolo rimanda ad altri (`\cref`), leggi solo i titoli e i punti citati.

## Passo 2 – Lettura delle nuove fonti (a blocchi)
Come in `procedure/aggiungi-lezione.md` Passo 2: **non leggere mai più di un blocco alla volta**.
- Slide e documenti con pagine: `codice/processa_slide.py --pacco verifica-<AAAA-MM-GG> init|prossimo|fatto` (blocchi da ~10 pagine).
- Testo digitale: pezzi di ~300 righe.
- Scritto a mano: **4–5 immagini o pagine alla volta**, a risoluzione leggibile (`pdftoppm -r 110`). Grafia incerta: segna `[?]`, non indovinare in silenzio.
- Dopo ogni blocco scrivi la lettura in `verifica-<AAAA-MM-GG>/lettura-<fonte>.md` (testo ricopiato, formule in LaTeX): dopo un azzeramento del contesto riparti dall'ultimo blocco scritto.

## Passo 3 – Confronto
Per **ogni** concetto delle nuove fonti confrontalo con l'elenco del Passo 1 e assegna uno stato:
- **Corretto e completo**: nessuna azione.
- **Mancante**: non compare nella dispensa.
- **Incompleto**: compare ma senza condizioni, passaggi, casi o esempi che le fonti danno.
- **Errato**: la dispensa dice una cosa diversa e le fonti (o un calcolo) mostrano che è sbagliata. Controlla **formule** (rifai i passaggi, coerenza dimensionale, segni, casi limite), **valori numerici**, **definizioni**, **notazione**, **unità**.
- **Conflitto**: le fonti nuove contraddicono la dispensa ma non è chiaro chi abbia ragione (es. appunti contro slide).
- **Non verificabile**: la fonte è illeggibile o ambigua.
Verifica anche il verso opposto: ciò che la dispensa afferma e **nessuna fonte conferma** va segnalato come «non confermato», non cancellato.

## Passo 4 – Rapporto di verifica (prima di modificare)
Mostra all'utente un **rapporto a punti**, e salvalo in `corsi/<corso>/sorgenti/CHANGELOG.md` alla fine del lavoro:
1. **Errori trovati** (sezione, cosa dice la dispensa, cosa dicono le fonti, correzione proposta).
2. **Informazioni mancanti o incomplete** (cosa aggiungere e dove).
3. **Conflitti e dubbi** (le due versioni, la fonte di ciascuna, la tua raccomandazione).
4. **Non confermato** e **non verificabile**.
Dichiara quanti punti applicherai subito e quali no. Non aspettare conferma per le correzioni **certe** e le aggiunte, a meno che l'utente l'abbia chiesto nel Passo 0; per i punti dubbi chiedi.

## Passo 5 – Correzioni (interventi minimi)
- **Errori**: cambia **solo** l'affermazione sbagliata (formula, valore, parola), lasciando struttura, stile e `\label` intatti. Se un errore si propaga (una formula usata più avanti), correggi tutte le occorrenze e controlla i `\cref`.
- **Mancanze**: inserisci il testo nel **punto logico** (sezione, sottosezione) con lo stile della dispensa (box `riquadro`, `esempio`, `attenzione`, `riassunto` dove servono; elenchi e `\textbf` per le parole chiave). Se serve una sezione nuova, tienila corta e collegala con `\cref`.
- **Formule sempre in LaTeX** (`equation` o `$…$`), mai come immagine; **figure** delle fonti portate secondo la regola in `CLAUDE.md` (`processa_slide.py prossimo` / `ritaglia ... --bianco`), oppure cercate e scaricate con fonte e licenza come in `procedure/aggiungi-lezione.md` Passo 5.
- **Dubbi e conflitti**: non toccare il testo; aggiungi un commento `% NOTA: …` accanto al punto con le due versioni e la fonte di ciascuna.
- **Non riscrivere** testo corretto, né riordinare o riformulare per gusto: la dispensa è già approvata.
- Registra ogni modifica nel `CHANGELOG.md` (data, fonte, sezione, «corretto: …» / «aggiunto: …»).

## Passo 6 – Revisione
1. `latexmk -pdf` in `sorgenti/`: zero errori, zero riferimenti mancanti, zero *Overfull* rilevanti.
2. **Verifica visiva** delle sole pagine toccate (`pdftoppm -r 40`): testo tagliato, figure fuori pagina, formule illeggibili, box spezzati male.
3. **Rilettura di completezza**: ripassa le tue `lettura-*.md` e controlla che ogni punto marcato «mancante» o «errato» sia ora risolto nel capitolo.

## Passo 7 – Chiusura
1. Copia il PDF nella cartella del corso con il nome definitivo.
2. **Riepilogo finale**: errori corretti, aggiunte fatte, punti ancora dubbi (con la domanda da porre al docente o all'utente), figure aggiunte, ciò che non hai potuto verificare.
3. Rifai `git fetch origin` (`procedure/aggiorna-repo.md`, sezione «Alla fine») e mostra `git status -sb`; se il remoto è avanti, integra e ricompila prima di proporre il commit. **Commit e push solo se l'utente lo chiede.**

## Regole sempre valide
- `materiali/` non va mai su GitHub (le fonti sono personali o del docente).
- Mai correggere «a intuito»: ogni modifica ha una fonte o una verifica esplicita nel rapporto.
- Non riscrivere testo già approvato; le correzioni sono locali e tracciate nel `CHANGELOG.md`.
