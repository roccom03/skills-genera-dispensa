# Repo aggiornata: `git fetch` prima di scrivere e prima del commit

Questo file è richiamato da **tutte le procedure che scrivono sulla dispensa** (`/nuova-dispensa`, `/traduci-slide`, `/aggiungi-lezione`, `/integra-informazione`, `/aderenza`): dal loro **Passo −1b** (sezione «All'inizio») e dal passo di chiusura (sezione «Alla fine»). Non è un comando a sé.

**Perché.** La dispensa si scrive da più sessioni e dispositivi, quindi `origin/main` può avere lezioni, capitoli o corsi che in locale non ci sono. È già successo: una lezione scritta altrove ha fatto rifiutare il push (`fetch first`) e ha obbligato a fare il rebase, a rinumerare i capitoli e a togliere i testi ripetuti.

# ISTRUZIONI PER CLAUDE

## All'inizio (Passo −1b, prima delle domande)
Dalla radice della repo:
1. Esegui `git fetch origin` (non modifica nulla), poi `git status -sb` e `git log --oneline HEAD..origin/main`.
2. **Nessun commit nuovo sul remoto**: prosegui.
3. **Ci sono commit nuovi**: mostra all'utente, in poche righe, che cosa contengono (`git diff --stat HEAD...origin/main`, con attenzione ai file del corso su cui si lavora). Integrali con `git pull --rebase` **solo se l'albero di lavoro è pulito** (nessuna modifica ai file tracciati), altrimenti chiedi come procedere. Poi rileggi indice e titoli dei capitoli del corso: ciò che l'utente sta per aggiungere potrebbe essere già in dispensa e la numerazione dei capitoli potrebbe essere cambiata.
4. **Mai `--force`.** Con i conflitti (di solito `CHANGELOG.md`, `README.md`, `main.tex` e il PDF) tieni **entrambe** le parti, senza perdere nulla di nessuna delle due, e rigenera il PDF compilando di nuovo. Se serve rinumerare i capitoli, rinomina i file (`git mv`) e aggiorna `main.tex`, il `README.md` del corso e il `CHANGELOG.md`.
5. Se `git fetch` fallisce (niente rete, remoto non raggiungibile) segnalalo all'utente e prosegui, avvisando che il remoto non è stato controllato.

## Alla fine (prima di proporre commit e push)
Ripeti `git fetch origin` (nel frattempo il remoto può essere cambiato) e mostra `git status -sb`. Se il remoto è avanti, integra come sopra, **ricompila** e controlla che non ci siano errori né riferimenti rotti prima di proporre il commit. **Commit e push solo se l'utente lo chiede** (se il push viene rifiutato con `fetch first`, non forzare: ripeti questa sezione).
