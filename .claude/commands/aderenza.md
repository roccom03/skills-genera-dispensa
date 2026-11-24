---
description: Allinea la dispensa alla struttura delle slide ufficiali: confronta gli indici, riordina, analizza cosa manca o è extra e integra dopo conferma
---

Esegui la procedura contenuta in `procedure/aderenza.md`, a partire dalla sezione «ISTRUZIONI PER CLAUDE», seguendo i passi in ordine. Leggi anche `CLAUDE.md` per le regole generali.

Argomento facoltativo: $ARGUMENTS (corso e/o dispensa da allineare, se già noti).

Prima di tutto esegui il Passo −1 (`procedure/ambiente.md`, `strumenti/controlla_ambiente.py`) e il Passo −1b (`procedure/aggiorna-repo.md`: `git fetch origin`, commit nuovi sul remoto da mostrare e integrare con `git pull --rebase` con l'albero di lavoro pulito, prima di scrivere). Poi comincia dal Passo 0: se mancano chiedi corso, dispensa e slide ufficiali, riassumi e aspetta conferma. Dai prima il riscontro dei Passi 1 e 2 (confronto degli indici e proposta del nuovo indice) e **fermati ad aspettare il via libera**; poi riordina senza riscrivere nulla, fai la gap analisi (cosa manca / cosa c'è in più) e chiedi conferma prima di integrare. Marca con `extraslide` solo ciò che era già nella dispensa e non è nelle slide.

Ricorda: le formule restano sempre in LaTeX e le figure delle slide vanno portate nel risultato (le estrae `processa_slide.py prossimo`; per le vettoriali `processa_slide.py ritaglia`, con `--bianco` per le formule).
