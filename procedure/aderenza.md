# Come allineare una dispensa alla struttura delle slide

Questo file è **eseguibile**: dato un pacco di **slide ufficiali** e una **dispensa già scritta**, Claude confronta gli indici, **riordina la dispensa** secondo le slide, trova ciò che **manca** e ciò che c'è **in più**, e dopo la tua conferma **integra** le parti mancanti marcando solo gli extra.

## Come eseguirlo
1. Apri Claude Code nella cartella della repo (o usa il comando globale, vedi `README.md`).
2. Scrivi `/aderenza` (o `/aderenza Nome Corso`).
3. Indica le slide ufficiali e la dispensa; Claude si ferma ai punti di conferma (dopo l'analisi iniziale e prima dell'integrazione).
4. Controlla il PDF e pubblica: `git add corsi/<corso> && git commit && git push`.

---

# ISTRUZIONI PER CLAUDE (esegui in ordine)

## Ruolo
Agisci da **assistente accademico esperto di revisione e sincronizzazione didattica**: l'obiettivo è allineare una dispensa già scritta alla struttura ufficiale delle slide del corso.

## Passo −1 – Ambiente
Esegui `procedure/ambiente.md` (Passo A–C) e `strumenti/controlla_ambiente.py`. Usa il comando Python che indica; su Windows niente `cp`/`mkdir -p`.

