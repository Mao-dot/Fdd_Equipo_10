"""Descarga y comprueba las fuentes CAD necesarias para regenerar FoodScan."""

import argparse
from hashlib import sha256
from io import BytesIO
from pathlib import Path, PurePosixPath
from tempfile import NamedTemporaryFile
from urllib.request import Request, urlopen
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "documentacion" / "SHA256SUMS-CAD.txt"

SOURCES = (
    (
        "commercial/auxiliary/oled/2_42inch_oled_module-sku25742_asm.stp",
        "https://files.waveshare.com/wiki/2.42inch%20OLED%20Module/2.42inch%20OLED%20Module_3D.zip",
        "2_42inch_oled_module-sku25742_asm.stp",
    ),
    (
        "commercial/auxiliary/door/asq10228.step",
        "https://mediap.industry.panasonic.eu/assets/imported/industrial.panasonic.com/ac/cdn/e/control/switch/micro/cad/3d_step/asq10228_step.zip",
        "asq10228.step",
    ),
    (
        "commercial/auxiliary/power/tensility_54-00406_original.step",
        "https://tensility.s3.us-west-2.amazonaws.com/imports/product_3d_models/54-00406.STEP",
        None,
    ),
    (
        "commercial/auxiliary/led/klus_A08504_original.obj",
        "https://klusdesign.pl/storage/pimcore/3D/OBJ/A08504.obj",
        None,
    ),
    (
        "commercial/electronics/originals/Adafruit-OV5640-Breakout.brd",
        "https://raw.githubusercontent.com/adafruit/Adafruit-OV5640-Camera-Breakout-PCB/adf6a654e8dfffa9a6b9d84681128a27a9fea257/Adafruit%20OV5640%20Breakout.brd",
        None,
    ),
    (
        "commercial/electronics/originals/ESP32-S3-DevKitC-1-v1.1.dxf",
        "https://dl.espressif.com/dl/schematics/esp_idf/DXF_ESP32-S3-DevKitC-1_V1.1_20220429.dxf",
        None,
    ),
    (
        "commercial/electronics/originals/Espressif-ESP32-S3-WROOM-1.step",
        "https://www.espressif.com/sites/default/files/3dmodel/ESP32-S3-WROOM-1%203D%20Model.STEP",
        None,
    ),
)


def load_manifest():
    hashes = {}
    for line in MANIFEST.read_text(encoding="utf-8-sig").splitlines():
        if line and not line.startswith("#"):
            digest, name = line.split(maxsplit=1)
            hashes[name] = digest.lower()
    return hashes


def download(url, member):
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=30) as response:
        data = response.read()
    if member is None:
        return data
    with ZipFile(BytesIO(data)) as archive:
        matches = [entry for entry in archive.namelist() if PurePosixPath(entry).name.casefold() == member.casefold()]
        if len(matches) != 1:
            raise ValueError(f"El ZIP debe contener una única copia de {member}")
        return archive.read(matches[0])


def restore(root, verify_only):
    hashes = load_manifest()
    for name, url, member in SOURCES:
        path = root / name
        expected = hashes[name]
        if path.is_file():
            if sha256(path.read_bytes()).hexdigest() != expected:
                raise ValueError(f"SHA-256 distinto en el archivo existente {name}")
            print(f"Verificado {name}")
            continue
        if verify_only:
            raise ValueError(f"Falta el archivo {name}")
        data = download(url, member)
        if sha256(data).hexdigest() != expected:
            raise ValueError(f"SHA-256 distinto en la descarga de {name}")
        path.parent.mkdir(parents=True, exist_ok=True)
        with NamedTemporaryFile(dir=path.parent, delete=False) as temporary:
            temporary.write(data)
        staged = Path(temporary.name)
        try:
            staged.replace(path)
        finally:
            staged.unlink(missing_ok=True)
        print(f"Descargado y verificado {name}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destino", type=Path, default=ROOT)
    parser.add_argument("--verificar", action="store_true", help="Comprueba los archivos locales sin descargarlos.")
    options = parser.parse_args()
    try:
        restore(options.destino, options.verificar)
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, f"{exc}\n")


if __name__ == "__main__":
    main()
