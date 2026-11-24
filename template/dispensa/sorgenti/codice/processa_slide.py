#!/usr/bin/env python3
"""Elabora un pacco di slide a blocchi, senza saturare la finestra di contesto.

Lo stato sta in  <materia>/materiali/avanzamento.json  (fuori da git): dopo un
azzeramento del contesto basta rilanciare `prossimo` per riprendere dal punto giusto.
Con più pacchi di slide nello stesso corso usa `--pacco NOME` (qualsiasi comando): ogni
pacco ha il suo stato  materiali/avanzamento-NOME.json  e non si sovrascrivono a vicenda.

Uso (dalla cartella sorgenti/; su Windows `python` al posto di `python3`):
  python3 codice/processa_slide.py [--pacco NOME] init slide1.pdf|.pptx|.docx [altre ...] [--blocco 10]
  python3 codice/processa_slide.py [--pacco NOME] prossimo [--dpi 60] [--senza-immagini] [--senza-figure]
  python3 codice/processa_slide.py fatto "argomento; file .tex scritto; note"
  python3 codice/processa_slide.py ritaglia FILE.pdf PAGINA x0 y0 x1 y1 [--dpi 220] [--bianco X0 Y0 X1 Y1]...   # figura vettoriale o con trasparenza
  python3 codice/processa_slide.py stato
  python3 codice/processa_slide.py mappa      # tabella pagine -> argomento

Ciclo per ogni blocco:  prossimo -> leggi testo (e immagini) -> scrivi il .tex -> fatto.
`prossimo` ESTRAE da solo le immagini incorporate nelle pagine del blocco (esclusi loghi e icone ripetuti)
in  sorgenti/figure/  e le elenca per pagina: vanno usate con \\slidefig. Per le figure disegnate in
vettoriale (nessuna immagine incorporata) o con sfondo trasparente usa `ritaglia`, con coordinate in
percentuale della pagina (0-100). Con `--bianco X0 Y0 X1 Y1` (in % del ritaglio, ripetibile; serve Pillow)
copri di bianco formule o testo da non lasciare come immagine: le formule vanno scritte in LaTeX.
`init` accetta anche PPTX/PPT/ODP, DOC/DOCX/ODT/RTF, XLS/XLSX/ODS: li converte in PDF con LibreOffice (in materiali/convertiti/).
Richiede poppler-utils (pdfinfo, pdftotext, pdftoppm) e, per i file Office, libreoffice.
"""
import argparse, json, os, platform, shutil, subprocess, sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):          # console Windows: stampa sempre UTF-8
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
SISTEMA = platform.system()                      # "Linux", "Windows", "Darwin"

MATERIALI = Path(__file__).resolve().parents[2] / "materiali"
STATO = MATERIALI / "avanzamento.json"
RENDER = MATERIALI / "render"
FIGURE = Path(__file__).resolve().parents[1] / "figure"       # sorgenti/figure/
CONVERTITI = MATERIALI / "convertiti"
ESTENSIONI_OFFICE = {".pptx", ".ppt", ".pps", ".ppsx", ".odp",      # presentazioni
                     ".docx", ".doc", ".odt", ".rtf",                 # documenti
                     ".xlsx", ".xls", ".ods"}                         # fogli di calcolo


def trova_soffice():
    """LibreOffice: nel PATH, altrimenti nei percorsi standard di Windows/macOS."""
    trovato = shutil.which("soffice") or shutil.which("libreoffice")
    if trovato:
        return trovato
    candidati = [
        os.path.join(os.environ.get(v, ""), "LibreOffice", "program", "soffice.exe")
        for v in ("ProgramFiles", "ProgramFiles(x86)", "LOCALAPPDATA")
    ] + ["/Applications/LibreOffice.app/Contents/MacOS/soffice"]
    return next((c for c in candidati if c and os.path.exists(c)), None)


