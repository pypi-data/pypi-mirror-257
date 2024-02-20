from pathlib import Path
import bibtexparser


def RichBibtextReader(source_path):
    source_path = Path(source_path)
    library = bibtexparser.parse_file(str(source_path))
    json_items = []
    for entry in library.entries:
        json_bl = {k: v for k, v in entry.items()}
        if "note" in json_bl:
            for _kv in json_bl["note"].split("; "):
                kv = _kv.split(":", maxsplit=1)
                if len(kv) == 2:
                    json_bl[kv[0].strip()] = kv[1].strip()
        json_items.append(json_bl)
    return json_items
