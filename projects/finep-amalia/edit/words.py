import json, sys, pathlib
src, a, b = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
d = json.load(open(pathlib.Path("transcripts")/f"{src}.json"))
for w in d["words"]:
    if w.get("type") != "word": continue
    if w["end"] >= a and w["start"] <= b:
        print(f'{w["start"]:8.2f}-{w["end"]:7.2f}  {w["text"]}')
