"""
generate_pacman_name.py  --  Animated Pac-Man eating dot-matrix NIKHIL (left to right)

Approach:
 - Pac-Man moves via animateMotion on a horizontal path.
 - Mouth chomps via animate on 'd' attribute (discrete, open/close cycle).
 - Each dot rect has an opacity animation: visible then eaten when Pac-Man reaches it.
 - Everything loops endlessly.
"""
import os, math

ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

# ── Grid constants ──────────────────────────────────────────────────────────
CELL   = 13     # dot square size px
GAP    = 5      # gap between dots
STEP   = CELL + GAP   # 18 px per cell

LETTER_ROWS = 5
LTR_COLS    = 5
LTR_GAP     = 2   # gap-columns between letters

NAME = "NIKHIL"

PATTERNS = {
    'N': [[1,0,0,0,1],[1,1,0,0,1],[1,0,1,0,1],[1,0,0,1,1],[1,0,0,0,1]],
    'I': [[1,1,1,1,1],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[1,1,1,1,1]],
    'K': [[1,0,0,1,0],[1,0,1,0,0],[1,1,0,0,0],[1,0,1,0,0],[1,0,0,1,0]],
    'H': [[1,0,0,0,1],[1,0,0,0,1],[1,1,1,1,1],[1,0,0,0,1],[1,0,0,0,1]],
    'L': [[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0],[1,1,1,1,1]],
}

# ── Canvas ────────────────────────────────────────────────────────────────
TOTAL_COLS = len(NAME) * LTR_COLS + (len(NAME) - 1) * LTR_GAP   # 36

PAD_LEFT  = 44     # Pac-Man starts here (needs at least PAC_R+gap)
PAD_RIGHT = 44     # same on the right
PAD_TOP   = 22     # room above letters
PAD_BOT   = 22     # room below letters

CANVAS_W = PAD_LEFT + TOTAL_COLS * STEP + PAD_RIGHT
CANVAS_H = PAD_TOP  + LETTER_ROWS * STEP + PAD_BOT

# ── Timing ────────────────────────────────────────────────────────────────
TRAVEL    = 7.0    # seconds for Pac-Man to cross from left edge to right edge
PAUSE     = 2.0    # seconds of pause at end before restarting
LOOP_DUR  = TRAVEL + PAUSE

CHOMP_HZ  = 4.5   # chomps per second (open-close-open = 1 chomp)

# ── Colors ────────────────────────────────────────────────────────────────
BG    = "#0d1117"
GRID  = "#161b22"
GBRD  = "#21262d"
DOT_F = "#3fb950"
DOT_S = "#2ea043"
PAC_C = "#f5c518"
EYE_C = "#111111"

# ── Helpers ───────────────────────────────────────────────────────────────
def col_cx(global_col):
    return PAD_LEFT + global_col * STEP + CELL / 2

def row_cy(row):
    return PAD_TOP + row * STEP + CELL / 2

def letter_col_start(li):
    return li * (LTR_COLS + LTR_GAP)


