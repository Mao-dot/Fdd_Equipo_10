"""Recupera las bibliotecas de EasyEDA y el STEP de RECOM."""

from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from html import unescape
from http.cookiejar import CookieJar
from pathlib import Path
import re
from urllib.parse import urljoin
from urllib.request import HTTPCookieProcessor, Request, build_opener, urlopen

DIRECTORY = Path(__file__).resolve().parent
API = "https://easyeda.com/api/components/"
RECOM_PAGE = (
    "https://recom-power.com/en/products/switching-regulators/"
    "switching-regulators-sip/rec-p-R-78K3.3-1.0.html"
)
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
    ),
    "Referer": "https://easyeda.com/editor",
    "Accept": "application/json, text/plain, */*",
    "X-Requested-With": "XMLHttpRequest",
}
COMPONENTS = {
    "C114662": "6c045d120fdf4a95aca76bc1f86f3206",
    "C144394": "f8c2129f3dff40c090840f2a45351855",
    "C144395": "56e0f24eac1546d49cbc18d9dc0216e9",
    "C144397": "1acac24ae9684b0ca050502de7e97f5b",
    "C144398": "ac950db5079c47f4a5b9d9b4db4a0055",
    "C14663": "154b66255b01a09bf1c88bb1ea89be78",
    "C157991": "faa2c89ef44b4088b639bacf1c63ab9e",
    "C158012": "e121d28526db42a1ab28c19b6da8c1fc",
    "C15849": "637415f70eb949abfaeba2abe658ee9b",
    "C19702": "3d033fcb6d334c25b65a754834cf5aaf",
    "C20917": "f80e29816fd30bb295222fb4f47bcc25",
    "C22775": "2291b26429a0a53b9787e50172e9245c",
    "C22936": "fecebe12cd81fd6870d9d2b387d69f2f",
    "C242145": "084fc40699894f69bbf96aaaeffba906",
    "C25804": "b210af5a1436310a86e8b108e2e5a90b",
    "C3817931": "156e40df46b4411cad65d94945b2beab",
    "C3819953": "65a1c9e99dff474ab26c2f326f4e3f80",
    "C7836": "16519f49285765eca132410b2e1e1b89",
}


def download_recom():
    opener = build_opener(HTTPCookieProcessor(CookieJar()))
    headers = {"User-Agent": HEADERS["User-Agent"]}
    with opener.open(Request(RECOM_PAGE, headers=headers), timeout=25) as response:
        page = response.read().decode("utf-8")
        link = re.search(
            r'<a[^>]+href="([^"]+)"[^>]*>\s*<i[^>]+></i>\s*R-78K-1\.0\.STEP',
            page,
        )
        if link is None:
            raise ValueError(f"No se encontró el STEP en {RECOM_PAGE}")
        url = urljoin(response.url, unescape(link[1]))
    with opener.open(Request(url, headers=headers), timeout=25) as response:
        return response.read()


def restore(filename, expected, uuid=None):
    target = DIRECTORY / filename
    if target.exists():
        if sha256(target.read_bytes()).hexdigest() == expected:
            return f"Verificado {filename}"
        raise ValueError(f"{filename} local no coincide con el inventario SHA-256")

    if uuid is None:
        data = download_recom()
    else:
        with urlopen(Request(API + uuid, headers=HEADERS), timeout=25) as response:
            data = response.read()
    if sha256(data).hexdigest() != expected:
        raise ValueError(f"{filename} descargado no coincide con el inventario SHA-256")
    with target.open("xb") as file:
        file.write(data)
    return f"Descargado y verificado {filename}"


def main():
    expected = {
        filename: digest
        for digest, filename in (
            line.split("  ", 1)
            for line in (DIRECTORY / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines()
        )
    }
    files = {f"EasyEDA-{code}-original.json": uuid for code, uuid in COMPONENTS.items()}
    files["EasyEDA-DevKitC-community-source.json"] = "f202b75334f94af1a1a7ebbcbafb3fae"
    files["RECOM-R-78K-1.0-original.STEP"] = None

    failed = False
    with ThreadPoolExecutor(max_workers=5) as executor:
        pending = {
            filename: executor.submit(restore, filename, expected[filename], uuid)
            for filename, uuid in files.items()
        }
        for filename, task in pending.items():
            try:
                print(task.result())
            except (OSError, ValueError) as error:
                failed = True
                print(f"Error al recuperar {filename}: {error}")
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
