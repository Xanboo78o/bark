#!/usr/bin/env python3
"""Slice one of Adam's biome sheets into a ground strip + platform pieces.

Each sheet is laid out the same way: a handful of floating platform blobs, plus
one wide ground strip (top of the sheet on grass.png, bottom on the others).
Text labels drawn on the sheet are skipped.

    python3 sheetcut.py ~/Doggos/rock.png rock

Writes doggos/rock-ground.png and doggos/rock-plat1..N.png, and prints the
colours to put in the biome table in sandbox.html.

IMPORTANT: the fringe passes are not optional. Flood-filling the checkerboard
alone leaves the anti-aliased pixels between the artwork and the background,
which show up in game as a white halo around everything.
"""
import subprocess, struct, sys, os
from collections import deque

CHECK_A = (250, 248, 247)
CHECK_B = (229, 234, 241)
TOL2    = 22 * 22
FRINGE  = 3
MIN_PX  = 2500
TRIM    = 0
DST_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'doggos')


def d2(p, q):
    return (p[0]-q[0])**2 + (p[1]-q[1])**2 + (p[2]-q[2])**2


def slice_sheet(src, prefix):
    w, h = struct.unpack('>II', open(src, 'rb').read(24)[16:24])
    buf = bytearray(subprocess.run(['magick', src, '-depth', '8', 'rgba:-'],
                                   capture_output=True).stdout)
    col = lambda i: (buf[i*4], buf[i*4+1], buf[i*4+2])
    bg  = lambda c: (d2(c, CHECK_A) <= TOL2 or d2(c, CHECK_B) <= TOL2
                     or (c[0] > 244 and c[1] > 244 and c[2] > 244))

    seen, q = bytearray(w*h), deque()
    border = ([y*w + x for x in range(w) for y in (0, h-1)] +
              [y*w + x for y in range(h) for x in (0, w-1)])
    for i in border:
        if not seen[i] and bg(col(i)):
            seen[i] = 1; q.append(i)
    while q:
        i = q.popleft(); x, y = i % w, i // w
        for dx, dy in ((1,0), (-1,0), (0,1), (0,-1)):
            nx, ny = x+dx, y+dy
            if 0 <= nx < w and 0 <= ny < h:
                j = ny*w + nx
                if not seen[j] and bg(col(j)):
                    seen[j] = 1; q.append(j)

    # Erode the edge unconditionally. A brightness test does NOT work: where the
    # artwork's black outline meets the light background the blend lands on a mid
    # grey (~#949190), which sails past any "is it nearly white" check and shows up
    # in game as a pale halo around every shape.
    for _ in range(FRINGE):
        add = []
        for i in range(w*h):
            if seen[i]:
                continue
            x, y = i % w, i // w
            for dx, dy in ((1,0), (-1,0), (0,1), (0,-1)):
                nx, ny = x+dx, y+dy
                if 0 <= nx < w and 0 <= ny < h and seen[ny*w + nx]:
                    add.append(i); break
        for i in add:
            seen[i] = 1

    for i in range(w*h):
        if seen[i]:
            buf[i*4+3] = 0
    raw = bytes(buf)

    # connected components
    lab, comps = bytearray(w*h), []
    for s in range(w*h):
        if seen[s] or lab[s]:
            continue
        dq = deque([s]); lab[s] = 1
        x0 = y0 = 10**9; x1 = y1 = -1; n = 0; rs = gs = bs = 0
        while dq:
            i = dq.popleft(); x, y = i % w, i // w; n += 1
            c = col(i); rs += c[0]; gs += c[1]; bs += c[2]
            x0 = min(x0, x); x1 = max(x1, x); y0 = min(y0, y); y1 = max(y1, y)
            for dx, dy in ((1,0), (-1,0), (0,1), (0,-1)):
                nx, ny = x+dx, y+dy
                if 0 <= nx < w and 0 <= ny < h:
                    j = ny*w + nx
                    if not seen[j] and not lab[j]:
                        lab[j] = 1; dq.append(j)
        if n < MIN_PX:
            continue
        mean = (rs//n, gs//n, bs//n)
        # skip the labels he writes on the sheets (pure green / red text)
        if (mean[1] > 170 and mean[0] < 130 and mean[2] < 130) or \
           (mean[0] > 190 and mean[1] < 140 and mean[2] < 130):
            continue
        comps.append((n, x0, y0, x1-x0+1, y1-y0+1))

    ground = [c for c in comps if c[3] > w*0.8]
    plats  = sorted([c for c in comps if c[3] <= w*0.8], reverse=True)

    def cut(box, name, trim_bottom=0):
        _, x, y, cw, chh = box
        chh -= trim_bottom
        subprocess.run(['magick', '-size', f'{w}x{h}', '-depth', '8', 'rgba:-',
                        '-crop', f'{cw}x{chh}+{x}+{y}', '+repage',
                        os.path.join(DST_DIR, name + '.png')], input=raw)
        return cw, chh

    if ground:
        g = max(ground)
        cw, chh = cut(g, prefix + '-ground', TRIM)
        gx, gy = g[1], g[2]
        def band(y0, y1):
            r = gg = b = n = 0
            for y in range(gy+y0, min(gy+y1, gy+chh)):
                for x in range(gx, gx+cw, 5):
                    i = (y*w + x)*4
                    if buf[i+3] < 200: continue
                    r += buf[i]; gg += buf[i+1]; b += buf[i+2]; n += 1
            return '#%02x%02x%02x' % (r//n, gg//n, b//n) if n else '?'
        print(f'{prefix}-ground  {cw}x{chh}')
        print(f'   top   {band(0, chh//5)}')
        print(f'   base  {band(chh - chh//6, chh)}   <- fill colour under the strip')
    else:
        print(f'{prefix}: no ground strip found')

    for k, p in enumerate(plats, 1):
        cw, chh = cut(p, f'{prefix}-plat{k}')
        print(f'{prefix}-plat{k}   {cw}x{chh}')


if __name__ == '__main__':
    # 3rd arg: rows to trim off the bottom of the ground strip. grass.png has a
    # black rule drawn under it that is part of the sheet layout, not the terrain,
    # and no brightness test separates it from his very dark dirt.
    if len(sys.argv) not in (3, 4):
        raise SystemExit(__doc__)
    TRIM = int(sys.argv[3]) if len(sys.argv) == 4 else 0
    globals()['TRIM'] = TRIM
    slice_sheet(sys.argv[1], sys.argv[2])
