# Template per slide tradotte

Scheletro Beamer 16:9 usato da `/traduci-slide`. Copialo in `corsi/<corso>/slide-<lingua>/` (es. `slide-it`) e compila con `latexmk -pdf` in `sorgenti/`.

**Un pacco di slide = un file `.tex` = un PDF.** Rinomina `Titolo-Pacco-Tradotto.tex` con il titolo del pacco tradotto (senza spazi né accenti, es. `Tecniche-di-modulazione-digitale.tex`) e rinomina `sezioni/nome-pacco/` con lo stesso nome in minuscolo. Per un secondo pacco copia il file `.tex` e crea un'altra cartella in `sezioni/`: `latexmk -pdf` compila tutti i pacchi insieme, e `preambolo.tex`, `GLOSSARIO.md` e `codice/` restano comuni. **Stile**: la riga `\input{stili/sobrio}` di `preambolo.tex` sceglie lo stile tra `classico`, `sobrio`, `colorato`, `accademico`, `topology` e `circuito` (file in `sorgenti/stili/`; anteprima in `anteprima-stili.png`). Colori e font di uno stile si cambiano solo nel suo file, uno stile nuovo si crea copiandone uno.
