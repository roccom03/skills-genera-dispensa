# Ambiente di lavoro: Linux, macOS o Windows

Questo file dice a Claude come **capire da solo su quale sistema si trova** e come prepararlo prima di eseguire `/nuova-dispensa` o `/traduci-slide`. Su Linux di solito non serve fare nulla. Su Windows servono alcuni programmi da installare una volta.

## Scorciatoia: `/prepara-ambiente`
Su un PC nuovo (anche senza Python) basta scrivere **`/prepara-ambiente`**: rileva il sistema con la shell, installa Python se manca, poi controlla e installa il resto con una sola conferma. Equivale ai Passi A e B qui sotto.

## Passo A – Rilevamento (sempre, prima di ogni procedura)
Dalla radice della repo esegui:
```
python3 strumenti/controlla_ambiente.py        # se non esiste: python strumenti/controlla_ambiente.py  oppure  py strumenti/controlla_ambiente.py
```
Lo script stampa il **sistema rilevato** (`Linux`, `Darwin` = macOS, `Windows`), il **comando Python da usare**, e per ogni strumento `[OK]` o `[MANCA]` con il comando d'installazione. Da qui in poi usa quel comando Python al posto di `python3` in tutte le istruzioni.
Se nessun comando Python esiste, il sistema si rileva con la shell (`uname -s` su Linux/macOS, `$env:OS` o `ver` su Windows) e si installa Python per primo (Linux: `sudo apt-get install -y python3`; macOS: `brew install python`; Windows: `winget install -e --id Python.Python.3.12`, poi riapri il terminale).

## Passo B – Installazione di ciò che manca
Spiega all'utente cosa manca e **chiedi conferma** prima di installare (TeX su Linux pesa circa 5 GB: dillo). Con il sì dell'utente usa lo script, che installa da solo ciò che manca:
```
python3 strumenti/controlla_ambiente.py --installa            # chiede conferma per ogni strumento
python3 strumenti/controlla_ambiente.py --installa --simula   # mostra i comandi senza eseguirli
```
Gestori usati: `apt-get` (Linux Debian/Ubuntu), `brew` (macOS), `winget` (Windows). Con altri gestori (dnf, pacman, ecc.) lo script lo dice: installa a mano con i pacchetti della tabella.
- **Password e permessi**: su Linux `sudo` chiede la password e su Windows `winget` può aprire la finestra UAC. Non chiedere mai la password in chat: se la sessione non ha un terminale interattivo (lo script lo segnala con «A terminal is required»), chiedi all'utente di lanciare il comando nel **proprio terminale** (in Claude Code: prefisso `!`), poi riprendi dal Passo A.
- Niente `--si` (nessuna domanda) senza che l'utente l'abbia chiesto esplicitamente.

Tabella dei pacchetti, se serve installare a mano:

| Strumento | Linux (apt) | macOS (brew) | Windows (winget) |
|---|---|---|---|
| Poppler (`pdftotext`, `pdftoppm`, `pdfinfo`) | `poppler-utils` | `poppler` | `oschwartz10612.Poppler` |
| TeX + `latexmk` | `texlive-full latexmk` | `--cask mactex` | `MiKTeX.MiKTeX` + `StrawberryPerl.StrawberryPerl` |
| LibreOffice (solo per .pptx/.docx/.xlsx) | `libreoffice-impress libreoffice-writer` | `--cask libreoffice` | `TheDocumentFoundation.LibreOffice` |

- **Windows**: dopo ogni installazione l'utente deve **riaprire il terminale** (il PATH si aggiorna solo ai nuovi terminali), poi rilancia `strumenti/controlla_ambiente.py`. MiKTeX al primo uso può chiedere di installare pacchetti mancanti: va abilitata l'installazione automatica («Always»), altrimenti la compilazione resta in attesa. Se `winget` non c'è, indica all'utente i siti ufficiali dei programmi.
- Ripeti il Passo A finché non è tutto `[OK]`. **Non iniziare la procedura con strumenti mancanti.**
- Microsoft Office non è usato: le conversioni Office → PDF passano da LibreOffice (anche con Office installato). Se l'utente non vuole installare LibreOffice, chiedigli di esportare i file in PDF da Office («Salva con nome → PDF»).

## Passo C – Differenze da tenere a mente
- **Percorsi**: usa `/` nei comandi (Python e LaTeX lo accettano anche su Windows); metti tra virgolette i percorsi con spazi. Nei file `.tex` solo `/`.
- **Shell**: su Windows i comandi `cp -r`, `mkdir -p`, `ls`, `rm` non esistono in `cmd`. In PowerShell usa `Copy-Item -Recurse`, `New-Item -ItemType Directory -Force`, `Remove-Item`. Oppure, meglio, **fai le operazioni sui file con Python** (`shutil.copytree`, `pathlib`), che funziona uguale ovunque. `&&` funziona solo in PowerShell 7+; altrimenti un comando per riga.
- **Compilazione**: `latexmk -pdf main.tex` funziona uguale, ma con MiKTeX richiede Perl (vedi tabella). In alternativa `pdflatex` due volte.
- **Script della dispensa** (`processa_slide.py`): sono già portabili; l'unico requisito sono gli strumenti del Passo B. `processa_slide.py` cerca LibreOffice anche in `C:\Program Files\LibreOffice\program\` e stampa il comando d'installazione se manca qualcosa.
- **Fine riga e codifica**: salva i file `.tex` e `.md` in **UTF-8**. In PowerShell 5 `>` salva in UTF-16: non usarlo per scrivere sorgenti, scrivi i file con gli strumenti di Claude.
- **WSL**: se l'utente lavora in WSL (Linux dentro Windows) il sistema rilevato è `Linux` e vale tutto il lato Linux; i file di Windows sono in `/mnt/c/...`.

## Cosa non è stato verificato
Lo script di rilevamento e `processa_slide.py` sono stati provati solo su Linux. Il supporto Windows/macOS (percorsi di LibreOffice, nomi dei pacchetti winget/brew, comportamento di MiKTeX e `latexmk`) è scritto ma non collaudato: alla **prima esecuzione su Windows** segnala all'utente ogni errore e correggi questo file di conseguenza.