def generate():
    # ── Pac-Man geometry ──────────────────────────────────────────────────
    PAC_R  = CELL // 2 + 5   # radius 11

    # Pac-Man moves along the vertical midline of the letters
    pac_y  = PAD_TOP + (LETTER_ROWS * STEP) / 2

    # Pac-Man start/end x (centre of Pac-Man)
    # Start inside left pad, end inside right pad so it stays in canvas
    pac_x0 = PAC_R + 4                           # just inside left edge
    pac_x1 = CANVAS_W - PAC_R - 4               # just inside right edge

    def mouth_path(angle_deg):
        """Pac-Man wedge path centred at 0,0 facing right."""
        a = math.radians(angle_deg)
        x1 = PAC_R * math.cos(-a);  y1 = PAC_R * math.sin(-a)
        x2 = PAC_R * math.cos(a);   y2 = PAC_R * math.sin(a)
        large = 1 if (360 - 2 * angle_deg) > 180 else 1
        return f"M 0,0 L {x1:.3f},{y1:.3f} A {PAC_R},{PAC_R} 0 {large} 1 {x2:.3f},{y2:.3f} Z"

    open_path  = mouth_path(35)    # wide open
    half_path  = mouth_path(15)    # half open
    close_path = mouth_path(2)     # nearly closed

    # ── Build chomp keyTimes + values ─────────────────────────────────────
    # One chomp cycle = 1/CHOMP_HZ seconds: open → close → open
    # We sample at 2× chomp rate (frames: open, close, open, close…)
    # The last keyTime must be ≤ travel_frac so mouth stops chomping at pause
    travel_frac     = TRAVEL / LOOP_DUR
    half_chomp_dur  = 1.0 / (CHOMP_HZ * 2)   # seconds between frames
    frames = []
    t = 0.0
    toggle = True   # True = open, False = close
    while t <= TRAVEL:
        frac = t / LOOP_DUR
        frames.append((frac, open_path if toggle else close_path))
        t      += half_chomp_dur
        toggle  = not toggle
    # At end (during pause) stay closed
    frames.append((travel_frac + 0.001, close_path))
    frames.append((1.0, close_path))

    mouth_kt  = ";".join(f"{f[0]:.5f}" for f in frames)
    mouth_val = ";".join(f[1]          for f in frames)

    # ── Collect dots ──────────────────────────────────────────────────────
    dots = []
    for li, letter in enumerate(NAME):
        pat = PATTERNS[letter]
        for row in range(LETTER_ROWS):
            for col in range(LTR_COLS):
                if pat[row][col]:
                    gc = letter_col_start(li) + col
                    cx = col_cx(gc)
                    cy = row_cy(row)
                    dots.append((cx, cy))

    # ── Write SVG ─────────────────────────────────────────────────────────
    L = []
    L.append(
        f'<svg xmlns="http://www.w3.org/2000/svg"'
        f' viewBox="0 0 {CANVAS_W} {CANVAS_H}"'
        f' width="{CANVAS_W}" height="{CANVAS_H}">'
    )

    # defs
    L.append('  <defs>')
    L.append(
        '    <filter id="gl" x="-40%" y="-40%" width="180%" height="180%">'
        '<feGaussianBlur in="SourceGraphic" stdDeviation="2.2" result="b"/>'
        '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>'
        '</filter>'
    )
    L.append(
        '    <filter id="yg" x="-80%" y="-80%" width="260%" height="260%">'
        '<feGaussianBlur in="SourceGraphic" stdDeviation="4" result="b"/>'
        '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>'
        '</filter>'
    )
    # Motion path — straight horizontal line at pac_y
    L.append(
        f'    <path id="mp" d="M {pac_x0},{pac_y:.2f} L {pac_x1},{pac_y:.2f}"/>'
    )
    L.append('  </defs>')

    # Background
    L.append(f'  <rect width="{CANVAS_W}" height="{CANVAS_H}" fill="{BG}" rx="6"/>')

    # Background grid (subtle dim cells for the whole letter area + margin)
    for row in range(-1, LETTER_ROWS + 1):
        for col in range(-1, TOTAL_COLS + 1):
            gx = PAD_LEFT + col * STEP
            gy = PAD_TOP  + row * STEP
            # only draw cells that are partially inside canvas
            if gx + CELL > 0 and gx < CANVAS_W and gy + CELL > 0 and gy < CANVAS_H:
                L.append(
                    f'  <rect x="{gx}" y="{gy}" width="{CELL}" height="{CELL}"'
                    f' rx="3" fill="{GRID}" stroke="{GBRD}" stroke-width="1"/>'
                )

    # ── Dots with eat-animation ───────────────────────────────────────────
    # Pac-Man centre x at time t_sec = pac_x0 + (pac_x1 - pac_x0) * t_sec / TRAVEL
    # Dot at cx is "eaten" when Pac-Man centre reaches cx
    x_range = pac_x1 - pac_x0

    for idx, (cx, cy) in enumerate(dots):
        x = cx - CELL / 2
        y = cy - CELL / 2

        # time (0..1 of LOOP_DUR) when Pac-Man centre aligns with dot
        eat_t_sec  = (cx - pac_x0) / x_range * TRAVEL
        eat_frac   = eat_t_sec / LOOP_DUR
        eat_frac   = min(max(eat_frac, 0.0), 0.98)
        after_frac = min(eat_frac + 0.03, 0.99)

        kts  = f"0;{eat_frac:.5f};{after_frac:.5f};1"
        vals = "1;1;0;0"

        L.append(
            f'  <rect x="{x:.1f}" y="{y:.1f}" width="{CELL}" height="{CELL}"'
            f' rx="3" fill="{DOT_F}" stroke="{DOT_S}" stroke-width="1"'
            f' filter="url(#gl)">'
            f'<animate attributeName="opacity" values="{vals}"'
            f' keyTimes="{kts}" dur="{LOOP_DUR:.3f}s"'
            f' repeatCount="indefinite" calcMode="linear"/>'
            f'</rect>'
        )

    # ── Pac-Man body with animateMotion ───────────────────────────────────
    # keyPoints/keyTimes: 0→1 during TRAVEL, then hold at 1 during PAUSE
    kp = f"0;1;1"
    kt = f"0;{travel_frac:.5f};1"

    ey_offset_x = int(PAC_R * 0.3)
    ey_offset_y = int(-PAC_R * 0.45)

    # Group: body + eye, both get same animateMotion
    L.append(f'  <g id="pac" filter="url(#yg)">')

    # Body path (mouth animates)
    L.append(f'    <path fill="{PAC_C}">')
    L.append(f'      <animate attributeName="d" values="{mouth_val}"')
    L.append(f'        keyTimes="{mouth_kt}" dur="{LOOP_DUR:.3f}s"')
    L.append(f'        repeatCount="indefinite" calcMode="discrete"/>')
    L.append(f'      <animateMotion keyPoints="{kp}" keyTimes="{kt}"')
    L.append(f'        dur="{LOOP_DUR:.3f}s" repeatCount="indefinite"')
    L.append(f'        calcMode="linear" rotate="0">')
    L.append(f'        <mpath href="#mp"/>')
    L.append(f'      </animateMotion>')
    L.append(f'    </path>')

    # Eye (offset from body centre)
    L.append(f'    <circle r="2" fill="{EYE_C}"'
             f' cx="{ey_offset_x}" cy="{ey_offset_y}">')
    L.append(f'      <animateMotion keyPoints="{kp}" keyTimes="{kt}"')
    L.append(f'        dur="{LOOP_DUR:.3f}s" repeatCount="indefinite"')
    L.append(f'        calcMode="linear" rotate="0">')
    L.append(f'        <mpath href="#mp"/>')
    L.append(f'      </animateMotion>')
    L.append(f'    </circle>')

    L.append(f'  </g>')
    L.append('</svg>')

    out = os.path.join(ASSETS_DIR, "pacman-name.svg")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(L))

    print(f"pacman-name.svg saved -> {out}")
    print(f"Canvas: {CANVAS_W}x{CANVAS_H}px | {len(dots)} dots | Loop: {LOOP_DUR}s")


if __name__ == "__main__":
    generate()
