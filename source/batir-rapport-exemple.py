#!/usr/bin/env python3
"""THE SAMPLE REPORT on the Screening page (29/09): the public example record of the screening tool
(exemple/contreparties-exemple.screening.json, 30 invented counterparties of an invented forwarder) rendered by the
same renderer that makes client reports, so the sample is the product and nothing else.
Writes source/rapports/screening-sample-report.pdf, its sidecar .json (seal, date, counts read from the record), and
source/rendus/rapport-exemple.webp (page 1). The assembler refuses a sidecar whose seal no longer matches the record."""
import json, pathlib, subprocess, sys
BASE = pathlib.Path(__file__).parent
MAISON = pathlib.Path.home() / "Documents"
RECORD = MAISON / "cascade-screening" / "exemple" / "contreparties-exemple.screening.json"
RENDU = MAISON / "cascade-portes" / "outils" / "rapport.py"
d = json.loads(RECORD.read_text())
(BASE / "rapports").mkdir(exist_ok=True); tmp = BASE / "rapports" / "_page.html"
subprocess.run([sys.executable, str(RENDU), str(RECORD), str(tmp)], check=True, capture_output=True)
pdf, webp = BASE / "rapports" / "screening-sample-report.pdf", BASE / "rendus" / "rapport-exemple.webp"
subprocess.run(["node", str(BASE / "capturer-rapport.mjs"), str(tmp), str(pdf), str(webp)], check=True)
tmp.unlink()
t = d["totaux"]
side = {"sceau": d["empreinte"], "emis": d["emisLe"][:10], "client": d["client"], "lignes": t["lignes"], "forts": t["forts"],
        "possibles": t["possibles"], "sans": t["sansCorrespondance"], "commit": d["commit"],
        "listes": min(l["telechargeLe"][:10] for l in d["listes"]), "source": "cascade-screening/exemple/contreparties-exemple.screening.json"}
(BASE / "rapports" / "screening-sample-report.json").write_text(json.dumps(side, indent=2) + "\n")
print("sample report:", pdf.stat().st_size // 1024, "KB pdf,", webp.stat().st_size // 1024, "KB page image, seal", side["sceau"])
