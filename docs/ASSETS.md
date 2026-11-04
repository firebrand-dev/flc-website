# Recursos visuales: origen y derechos

| Recurso | Origen | Derechos / notas |
|---|---|---|
| Capturas (`media/src`, lista en `media/manifest.json`) | Tomadas por el equipo de FLC con su agente de pruebas en el cliente de WoW Forever (reino de desarrollo, personajes de prueba), entre FLC 0.4 y 0.8.0-rc2. Cada entrada guarda el archivo de origen, el recorte, la versión y la fecha. | Muestran el juego de Blizzard con FLC en pantalla. Uso como capturas de un proyecto de fans, con aviso de no afiliación. **Revisar** la política de contenido de fans de Blizzard antes de publicar, porque el sitio pide donaciones (el sitio no vende ni usa arte de Blizzard fuera de las capturas). |
| Logo/emblema, brújula, curvas de nivel, ornamentos, íconos | Originales, dibujados para este sitio (`templates/macros.html`, `tools/art.py`). | Del proyecto FLC. |
| Tipografías Cinzel y Alegreya Sans | Google Fonts, autoalojadas en `assets/fonts` (solo latin y latin-ext). | SIL Open Font License 1.1; las licencias van junto a los archivos y se enlazan desde Créditos. |
| Datos (mazmorras, funciones, changelog) | Documentos del repositorio del addon (`docs/STATUS.md`, `docs/release/*`, `CHANGELOG.md`, `docs/DUNGEON_GUIDE.md`), leídos el 2026-10-30. | Textos propios. Los nombres de lugares son de Blizzard. |

## Decisiones sobre las capturas

- Ninguna imagen del sitio está retocada: los recortes son el píxel del juego. El héroe es una **composición** de
  capturas reales y lo dice debajo. En escritorio: la panorámica de la Isla de Zephras con la ventana de la guía. En
  celulares (≤ 680 px) se usa otra captura, no la misma recortada por CSS: el Valle de las Pruebas con la flecha
  "In the area" (`hero-mobile`) y, del mismo momento, la ventana de la guía "Kill: Mottled Boar 1/10" (`guide-kill`)
  a todo el ancho para que se lea. Ambas son de FLC 0.8.0-rc3, prueba `scenario-quests` del 2026-10-30.
- Nitidez: las ventanas del addon (`kind: "ui"` en el manifiesto) se publican en un solo WebP a su ancho original,
  calidad 95, y el CSS nunca las estira ni las rota (estirar, rotar o comprimir fuerte era lo que borroneaba el
  texto). Las escenas (`kind: "scene"`) van en varios anchos, calidad 88.
- Se evitaron recortes con textos viejos del addon que hablaban de "test server" (la regla nueva del addon es decir
  "en revisión"). Las capturas de 0.4/0.5 que quedan no tienen ese texto, salvo la panorámica de la Isla de Zephras,
  que no incluye ninguna ventana del addon.
- Las capturas tienen la interfaz del addon en inglés (el cliente de pruebas es enUS). Las leyendas en español lo
  aclaran donde hace falta.
- Pendiente cuando haya cliente en vivo: reemplazar por capturas del reino oficial con la versión publicada
  (`media/manifest.json` → `python tools/media.py`).
