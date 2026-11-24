---
description: Controlla e installa gli strumenti necessari (Python, Poppler, TeX, LibreOffice) su Linux, macOS o Windows
---

All'inizio ricorda all'utente, in una riga, che se vuole controllare la sessione da remoto deve digitare `/remote-control` (tu non puoi eseguirlo). Non aspettare una risposta: prosegui subito.

Esegui il Passo A e il Passo B di `procedure/ambiente.md`, **senza dare per scontato che Python sia installato**.

1. **Rileva il sistema con la shell**, non con Python (`uname -s` su Linux/macOS; su Windows `$env:OS` in PowerShell o `ver` in cmd) e controlla se esiste un comando Python (`python3 --version`, poi `python --version`, poi `py --version`).
2. **Se Python manca**, installalo per primo (Linux: `sudo apt-get install -y python3`; macOS: `brew install python`; Windows: `winget install -e --id Python.Python.3.12`). Su Windows riapri il terminale se il comando non viene riconosciuto subito.
3. Lancia `strumenti/controlla_ambiente.py` (senza opzioni) e riassumi all'utente cosa è `[OK]` e cosa `[MANCA]`, con le dimensioni (TeX su Linux ≈ 5 GB).
4. Se manca qualcosa, **chiedi una sola conferma** per l'insieme e, se l'utente accetta, esegui `strumenti/controlla_ambiente.py --installa --si`. Non chiedere mai password in chat: se `sudo` o il controllo account di Windows richiedono interazione che la sessione non può dare, di' all'utente di lanciare lo stesso comando nel proprio terminale con il prefisso `!`.
5. Rilancia il controllo e riporta il risultato. Se tutto è `[OK]`, di' che si può usare `/nuova-dispensa` o `/traduci-slide`; se resta qualcosa `[MANCA]` o richiede di riaprire il terminale, dillo chiaramente.

Argomento facoltativo: $ARGUMENTS (per esempio `simula`: in tal caso usa `--installa --simula` e non installare nulla).
