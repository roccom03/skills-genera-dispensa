# skills-genera-dispensa

Un insieme di **skill per [Claude Code](https://claude.com/claude-code)** che trasformano slide, appunti e registrazioni delle lezioni universitarie in **dispense di studio in LaTeX** (e in slide tradotte in italiano), con PDF pronto da stampare. Questa repo è **vuota di contenuti**: contiene solo gli strumenti. I corsi nascono nella cartella `corsi/` man mano che li crei.

## Come funziona una skill

Ogni skill è un **comando** (`/nome-comando`) che Claude Code esegue seguendo una procedura scritta in chiaro. Il meccanismo ha quattro pezzi:

| Pezzo | Dove | Cosa fa |
|---|---|---|
| **Comando** | `.claude/commands/<nome>.md` | È ciò che digiti (`/nuova-dispensa`). Contiene poche righe: dice a Claude quale procedura eseguire e da dove partire. |
| **Procedura** | `procedure/<nome>.md` | È il cuore: la sezione «ISTRUZIONI PER CLAUDE» elenca i passi in ordine (domande iniziali, stesura, controlli, chiusura). La parte in alto spiega a te come usarla. |
| **Regole** | `CLAUDE.md` | Claude lo legge in automatico a ogni sessione: regole sempre valide (figure sempre portate, formule in LaTeX, slide lunghe a blocchi, cosa va in git, commit solo su richiesta). |
| **Template e strumenti** | `template/`, `strumenti/` | Lo scheletro LaTeX da cui parte ogni dispensa o pacco di slide, lo script che divide le slide in blocchi (`processa_slide.py`) e quello che controlla l'ambiente (`controlla_ambiente.py`). |

Il flusso tipico di ogni comando è sempre lo stesso:

1. **Ambiente**: controlla che Python, Poppler, TeX e (se servono) LibreOffice siano installati; se manca qualcosa propone l'installazione e aspetta il tuo sì.
2. **Repo aggiornata**: fa `git fetch` e integra eventuali commit nuovi prima di scrivere, così più sessioni o più PC non si pestano i piedi.
3. **Domande iniziali**: ti chiede materia, docente, dove sono le fonti, lingua. **Non scrive nulla finché non confermi** il riepilogo.
4. **Lavoro a blocchi**: le slide non vengono mai lette tutte insieme ma a blocchi da 10 pagine; l'avanzamento è salvato su file, quindi se la sessione si interrompe riprende dal punto giusto.
5. **Punti di conferma**: nei passi delicati (riordino dei capitoli, integrazione di parti mancanti, correzioni) mostra prima il piano e aspetta il via libera.
6. **Compilazione e controllo**: compila con `latexmk`, verifica che non ci siano errori né riferimenti rotti e che ogni figura delle slide compaia nel PDF.
7. **Commit solo su richiesta**: non fa mai commit o push da solo.

## I comandi

| Comando | A cosa serve | Cosa ottieni |
|---|---|---|
| `/prepara-ambiente` | Prima volta su un PC (Linux, macOS o Windows, anche senza Python): rileva il sistema e installa gli strumenti mancanti dopo una tua conferma. | Ambiente pronto. |
| `/nuova-dispensa` | Crei la dispensa di una materia a partire da un pacco di slide (e, se ci sono, codici e tracce d'esame). | `corsi/<materia>/` con sorgenti LaTeX e PDF discorsivo, con Capitolo 0 di prerequisiti. |
| `/aggiungi-lezione` | Unisci in un capitolo le fonti di **una lezione**: slide, appunti (a mano o digitali), trascrizione o anche solo la registrazione audio/video (la trascrive con whisper). | Nuovo capitolo nella dispensa esistente, senza stravolgerla. Le immagini mancanti le cerca e le scarica Claude, con fonte e licenza. |
| `/integra-informazione` | Hai nuove fonti per una lezione già scritta: Claude confronta, trova informazioni mancanti ed errori. | Rapporto di verifica, correzioni minime tracciate in `CHANGELOG.md`; i dubbi restano come `% NOTA:` senza toccare il testo. |
| `/aderenza` | Vuoi che la dispensa segua la struttura delle slide ufficiali. | Confronto degli indici, nuovo indice proposto, riordino (solo taglia-e-incolla), poi integrazione di ciò che manca; ciò che c'è in più è marcato `extraslide`. |
| `/traduci-slide` | Traduci in italiano un pacco di slide e le riprogetti graficamente (Beamer 16:9), senza aggiungere contenuto. | Un PDF per pacco in `corsi/<corso>/slide-it/`, con glossario in `GLOSSARIO.md`. |

Non serve ricordare i nomi: puoi anche dire a parole «voglio aggiungere una nuova materia» e Claude sceglie la procedura giusta (è scritto in `CLAUDE.md`).

## Avvio rapido

```
git clone https://github.com/roccom03/skills-genera-dispensa.git
cd skills-genera-dispensa
claude                      # avvia Claude Code in questa cartella
```

Poi, dentro Claude Code:

1. `/prepara-ambiente` (solo la prima volta su un PC).
2. `/nuova-dispensa Nome Materia`: rispondi alle domande (slide, codici, lingua) e conferma il riepilogo.
3. Per ogni lezione successiva: `/aggiungi-lezione`.
4. Controlla il PDF in `corsi/<materia>/` e, se vuoi, fai commit e push.

Le slide e i materiali del docente finiscono in `corsi/<materia>/materiali/`, che è nel `.gitignore` e **non** viene mai pubblicata.

## Comandi globali

Per usare `/nuova-dispensa`, `/traduci-slide`, `/aggiungi-lezione`, `/integra-informazione`, `/aderenza` e `/prepara-ambiente` da qualsiasi cartella (non solo dentro la repo), esegui una volta:

```
python3 strumenti/installa_comandi_globali.py            # installa in ~/.claude/commands
python3 strumenti/installa_comandi_globali.py --rimuovi  # disinstalla
```

Le copie globali puntano ai percorsi assoluti della repo: rilancia lo script se la sposti o modifichi i comandi.

## Struttura della repo

```
.claude/commands/             # comandi /nuova-dispensa, /traduci-slide, /aggiungi-lezione, /integra-informazione, /aderenza
CLAUDE.md                     # regole sempre valide per Claude
procedure/                    # procedure eseguibili dai comandi
├── nuova-dispensa.md
├── traduci-slide.md
├── aggiungi-lezione.md
├── integra-informazione.md
├── aderenza.md
├── aggiorna-repo.md          # git fetch prima di scrivere e prima del commit (richiamato da tutte)
└── ambiente.md               # rilevamento Linux/macOS/Windows e installazioni
strumenti/
└── controlla_ambiente.py     # rileva il sistema operativo e controlla gli strumenti richiesti
template/
├── dispensa/                 # scheletro LaTeX per una nuova dispensa
└── slide/                    # scheletro Beamer per slide tradotte
                              # (entrambi contengono sorgenti/codice/processa_slide.py)
corsi/
└── <nome-corso>/
    ├── README.md             # descrizione del corso e della dispensa
    ├── <Nome-Dispensa>.pdf   # PDF compilato, pronto da stampare
    ├── sorgenti/             # sorgenti LaTeX (main.tex, capitoli/, figure/, codice/)
    ├── slide-it/             # (facoltativo) slide tradotte, stessa struttura
    └── materiali/            # solo locale (.gitignore): slide e codici del docente
```

## Prima di iniziare: strumenti necessari

Servono Python 3, Poppler (`pdftotext`, `pdftoppm`, `pdfinfo`), TeX con `latexmk` e, solo se le slide non sono in PDF, LibreOffice. Non devi controllare nulla a mano: su un PC nuovo, anche senza Python, scrivi **`/prepara-ambiente`** in Claude Code e fa tutto lui (rileva il sistema, installa Python e il resto dopo una tua conferma). In più, ogni comando parte da `strumenti/controlla_ambiente.py`, che **rileva da solo Linux, macOS o Windows**, dice cosa manca e propone i comandi d'installazione (`apt`, `brew`, `winget`). Se vuoi che installi lui ciò che manca: `python3 strumenti/controlla_ambiente.py --installa` (chiede conferma per ogni strumento; `--simula` mostra i comandi senza eseguirli; su Linux la password di `sudo` la digiti tu nel terminale). Su Windows dopo ogni installazione riapri il terminale. Dettagli in [procedure/ambiente.md](procedure/ambiente.md).

## Come lavorano i comandi (slide lunghe incluse)

Le slide non vengono mai lette tutte insieme: lo script `processa_slide.py` le divide in **blocchi da 10 pagine** e Claude le elabora un blocco alla volta (`init` → `prossimo` → scrittura → `fatto`), anche per centinaia di pagine. L'avanzamento è salvato in `materiali/avanzamento.json`, quindi se la sessione si interrompe o il contesto si azzera il lavoro riprende dal blocco giusto. Sono accettati PDF e, convertiti in automatico in PDF con LibreOffice, PPTX/PPT/ODP, DOC/DOCX/ODT/RTF, XLS/XLSX/ODS, anche mescolati. I file Keynote (`.key`) vanno prima esportati in PDF.

## Aggiungere una nuova dispensa con Claude

La repo contiene un prompt già pronto (`/nuova-dispensa`) che guida Claude Code nella creazione di una dispensa, dalle slide al PDF.

**Come usarlo**
1. Installa [Claude Code](https://claude.com/claude-code) e clona la repo: `git clone https://github.com/roccom03/skills-genera-dispensa.git`
2. Apri il terminale **nella cartella della repo** e avvia `claude` (Claude legge in automatico `CLAUDE.md` con tutte le istruzioni).
3. Scrivi:
   ```
   /nuova-dispensa
   ```
   oppure, con il nome già pronto: `/nuova-dispensa Computer Vision`. In alternativa basta dire a parole «voglio aggiungere una nuova materia».
4. Rispondi alle domande che Claude ti pone:
   - **nome della materia**;
   - **percorso delle slide** (PDF, PPTX, DOCX… file o cartella), per esempio `~/Download/slide-cv/`;
   - **codici di partenza** (script MATLAB/Python, dati, note del docente, tracce d'esame), se ci sono;
   - **lingua** (italiano, inglese o entrambe).
5. Claude riassume le risposte e aspetta la tua conferma, poi lavora per fasi (analisi delle slide, stesura, Capitolo 0 di prerequisiti, riordino, impaginazione). Si ferma a chiederti conferma sul **piano di riordino** prima di spostare i capitoli.
6. Alla fine trovi il PDF nella cartella della materia. Controllalo, poi pubblica:
   ```
   git add corsi/<cartella-materia> README.md
   git commit -m "Aggiunge <materia>"
   git push
   ```

Slide e codici di partenza vengono copiati in `corsi/<materia>/materiali/`, che non viene caricata su GitHub. Dettagli e fasi in [procedure/nuova-dispensa.md](procedure/nuova-dispensa.md); le regole operative per Claude sono in [CLAUDE.md](CLAUDE.md).

## Tradurre un pacco di slide con Claude

`/traduci-slide` traduce in italiano un pacco di slide e le riprogetta graficamente (Beamer 16:9), mantenendo il contenuto e l'ordine originali.

1. Apri `claude` nella cartella della repo.
2. Scrivi `/traduci-slide` (o `/traduci-slide Nome Corso`).
3. Rispondi alle domande: corso e docente, percorso delle slide (PDF, PPTX, DOCX…), lingua di partenza, stile grafico, se accorpare le varianti di build.
4. Claude riassume e aspetta conferma, poi lavora a blocchi di 10 pagine (traduzione con glossario in `GLOSSARIO.md`, restyling, revisione visiva). Ogni pacco di slide dà un PDF a sé, col titolo del pacco tradotto, in `corsi/<corso>/slide-it/`.
5. Controlla il PDF e pubblica: `git add corsi/<corso> README.md`, `git commit`, `git push`.

Procedura completa in [procedure/traduci-slide.md](procedure/traduci-slide.md); scheletro in `template/slide/`.

## Stato del supporto Windows/macOS
Collaudato solo su Linux. Il supporto Windows e macOS (percorsi di LibreOffice, pacchetti `winget`/`brew`, MiKTeX con `latexmk`) è scritto ma non ancora provato: alla prima esecuzione segnala gli errori a Claude, che corregge [procedure/ambiente.md](procedure/ambiente.md).

## Compilare

```
cd corsi/<corso>/sorgenti            # per le slide tradotte: corsi/<corso>/slide-it/sorgenti
latexmk -pdf                       # slide: un PDF per pacco; dispense: main.tex
```
Richiede una distribuzione TeX (TeX Live, o MiKTeX su Windows) con i pacchetti usati in `preambolo.tex`.

Le slide dei corsi appartengono ai docenti (uso riservato agli studenti iscritti): non pubblicarle, e non committare il contenuto di `materiali/`.
