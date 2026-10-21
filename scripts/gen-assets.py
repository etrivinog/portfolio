#!/usr/bin/env python3
"""Generate favicons and Open Graph preview images (requires playwright + pillow)."""
import asyncio, io, json, pathlib
from PIL import Image
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent

ICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#0071e3"/><stop offset=".5" stop-color="#5e5ce6"/><stop offset="1" stop-color="#af52de"/>
</linearGradient></defs>
<rect width="512" height="512" rx="114" fill="url(#g)"/>
<text x="256" y="336" font-family="-apple-system,BlinkMacSystemFont,'Helvetica Neue',Helvetica,Arial,sans-serif" font-size="220" font-weight="700" letter-spacing="-6" fill="#fff" text-anchor="middle">ET</text>
</svg>"""

OG = {
    "en": dict(file="og-image.png", lang="en", role="Senior iOS Developer &amp; Software Engineer",
               tag="9 years in software · 5 years iOS · Fintech &amp; digital wallets", loc="Colombia · Remote",
               badge="Available for Senior iOS / AI roles"),
    "es": dict(file="og-image-es.png", lang="es", role="Senior iOS Developer &amp; Ingeniero de Software",
               tag="9 años en software · 5 años iOS · Fintech y billeteras digitales", loc="Colombia · Remoto",
               badge="Disponible para roles Senior iOS / IA"),
}

OG_HTML = """<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1200px;height:630px;background:#000;color:#f5f5f7;overflow:hidden;
font-family:-apple-system,BlinkMacSystemFont,'SF Pro Display','Helvetica Neue',Helvetica,Arial,sans-serif;position:relative}}
.glow{{position:absolute;border-radius:50%;filter:blur(90px);opacity:.55}}
.g1{{width:560px;height:560px;background:#0071e3;left:-160px;top:-220px}}
.g2{{width:520px;height:520px;background:#5e5ce6;right:-140px;top:120px}}
.g3{{width:420px;height:420px;background:#af52de;left:420px;bottom:-300px}}
.card{{position:absolute;inset:48px;border-radius:44px;background:rgba(28,28,30,.55);
border:1px solid rgba(255,255,255,.14);box-shadow:inset 0 1px 0 rgba(255,255,255,.12);padding:64px 72px;display:flex;flex-direction:column}}
.top{{display:flex;align-items:center;gap:22px}}
.logo{{width:84px;height:84px}}
.badge{{margin-left:auto;display:flex;align-items:center;gap:12px;background:#000;border:1px solid rgba(255,255,255,.14);
border-radius:999px;padding:14px 24px;font-size:22px;font-weight:600;color:#d1d1d6}}
.dot{{width:13px;height:13px;border-radius:50%;background:#30d158;box-shadow:0 0 14px #30d158}}
h1{{font-size:92px;font-weight:800;letter-spacing:-.045em;line-height:1;margin-top:46px}}
h2{{font-size:42px;font-weight:700;letter-spacing:-.02em;margin-top:18px;
background:linear-gradient(90deg,#2997ff,#7d7aff 50%,#bf5af2);-webkit-background-clip:text;color:transparent}}
p{{white-space:nowrap;font-size:24px;color:#a1a1a6;margin-top:18px;font-weight:500}}
.chips{{display:flex;gap:12px;margin-top:auto;align-items:center}}
.chip{{white-space:nowrap;font-size:22px;font-weight:600;padding:10px 20px;border-radius:999px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.12)}}
.url{{margin-left:auto;font-size:26px;font-weight:700;color:#f5f5f7}}
</style></head><body>
<div class="glow g1"></div><div class="glow g2"></div><div class="glow g3"></div>
<div class="card">
 <div class="top"><img class="logo" src="data:image/svg+xml;base64,{logo}"><div class="badge"><span class="dot"></span>{badge}</div></div>
 <h1>Esteban Triviño</h1>
 <h2>{role}</h2>
 <p>{tag} · {loc}</p>
 <div class="chips"><span class="chip">Swift</span><span class="chip">SwiftUI</span><span class="chip">TCA</span><span class="chip">Combine</span><span class="chip">Claude Code · Copilot</span>
 <span class="url">estebantrivino.com</span></div>
</div></body></html>"""


async def main():
    import base64
    logo = base64.b64encode(ICON_SVG.encode()).decode()
    (ROOT / "favicon.svg").write_text(ICON_SVG + "\n")
    async with async_playwright() as p:
        b = await p.chromium.launch(channel="chrome")
        pg = await b.new_page(viewport={"width": 512, "height": 512})
        await pg.set_content(f'<html><body style="margin:0;background:transparent">{ICON_SVG.replace("<svg ", "<svg width=512 height=512 ", 1)}</body></html>')
        big = Image.open(io.BytesIO(await pg.screenshot(omit_background=True))).convert("RGBA")
        square_svg = ICON_SVG.replace("<svg ", "<svg width=512 height=512 ", 1).replace('rx="114"', 'rx="0"')
        await pg.set_content('<html><body style="margin:0">' + square_svg + '</body></html>')
        square = Image.open(io.BytesIO(await pg.screenshot())).convert("RGB")
        for name, size in {"apple-touch-icon.png": 180, "icon-192.png": 192, "icon-512.png": 512, "favicon-32x32.png": 32}.items():
            img = big.resize((size, size), Image.LANCZOS)
            if name == "apple-touch-icon.png":  # iOS applies its own rounded mask
                img = square.resize((size, size), Image.LANCZOS)
            img.save(ROOT / name, optimize=True)
        big.save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
        await pg.set_viewport_size({"width": 1200, "height": 630})
        for o in OG.values():
            await pg.set_content(OG_HTML.format(logo=logo, **o))
            await pg.wait_for_timeout(200)
            Image.open(io.BytesIO(await pg.screenshot())).convert("RGB").save(ROOT / o["file"], optimize=True)
        await b.close()
    (ROOT / "site.webmanifest").write_text(json.dumps({
        "name": "Esteban Triviño — Senior iOS Developer", "short_name": "Esteban T.",
        "start_url": "/", "display": "standalone", "background_color": "#000000", "theme_color": "#000000",
        "icons": [{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    asyncio.run(main())
