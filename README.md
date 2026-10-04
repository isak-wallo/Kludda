# Kludd

En enkel fullskärms-ritapp för barn, byggd som en PWA och avsedd att
installeras på en gammal Android-platta och användas offline.

Rita med 6 mjuka färger (samma lugna toner som syskonappen Poppa), ångra upp till 10 streck och rensa duken. Appen låser
orienteringen till landskap, går i helskärm och låser fast layouten så att
systemfälten inte stör ritytan. Multi-touch hanteras så att barnet kan vila
en hand på skärmen medan det ritar med den andra.

## Installera på en Android-platta

1. Öppna appens URL i Chrome på Android: <https://isak-wallo.github.io/Kludda/>
2. Välj **Lägg till på hemskärm** (Chrome-meny → "Lägg till på hemskärm").
3. Starta från hemskärmen — då körs appen i standalone-läge och fungerar
   offline tack vare service workern.

## Köra lokalt

Inget byggsteg och inga beroenden. Bara öppna `index.html` i en webbläsare,
eller servea mappen med valfri statisk server (t.ex.
`python -m http.server`) om du vill testa service workern.

## Projektstruktur

| Fil | Roll |
|-----|------|
| `index.html` | Markup: startskärm, rityta, knapp-panel. |
| `app.js` | All app-logik: ritande, ångra, rensa, layout, fullscreen, SW-registrering. |
| `style.css` | Layout, safe-area, knapp-panel i porträtt och landskap. |
| `sw.js` | Service worker för offline-caching. |
| `manifest.json` | PWA-manifest (`standalone`, `landscape`, ikoner). |
| `icon-192.png`, `icon-512.png` | App-ikoner. |

## Uppdatera appen (viktigt)

Service workern cachar filerna offline. För att garantera att plattan hämtar
ny kod vid en uppdatering: **höj `VERSION`** i `sw.js` (t.ex. `v11` → `v12`)
varje gång du ändrar filer och pushar till `main`. Glömmer du det kan
plattan fastna på en gammal cachad version.

Se `CLAUDE.md` för en utförlig teknisk beskrivning av arkitektur och
konventioner.