#!/usr/bin/env python3
"""Turn one of Adam's Scratch SVG exports into polygon data for the game.

Why polygons and not the bitmap: his rule is a HEAVY constant outline, and an
outline baked into a PNG scales with the sprite -- thin on small pieces, uneven
on stretched ones. With the shape as points the game strokes it in code after
the geometry is final, so the outline is exactly OUT px at any size, stretch or
rotation.

His costumes come out at game scale already: 1 tile = 32 SVG units. So the
points are emitted in game pixels, no rescaling.

    python3 svgcut.py ~/Doggos/Grass.svg grass > pieces-grass.json
"""
import re, sys, json, xml.etree.ElementTree as ET

NS   = '{http://www.w3.org/2000/svg}'
STEP = 10          # samples per cubic segment when flattening
EPS  = 0.35        # point-drop tolerance in game px


def grads(root):
    """id -> (top colour, bottom colour) for the gradients his fills point at."""
    out = {}
    for g in root.iter(NS + 'linearGradient'):
        stops = [s.get('stop-color') for s in g.iter(NS + 'stop')]
        if stops:
            out[g.get('id')] = (stops[0], stops[-1])
    return out


def outer_transform(root):
    for g in root.iter(NS + 'g'):
        t = g.get('transform') or ''
        m = re.match(r'translate\(([-\d.]+),([-\d.]+)\)', t)
        if m:
            return float(m.group(1)), float(m.group(2))
    return 0.0, 0.0


def tokens(d):
    return re.findall(r'[MmLlHhVvCcSsZz]|-?\d*\.?\d+(?:e-?\d+)?', d)


def bez(p0, p1, p2, p3):
    for i in range(1, STEP + 1):
        t = i / STEP; u = 1 - t
        yield (u*u*u*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t*t*t*p3[0],
               u*u*u*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t*t*t*p3[1])


def flatten(d):
    """SVG path -> list of points. Covers the commands Scratch actually emits."""
    tk, i = tokens(d), 0
    pts, cur, start, cmd = [], (0.0, 0.0), (0.0, 0.0), None
    num = lambda: float(tk[i])
    while i < len(tk):
        if re.match(r'[A-Za-z]', tk[i]):
            cmd = tk[i]; i += 1
        rel = cmd.islower()
        c = cmd.upper()
        if c == 'M':
            x, y = num(), float(tk[i+1]); i += 2
            cur = (cur[0]+x, cur[1]+y) if rel else (x, y)
            start = cur; pts.append(cur)
            cmd = 'l' if rel else 'L'          # implicit lineto after moveto
        elif c == 'L':
            x, y = num(), float(tk[i+1]); i += 2
            cur = (cur[0]+x, cur[1]+y) if rel else (x, y)
            pts.append(cur)
        elif c == 'H':
            x = num(); i += 1
            cur = (cur[0]+x, cur[1]) if rel else (x, cur[1])
            pts.append(cur)
        elif c == 'V':
            y = num(); i += 1
            cur = (cur[0], cur[1]+y) if rel else (cur[0], y)
            pts.append(cur)
        elif c == 'C':
            v = [float(t) for t in tk[i:i+6]]; i += 6
            if rel:
                p1 = (cur[0]+v[0], cur[1]+v[1]); p2 = (cur[0]+v[2], cur[1]+v[3])
                p3 = (cur[0]+v[4], cur[1]+v[5])
            else:
                p1, p2, p3 = (v[0], v[1]), (v[2], v[3]), (v[4], v[5])
            pts.extend(bez(cur, p1, p2, p3)); cur = p3
        elif c == 'Z':
            cur = start
        else:
            i += 1
    return pts


def simplify(pts, eps):
    out = [pts[0]]
    for p in pts[1:]:
        if abs(p[0]-out[-1][0]) + abs(p[1]-out[-1][1]) > eps:
            out.append(p)
    if len(out) > 1 and abs(out[0][0]-out[-1][0]) + abs(out[0][1]-out[-1][1]) < eps:
        out.pop()
    return out


def raw_paths(src):
    """Walk the tree so paths INHERIT fill/stroke from their groups. Scratch hangs
    the stroke colour on the enclosing <g> and leaves the paths bare — reading only
    a path's own attributes is what made his crate's X invisible."""
    root = ET.parse(src).getroot()
    gr = grads(root)
    out = []

    def walk(node, inherit, tx, ty):
        attrs = dict(inherit)
        for k in ('fill', 'stroke', 'stroke-width'):
            if node.get(k) is not None:
                attrs[k] = node.get(k)
        m = re.match(r'translate\(([-\d.]+),([-\d.]+)\)', node.get('transform') or '')
        if m:
            tx, ty = tx + float(m.group(1)), ty + float(m.group(2))

        if node.tag == NS + 'path' and node.get('d'):
            fill = attrs.get('fill', 'none')
            g = re.match(r'url\(#(.+)\)', fill)
            top, bot = gr.get(g.group(1), ('#888888', '#888888')) if g else (fill, fill)
            pts = simplify(flatten(node.get('d')),
                           EPS if fill != 'none' else EPS * 3)
            # 2 points is a LINE, not junk — the X across his crate is two of them
            if len(pts) >= 2:
                pts = [(x + tx, y + ty) for x, y in pts]
                xs = [q[0] for q in pts]; ys = [q[1] for q in pts]
                out.append({'pts': pts, 'fill': top, 'fillLow': bot,
                            'edge': attrs.get('stroke', 'none'),
                            'box': (min(xs), min(ys), max(xs), max(ys))})
        for child in node:
            walk(child, attrs, tx, ty)

    walk(root, {}, 0.0, 0.0)
    return out


