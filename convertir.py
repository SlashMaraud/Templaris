import json
import re
import urllib.request

URL = "https://raw.githubusercontent.com/voluntosmister-cell/Voluntos-Mister/main/AcEStREAM%20iDs.w3u"


def descargar(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=30).read().decode("utf-8")


def titulo(n):
    """Nombre limpio para cruzar con los canales de la web de eventos."""
    n = re.sub(r"\[[^\]]*\]", " ", n)        # quita [1080], [720p]...
    n = re.sub(r"\(\d+\)", " ", n)           # quita (1), (2)...
    n = re.sub(r"\s\d{3,4}p?\s*$", "", n)    # quita " 1080" al final
    n = re.sub(r"^M\.\s+", "Movistar ", n)   # "M. Liga..." -> "Movistar Liga..."
    n = re.sub(r"^M\+\s*", "Movistar ", n)   # "M+ LaLiga" -> "Movistar LaLiga"
    n = re.sub(r"^M\s+", "Movistar ", n)     # "M Deportes" -> "Movistar Deportes"
    return re.sub(r"\s+", " ", n).strip()


def main():
    txt = descargar(URL)
    txt = re.sub(r",(\s*[}\]])", r"\1", txt)  # quita comas finales sobrantes
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
            base = (s.get("name") or "").strip()
            info = (s.get("info") or "").strip()
            nombre = base + (" " + info if info and not info.startswith("[") else "")
            out.append({"name": nombre, "title": titulo(base), "id": h})

    with open("lista.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    print(f"{len(out)} canales escritos en lista.json")


if __name__ == "__main__":
    main()
