import json, re, urllib.request

URL = "https://raw.githubusercontent.com/voluntosmister-cell/Voluntos-Mister/main/AcEStREAM%20iDs.w3u"
txt = urllib.request.urlopen(URL, timeout=30).read().decode("utf-8")
txt = re.sub(r",(\s*[}\]])", r"\1", txt)  # quita comas finales
data = json.loads(txt)

out = []
for g in data.get("groups", []):
    for s in g.get("stations", []):
        url = (s.get("url") or "").strip()
        if not url.startswith("acestream://"):
            continue
        h = url[len("acestream://"):].strip()
        if not re.fullmatch(r"[0-9a-fA-F]{40}", h):
            continue
        name = (s.get("name") or "").strip()
        info = (s.get("info") or "").strip()
        if info and not info.startswith("["):
            name += " " + info
        out.append({"name": name, "id": h})

with open("lista.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
