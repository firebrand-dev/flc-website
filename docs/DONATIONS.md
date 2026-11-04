# Donaciones: plataformas para un desarrollador en Argentina

Verificado el **2026-10-30**, rechequeado el **2026-11-04** (actualiza `FoLeCom/docs/DONATIONS_RESEARCH.md` del 2026-10-24). **No es asesoramiento
impositivo ni legal.** Lo marcado *SIN VERIFICAR* no se pudo leer en una fuente primaria (el centro de ayuda de Ko-fi
y ko-fi.com devuelven 403 a lecturas automáticas): confirmarlo en el panel de cada plataforma al crear la cuenta.

## Rechequeo del 2026-11-04

- **PayPal Argentina:** confirmado en sus páginas (actualizadas el 2026-10-28): 5,40 % + USD 0,30 por cobro
  internacional, 3,5 % de conversión, ARS 75 por retiro a banco; trata las donaciones como transacciones comerciales.
- **Ko-fi:** sigue funcionando desde Argentina solo vía PayPal (Stripe no opera en Argentina; stripe.com/global).
  **Corrección:** según fuentes secundarias de 2026, el 0 % en aportes únicos aplica solo si se apaga la opción
  "Contributor" (o "Standard") en Settings → Payment; las cuentas nuevas la traen encendida y suma un 5 %. Revisarla
  al crear la página. Que un donante pueda pagar con tarjeta sin cuenta PayPal sigue *SIN VERIFICAR* (las páginas de
  ayuda de Ko-fi devuelven 403 a lecturas automáticas): hacer un aporte de prueba.
- **Cafecito:** operando (términos versión 2026-08-25). Medios de pago para quien dona: Mercado Pago, Galio Pay
  (transferencia) o Amplify (cripto), según lo que active el creador; sin PayPal ni tarjeta internacional mencionados.
  No publica su comisión ("se informan en la Plataforma"): **no poner un porcentaje en el sitio**. Requisitos: mayor de
  18; algunas funciones piden verificación de identidad. Si pueden donar personas de fuera de Argentina: *SIN VERIFICAR*.
- El sitio no muestra comisiones: solo "Ko-fi: internacional, en dólares, vía PayPal" y "Cafecito: desde Argentina,
  en pesos". Las dos tarjetas siguen en "muy pronto" hasta tener las URLs propias y probadas.

## Comparación

| Plataforma | ¿Sirve viviendo en Argentina? | Cómo paga quien dona | Comisiones | Cobro | Veredicto |
|---|---|---|---|---|---|
| **Ko-fi + PayPal** | Sí, vía PayPal (Stripe no opera en AR). Una cuenta PayPal personal alcanzaría (*SIN VERIFICAR*: solo un fragmento de búsqueda de la ayuda de Ko-fi). | PayPal; con tarjeta sin cuenta PayPal normalmente hace falta Stripe, así que algunos donantes podrían necesitar PayPal (*SIN VERIFICAR*). | Ko-fi 0 % en aportes únicos del plan gratis (*SIN VERIFICAR*, fuentes secundarias). PayPal AR: 5,40 % + USD 0,30 por cobro internacional (verificado). | Directo al saldo de PayPal | **Principal internacional** |
| **PayPal directo** | Sí, una cuenta personal puede recibir. | PayPal | Igual que arriba; PayPal trata las donaciones como transacciones comerciales; 3,5 % de conversión. | Retiro a banco argentino: ARS 75 por retiro, convertido a pesos. | Alternativa; Ko-fi da mejor página |
| **Cafecito** | Sí (plataforma argentina; mayor de 18; puede pedir verificación de identidad). | Mercado Pago, transferencia (Galio Pay), cripto (Amplify). Sin PayPal. Donantes del exterior: no lo aclara. | No publica el %: "se muestra en la plataforma". La prensa dice 5 % (*SIN VERIFICAR*). | Mercado Pago / transferencia | **Principal Argentina** |
| **Ayudar.ar** | Sí; menciona desarrolladores y creadores además de ONG. | Mercado Pago (solo AR) y PayPal | 5 % en Mercado Pago (baja con referidos); 0 % de la plataforma en PayPal; más las del procesador. | PayPal inmediato; Mercado Pago según su liberación | Opcional: no suma frente a Ko-fi + Cafecito |
| **Buy Me a Coffee** | En la práctica no: cobra por Stripe (no AR); Payoneer se habría dado de baja en 2024 (*SIN VERIFICAR* para AR). | — | — | — | **No usar** |

**Recomendación:** Ko-fi conectado a PayPal para el exterior + Cafecito para Argentina. Ayudar.ar solo si se quiere una
única página con Mercado Pago y PayPal; no hace falta con las otras dos. Coincide con lo que ya muestra el sitio.

## Pasos que tiene que hacer el dueño (no se pueden delegar)

1. **PayPal:** cuenta verificada que pueda recibir pagos. Hacer un aporte de prueba pequeño y mirar la comisión real.
2. **Ko-fi:** crear la página (por ejemplo `ko-fi.com/<nombre>`), Settings → Payments → conectar PayPal. Dejar
   apagados membresías, tienda, comisiones y metas con recompensas (mantiene el 0 % y evita "ventajas"). Texto: FLC es
   gratis y donar no desbloquea nada. Probar con un aporte real y confirmar si se puede pagar con tarjeta sin PayPal.
3. **Cafecito:** cuenta, verificación de identidad, medio de cobro (Mercado Pago o CBU/CVU). Anotar la comisión que
   muestra el panel. Mismo texto. Aporte de prueba.
4. Pegar **las URLs propias** en `content/site.json` → `donations.platforms[].url`, `python tools/build.py`,
   `python tools/check.py`.
5. Consultar a un contador sobre ARCA/monotributo antes de que los aportes sean regulares.

## Reglas (Blizzard y proyecto)

- Pedir donaciones solo en el sitio web o páginas de distribución, **nunca dentro del juego** (política de addons de
  Blizzard). El sitio lo dice en Apoyar, en el pie y en las FAQ.
- Sin recompensas, contenido exclusivo ni acceso anticipado. El sitio no muestra barras de progreso ni montos salvo
  datos reales y verificables (`donations.campaign`).
- Campaña USD 10.000–20.000: si se hace, publicar la meta solo con una fuente verificable (por ejemplo, la meta
  pública de Ko-fi) y actualizarla en `donations.campaign` con fecha.

## Fuentes

Verificadas (2026-10-30): ayudar.ar; cafecito.app/terms y sus FAQ (requisitos, medios de pago, medios de cobro,
retiros, comisiones); more.ko-fi.com/terms (actualizado 2026-07-13); paypal.com/ar/webapps/mpp/merchant-fees y
paypal.com/ar/webapps/mpp/paypal-fees (actualizadas 2026-10-28).
Sin verificar: help.ko-fi.com (403), notas de prensa sobre la comisión de Cafecito (iProfesional, El Cronista),
zverok.space (Buy Me a Coffee, 2024).
