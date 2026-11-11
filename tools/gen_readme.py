"""Generate README.md for BorePilot from tools/gen_pages.py data and hardware/bom CSV.
Run from the repo root:  python -X utf8 -I tools/gen_readme.py"""
import os, sys, io, contextlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
with contextlib.redirect_stdout(io.StringIO()):
    import gen_pages as G

ROOT = G.ROOT


def bom_section(sid):
    groups, order = {}, []
    for sec, ref, name, c, q, note in G.P:
        if sec != sid:
            continue
        if c not in groups:
            groups[c] = {"refs": [], "q": 0, "names": []}
            order.append(c)
        g = groups[c]
        g["refs"].append(ref)
        g["q"] += q
        short = name.split(",")[0].replace("OPTIONAL ", "").replace(" (optional)", "").replace(" (DNP)", "")
        if short not in g["names"]:
            g["names"].append(short)
    rows = []
    for c in order:
        g = groups[c]
        mpn = G.info(c)[0]
        opt = " *(optional)*" if any("OPTIONAL" in p[2] or "optional" in p[2] or "DNP" in p[2] for p in G.P if p[3] == c and p[0] == sid and p[1] in g["refs"]) else ""
        fn = " / ".join(g["names"][:2]) if len(g["names"]) > 1 else g["names"][0]
        link = f"[{c}](https://www.lcsc.com/product-detail/{c}.html)" if c.startswith("C") and c != "TBD" else c
        rows.append(f"| {', '.join(g['refs'])} | {g['q']} | {fn}{opt} | `{mpn}` | {link} |")
    return "| Ref | Qty | Function | Part | LCSC |\n|---|---:|---|---|---|\n" + "\n".join(rows) + "\n"


def bom_all():
    out = []
    for sid, title, col, desc in G.S:
        out.append(f"**{title}**  \n<sub>{desc}</sub>\n\n{bom_section(sid)}")
    return "\n".join(out)


def cost():
    tot, n = 0.0, 0
    for r in G.rows:
        try:
            tot += float(r["Unit price USD"]) * int(r["Qty"])
            n += int(r["Qty"])
        except ValueError:
            pass
    return tot, n


tot, nparts = cost()

TPL = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "readme_template.md"), encoding="utf-8").read()
README = TPL.replace("{nparts}", str(nparts)).replace("{tot:.2f}", f"{tot:.2f}").replace("{bom_all()}", bom_all())

open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8", newline="\n").write(README)
print("README.md", len(README))