def verifica_poppler():
    mancanti = [t for t in ("pdfinfo", "pdftotext", "pdftoppm") if not shutil.which(t)]
    if mancanti:
        aiuto = {"Windows": "winget install oschwartz10612.Poppler  (poi riapri il terminale)",
                 "Darwin": "brew install poppler"}.get(SISTEMA, "sudo apt install poppler-utils")
        sys.exit(f"Mancano {', '.join(mancanti)} (poppler). Installa con: {aiuto}\n"
                 "Controllo completo: python strumenti/controlla_ambiente.py (nella radice della repo).")


def in_pdf(f):
    """Restituisce il percorso di un PDF: converte con LibreOffice se il file è un documento Office."""
    f = Path(f).resolve()
    if f.suffix.lower() == ".pdf":
        return f
    if f.suffix.lower() not in ESTENSIONI_OFFICE:
        sys.exit(f"{f.name}: formato non supportato (esporta le slide in PDF; .key: Keynote > Esporta > PDF).")
    # nome univoco per file: lo stesso nome con estensioni diverse (a.doc, a.docx) non deve collidere
    out = CONVERTITI / (f.stem + "-" + f.suffix[1:].lower() + ".pdf")
    if out.exists() and out.stat().st_mtime >= f.stat().st_mtime:
        return out
    soffice = trova_soffice()
    if not soffice:
        aiuto = {"Windows": "winget install TheDocumentFoundation.LibreOffice",
                 "Darwin": "brew install --cask libreoffice"}.get(SISTEMA, "sudo apt install libreoffice-impress")
        sys.exit(f"{f.name}: serve LibreOffice per convertire in PDF. Installa con: {aiuto}")
    CONVERTITI.mkdir(parents=True, exist_ok=True)
    print(f"Converto {f.name} in PDF...")
    subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", str(CONVERTITI), str(f)],
                   check=True, capture_output=True)
    (CONVERTITI / (f.stem + ".pdf")).replace(out)
    if not out.exists():
        sys.exit(f"Conversione di {f.name} fallita.")
    return out


def carica():
    if not STATO.exists():
        sys.exit("Stato assente: lancia prima `init`.")
    return json.loads(STATO.read_text())


def salva(s):
    MATERIALI.mkdir(exist_ok=True)
    STATO.write_text(json.dumps(s, ensure_ascii=False, indent=1))


def npagine(pdf):
    out = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True, encoding="utf-8", errors="replace", check=True).stdout
    return int(next(r.split()[1] for r in out.splitlines() if r.startswith("Pages:")))


def cmd_init(a):
    verifica_poppler()
    if STATO.exists() and not a.forza:
        sys.exit(f"{STATO} esiste già (usa --forza per ricominciare, perdi lo stato).")
    blocchi = []
    for f in a.pdf:
        p = str(in_pdf(f))
        n = npagine(p)
        for i in range(1, n + 1, a.blocco):
            blocchi.append({"pdf": p, "da": i, "a": min(i + a.blocco - 1, n), "nota": None})
        print(f"{f}: {n} pagine")
    salva({"blocco": a.blocco, "blocchi": blocchi})
    print(f"{len(blocchi)} blocchi da {a.blocco} pagine. Stato: {STATO}")


