import sys, os

# Re-use xdvdfs extractor from ShaolinMonks (copied to tools/ for standalone).
MAGIC = b"MICROSOFT*XBOX*MEDIA"

def walk(root_table, off):
    if off * 4 + 14 > len(root_table):
        return None
    left, right, sector, size, attr, nlen = struct.unpack_from("<HHIIBB", root_table, off * 4)
    if left == 0xFFFF:
        return None
    name = root_table[off * 4 + 14: off * 4 + 14 + nlen].decode("latin-1")
    if name.lower() == "default.xbe":
        return sector, size
    for nxt in (left, right):
        if nxt:
            r = walk(root_table, nxt)
            if r:
                return r
    return None

def extract_iso(iso_path, out_xbe):
    with open(iso_path, "rb") as f:
        for part in (0, 0x18300000, 0xFD90000, 0x2080000):
            f.seek(part + 32 * 2048)
            if f.read(20) == MAGIC:
                root_sector, root_size = struct.unpack_from("<II", f.read(8))
                f.seek(part + root_sector * 2048)
                root_table = f.read(root_size)
                hit = walk(root_table, 0)
                if hit:
                    sector, size = hit
                    f.seek(part + sector * 2048)
                    os.makedirs(os.path.dirname(out_xbe), exist_ok=True)
                    with open(out_xbe, "wb") as o:
                        o.write(f.read(size))
                    return True
    return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: extract_iso.py <iso> <out_xbe>")
        sys.exit(1)
    ok = extract_iso(sys.argv[1], sys.argv[2])
    print("OK" if ok else "FAILED")
    sys.exit(0 if ok else 1)
