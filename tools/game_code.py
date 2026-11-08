"""Load the game's own Python modules outside the game, for offline tools.

TeamPrincipal.exe is a PyInstaller build. unpack() copies the marshalled
module code out of it into private/game_code/<build>/ (gitignored, never
published). install() then lets `import game_state`, `import managers.x`
etc. work from that copy, as if the game were running from `sandbox`.

The game resolves every data path from the folder of its executable, so
`sandbox` must look like a game folder (active_pack.json, data/<pack>/,
saves/). Point it at a scratch folder, never at the real install: the
game writes options and saves next to its data.

The code objects only load in the Python version the game was built
with (3.13); the UI screens also need pygame 2.6.1. See
tools/simulate.py for the setup.
"""

import importlib.abc
import importlib.util
import marshal
import struct
import sys
import zlib
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CACHE = REPO / "private" / "game_code"
COOKIE = b"MEI\x0c\x0b\x0a\x0b\x0e"


def build_id(exe):
    st = Path(exe).stat()
    return f"{st.st_size}-{int(st.st_mtime)}"


def exe_python_version(exe):
    """(major, minor) of the Python the game was built with, from the PyInstaller cookie."""
    raw = Path(exe).read_bytes()
    pos = raw.rfind(COOKIE)
    pyver = struct.unpack("!I", raw[pos + 20:pos + 24])[0]
    return pyver // 100, pyver % 100


def unpack(exe):
    """Unpack the game's PYZ archive once per game build; return the folder of *.marshal files."""
    exe = Path(exe)
    out = CACHE / build_id(exe) / "pyz"
    if (out / "game_state.marshal").exists():
        return out
    raw = exe.read_bytes()
    cookie = raw.rfind(COOKIE)
    _magic, pkg_len, toc_off, toc_len, _pyver = struct.unpack("!8sIIII", raw[cookie:cookie + 24])
    pkg_start = len(raw) - pkg_len
    toc = raw[pkg_start + toc_off:pkg_start + toc_off + toc_len]
    p = 0
    tmp = out.with_name("pyz.partial")
    tmp.mkdir(parents=True, exist_ok=True)
    while p < len(toc):
        (size,) = struct.unpack("!i", toc[p:p + 4])
        pos, clen, _ulen, cflag, typ = struct.unpack("!IIIBc", toc[p + 4:p + 18])
        p += size
        if typ != b"z":
            continue
        data = raw[pkg_start + pos:pkg_start + pos + clen]
        if cflag:
            data = zlib.decompress(data)
        (ztoc_pos,) = struct.unpack("!i", data[8:12])
        # The PYZ table of contents is plain marshalled data (names and offsets).
        for name, (_ispkg, mpos, mlen) in marshal.loads(data[ztoc_pos:]):
            (tmp / f"{name}.marshal").write_bytes(zlib.decompress(data[mpos:mpos + mlen]))
    tmp.rename(out)
    return out


class _Finder(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    """Imports the game's own modules; anything installed locally (stdlib, pygame) wins."""

    def __init__(self, pyz, sandbox):
        self.pyz = Path(pyz)
        self.sandbox = Path(sandbox)
        self.names = {f.name[:-8] for f in self.pyz.glob("*.marshal")}

    def find_spec(self, name, path, target=None):
        if name not in self.names:
            return None
        pkg = any(n.startswith(name + ".") for n in self.names)
        spec = importlib.util.spec_from_loader(name, self, is_package=pkg)
        spec.origin = str(self.sandbox / (name.replace(".", "/") + ("/__init__.py" if pkg else ".py")))
        spec.has_location = True
        return spec

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        if module.__spec__.submodule_search_locations is not None:
            module.__path__ = []
        module.__file__ = module.__spec__.origin
        exec(marshal.loads((self.pyz / f"{module.__name__}.marshal").read_bytes()), module.__dict__)


def install(exe, sandbox):
    """Make the game's modules importable, with `sandbox` standing in for the game folder."""
    want = exe_python_version(exe)
    if sys.version_info[:2] != want:
        sys.exit(f"the game's code needs Python {want[0]}.{want[1]}; this is {sys.version.split()[0]}")
    pyz = unpack(exe)
    sys.frozen = True
    sys._MEIPASS = str(sandbox)
    sys.executable = str(Path(sandbox) / "TeamPrincipal.exe")
    sys.meta_path.append(_Finder(pyz, sandbox))
    return pyz
