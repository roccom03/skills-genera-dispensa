#!/usr/bin/env python3
"""Rileva il sistema operativo, controlla gli strumenti richiesti dalle procedure e, se richiesto, li installa.

Uso (dalla radice della repo; Windows: `python` o `py` al posto di `python3`):
  python3 strumenti/controlla_ambiente.py                 # solo controllo
  python3 strumenti/controlla_ambiente.py --installa      # installa ciò che manca, chiedendo conferma per ciascuno
  python3 strumenti/controlla_ambiente.py --installa --si # senza domande (solo se sai cosa stai facendo)
  python3 strumenti/controlla_ambiente.py --installa --simula   # mostra i comandi senza eseguirli

Installa con: apt-get (Linux Debian/Ubuntu), brew (macOS), winget (Windows). Altri gestori: stampa le istruzioni.
Su Linux serve sudo: la password la digita l'utente nel proprio terminale (non in chat).
Codice di uscita 0 = tutto pronto, 1 = manca qualcosa.
"""
import argparse, os, platform, shutil, subprocess, sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
S = platform.system()                 # "Linux", "Windows", "Darwin"


def soffice():
    t = shutil.which("soffice") or shutil.which("libreoffice")
    if t:
        return t
    cand = [os.path.join(os.environ.get(v, ""), "LibreOffice", "program", "soffice.exe")
            for v in ("ProgramFiles", "ProgramFiles(x86)", "LOCALAPPDATA")]
    cand.append("/Applications/LibreOffice.app/Contents/MacOS/soffice")
    return next((c for c in cand if c and os.path.exists(c)), None)


def winget(*ids):
    return [["winget", "install", "-e", "--id", i, "--accept-package-agreements", "--accept-source-agreements"]
            for i in ids]


def apt(*pacchetti):
    pre = [] if (hasattr(os, "geteuid") and os.geteuid() == 0) else ["sudo"]
    return [pre + ["apt-get", "install", "-y", *pacchetti]]


# nome, test, a cosa serve, comandi di installazione per sistema
CONTROLLI = [
    ("pdftotext/pdfinfo/pdftoppm (poppler)",
     lambda: all(shutil.which(t) for t in ("pdftotext", "pdfinfo", "pdftoppm")), "tutte le procedure",
     {"Linux": apt("poppler-utils"), "Darwin": [["brew", "install", "poppler"]],
      "Windows": winget("oschwartz10612.Poppler")}),
    ("latexmk + pdflatex (TeX)",
     lambda: shutil.which("latexmk") and shutil.which("pdflatex"), "compilazione PDF (Linux: ~5 GB con texlive-full)",
     {"Linux": apt("texlive-full", "latexmk"), "Darwin": [["brew", "install", "--cask", "mactex"]],
      "Windows": winget("MiKTeX.MiKTeX", "StrawberryPerl.StrawberryPerl")}),
    ("LibreOffice (soffice)", soffice, "solo file .pptx/.docx/.xlsx ecc.",
     {"Linux": apt("libreoffice-impress", "libreoffice-writer"), "Darwin": [["brew", "install", "--cask", "libreoffice"]],
      "Windows": winget("TheDocumentFoundation.LibreOffice")}),
]


def installa(nome, comandi, a):
    gestore = comandi[0][comandi[0][0] == "sudo"]       # primo token dopo un eventuale sudo
    if not shutil.which(gestore):
        print(f"        {gestore} non trovato: installa {nome} a mano (vedi procedure/ambiente.md).")
        return False
    testo = " && ".join(" ".join(c) for c in comandi)
    if a.simula:
        print(f"        [simula] {testo}")
        return True
    if not a.si and input(f"        Eseguo «{testo}»? [s/N] ").strip().lower() not in ("s", "si", "sì", "y"):
        print("        saltato.")
        return False
    return all(subprocess.run(c).returncode == 0 for c in comandi)


ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("--installa", action="store_true", help="installa gli strumenti mancanti")
ap.add_argument("--si", action="store_true", help="con --installa: non chiedere conferma")
ap.add_argument("--simula", action="store_true", help="con --installa: stampa i comandi senza eseguirli")
a = ap.parse_args()

print(f"Sistema: {S} ({platform.platform()})")
print(f"Python da usare: {os.path.basename(sys.executable) or sys.executable}  ({sys.executable})")
print(f"Shell: {'PowerShell/cmd (usa / nei percorsi, niente && in cmd)' if S == 'Windows' else 'POSIX'}")
manca = False
for nome, test, serve, inst in CONTROLLI:
    ok = bool(test())
    print(f"[{'OK' if ok else 'MANCA'}] {nome}  (serve per: {serve})")
    if ok:
        continue
    manca = True
    comandi = inst.get(S, inst["Linux"])
    if a.installa:
        if installa(nome, comandi, a) and not a.simula:
            print("        installato (verifica con un nuovo controllo).")
    else:
        print(f"        installa con: {' && '.join(' '.join(c) for c in comandi)}   (oppure rilancia con --installa)")
if manca:
    print("\nDopo l'installazione riapri il terminale (il PATH si aggiorna) e rilancia questo script senza opzioni.")
sys.exit(1 if manca else 0)
