#!/usr/bin/env python3
"""Cut a doggo drawing out of its baked-in checkerboard background.

Adam's drawing app exports the transparency checkerboard as real pixels
(#FAF8F7 and #E5EAF1), so `magick -trim` does nothing. A global colour
replace is not safe either — the Dalmatian's white body is nearly the same
white as the checker. So: flood-fill inward from the border and let the
black outline of the drawing stop the fill.

    python3 cutout.py ~/Doggos/Cowboy.png Cowboy-Doggo

Second argument is the name the game looks for in doggos/ (no extension).
"""
import subprocess, struct, sys, os
from collections import deque

CHECK_A = (250, 248, 247)
CHECK_B = (229, 234, 241)
TOL2    = 20 * 20          # squared euclidean; the two checker colours are ~26 apart
FRINGE  = 2                # passes clearing anti-aliased edge pixels
OUT_H   = 220              # everything is normalised to this height
RAW     = False
DST_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'doggos')


def d2(p, q):
    return (p[0]-q[0])**2 + (p[1]-q[1])**2 + (p[2]-q[2])**2


def cutout(src, name):
    w, h = struct.unpack('>II', open(src, 'rb').read(24)[16:24])
    buf = bytearray(subprocess.run(['magick', src, '-depth', '8', 'rgba:-'],
                                   capture_output=True).stdout)
    if len(buf) != w*h*4:
        raise SystemExit(f'unexpected pixel count for {src}')

    col = lambda i: (buf[i*4], buf[i*4+1], buf[i*4+2])
    ok  = lambda c: d2(c, CHECK_A) <= TOL2 or d2(c, CHECK_B) <= TOL2

    seen, q = bytearray(w*h), deque()
    border = ([y*w + x for x in range(w) for y in (0, h-1)] +
              [y*w + x for y in range(h) for x in (0, w-1)])
    for i in border:
        if not seen[i] and ok(col(i)):
            seen[i] = 1; q.append(i)
    while q:
        i = q.popleft(); x, y = i % w, i // w
        for dx, dy in ((1,0), (-1,0), (0,1), (0,-1)):
            nx, ny = x+dx, y+dy
            if 0 <= nx < w and 0 <= ny < h:
                j = ny*w + nx
                if not seen[j] and ok(col(j)):
                    seen[j] = 1; q.append(j)

    # Erode unconditionally — where a black outline meets the light background the
    # blend is a mid grey, which no "is it nearly white" test will catch, and it
    # renders as a pale halo around the art.
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

    dst = os.path.join(DST_DIR, name + '.png')
    args = ['magick', '-size', f'{w}x{h}', '-depth', '8', 'rgba:-', '-trim', '+repage']
    if not RAW:                      # --raw keeps native size, so a SET of frames
        args += ['-resize', f'x{OUT_H}']   # keeps the relative scale the artist drew
    subprocess.run(args + [dst], input=bytes(buf))
    ow, oh = struct.unpack('>II', open(dst, 'rb').read(24)[16:24])
    pct = sum(seen) * 100 // (w*h)

    # nose-to-tail width: the game scales every doggo so THIS lands on BODY_LEN,
    # which is what keeps hats and long necks from shrinking the animal.
    out = subprocess.run(['magick', dst, '-depth', '8', 'rgba:-'],
                         capture_output=True).stdout
    bw = 0
    for y in range(oh):
        xs = [x for x in range(ow) if out[(y*ow + x)*4 + 3] > 40]
        if xs:
            bw = max(bw, xs[-1] - xs[0] + 1)

    print(f'{name}: {pct}% background removed, {ow}x{oh} -> {dst}')
    print(f'  put  bw:{bw}  on this doggo in sandbox.html')
    if pct > 88:
        print('  WARNING: that is a lot. check the outline has no gaps.')


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != '--raw']
    if len(args) != 2:
        raise SystemExit(__doc__)
    RAW = '--raw' in sys.argv
    globals()['RAW'] = RAW
    cutout(args[0], args[1])
