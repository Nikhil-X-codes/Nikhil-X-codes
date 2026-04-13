"""
Generate animated SVG assets for GitHub README:
  - assets/mac-terminal.svg  → Macbook-style terminal showing "Nikhil Nagar"
  - assets/tech-stack.svg    → Categorised tech icons with float animation
Run:  python generate_svgs.py
"""

import os, base64, urllib.request, urllib.error
from xml.sax.saxutils import escape
from concurrent.futures import ThreadPoolExecutor, as_completed

ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; README-SVG-Generator/1.0)"}


# ─── helpers ────────────────────────────────────────────────────────────────

def fetch_b64(url: str, _depth: int = 0) -> str:
    if _depth > 5:
        return ""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as r:
            data = r.read()
            ct   = r.headers.get("Content-Type", "")
            mime = "image/svg+xml" if ("svg" in ct or url.lower().endswith(".svg")) else "image/png"
            return f"data:{mime};base64,{base64.b64encode(data).decode()}"
    except urllib.error.HTTPError as e:
        if e.code in (301, 302):
            return fetch_b64(e.headers.get("Location", ""), _depth + 1)
        print(f"  HTTP {e.code} — {url}")
        return ""
    except Exception as ex:
        print(f"  Error — {url}: {ex}")
        return ""


def w(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# ─── 1. mac-terminal.svg ────────────────────────────────────────────────────

def generate_terminal() -> None:
    """
    Terminal window that types a command then reveals 'Nikhil Nagar'.
    Uses only opacity/visibility animations — works in all SVG renderers
    including GitHub's image proxy.
    """
    svg = """\
<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 820 290" width="820" height="290">
  <defs>
    <style>
      .m { font-family: "JetBrains Mono","Courier New",monospace; }

      /* fade-in helper — override delay per class */
      @keyframes fi { from{opacity:0} to{opacity:1} }
      @keyframes bl { 0%,100%{opacity:1} 50%{opacity:0} }

      .r0 { opacity:0; animation: fi .01s  0.5s both; }
      .r1 { opacity:0; animation: fi .01s  1.6s both; }
      .r2 { opacity:0; animation: fi .01s  2.0s both; }
      .r3 { opacity:0; animation: fi .01s  3.6s both; }
      .r4 { opacity:0; animation: fi .01s  4.0s both; }
      .r5 { opacity:0; animation: fi .01s  6.0s both; }
      .r6 { opacity:0; animation: fi .01s  6.4s both; }

      /* typing cursor */
      .cur { animation: bl 1s step-end 6.4s infinite; }
    </style>
  </defs>

  <!-- ── window shell ── -->
  <rect x="0" y="0" width="820" height="290" rx="11" ry="11"
        fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>

  <!-- title bar -->
  <rect x="0" y="0" width="820" height="38" rx="11" ry="11" fill="#161b22"/>
  <rect x="0" y="26" width="820" height="12"              fill="#161b22"/>

  <!-- traffic lights -->
  <circle cx="22" cy="19" r="7" fill="#ff5f56"/>
  <circle cx="43" cy="19" r="7" fill="#ffbd2e"/>
  <circle cx="64" cy="19" r="7" fill="#27c93f"/>

  <!-- title -->
  <text class="m" x="410" y="25" text-anchor="middle"
        fill="#6e7681" font-size="12.5">
    bash &#x2014; nikhil@iiit-sonepat: ~/portfolio
  </text>

  <!-- ── Row 0: first prompt ── -->
  <g class="r0">
    <text class="m" x="24"  y="76" fill="#00F0FF" font-size="14" font-weight="700">nikhil@iiit-sonepat</text>
    <text class="m" x="199" y="76" fill="#c9d1d9" font-size="14">:~/portfolio$</text>
  </g>

  <!-- ── Row 1: command appears (simulated typing done) ── -->
  <g class="r1">
    <text class="m" x="310" y="76" fill="#e6edf3" font-size="14"> cat name.txt</text>
  </g>

  <!-- ── Row 2: output — NAME in large cyan ── -->
  <g class="r2">
    <text class="m" x="24" y="128"
          fill="#00F0FF" font-size="38" font-weight="700"
          letter-spacing="2">Nikhil Nagar</text>
  </g>

  <!-- ── Row 3: subtitle under name ── -->
  <g class="r3">
    <text class="m" x="28" y="158" fill="#70A4FF" font-size="14">
      B.Tech CSE &#x2022; IIIT Sonepat &#x2022; AI/ML &amp; Full Stack Dev
    </text>
  </g>

  <!-- ── Row 4: second prompt ── -->
  <g class="r4">
    <text class="m" x="24"  y="196" fill="#00F0FF" font-size="14" font-weight="700">nikhil@iiit-sonepat</text>
    <text class="m" x="199" y="196" fill="#c9d1d9" font-size="14">:~/portfolio$</text>
    <text class="m" x="310" y="196" fill="#e6edf3" font-size="14"> exit 0</text>
  </g>

  <!-- ── Row 5: status bar ── -->
  <g class="r5">
    <text class="m" x="24" y="237" fill="#6e7681" font-size="11">
      &#x25CF; main &#x2713; up to date
      &#x2003;&#x2003;&#x2003;&#x2003;&#x2003;&#x2003;&#x2003;&#x2003;&#x2003;&#x2003;
      &#x2003;&#x2003;&#x2003;&#x2003;&#x2003;&#x2003;&#x2003;&#x2003;&#x2003;
      UTF-8 &#x2022; LF &#x2022; bash 5.2
    </text>
  </g>

  <!-- ── Row 6: final prompt + blinking cursor ── -->
  <g class="r6">
    <text class="m" x="24"  y="265" fill="#00F0FF" font-size="14" font-weight="700">nikhil@iiit-sonepat</text>
    <text class="m" x="199" y="265" fill="#c9d1d9" font-size="14">:~/portfolio$</text>
    <rect class="cur" x="308" y="249" width="9" height="18" fill="#00F0FF"/>
  </g>

</svg>"""

    path = os.path.join(ASSETS_DIR, "mac-terminal.svg")
    w(path, svg)
    print("✓ mac-terminal.svg written")


# ─── 2. tech-stack.svg ──────────────────────────────────────────────────────

CATEGORIES = [
    {
        "title": "Languages &amp; Core",
        "color": "#00F0FF",
        "items": [
            {"label": "C++",    "desc": "DSA &amp; logic",   "url": "https://skillicons.dev/icons?i=cpp"},
            {"label": "C",      "desc": "Systems",            "url": "https://skillicons.dev/icons?i=c"},
            {"label": "Python", "desc": "ML &amp; scripting", "url": "https://skillicons.dev/icons?i=python"},
            {"label": "JS",     "desc": "Node &amp; browser", "url": "https://skillicons.dev/icons?i=js"},
        ],
    },
    {
        "title": "AI / ML Stack",
        "color": "#A78BFA",
        "items": [
            {"label": "Scikit-Learn", "desc": "Modeling",        "url": "https://skillicons.dev/icons?i=sklearn"},
            {"label": "Pandas",       "desc": "Data processing", "url": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/pandas/pandas-original.svg"},
            {"label": "NumPy",        "desc": "Calculations",    "url": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/numpy/numpy-original.svg"},
        ],
    },
    {
        "title": "Web Frontend",
        "color": "#38BDF8",
        "items": [
            {"label": "React",    "desc": "UI library",      "url": "https://skillicons.dev/icons?i=react"},
            {"label": "Next.js",  "desc": "React framework", "url": "https://skillicons.dev/icons?i=nextjs"},
            {"label": "Tailwind", "desc": "Styling",         "url": "https://skillicons.dev/icons?i=tailwind"},
            {"label": "HTML5",    "desc": "Structure",       "url": "https://skillicons.dev/icons?i=html"},
            {"label": "CSS3",     "desc": "Styles",          "url": "https://skillicons.dev/icons?i=css"},
        ],
    },
    {
        "title": "Backend &amp; Databases",
        "color": "#34D399",
        "items": [
            {"label": "Node.js",    "desc": "Evented runtime", "url": "https://skillicons.dev/icons?i=nodejs"},
            {"label": "Express",    "desc": "HTTP layer",       "url": "https://skillicons.dev/icons?i=express"},
            {"label": "MongoDB",    "desc": "Document store",   "url": "https://skillicons.dev/icons?i=mongodb"},
            {"label": "PostgreSQL", "desc": "Relational core",  "url": "https://skillicons.dev/icons?i=postgresql"},
            {"label": "MySQL",      "desc": "SQL database",     "url": "https://skillicons.dev/icons?i=mysql"},
        ],
    },
    {
        "title": "Tools",
        "color": "#FB923C",
        "items": [
            {"label": "Git",     "desc": "Version control", "url": "https://skillicons.dev/icons?i=git"},
            {"label": "GitHub",  "desc": "Collaboration",   "url": "https://skillicons.dev/icons?i=github"},
            {"label": "Postman", "desc": "API testing",     "url": "https://skillicons.dev/icons?i=postman"},
            {"label": "VS Code", "desc": "Editor",          "url": "https://skillicons.dev/icons?i=vscode"},
        ],
    },
]

ICON_SZ  = 50
ROW_H    = 180
HDR_H    = 58
W        = 820
PX       = 30


def generate_tech_stack() -> None:
    # ── parallel icon fetch ──────────────────────────────────────────────────
    all_items = [
        (ci, ii, item)
        for ci, cat in enumerate(CATEGORIES)
        for ii, item  in enumerate(cat["items"])
    ]
    cache: dict[tuple[int, int], str] = {}

    print(f"  Fetching {len(all_items)} icons in parallel …")
    with ThreadPoolExecutor(max_workers=12) as pool:
        futs = {pool.submit(fetch_b64, itm["url"]): (ci, ii) for ci, ii, itm in all_items}
        for fut in as_completed(futs):
            ci, ii = futs[fut]
            cache[(ci, ii)] = fut.result()
            lbl    = CATEGORIES[ci]["items"][ii]["label"]
            status = "ok" if cache[(ci, ii)] else "FAILED"
            print(f"    [{status}] {lbl}")

    # ── build SVG ───────────────────────────────────────────────────────────
    total_h = HDR_H + len(CATEGORIES) * ROW_H + 20
    p: list[str] = []

    p.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"'
        f' viewBox="0 0 {W} {total_h}" width="{W}" height="{total_h}">'
    )

    # CSS
    row_css  = []
    icon_css = []
    for ci, cat in enumerate(CATEGORIES):
        d = 0.1 + ci * 0.18
        row_css.append(f".cat-{ci}{{opacity:0;animation:fs .55s ease {d:.2f}s both}}")
        for ii in range(len(cat["items"])):
            fd  = 0.2 + ci * 0.18 + ii * 0.07
            fa  = 3.2 + ii * 0.5
            fad = ci * 250 + ii * 550
            icon_css.append(
                f".ic-{ci}-{ii}{{opacity:0;"
                f"animation:fs .45s ease {fd:.2f}s both,"
                f"fl {fa:.1f}s ease-in-out {fad}ms infinite}}"
            )

    p.append(f"""\
  <defs>
    <linearGradient id="hg" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%"   stop-color="#00F0FF" stop-opacity=".95"/>
      <stop offset="100%" stop-color="#7B61FF" stop-opacity=".95"/>
    </linearGradient>
    <style>
      .ct{{font-family:system-ui,sans-serif;font-size:16px;font-weight:700}}
      .cl{{font-family:system-ui,sans-serif;font-size:12px;font-weight:600;fill:#c9d1d9}}
      .cd{{font-family:system-ui,sans-serif;font-size:11px;fill:#8b949e}}
      @keyframes fl{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-5px)}}}}
      @keyframes fs{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:translateY(0)}}}}
      {" ".join(row_css)}
      {" ".join(icon_css)}
    </style>
  </defs>""")

    p.append(f'  <rect width="{W}" height="{total_h}" fill="#0d1117"/>')

    # header
    mid = W // 2
    p.append(
        f'  <text x="{mid}" y="36" text-anchor="middle"'
        f' font-family="system-ui,sans-serif" font-size="22" font-weight="800"'
        f' fill="url(#hg)">&#x1F6E0;&#xFE0F; Tech Arsenal</text>'
    )
    p.append(
        f'  <line x1="{PX}" y1="{HDR_H-6}" x2="{W-PX}" y2="{HDR_H-6}"'
        f' stroke="#21262d" stroke-width="1"/>'
    )

    # categories
    y = HDR_H
    for ci, cat in enumerate(CATEGORIES):
        n     = len(cat["items"])
        col_w = (W - PX * 2) // n
        color = cat["color"]

        p.append(f'  <g class="cat-{ci}">')
        p.append(
            f'    <text x="{PX}" y="{y + 22}" class="ct" fill="{color}">'
            f'{cat["title"]}</text>'
        )

        for ii, item in enumerate(cat["items"]):
            ix = PX + ii * col_w + (col_w - ICON_SZ) // 2
            iy = y + 34
            cx = ix + ICON_SZ // 2
            b64 = cache.get((ci, ii), "")

            p.append(f'    <g class="ic-{ci}-{ii}">')
            if b64:
                p.append(
                    f'      <rect x="{ix-7}" y="{iy-7}"'
                    f' width="{ICON_SZ+14}" height="{ICON_SZ+14}"'
                    f' rx="13" ry="13" fill="#161b22" stroke="#21262d" stroke-width="1"/>'
                )
                p.append(
                    f'      <image href="{b64}" x="{ix}" y="{iy}"'
                    f' width="{ICON_SZ}" height="{ICON_SZ}"/>'
                )
            p.append(
                f'      <text x="{cx}" y="{iy+ICON_SZ+20}"'
                f' text-anchor="middle" class="cl">{escape(item["label"])}</text>'
            )
            p.append(
                f'      <text x="{cx}" y="{iy+ICON_SZ+34}"'
                f' text-anchor="middle" class="cd">{item["desc"]}</text>'
            )
            p.append("    </g>")

        p.append("  </g>")

        if ci < len(CATEGORIES) - 1:
            dy = y + ROW_H - 9
            p.append(
                f'  <line x1="{PX}" y1="{dy}" x2="{W-PX}" y2="{dy}"'
                f' stroke="#21262d" stroke-width="1"/>'
            )

        y += ROW_H

    p.append("</svg>")

    path = os.path.join(ASSETS_DIR, "tech-stack.svg")
    w(path, "\n".join(p))
    print("✓ tech-stack.svg written")


# ─── 3. quote-card.svg ──────────────────────────────────────────────────────

def generate_quote_card() -> None:
    svg = """\
<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 820 200" width="820" height="200">
  <defs>
    <!-- background gradient -->
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%"   stop-color="#0d1117"/>
      <stop offset="100%" stop-color="#0a1f3a"/>
    </linearGradient>

    <!-- cyan left-bar gradient -->
    <linearGradient id="bar" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="#00F0FF"/>
      <stop offset="100%" stop-color="#7B61FF"/>
    </linearGradient>

    <!-- shimmer sweep -->
    <linearGradient id="shim" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%"   stop-color="#ffffff" stop-opacity="0"/>
      <stop offset="50%"  stop-color="#ffffff" stop-opacity="0.06"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
      <animateTransform attributeName="gradientTransform" type="translate"
        from="-1 0" to="2 0" dur="3s" repeatCount="indefinite"/>
    </linearGradient>

    <!-- glow filter on quote marks -->
    <filter id="qglow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>

    <style>
      .mono { font-family: "JetBrains Mono","Courier New",monospace; }
      .sans { font-family: system-ui,sans-serif; }

      @keyframes fi   { from{opacity:0;transform:translateY(8px)} to{opacity:1;transform:translateY(0)} }
      @keyframes fi2  { from{opacity:0} to{opacity:1} }
      @keyframes pulse{ 0%,100%{opacity:.7} 50%{opacity:1} }

      .q1  { opacity:0; animation: fi  .6s ease  .3s both; }
      .q2  { opacity:0; animation: fi  .6s ease  .6s both; }
      .qt  { opacity:0; animation: fi  .7s ease 1.0s both; }
      .ql2 { opacity:0; animation: fi  .7s ease 1.5s both; }
      .attr{ opacity:0; animation: fi2 .8s ease 2.2s both; }
      .bar { animation: pulse 3s ease-in-out infinite; }
    </style>
  </defs>

  <!-- card background -->
  <rect width="820" height="200" rx="10" ry="10" fill="url(#bg)"
        stroke="#21262d" stroke-width="1.5"/>

  <!-- shimmer overlay -->
  <rect width="820" height="200" rx="10" ry="10" fill="url(#shim)"/>

  <!-- left accent bar -->
  <rect class="bar" x="0" y="0" width="5" height="200" rx="3" ry="3"
        fill="url(#bar)"/>

  <!-- large opening quote mark -->
  <text class="q1 sans" x="32" y="75"
        fill="#00F0FF" font-size="72" font-weight="900"
        opacity="0.18" filter="url(#qglow)">"</text>

  <!-- quote line 1 -->
  <text class="qt mono" x="32" y="92"
        fill="#e6edf3" font-size="16" font-weight="500">
    "A mistake is only an error, it becomes a mistake when you fail to correct it."
  </text>

  <!-- quote line 2 (attribution) -->
  <g class="attr">
    <line x1="32" y1="118" x2="120" y2="118"
          stroke="url(#bar)" stroke-width="1.5"/>
    <text class="sans" x="130" y="122"
          fill="#70A4FF" font-size="14" font-weight="600">
      &#x2014;&#x2002;John Lennon
    </text>
    <text class="mono" x="285" y="122"
          fill="#6e7681" font-size="12">
      &#x2022; Linux Kernel Mailing List, Aug 25, 2008
    </text>
  </g>

  <!-- closing quote mark -->
  <text class="q2 sans" x="765" y="155"
        fill="#7B61FF" font-size="72" font-weight="900"
        opacity="0.15" filter="url(#qglow)">"</text>

  <!-- bottom tag -->
  <g class="ql2">
    <rect x="32" y="148" width="130" height="24" rx="4" ry="4"
          fill="#161b22" stroke="#30363d" stroke-width="1"/>
    <text class="mono" x="42" y="164"
          fill="#00F0FF" font-size="11.5" font-weight="600">
      &#x25CF; Dev Quote of the Day
    </text>
  </g>
</svg>
"""
    path = os.path.join(ASSETS_DIR, "quote-card.svg")
    w(path, svg)
    print("✓ quote-card.svg written")


# ─── entry point ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Generating mac-terminal.svg …")
    generate_terminal()

    print("\nGenerating quote-card.svg …")
    generate_quote_card()

    print("\nGenerating tech-stack.svg …")
    generate_tech_stack()

    print("\n✅ Done — all SVGs are in assets/")
