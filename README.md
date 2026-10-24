# danuwater.com

Static site served by GitHub Pages from the `main` branch.

- Edit industry sheets in `_src/content/industries.json` and news in `_src/content/news.json`.
- Page text and layout live in `_src/build.py`; styles in `assets/site.css`.
- Run `python3 _src/build.py`, check the result, and commit the generated `index.html` files.
- `/cups/`, `/power-bank/` and `/giveaways/` are hand-built impact pages linked from printed QR codes. Keep these URLs.
- `/newsletter/` redirects to the Google Form sign-up.

Folders starting with `_` are not published.
