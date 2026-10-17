# Profile asset source

Every SVG in `assets/` is generated from this folder, so text, systems and versions can change without touching artwork by hand.

```sh
pip install -r assets/src/requirements.txt
python assets/src/build.py              # rebuild everything
python assets/src/build.py hero         # or one target: hero, headers, dossier, stack,
                                        # systems, repos, philosophy, footer, discord, atlas
```

| File | What it holds |
|---|---|
| `build.py` | Entry point and the glyph atlas used by the telemetry renderer |
| `hero.py` | The animated skyline banner |
| `sections.py` | Section headers, developer file, stack, systems, repositories, philosophy, footer. **Content lives here** (`ROLES`, `STACK`, `SYSTEMS`, `REPOS`, `PRINCIPLES`) |
| `svgkit.py` | Text-to-outline engine, Reborn colour tokens, shared drawing helpers |
| `icons.py` | Vendored Lucide (ISC) and Simple Icons (CC0) path data |
| `fonts/` | Sora and Manrope from `reborn_ui`, plus JetBrains Mono, all under the SIL OFL 1.1 (licences alongside) |
| `brand/` | The Project Reborn wordmark and R mark, and the Rebornium item art, used as supplied |

## How the SVGs stay reliable on GitHub

- GitHub shows README images through `<img>`, which can't load web fonts or scripts. All text is converted to vector outlines (shaped with HarfBuzz, so kerning matches the real fonts), and each glyph is defined once and reused with `<use>`.
- Motion is plain CSS keyframes inside each SVG, plus SMIL for the typing line. There's no JavaScript and nothing external, and every file honours `prefers-reduced-motion`.
- Key content never depends on an animation: frame zero of every asset is complete, so static renderers still show the full design.

## Telemetry

`assets/telemetry.svg` is not built here. `.github/scripts/telemetry.mjs` draws it from the real GitHub contribution calendar (GraphQL, falling back to the public contributions page) using `glyphs.json` from `build.py atlas`. `.github/workflows/telemetry.yml` runs it daily at 00:17 AEST, on demand, and whenever the renderer changes. If GitHub can't be reached, the run fails and the last good console stays up. It never invents numbers.

Private work only shows up if **Settings → Public profile → Contributions & activity → Include private contributions on my profile** is on, or if a `TELEMETRY_TOKEN` secret (classic PAT with `read:user`) is added to the repository.
