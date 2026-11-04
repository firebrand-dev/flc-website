# Web oficial de Forever Leveling Companion (FLC)

Sitio estático, bilingüe (inglés por defecto, español), generado con Python + Jinja2. No tiene backend, base de datos
ni credenciales. Se puede publicar en cualquier hosting estático (ver [docs/HOSTING.md](docs/HOSTING.md)).

**Estado:** listo para revisión, **no publicado**. La descarga está deshabilitada y los enlaces de donación vacíos
hasta que el dueño lo autorice.

## Construir y ver

```bash
python -m pip install -r requirements.txt
```

```bash
python tools/build.py --serve
```

Abre `http://localhost:8791/`. `python tools/build.py` solo genera `dist/`. Para probar el sitio en una subcarpeta
(como en GitHub Pages de un repositorio): `python tools/build.py --serve --base-url http://localhost:8796/ForeverLevelingCompanion`. Después de cada build:

```bash
python tools/check.py --external
```

(enlaces internos y externos, `alt` de imágenes, un `h1` por página, ids únicos, contraste AA, enlaces de donación).

Revisión visual y de carga en un navegador real (Edge o Chrome sin interfaz; necesita Node 22 o más nuevo, sin
paquetes):

```bash
node tools/shots.mjs --root dist --out build/shots/after --pages all --views mobile320,mobile375,mobile390
```

Guarda una captura por página y vista, y `metrics.json` con bytes transferidos, pedidos, FCP, LCP, CLS, desborde
horizontal y títulos que no entran. `--full` captura la página entera, `--menu` con el menú abierto, `--throttle`
simula una red móvil lenta (1,6 Mbps, 150 ms).

## Qué editar para cada cosa

| Quiero cambiar… | Archivo |
|---|---|
| Versión candidata, fecha, estado de desarrollo, números de pruebas | `content/site.json` → `status` |
| La descarga (versión, zip, tamaño, SHA-256, URL) | `content/site.json` → `download` (lo llena `tools/sync_release.py`) |
| Builds del juego probadas | `content/site.json` → `builds` |
| Enlaces de reportes | `content/site.json` → `reports` |
| Enlaces de donación / campaña | `content/site.json` → `donations` |
| Dirección pública del sitio (SEO, sitemap, Open Graph) | `content/site.json` → `site.base_url` |
| Funciones y su nivel de prueba | `content/features.json` (+ textos en `i18n/*.json` → `feat`) |
| Novedades (changelog para jugadores) | `content/changelog.json` |
| Mazmorras y bandas listadas | `content/dungeons.json` |
| Cualquier texto | `i18n/en.json` y `i18n/es.json` (mismas claves; el build falla si falta una) |
| Capturas | `media/manifest.json` → `python tools/media.py` |

## Al publicar una versión del addon

1. El otro equipo congela el release (por ejemplo `dist/releases/0.8.0/` en el repo del addon).
2. `python tools/sync_release.py --from-folder <carpeta del release>` → completa versión, zip, tamaño y SHA-256
   (verifica contra `SHA256SUMS.txt`).
3. Cuando exista el GitHub Release público: `python tools/sync_release.py --from-github` → agrega la URL real del
   asset y la página del release.
4. **Solo con autorización del dueño:** `download.enabled: true` y `status.stage: "released"` en `content/site.json`.
   El build se niega a habilitar la descarga sin `url`, `version` y `sha256`.
5. Agregar la entrada en `content/changelog.json` (EN y ES), `python tools/build.py`, `python tools/check.py --external`.

## Donaciones

Completar `donations.platforms[].url` con la página **propia** de Ko-fi y Cafecito cuando las cuentas existan y estén
probadas. El build rechaza la página genérica de la plataforma (`ko-fi.com`, `cafecito.app`). Investigación y pasos:
[docs/DONATIONS.md](docs/DONATIONS.md). La campaña (`donations.campaign`) solo se muestra con `enabled: true` y una
fuente verificable.

## Idiomas

- `/` inglés, `/es/` español. La primera visita sigue el idioma del navegador; si la persona elige con el selector,
  se recuerda (`localStorage`, clave `flc-lang`) y gana siempre.
- Sumar un idioma (fr, de, pt): copiar `i18n/en.json` a `i18n/<código>.json`, traducir, agregar el código a
  `site.languages`, y los nombres de meses en `fmt_date` de `tools/build.py`. Las URLs, `hreflang` y el sitemap se
  generan solos.

## Estructura

```
content/        datos centralizados (site, features, changelog, dungeons)
i18n/           textos por idioma
templates/      páginas Jinja2 (base.html = layout, macros.html = componentes)
assets/         css, js (sin dependencias), fuentes OFL autoalojadas, arte SVG original
media/          manifest de capturas reales + recortes maestros (media/src)
tools/          build.py, check.py, media.py, sync_release.py, art.py, shots.mjs
dist/           salida (no se versiona)
```

## Reglas que el sitio respeta

- No modifica nada del addon, su catálogo ni sus pruebas: solo **lee** capturas y releases congelados.
- Nada de donaciones dentro del juego; en la web son voluntarias y no desbloquean nada.
- No se afirma compatibilidad con el reino oficial ni se inventan descargas, cifras o testimonios.
- Proyecto de fans, sin afiliación con Blizzard (aviso en cada pie de página y en Créditos).
