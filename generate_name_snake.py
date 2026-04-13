"""
generate_name_snake.py  —  Pac-Man eating dot-matrix NIKHIL
"""
import os, math

ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

CELL = 14; GAP = 4; STEP = CELL + GAP   # 18 px

PATTERNS = {
    'N': [[1,0,0,0,1],[1,1,0,0,1],[1,0,1,0,1],[1,0,0,1,1],[1,0,0,0,1]],
    'I': [[1,1,1,1,1],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[1,1,1,1,1]],
    'K': [[1,0,0,1,0],[1,0,1,0,0],[1,1,0,0,0],[1,0,1,0,0],[1,0,0,1,0]],
    'H': [[1,0,0,0,1],[1,0,0,0,1],[1,1,1,1,1],[1,0,0,0,1],[1,0,0,0,1]],
    'L': [[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0],[1,1,1,1,1]],
}

NAME         = "NIKHIL"
LTR_COLS     = 5
LTR_GAP      = 2
TOTAL_COLS   = len(NAME)*LTR_COLS + (len(NAME)-1)*LTR_GAP   # 40
CANVAS_W     = 820
PAD_X        = (CANVAS_W - TOTAL_COLS * STEP) // 2          # 50
BG_R         = 2          # extra bg rows above/below
LETTER_ROWS  = 5
PAD_Y        = BG_R * STEP + 6
CANVAS_H     = (LETTER_ROWS + 2*BG_R) * STEP + 24

DURATION     = 8.0
LOOP_DUR     = DURATION + 1.5    # pause before restart

BG   = "#0d1117"; GF = "#161b22"; GS = "#21262d"
LF   = "#3fb950"; LS = "#2ea043"; PC = "#f5c518"


def lcs(li):  return li * (LTR_COLS + LTR_GAP)
def gpx(col, row):  return PAD_X+col*STEP+CELL/2, PAD_Y+row*STEP+CELL/2


def build():
    """Row-major serpentine traversal (row 0 → L-R, row 1 → R-L, ...)."""
    pts, meta = [], []
    for row in range(LETTER_ROWS):
        rp, rm = [], []
        for li, letter in enumerate(NAME):
            pat = PATTERNS[letter]
            for col in range(LTR_COLS):
                if pat[row][col]:
                    cx, cy = gpx(lcs(li)+col, row)
                    rp.append((cx,cy)); rm.append((li,row,col))
        if row % 2 == 1:
            rp.reverse(); rm.reverse()
        pts.extend(rp); meta.extend(rm)
    return pts, meta


def cumlen(pts):
    d = [0.0]
    for i in range(1, len(pts)):
        d.append(d[-1] + math.hypot(pts[i][0]-pts[i-1][0], pts[i][1]-pts[i-1][1]))
    return d


def generate():
    wpts, meta = build()
    segs  = cumlen(wpts)
    total = segs[-1]
    N     = len(wpts)

    # Path string
    path_d = f"M {wpts[0][0]:.1f},{wpts[0][1]:.1f}" + \
             "".join(f" L {p[0]:.1f},{p[1]:.1f}" for p in wpts[1:])

    # Per-waypoint: fraction of LOOP_DUR when Pac-Man arrives
    def tf(i):   # time fraction [0,1] within LOOP_DUR
        return max(0.003, segs[i]/total * DURATION/LOOP_DUR)

    # animateMotion keyPoints / keyTimes (distance-based, + hold at end)
    kp = ";".join(f"{segs[i]/total:.4f}" for i in range(N)) + ";1.0000"
    kt = ";".join(f"{tf(i):.4f}"         for i in range(N)) + ";1.0000"

    # Pac-Man path (facing right, mouth ~38°)
    R  = CELL//2 + 4   # 11 px
    mo = math.radians(38)
    m1x,m1y = R*math.cos(-mo), R*math.sin(-mo)
    m2x,m2y = R*math.cos( mo), R*math.sin( mo)
    pac = f"M 0,0 L {m1x:.2f},{m1y:.2f} A {R},{R} 0 1 1 {m2x:.2f},{m2y:.2f} Z"

    # eat-time lookup keyed by (li,row,col)
    eat = {meta[i]: tf(i) for i in range(N)}

    L = []
    L.append(f'<svg xmlns="http://www.w3.org/2000/svg"'
             f' viewBox="0 0 {CANVAS_W} {CANVAS_H}"'
             f' width="{CANVAS_W}" height="{CANVAS_H}">')
    L.append('  <defs>')
    L.append('    <filter id="gl" x="-25%" y="-25%" width="150%" height="150%">'
             '<feGaussianBlur stdDeviation="2.2" result="b"/>'
             '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>'
             '</filter>')
    L.append(f'    <path id="mp" d="{path_d}"/>')
    L.append('  </defs>')

    # Background
    L.append(f'  <rect width="{CANVAS_W}" height="{CANVAS_H}" fill="{BG}"/>')

    # Full background grid (dim cells)
    for row in range(-BG_R, LETTER_ROWS+BG_R):
        for col in range(-1, TOTAL_COLS+1):
            cx,cy = gpx(col, row)
            if 0 < cx < CANVAS_W and 0 < cy < CANVAS_H:
                x,y = cx-CELL/2, cy-CELL/2
                L.append(f'  <rect x="{x:.0f}" y="{y:.0f}" width="{CELL}" height="{CELL}"'
                         f' rx="3" fill="{GF}" stroke="{GS}" stroke-width="1"/>')

    # Letter dots with SMIL eat animation (loops every LOOP_DUR seconds)
    for li, letter in enumerate(NAME):
        pat = PATTERNS[letter]
        for row in range(LETTER_ROWS):
            for col in range(LTR_COLS):
                if not pat[row][col]: continue
                cx,cy = gpx(lcs(li)+col, row)
                x,y   = cx-CELL/2, cy-CELL/2
                et    = eat.get((li,row,col), 0.9)
                et2   = min(et + 0.009, 0.999)   # eat lasts ~0.08s
                kts   = f"0;{et:.4f};{et2:.4f};1"
                # values: visible → visible → invisible → invisible
                # on next loop cycle the animation resets to values[0]=1 automatically
                L.append(
                    f'  <rect x="{x:.0f}" y="{y:.0f}" width="{CELL}" height="{CELL}"'
                    f' rx="3" fill="{LF}" stroke="{LS}" stroke-width="1" filter="url(#gl)">'
                    f'<animate attributeName="opacity" values="1;1;0;0"'
                    f' keyTimes="{kts}" dur="{LOOP_DUR:.1f}s"'
                    f' repeatCount="indefinite" calcMode="linear"/>'
                    f'</rect>'
                )

    # Pac-Man  
    L.append(f'  <path d="{pac}" fill="{PC}" filter="url(#gl)">')
    L.append(f'    <animateMotion dur="{LOOP_DUR:.1f}s" repeatCount="indefinite"'
             f' rotate="auto" calcMode="linear" keyPoints="{kp}" keyTimes="{kt}">')
    L.append(f'      <mpath href="#mp"/>')
    L.append(f'    </animateMotion>')
    L.append(f'  </path>')
    L.append('</svg>')

    out = os.path.join(ASSETS_DIR, "name-snake.svg")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print(f"name-snake.svg: {N} dots, path={int(total)}px, loop={LOOP_DUR}s")


if __name__ == "__main__":
    generate()
