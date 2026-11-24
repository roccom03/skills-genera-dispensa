---
description: Traduce in italiano e riprogetta graficamente un pacco di slide (Beamer)
---

All'inizio ricorda all'utente, in una riga, che se vuole controllare la sessione da remoto deve digitare `/remote-control` (tu non puoi eseguirlo). Non aspettare una risposta: prosegui subito.

Esegui la procedura contenuta in `procedure/traduci-slide.md`, a partire dalla sezione «ISTRUZIONI PER CLAUDE», seguendo i passi in ordine. Leggi anche `CLAUDE.md` per le regole generali.

Argomento facoltativo: $ARGUMENTS (nome del corso, se già noto).

Prima di tutto esegui il Passo −1 (`procedure/ambiente.md`, `strumenti/controlla_ambiente.py`) e il Passo −1b (`procedure/aggiorna-repo.md`: `git fetch origin`, commit nuovi sul remoto da mostrare e integrare con `git pull --rebase` con l'albero di lavoro pulito, prima di scrivere). Poi comincia dal Passo 0: se il corso non è in $ARGUMENTS chiedilo, poi chiedi le slide, la lingua di partenza e lo stile grafico; riassumi e aspetta conferma prima di creare la cartella con `template/slide`.

Ricorda: le figure delle slide vanno sempre portate nel risultato (le estrae `processa_slide.py prossimo`; per le vettoriali `processa_slide.py ritaglia`), non saltarle né descriverle a parole; a fine lavoro controlla che compaiano tutte.