def convert_prop(src):
    """A prop is ONE object drawn as several paths — a crate plus its planks, a
    target plus its rings. Nothing here is interchangeable, so everything keeps
    its place relative to everything else and the whole lot normalises to the
    union box. (Treating a prop like a terrain sheet is what silently dropped
    the detail off his crate and left a bare square.)"""
    paths = raw_paths(src)
    if not paths:
        return []
    x0 = min(p['box'][0] for p in paths); y0 = min(p['box'][1] for p in paths)
    x1 = max(p['box'][2] for p in paths); y1 = max(p['box'][3] for p in paths)
    box = (x0, y0, x1, y1)
    sx, sy = (x1-x0) or 1, (y1-y0) or 1
    norm = lambda pts: [[round((q[0]-x0)/sx, 4), round((q[1]-y0)/sy, 4)] for q in pts]

    big = max(paths, key=lambda p: (p['box'][2]-p['box'][0]) * (p['box'][3]-p['box'][1]))
    piece = {'w': round(sx, 2), 'h': round(sy, 2), 'fill': big['fill'],
             'fillLow': big['fillLow'], 'edge': big['edge'],
             'pts': norm(big['pts']),
             # kept in the order he drew them, so what he layered on top stays on top
             'on': [{'fill': p['fill'], 'fillLow': p['fillLow'], 'edge': p['edge'],
                     'pts': norm(p['pts'])}
                    for p in paths if p is not big]}
    return [piece]


def convert(src):
    paths = raw_paths(src)

    # A stroke-only path is one of his surface marks (rock's cracks, the # signs).
    # A very wide one is the ground slab. Everything else is a candidate body.
    for p in paths:
        x0, y0, x1, y1 = p['box']
        w, h = x1-x0, y1-y0
        p['role'] = ('mark' if p['fill'] == 'none' else
                     'strip' if w > 300 else 'body')

    # The colour covering the most area is the terrain itself; anything else is
    # decoration drawn on top — wildfire's ash, underwater's seaweed and bubbles.
    area = {}
    for p in paths:
        if p['role'] != 'body':
            continue
        x0, y0, x1, y1 = p['box']
        area[p['fill']] = area.get(p['fill'], 0) + (x1-x0) * (y1-y0)
    body_fill = max(area, key=area.get) if area else None
    for p in paths:
        if p['role'] == 'body' and p['fill'] != body_fill:
            p['role'] = 'decor'

    # a stray speck is a slip of the pen, not a platform
    for p in paths:
        if p['role'] == 'body':
            x0, y0, x1, y1 = p['box']
            if x1-x0 < 8 or y1-y0 < 8:
                p['role'] = 'decor'
    for p in paths:
        if p['role'] == 'body' and len(p['pts']) < 3:
            p['role'] = 'mark'
    bodies = [p for p in paths if p['role'] == 'body']

    def norm(pts, box):
        x0, y0, x1, y1 = box
        sx, sy = (x1-x0) or 1, (y1-y0) or 1
        return [[round((q[0]-x0)/sx, 4), round((q[1]-y0)/sy, 4)] for q in pts]

    def emit(p, box, coarse=False):
        # decoration is small on screen, so it carries far more points than it
        # needs — thin it out hard rather than ship a 1200-point platform
        pts = simplify(p['pts'], 1.4) if coarse else p['pts']
        return {'fill': p['fill'], 'fillLow': p['fillLow'], 'edge': p['edge'],
                'pts': norm(pts, box)}

    out = []
    for b in bodies:
        x0, y0, x1, y1 = b['box']
        piece = emit(b, b['box'])
        piece['w'] = round(x1-x0, 2); piece['h'] = round(y1-y0, 2)
        piece['on'] = []
        out.append(piece)

    # Attach each mark/decor to the body it sits on, in that body's coordinates.
    # Seaweed overlaps the top edge of its platform and keeps going upward, so its
    # points land outside 0..1 — which is what makes it stand proud in game
    # instead of being squashed into the platform.
    for d in paths:
        if d['role'] not in ('mark', 'decor') or not bodies:
            continue
        dx0, dy0, dx1, dy1 = d['box']
        def score(b):
            bx0, by0, bx1, by1 = b['box']
            ox = min(dx1, bx1) - max(dx0, bx0)
            oy = min(dy1, by1) - max(dy0, by0)
            if ox > 0 and oy > 0:
                return -ox * oy                       # prefer real overlap
            cx, cy = (dx0+dx1)/2 - (bx0+bx1)/2, (dy0+dy1)/2 - (by0+by1)/2
            return (cx*cx + cy*cy) ** .5              # else nearest centre
        host = min(bodies, key=score)
        e = emit(d, host['box'], coarse=True)
        if len(e['pts']) >= 2:                 # 2 points is a line, still worth drawing
            out[bodies.index(host)]['on'].append(e)
    return out


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != '--prop']
    out = convert_prop(args[0]) if '--prop' in sys.argv else convert(args[0])
    out.sort(key=lambda p: -p['w'] * p['h'])
    print(json.dumps(out, indent=None))
    for p in out:
        pts = len(p['pts']) + sum(len(d['pts']) for d in p['on'])
        print(f"  {p['w']:>7.1f} x {p['h']:<7.1f} {pts:>4} pts  "
              f"{len(p['on'])} decor  {p['fill']} -> {p['fillLow']}  "
              f"edge {p['edge']}", file=sys.stderr)
