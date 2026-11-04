# Hosting y publicación (preparado; nada publicado)

El sitio es HTML estático en `dist/` (~3,7 MB con todas las capturas en WebP). Dominio: **flc.quest**, registrado por
el dueño en Porkbun el 2026-11-04 (`site.base_url` = `https://flc.quest`). Hosting elegido: **GitHub Pages**, gratis,
con HTTPS. No hace falta el webhosting que ofrece Porkbun.

## Cómo se publica

- Un repositorio propio para la web, separado del addon (propuesta: `firebrand-dev/flc-website`), con este directorio.
  Los recortes maestros de las capturas (`media/src`) están versionados, así que el build no necesita las carpetas del
  addon. `dist/` y `build/` no se suben (`.gitignore`).
- `.github/workflows/pages.yml` construye y publica en cada push a `main`: instala `requirements.txt`, corre
  `tools/build.py` y `tools/check.py`, y sube `dist/` a Pages. En el repositorio: Settings → Pages → Source: GitHub
  Actions.
- El build escribe `dist/CNAME` con `flc.quest`. Con Actions, GitHub toma el dominio de Settings → Pages → Custom
  domain, que hay que cargar igual.

## DNS en Porkbun (el dueño; en este orden)

1. **Verificar el dominio en GitHub** (recomendado, se puede hacer ya): organización `firebrand-dev` → Settings →
   Pages → *Add a domain* → `flc.quest`. GitHub muestra un registro TXT (`_github-pages-challenge-firebrand-dev`, con
   un valor propio): cargarlo en Porkbun → Domain Management → DNS, y volver a GitHub → *Verify*.
2. **Crear el repositorio y cargar el dominio** en Settings → Pages → Custom domain (`flc.quest`). Recién después
   apuntar el DNS: así nadie más puede usar el dominio en GitHub Pages.
3. En Porkbun, **borrar los registros por defecto** que apuntan a `pixie.porkbun.com` (la página de estacionamiento:
   el ALIAS de `flc.quest` y los CNAME de `www` y `*`). GitHub desaconseja los comodines (`*`).
4. **Agregar** (valores de la documentación de GitHub Pages, consultada el 2026-11-04):

| Tipo | Host | Respuesta |
|---|---|---|
| A | (vacío, el dominio) | 185.199.108.153 |
| A | (vacío) | 185.199.109.153 |
| A | (vacío) | 185.199.110.153 |
| A | (vacío) | 185.199.111.153 |
| AAAA | (vacío) | 2606:50c0:8000::153 |
| AAAA | (vacío) | 2606:50c0:8001::153 |
| AAAA | (vacío) | 2606:50c0:8002::153 |
| AAAA | (vacío) | 2606:50c0:8003::153 |
| CNAME | www | firebrand-dev.github.io |

5. Cuando GitHub muestre el certificado listo (puede tardar hasta 24 horas): Settings → Pages → **Enforce HTTPS**.
6. Comprobar: `nslookup flc.quest`, `https://flc.quest/` y `https://www.flc.quest/` (redirige al dominio).

## El primer sitio simple

https://firebrand-dev.github.io/ForeverLevelingCompanion/ sale del repositorio del addon (lo mantiene el Claude del
addon). Cuando flc.quest esté publicado, conviene que ese sitio enlace o redirija a flc.quest, para no tener dos webs
oficiales. Es trabajo del repositorio del addon, no de este.

## Otras direcciones

El build también sirve en una subcarpeta (`python tools/build.py --base-url https://firebrand-dev.github.io/<repo>`):
todas las rutas llevan `/<repo>/` delante. En una subcarpeta los buscadores no leen `robots.txt`.

## Alternativa: Cloudflare Pages

Igual de simple (comando de build `python tools/build.py`, salida `dist`), CDN global y cabeceras configurables con un
archivo `_headers` (CSP, cache larga para `/media/*` y `/assets/fonts/*`, que llevan hash o no cambian).

## Antes de publicar

1. Autorización del dueño para crear el repositorio, subir el código y publicar.
2. `python tools/check.py --external` sin problemas.
3. Donaciones: siguen en "muy pronto" hasta tener las URLs propias y probadas.

## Cabeceras sugeridas (si el hosting las permite; GitHub Pages no deja configurarlas)

```
Content-Security-Policy: default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self' 'sha256-<hash del script de idioma>'; font-src 'self'; frame-ancestors 'none'
Referrer-Policy: strict-origin-when-cross-origin
X-Content-Type-Options: nosniff
```

El sitio no carga nada de terceros: fuentes, estilos, scripts e imágenes salen del propio dominio. El único script en
línea es la detección de idioma del `<head>` (y el JSON-LD, que no se ejecuta).
