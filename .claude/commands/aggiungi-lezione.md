---
description: Unisce slide, appunti e trascrizione (a mano o digitali) di una lezione in un capitolo e aggiorna la dispensa, con immagini cercate da Claude
---

All'inizio ricorda all'utente, in una riga, che se vuole controllare la sessione da remoto deve digitare `/remote-control` (tu non puoi eseguirlo). Non aspettare una risposta: prosegui subito.

Esegui la procedura contenuta in `procedure/aggiungi-lezione.md`, a partire dalla sezione «ISTRUZIONI PER CLAUDE», seguendo i passi in ordine. Leggi anche `CLAUDE.md` per le regole generali.

Argomento facoltativo: $ARGUMENTS (corso e/o argomento della lezione, se già noti).

Prima di tutto esegui il Passo −1 (`procedure/ambiente.md`, `strumenti/controlla_ambiente.py`) e il Passo −1b (`procedure/aggiorna-repo.md`: `git fetch origin`, commit nuovi sul remoto da mostrare e integrare con `git pull --rebase` con l'albero di lavoro pulito, prima di scrivere), perché la lezione o i capitoli potrebbero essere già in dispensa. Poi comincia dal Passo 0: se mancano chiedi corso, argomento, data e quali fonti hai (slide, appunti, trascrizione: anche solo alcune, a mano o digitali), riassumi e aspetta conferma prima di scrivere. Se la dispensa del corso esiste già, aggiornala senza stravolgerla; le immagini le cerchi e le scarichi tu.

Ricorda: le figure delle slide vanno sempre portate nel risultato (le estrae `processa_slide.py prossimo`; per le vettoriali `processa_slide.py ritaglia`), non saltarle né descriverle a parole; a fine lavoro controlla che compaiano tutte.

Se c'è una trascrizione (di solito rumorosa), **prima di ogni sintesi** esegui il Passo 2a: crea per ogni lezione il file `lezione-pulita.md` (senza rumore, intercalari, frasi fuori contesto, con termini tecnici corretti dalle slide, tutto il contenuto didattico conservato) e aspetta il via dell'utente. Il capitolo si scrive solo da quel file, mai dalla trascrizione grezza.
