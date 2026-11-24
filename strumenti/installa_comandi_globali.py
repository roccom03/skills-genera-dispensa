#!/usr/bin/env python3
"""Installa i comandi della repo (/nuova-dispensa, /traduci-slide, /aggiungi-lezione, /integra-informazione, /aderenza, /prepara-ambiente)
in ~/.claude/commands, così sono disponibili da qualunque cartella.

Le copie globali hanno i percorsi relativi riscritti in assoluti verso questa repo,
quindi vanno reinstallate se la repo viene spostata. Uso:
    python3 strumenti/installa_comandi_globali.py            # installa/aggiorna
    python3 strumenti/installa_comandi_globali.py --rimuovi  # disinstalla
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SORGENTE = REPO / ".claude" / "commands"
DEST = Path.home() / ".claude" / "commands"
PERCORSI = re.compile(r"`((?:procedure|strumenti|template|sorgenti|materiali)/[^`\s]*|CLAUDE\.md)")


def globale(testo: str) -> str:
    testo = PERCORSI.sub(lambda m: "`" + (REPO / m.group(1)).as_posix(), testo)
    if testo.startswith("---"):
        testa, _, corpo = testo[3:].partition("\n---\n")
        testo = f"---{testa}\n---\n"
    else:
        corpo = testo
        testo = ""
    nota = (f"Repo delle dispense: `{REPO.as_posix()}`. I percorsi sotto sono già assoluti; "
            "lavora in quella cartella (cd) e crea lì le nuove materie.\n\n")
    return testo + "\n" + nota + corpo.lstrip("\n") if testo else nota + corpo


def main() -> None:
    rimuovi = "--rimuovi" in sys.argv
    for src in sorted(SORGENTE.glob("*.md")):
        dst = DEST / src.name
        if rimuovi:
            if dst.exists():
                dst.unlink()
                print(f"rimosso   {dst}")
            continue
        DEST.mkdir(parents=True, exist_ok=True)
        dst.write_text(globale(src.read_text(encoding="utf-8")), encoding="utf-8")
        print(f"installato /{src.stem} -> {dst}")


if __name__ == "__main__":
    main()
