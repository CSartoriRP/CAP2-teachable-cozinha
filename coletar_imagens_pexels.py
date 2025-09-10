import os, io, random, time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from PIL import Image, UnidentifiedImageError
import imagehash
from tqdm import tqdm

# =========================
# CONFIGURAÇÕES
# =========================
CLASSES = {
    "talheres": [
        "cutlery set", "fork spoon knife", "flatware on white background",
        "talheres cozinha", "garfo colher faca"
    ],
    "panelas": [
        "cooking pot", "saucepan", "nonstick frying pan", "panela cozinha", "frigideira"
    ],
    "utensilios_preparo": [
        "kitchen spatula", "whisk", "kitchen tongs", "peeler", "grater", "rolling pin", "fouet batedor"
    ],
}
IMAGENS_POR_CLASSE = 100
SPLIT_TEST = 0.2
PASTA_BASE = Path("data")
MIN_LADO = 256
TIMEOUT = 25
MAX_THREADS = 8

PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")
PEXELS_URL = "https://api.pexels.com/v1/search"
HEADERS = {"Authorization": PEXELS_API_KEY} if PEXELS_API_KEY else None


def ensure_dirs():
    for classe in CLASSES.keys():
        (PASTA_BASE / classe / "train").mkdir(parents=True, exist_ok=True)
        (PASTA_BASE / classe / "test").mkdir(parents=True, exist_ok=True)


def baixar(url: str, dest: Path) -> Path | None:
    try:
        r = requests.get(url, timeout=TIMEOUT, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code != 200 or not r.content:
            return None
        bio = io.BytesIO(r.content)
        with Image.open(bio) as im:
            im.load()
            if min(im.size) < MIN_LADO:
                return None
            if im.mode not in ("RGB", "RGBA"):
                im = im.convert("RGB")
            dest.parent.mkdir(parents=True, exist_ok=True)
            im.save(dest)
        return dest
    except (requests.RequestException, UnidentifiedImageError, OSError):
        return None


def buscar_pexels(consulta: str, alvo_urls: int) -> list[str]:
    if not HEADERS:
        raise RuntimeError("Defina a variável de ambiente PEXELS_API_KEY.")
    urls = []
    per_page = 80
    page = 1
    while len(urls) < alvo_urls and page <= 10:
        params = {"query": consulta, "per_page": per_page, "page": page, "locale": "en-US"}
        resp = requests.get(PEXELS_URL, headers=HEADERS, params=params, timeout=TIMEOUT)
        if resp.status_code != 200:
            break
        data = resp.json()
        photos = data.get("photos", [])
        if not photos:
            break
        for ph in photos:
            src = ph.get("src", {})
            u = src.get("original") or src.get("large") or src.get("large2x")
            if u:
                urls.append(u)
            if len(urls) >= alvo_urls:
                break
        page += 1
        time.sleep(0.8)
    random.shuffle(urls)
    return list(dict.fromkeys(urls))


def hash_arquivo(p: Path) -> str | None:
    try:
        with Image.open(p) as im:
            im.load()
            return str(imagehash.average_hash(im))
    except Exception:
        return None


def coletar_para_classe(classe: str, termos: list[str], alvo: int):
    print(f"\n=== Classe: {classe} | alvo={alvo} imagens ===")
    buffer_alvo = alvo * 2
    urls_total = []
    por_termo = max(30, buffer_alvo // max(1, len(termos)))

    for termo in termos:
        u = buscar_pexels(termo, por_termo)
        print(f"[INFO] '{termo}' -> {len(u)} URLs")
        urls_total.extend(u)

    urls_total = list(dict.fromkeys(urls_total))
    print(f"[INFO] Total de URLs únicas: {len(urls_total)}")

    pasta_tmp = PASTA_BASE / classe / "_tmp"
    pasta_tmp.mkdir(parents=True, exist_ok=True)

    futures = []
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as ex:
        for i, url in enumerate(urls_total):
            nome = f"{i:05d}.jpg"
            dest = pasta_tmp / nome
            futures.append(ex.submit(baixar, url, dest))
        for _ in tqdm(as_completed(futures), total=len(futures), desc=f"Baixando {classe}"):
            pass

    validas = []
    hashes = set()
    for p in pasta_tmp.glob("*.jpg"):
        h = hash_arquivo(p)
        if not h or h in hashes:
            p.unlink(missing_ok=True)
            continue
        hashes.add(h)
        validas.append(p)

    random.shuffle(validas)
    selecionadas = validas[:alvo]
    n_test = max(1, int(len(selecionadas) * SPLIT_TEST))
    test_set = selecionadas[:n_test]
    train_set = selecionadas[n_test:]

    for p in test_set:
        p.rename(PASTA_BASE / classe / "test" / p.name)
    for p in train_set:
        p.rename(PASTA_BASE / classe / "train" / p.name)

    for p in pasta_tmp.glob("*"):
        p.unlink(missing_ok=True)
    try:
        pasta_tmp.rmdir()
    except OSError:
        pass

    print(f"[OK] {classe} → train={len(train_set)} | test={len(test_set)} | total={len(selecionadas)}")


def main():
    random.seed(42)
    ensure_dirs()
    for classe, termos in CLASSES.items():
        coletar_para_classe(classe, termos, IMAGENS_POR_CLASSE)
    print("\nConcluído. Use as pastas 'train' e 'test' no Teachable Machine.")


if __name__ == "__main__":
    main()
