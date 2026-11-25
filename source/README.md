# How the profile sheets are made

The profile README is a set of SVG sheets in `assets/`, one light and one dark version of each. The text in them is outlined type, so it cannot be edited by hand. Change the words or numbers in `sheets.py` and redraw.

```
cd source
npm install
pip install fonttools brotli uharfbuzz
python3 sheets.py
```

That rewrites every file in `assets/`. `kit.py` holds the type, colours, walls and doors. `sheets.py` holds the content of each sheet.

Typefaces: Instrument Sans and Playfair, both under the SIL Open Font License.