## Passo −1b – Repo aggiornata (`git fetch`)
Esegui **`procedure/aggiorna-repo.md`** (sezione «All'inizio»): `git fetch origin`, controllo dei commit nuovi sul remoto e, se ce ne sono, integrazione con `git pull --rebase` (albero di lavoro pulito) **prima di scrivere**. Dopo l'integrazione rileggi indice e capitoli della dispensa (Passo 1): potrebbero essere stati riordinati altrove.

## Passo 0 – Domande (prima di toccare qualsiasi file)
Chiedi, una alla volta o con `AskUserQuestion`:
1. **Corso** e **dispensa** da allineare (`corsi/<corso>/sorgenti/main.tex`; se ce n'è più di una, quale).
2. **Slide ufficiali**: percorso di file o cartella (PDF, PPTX…; anche più file). Se sono già tradotte in `slide-it/`, usa i sorgenti per l'indice ma verifica i contenuti sulle slide originali.
3. **Ambito**: tutta la dispensa o solo alcuni capitoli.
Riassumi in 3 righe e **aspetta la conferma**. Copia le slide in `corsi/<corso>/materiali/` (in `.gitignore`).

## Passo 1 – Estrazione e confronto degli indici
1. **Indice delle slide**: leggi le slide **a blocchi** (`codice/processa_slide.py --pacco aderenza-<corso> init|prossimo|fatto`, mai più di ~10 pagine per volta; accorpa le build ripetute con la numerazione «n / N» del piè di pagina). Per ogni blocco annota nella nota di `fatto`: titolo delle slide, argomento, pagine. `mappa` ricostruisce la tabella *pagine → argomento*. Ricava l'**indice dettagliato** (sezioni e sottosezioni nell'ordine delle slide, con i numeri di pagina).
2. **Indice della dispensa**: leggi `main.tex` e **i soli titoli** di capitoli, sezioni e sottosezioni (`grep` su `\chapter|\section|\subsection`, senza rileggere i capitoli interi). Il Capitolo 0 «Prerequisiti», se c'è, resta fuori dal confronto.
3. **Confronto**. Mostra due indici affiancati e un elenco delle **differenze strutturali**:
   - sezioni o capitoli **invertiti** (ordine diverso dalle slide);
   - argomenti delle slide **mancanti** come titolo nella dispensa;
   - capitoli o sezioni **extra** (nella dispensa e non nelle slide);
   - sezioni **spezzate** (stesso argomento in punti diversi) o **accorpate** (più argomenti delle slide in un solo capitolo).
   A questo punto non modificare nessun file.

## Passo 2 – Proposta di riorganizzazione (si ferma qui)
Stampa un **«Piano di Riordino»**: tabella *posizione attuale → nuova posizione* per ogni capitolo/sezione, con le pagine di slide corrispondenti e il **nuovo indice proposto**. Regole:
- è **solo taglia-e-incolla**: **non modificare, riscrivere o cancellare** il contenuto dei testi esistenti; si spostano blocchi interi tra file/sezioni e si adattano soltanto i comandi strutturali (`\chapter`/`\section`, `\include`/`\input`, `\label` e `\cref` che restano validi);
- il Capitolo 0 resta in testa;
- se una sezione non si può spostare senza spezzarla, **segnalalo e lasciala com'è**;
- elenca i capitoli che spezzeresti o accorperesti e perché.
**Aspetta il via libera dell'utente.** Dopo il via libera applica il riordino e compila (`latexmk -pdf` in `sorgenti/`): zero errori, zero riferimenti mancanti, indice uguale a quello approvato. Poi continua.

## Passo 3 – Analisi dei contenuti (gap analysis)
Con la dispensa riordinata, **argomento per argomento** (slide per slide, usando la mappa del Passo 1) confronta le slide con il capitolo corrispondente. Leggi la dispensa **a sezioni** (mai più di ~300 righe di `.tex` o ~10 pagine di PDF per volta). Elenca in modo puntuale in due liste numerate:
1. **Cosa manca nella dispensa**: contenuti presenti nelle slide (definizioni, formule, esempi, figure, tabelle, valori) e assenti o solo accennati nella dispensa, con la pagina di slide e la sezione in cui andrebbero.
2. **Cosa c'è in più nella dispensa**: approfondimenti, dimostrazioni, esempi o richiami presenti nella dispensa e non trattati nelle slide, con la sezione.
Aggiungi, se ci sono, i punti **dubbi o in conflitto** (la dispensa dice una cosa diversa dalle slide): non risolverli da solo, segnalali. Non modificare ancora la dispensa.

## Passo 4 – Integrazione e marcatura
1. **Chiedi conferma** prima di integrare le parti mancanti (di norma mostra l'elenco del Passo 3 e chiedi quali includere). Non procedere senza l'ok.
2. Dopo l'ok **scrivi tu le parti mancanti**, prese dalle slide, nel punto logico del capitolo giusto, con lo stile della dispensa (box `riquadro`/`esempio`/`attenzione`, `\textbf` per le parole chiave, formule sempre in LaTeX, **figure** delle slide portate secondo la regola in `CLAUDE.md`). **Non** aggiungere tag alle parti integrate dalle slide.
3. **Marcatura**: segna in modo evidente **solo** le parti che erano **già nella dispensa** e non trovano riscontro nelle slide, con l'ambiente `extraslide` (`\begin{extraslide} … \end{extraslide}`, che stampa «[CONTENUTO EXTRA NON PRESENTE NELLE SLIDE]»). Se `preambolo.tex` non lo definisce, copialo dalla fine di `template/dispensa/sorgenti/preambolo.tex`. Il testo segnato **non si modifica**: lo si racchiude soltanto nel box. Per un extra di poche righe dentro un paragrafo, premetti il tag in grassetto rosso all'inizio e chiudi con una riga vuota.
4. I punti dubbi o in conflitto restano come `% NOTA:` accanto al testo, senza cambiare né marcare.
5. Registra tutto nel `CHANGELOG.md` (data, riordino applicato, parti integrate con pagina di slide, parti marcate come extra).

## Passo 5 – Revisione e chiusura
1. `latexmk -pdf` senza errori né riferimenti mancanti; **verifica visiva** delle pagine toccate (`pdftoppm -r 40`, fogli da 12): testo tagliato, box spezzati male, figure fuori pagina.
2. **Controllo di completezza**: ogni slide ha il suo riscontro nella dispensa (o è elencata come esclusa dall'utente).
3. Copia il PDF nella cartella del corso con il nome definitivo; aggiorna il `README.md` della materia.
4. **Riepilogo**: riordino applicato, parti integrate, parti marcate come extra, dubbi aperti.
5. Rifai `git fetch origin` (`procedure/aggiorna-repo.md`, sezione «Alla fine») e mostra `git status -sb`; se il remoto è avanti, integra e ricompila prima di proporre il commit. **Commit e push solo se l'utente lo chiede.**

## Regole sempre valide
- `materiali/` non va mai su GitHub.
- Il riordino è solo taglia-e-incolla: mai riscrivere, riassumere o cancellare testo già scritto.
- Fermati sempre ai due punti di conferma (dopo il Passo 2 e prima del Passo 4).
- I tag «extra» servono solo per ciò che era già nella dispensa; le integrazioni dalle slide non si marcano.
