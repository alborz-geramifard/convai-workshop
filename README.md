# Conversational AI Workshop series (NeurIPS 2017–2019)

Archive site for the three editions of **Conversational AI: Today's Practice and Tomorrow's Potential**, rebuilt from the original workshop pages (originally hosted at alborz-geramifard.com/workshops/, recovered via the Wayback Machine).

- `2017.html`, `2018.html`, `2019.html` – one page per edition; `index.html` redirects to the latest
- `data/convai.json` – all content (description, speakers, schedule, papers, organizers, program committee)
- `files/<edition>/Papers/*.pdf`, `files/<edition>/Slides/*.pdf` – accepted papers and invited-talk slides
- `tools/build.py` – regenerates the HTML pages from the JSON

```sh
python3 tools/build.py
python3 -m http.server 8790   # preview at http://127.0.0.1:8790/
```

## Publish on GitHub Pages

Push this folder to a repo (for example `convai-workshop`), then Settings → Pages → Deploy from branch `main`, folder `/ (root)`. The site will be served at `https://<user>.github.io/convai-workshop/`.