def estrai_figure(pdf, da, a):
    """Estrae le immagini incorporate nelle pagine da..a (grandi, non ripetute) in sorgenti/figure/."""
    if not shutil.which("pdfimages"):
        return print("\n(pdfimages non trovato: figure non estratte; installa poppler)")
    def righe(f=None, l=None):
        cmd = ["pdfimages", "-list"] + (["-f", str(f), "-l", str(l)] if f else []) + [pdf]
        out = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace").stdout.splitlines()[2:]
        return [r.split() for r in out if len(r.split()) >= 12]
    ripetute = {}                                    # oggetto immagine -> pagine in cui compare (loghi, sfondi)
    for r in righe():
        ripetute.setdefault(r[10], set()).add(r[0])
    FIGURE.mkdir(parents=True, exist_ok=True)
    stem = Path(pdf).stem
    print("\n--- Figure estratte (usale con \\slidefig) ---")
    trovate = False
    for p in range(da, a + 1):
        rr = righe(p, p)
        if not rr:
            continue
        tmp = FIGURE / f".tmp_{stem}_{p}"
        subprocess.run(["pdfimages", "-png", "-f", str(p), "-l", str(p), pdf, str(tmp)], capture_output=True)
        files = sorted(FIGURE.glob(f".tmp_{stem}_{p}-*.png"))
        k = 0
        for i, r in enumerate(rr):
            if i >= len(files):
                break
            w, h = int(r[3]), int(r[4])
            if r[2] != "image" or w < 150 or h < 150 or len(ripetute.get(r[10], ())) >= 3:
                continue                             # maschere, icone, loghi ripetuti
            trasp = i + 1 < len(rr) and rr[i + 1][2] == "smask"
            k += 1
            dest = FIGURE / f"{stem}_p{p:03d}_{k}.png"
            files[i].replace(dest)
            trovate = True
            print(f"pagina {p}: figure/{dest.name} ({w}x{h}px)" + ("  [trasparenza: se appare nera usa `ritaglia`]" if trasp else ""))
        for f in files:
            if f.exists():
                f.unlink()
    if not trovate:
        print("(nessuna immagine incorporata: le figure di queste pagine, se ci sono, sono vettoriali -> `ritaglia`)")


