# How the profile scenes are made

The profile README is ten animated SVG scenes in `assets/`. The text in them is outlined type, so it cannot be edited by hand. Change the words, numbers or cities in `scenes.py` and redraw.

```
cd source
npm install
pip install fonttools brotli uharfbuzz shapely
python3 scenes.py
```

That rewrites every file in `assets/`. To redraw one scene, name it: `python3 scenes.py tour`.

- `scenes.py` holds each scene and its content. The 2025 and 2026 rooms are the `R25` and `R26` lists; the calendar on the map is the `YEARS` list.
- `kit2.py` holds the colours, the isometric drawing helpers and the little figures.
- `kit.py` turns text into outlines.

Typefaces: Instrument Sans and Playfair, both under the SIL Open Font License. Map data: Natural Earth, via world-atlas.
