---
description: Verifica la dispensa di una lezione con nuove fonti, cerca informazioni mancanti o errori e corregge
---

Esegui la procedura contenuta in `procedure/integra-informazione.md`, a partire dalla sezione «ISTRUZIONI PER CLAUDE», seguendo i passi in ordine. Leggi anche `CLAUDE.md` per le regole generali.

Argomento facoltativo: $ARGUMENTS (corso e/o lezione da verificare, se già noti).

Prima di tutto esegui il Passo −1 (`procedure/ambiente.md`, `strumenti/controlla_ambiente.py`) e il Passo −1b (`procedure/aggiorna-repo.md`: `git fetch origin`, commit nuovi sul remoto da mostrare e integrare con `git pull --rebase` con l'albero di lavoro pulito, prima di scrivere). Poi comincia dal Passo 0: se mancano chiedi corso, capitolo/lezione e quali sono le nuove fonti (slide, appunti, trascrizione, libro: a mano o digitali), riassumi e aspetta conferma. Confronta con la dispensa già scritta, mostra il rapporto (errori, mancanze, dubbi) e correggi con interventi minimi: ogni modifica ha una fonte; i punti dubbi si segnalano con `% NOTA:` senza cambiare il testo.

Ricorda: le formule restano sempre in LaTeX e le figure delle fonti vanno portate nel risultato (le estrae `processa_slide.py prossimo`; per le vettoriali `processa_slide.py ritaglia`, con `--bianco` per le formule).