def cmd_ritaglia(a):
    """Ritaglia un riquadro di una pagina (coordinate in % della pagina) in sorgenti/figure/."""
    verifica_poppler()
    pdf = str(Path(a.pdf).resolve())
    info = subprocess.run(["pdfinfo", "-f", str(a.pagina), "-l", str(a.pagina), pdf],
                          capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
    import re
    w, h = [float(v) for v in re.search(r"Page\s+%d size:\s+([\d.]+) x ([\d.]+)" % a.pagina, info).groups()]
    k = a.dpi / 72
    FIGURE.mkdir(parents=True, exist_ok=True)
    nome = f"{Path(pdf).stem}_p{a.pagina:03d}_ritaglio"
    subprocess.run(["pdftoppm", "-f", str(a.pagina), "-l", str(a.pagina), "-r", str(a.dpi), "-png",
                    "-x", str(int(a.x0 / 100 * w * k)), "-y", str(int(a.y0 / 100 * h * k)),
                    "-W", str(int((a.x1 - a.x0) / 100 * w * k)), "-H", str(int((a.y1 - a.y0) / 100 * h * k)),
                    "-singlefile", pdf, str(FIGURE / nome)], check=True)
    if a.bianco:
        try:
            from PIL import Image, ImageDraw
        except ImportError:
            sys.exit("Per --bianco serve Pillow: pip install pillow")
        f = FIGURE / (nome + ".png")
        im = Image.open(f).convert("RGB")
        d = ImageDraw.Draw(im)
        for x0, y0, x1, y1 in a.bianco:
            d.rectangle((x0 / 100 * im.width, y0 / 100 * im.height, x1 / 100 * im.width, y1 / 100 * im.height), fill="white")
        im.save(f)
    print(f"Creato {FIGURE / (nome + '.png')}: aprilo per verificare che la figura sia intera, altrimenti allarga il riquadro.")


def cmd_prossimo(a):
    verifica_poppler()
    s = carica()
    ix = next((i for i, b in enumerate(s["blocchi"]) if b["nota"] is None), None)
    if ix is None:
        return print("Tutti i blocchi sono completati.")
    b = s["blocchi"][ix]
    precedenti = [x for x in s["blocchi"][:ix] if x["nota"]][-3:]
    print(f"=== BLOCCO {ix + 1}/{len(s['blocchi'])}: {Path(b['pdf']).name} pagine {b['da']}-{b['a']} ===")
    if precedenti:
        print("--- Contesto dai blocchi precedenti (ultime note) ---")
        for x in precedenti:
            print(f"[{Path(x['pdf']).name} p.{x['da']}-{x['a']}] {x['nota']}")
    for p in range(b["da"], b["a"] + 1):
        t = subprocess.run(["pdftotext", "-layout", "-f", str(p), "-l", str(p), b["pdf"], "-"],
                           capture_output=True, text=True, encoding="utf-8", errors="replace").stdout.strip()
        print(f"\n--- pagina {p} ---\n{t if t else '(nessun testo: contenuto in immagine)'}")
    if not a.senza_immagini:
        RENDER.mkdir(parents=True, exist_ok=True)
        for old in RENDER.glob("*.png"):
            old.unlink()
        subprocess.run(["pdftoppm", "-r", str(a.dpi), "-png", "-f", str(b["da"]), "-l", str(b["a"]),
                        b["pdf"], str(RENDER / "p")], check=True)
        print(f"\nImmagini del blocco in {RENDER}/ (aprile solo per pagine con formule o schemi).")
    if not a.senza_figure:
        estrai_figure(b["pdf"], b["da"], b["a"])
    print("\nOra scrivi il .tex di questo blocco, poi: processa_slide.py fatto \"nota\"")


def cmd_fatto(a):
    s = carica()
    ix = next((i for i, b in enumerate(s["blocchi"]) if b["nota"] is None), None)
    if ix is None:
        sys.exit("Nessun blocco in sospeso.")
    s["blocchi"][ix]["nota"] = a.nota
    salva(s)
    resto = sum(b["nota"] is None for b in s["blocchi"])
    print(f"Blocco {ix + 1} chiuso. Rimasti: {resto}.")


def cmd_stato(_):
    s = carica()
    fatti = sum(b["nota"] is not None for b in s["blocchi"])
    print(f"{fatti}/{len(s['blocchi'])} blocchi completati.")


def cmd_mappa(_):
    s = carica()
    print("| File | Pagine | Nota |\n|---|---|---|")
    for b in s["blocchi"]:
        print(f"| {Path(b['pdf']).name} | {b['da']}-{b['a']} | {b['nota'] or '(da fare)'} |")


ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("--pacco", help="nome del pacco di slide (stato separato per ogni pacco)")
sp = ap.add_subparsers(dest="cmd", required=True)
i = sp.add_parser("init"); i.add_argument("pdf", nargs="+"); i.add_argument("--blocco", type=int, default=10)
i.add_argument("--forza", action="store_true"); i.set_defaults(f=cmd_init)
p = sp.add_parser("prossimo"); p.add_argument("--dpi", type=int, default=60)
p.add_argument("--senza-immagini", action="store_true"); p.add_argument("--senza-figure", action="store_true"); p.set_defaults(f=cmd_prossimo)
c = sp.add_parser("ritaglia"); c.add_argument("pdf"); c.add_argument("pagina", type=int)
for n_ in ("x0", "y0", "x1", "y1"): c.add_argument(n_, type=float)
c.add_argument("--dpi", type=int, default=220)
c.add_argument("--bianco", nargs=4, type=float, action="append", metavar=("X0", "Y0", "X1", "Y1"))
c.set_defaults(f=cmd_ritaglia)
f = sp.add_parser("fatto"); f.add_argument("nota"); f.set_defaults(f=cmd_fatto)
sp.add_parser("stato").set_defaults(f=cmd_stato)
sp.add_parser("mappa").set_defaults(f=cmd_mappa)
a = ap.parse_args()
if a.pacco:                                      # stato e immagini separati per pacco
    STATO = MATERIALI / f"avanzamento-{a.pacco}.json"
    RENDER = MATERIALI / f"render-{a.pacco}"
a.f(a)
