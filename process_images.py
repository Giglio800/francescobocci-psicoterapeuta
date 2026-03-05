#!/usr/bin/env python3
"""
Ottimizzazione foto per landing page professionale.
Applica filtri warm, contrasto migliorato, nitidezza e bilanciamento colori
senza snaturare le immagini originali.
"""

from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import os

def enhance_portrait(img_path, out_path, size=(900, 1100)):
    """Migliora il ritratto professionale: warm tone, contrasto, nitidezza."""
    img = Image.open(img_path).convert("RGB")
    
    # Resize mantenendo proporzioni, crop centrato
    img.thumbnail((size[0] * 2, size[1] * 2), Image.LANCZOS)
    w, h = img.size
    # Crop centrato
    left = max(0, (w - size[0]) // 2)
    top = max(0, (h - size[1]) // 2)
    right = left + min(w, size[0])
    bottom = top + min(h, size[1])
    img = img.crop((left, top, right, bottom))
    
    # 1. Leggero boost luminosità (+5%)
    img = ImageEnhance.Brightness(img).enhance(1.05)
    
    # 2. Contrasto migliorato (+15%)
    img = ImageEnhance.Contrast(img).enhance(1.15)
    
    # 3. Saturazione leggermente ridotta per look professionale
    img = ImageEnhance.Color(img).enhance(0.92)
    
    # 4. Nitidezza
    img = ImageEnhance.Sharpness(img).enhance(1.4)
    
    # 5. Warm tone: leggero boost rosso/giallo
    r, g, b = img.split()
    r = ImageEnhance.Brightness(r.convert("RGB")).enhance(1.04).split()[0]
    img = Image.merge("RGB", (r, g, b))
    
    # 6. Leggero smoothing finale
    img = img.filter(ImageFilter.SMOOTH_MORE)
    img = ImageEnhance.Sharpness(img).enhance(1.1)
    
    img.save(out_path, "JPEG", quality=92, optimize=True)
    print(f"✓ Ritratto salvato: {out_path} ({img.size})")

def enhance_studio(img_path, out_path, size=(1200, 900)):
    """Migliora le foto dello studio: warm, luminoso, accogliente."""
    img = Image.open(img_path).convert("RGB")
    
    # Resize
    img.thumbnail((size[0] * 2, size[1] * 2), Image.LANCZOS)
    w, h = img.size
    # Crop centrato
    left = max(0, (w - size[0]) // 2)
    top = max(0, (h - size[1]) // 2)
    right = left + min(w, size[0])
    bottom = top + min(h, size[1])
    img = img.crop((left, top, right, bottom))
    
    # 1. Luminosità +10%
    img = ImageEnhance.Brightness(img).enhance(1.10)
    
    # 2. Contrasto +12%
    img = ImageEnhance.Contrast(img).enhance(1.12)
    
    # 3. Saturazione +8% per rendere i colori più vivaci ma naturali
    img = ImageEnhance.Color(img).enhance(1.08)
    
    # 4. Nitidezza
    img = ImageEnhance.Sharpness(img).enhance(1.3)
    
    # 5. Warm tone leggero
    r, g, b = img.split()
    r = r.point(lambda x: min(255, int(x * 1.03)))
    g = g.point(lambda x: min(255, int(x * 1.01)))
    img = Image.merge("RGB", (r, g, b))
    
    img.save(out_path, "JPEG", quality=90, optimize=True)
    print(f"✓ Studio salvato: {out_path} ({img.size})")

def enhance_vgt(img_path, out_path, size=(1200, 900)):
    """Migliora la foto VGT setup: contrasto, colori vivaci ma non esagerati."""
    img = Image.open(img_path).convert("RGB")
    
    img.thumbnail((size[0] * 2, size[1] * 2), Image.LANCZOS)
    w, h = img.size
    left = max(0, (w - size[0]) // 2)
    top = max(0, (h - size[1]) // 2)
    right = left + min(w, size[0])
    bottom = top + min(h, size[1])
    img = img.crop((left, top, right, bottom))
    
    # 1. Luminosità +15% (era scura)
    img = ImageEnhance.Brightness(img).enhance(1.15)
    
    # 2. Contrasto +20%
    img = ImageEnhance.Contrast(img).enhance(1.20)
    
    # 3. Saturazione +10%
    img = ImageEnhance.Color(img).enhance(1.10)
    
    # 4. Nitidezza
    img = ImageEnhance.Sharpness(img).enhance(1.35)
    
    img.save(out_path, "JPEG", quality=90, optimize=True)
    print(f"✓ VGT setup salvato: {out_path} ({img.size})")

def create_hero_bg(img_path, out_path, size=(1920, 1080)):
    """Crea versione hero della foto ritratto: scurita per overlay testo."""
    img = Image.open(img_path).convert("RGB")
    img = img.resize(size, Image.LANCZOS)
    
    # Scurisci per hero
    img = ImageEnhance.Brightness(img).enhance(0.55)
    img = ImageEnhance.Contrast(img).enhance(1.1)
    
    img.save(out_path, "JPEG", quality=85, optimize=True)
    print(f"✓ Hero bg salvato: {out_path} ({img.size})")

if __name__ == "__main__":
    base = "/home/ubuntu/bocci-landing/assets/img"
    
    # Ritratto professionale
    enhance_portrait(
        f"{base}/foto_originale.jpg",
        f"{base}/foto_bocci.jpg",
        size=(800, 1000)
    )
    
    # Studio 1 (Il Telaio - verde)
    enhance_studio(
        f"{base}/studio1_originale.jpg",
        f"{base}/studio_telaio.jpg",
        size=(1200, 900)
    )
    
    # Studio 2 (Brescia - giallo)
    enhance_studio(
        f"{base}/studio2_originale.png",
        f"{base}/studio_brescia.jpg",
        size=(1200, 900)
    )
    
    # VGT setup
    enhance_vgt(
        f"{base}/vgt_setup_originale.png",
        f"{base}/vgt_setup.jpg",
        size=(1200, 900)
    )
    
    print("\n✓ Tutte le immagini elaborate con successo!")
