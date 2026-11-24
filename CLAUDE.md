# Istruzioni per Claude – repo delle dispense

Questa repo raccoglie dispense di studio in LaTeX, una cartella per materia (vedi `README.md`). Quando l'utente chiede di **aggiungere una materia / creare una nuova dispensa** (o digita `/nuova-dispensa`), segui questo flusso. Parla in italiano.

## Procedura
Per creare una nuova dispensa esegui **`procedure/nuova-dispensa.md`** (sezione «ISTRUZIONI PER CLAUDE»): contiene le domande iniziali, l'albero delle cartelle, il metodo di scrittura di Image Processing, il Capitolo 0, il riordino e la revisione tipografica. Parti sempre dal Passo 0 e non scrivere contenuti prima della conferma dell'utente. Il template è in `template/dispensa/`.

## Tradurre un pacco di slide
Quando l'utente chiede di **tradurre in italiano e rifare graficamente delle slide** (o digita `/traduci-slide`), esegui **`procedure/traduci-slide.md`** (sezione «ISTRUZIONI PER CLAUDE»), partendo dal Passo 0. Il template è in `template/slide/`. Non aggiungere contenuto alle slide: per una dispensa discorsiva usa `/nuova-dispensa`.

## Aggiungere una lezione a una dispensa
Quando l'utente chiede di **unire slide, appunti e/o trascrizione di una lezione** (a mano o digitali, in qualsiasi combinazione) in una dispensa, o di aggiungere una lezione (o digita `/aggiungi-lezione`), esegui **`procedure/aggiungi-lezione.md`** (sezione «ISTRUZIONI PER CLAUDE»), partendo dal Passo 0. Aggiorna la dispensa esistente senza stravolgerla; se c'è una trascrizione rumorosa, **prima** crei per ogni lezione il file `lezione-pulita.md` (Passo 2a) e aspetti il via dell'utente; le immagini le cerchi e le scarichi tu, con fonte e licenza.

## Verificare e correggere una lezione già scritta
Quando l'utente ha **nuove fonti per una lezione già in dispensa** e vuole controllare se mancano informazioni o se ci sono errori (o digita `/integra-informazione`), esegui **`procedure/integra-informazione.md`** (sezione «ISTRUZIONI PER CLAUDE»), partendo dal Passo 0. Confronta, mostra il rapporto e correggi con interventi minimi e tracciati nel `CHANGELOG.md`; i punti dubbi si segnalano con `% NOTA:` senza cambiare il testo.

## Allineare la dispensa alle slide
Quando l'utente vuole **allineare una dispensa già scritta alla struttura ufficiale delle slide** (confronto degli indici, riordino, cosa manca / cosa c'è in più) o digita `/aderenza`, esegui **`procedure/aderenza.md`** (sezione «ISTRUZIONI PER CLAUDE»), partendo dal Passo 0. Dai prima il confronto degli indici e il nuovo indice proposto e **aspetta il via libera**; il riordino è solo taglia-e-incolla; chiedi conferma prima di integrare; marca con `extraslide` solo ciò che era già nella dispensa e non è nelle slide.


## Regole sempre valide
- **Ambiente**: su un PC nuovo l'utente usa `/prepara-ambiente` (funziona anche senza Python). Prima di ogni procedura esegui `strumenti/controlla_ambiente.py` (vedi `procedure/ambiente.md`): rileva Linux/macOS/Windows e gli strumenti mancanti. Su Windows niente comandi bash (`cp`, `mkdir -p`): usa Python.
- **Repo aggiornata**: la dispensa si scrive da più sessioni. Ogni comando che scrive sulla dispensa parte da `git fetch origin` e lo ripete prima di proporre il commit (vedi `procedure/aggiorna-repo.md`): se il remoto è avanti, integra con `git pull --rebase` (albero pulito, mai `--force`) e ricompila.
- **Figure**: le figure delle slide vanno **sempre portate** nel risultato (mai saltate né sostituite da una descrizione a parole). `processa_slide.py prossimo` le estrae in `sorgenti/figure/`; per quelle vettoriali o trasparenti usa `processa_slide.py ritaglia`. **Le formule sono sempre in LaTeX**, mai come immagine: nei ritagli delle figure coprile con `ritaglia ... --bianco` e riscrivile nel testo. Controlla a fine lavoro che ogni figura delle slide compaia nel PDF e riporta quelle mancanti. Se una lezione ha disegni a mano o figure assenti dalle slide, `/aggiungi-lezione` le cerca e le scarica (con fonte e licenza).
- **Slide lunghe**: non leggere mai più di ~10 pagine alla volta. Usa `sorgenti/codice/processa_slide.py` (`init` → `prossimo` → `fatto`, stato in `materiali/avanzamento.json`) e a inizio sessione riprendi con `stato`/`prossimo`.
- Rispondi in italiano. Compila con `latexmk -pdf` in `sorgenti/` e consegna solo senza errori né riferimenti mancanti.
- `materiali/` (slide, codici di partenza) è in `.gitignore`: non va su GitHub.
- **Cosa va in git**: solo PDF, codici (sorgenti) di ogni corso e ciò che serve ai comandi (`.claude/`, `CLAUDE.md`, `procedure/`, `template/`, `strumenti/`). Ogni volta che usi un comando, **controlla e aggiorna `.gitignore`**: devono essere ignorati `**/materiali/`, `**/slide-da-tradurre/` e qualunque altra cartella o file di slide, appunti, trascrizioni o zip del docente che l'utente ha messo nella repo (aggiungi la riga se manca). Verifica con `git check-ignore -v <percorso>` e con `git status` che nulla di tutto ciò risulti tracciabile; segnala all'utente cosa hai aggiunto.
- Commit e push solo su richiesta; non chiedere token o password in chat.
- Non riscrivere testo già approvato quando fai riordino o impaginazione.
