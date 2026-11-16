# Anbindung an Apple Home

Vorhandenes Setup: Homebridge auf einem Raspberry Pi, Apple TV als Steuerzentrale, Bedienung über die Home-App. MQTT soll nicht verwendet werden.

## Stand der Recherche (November 2026)

- ESPSomfy-RTS bringt **kein** eigenes HomeKit mit. Offizielle Integrationen gibt es für Home Assistant und MQTT.
- Auf npm gibt es **kein** Homebridge-Plugin speziell für ESPSomfy-RTS.
- ESPSomfy-RTS 4.x stellt eine lokale API auf Port 80 bereit:
  - **Befehle:** `POST /shadeCommand` mit JSON `{"shadeId": 1, "command": "Up"}` (auch `Down`, `My`, `Stop`) oder `{"shadeId": 1, "target": 50}` für eine Position in Prozent. Alternativ als Query-Parameter per GET.
  - **Zustand:** WebSocket `ws://<gerät>/ws` mit Events wie `shadeState` (Position, Ziel, Richtung). Protokoll: [PROTOCOL.md](https://github.com/cjkas/ESPSomfy-RTS/blob/main/docs/PROTOCOL.md).
  - Ist im Web-UI ein PIN/Passwort gesetzt, braucht jede Anfrage einen Token (`/login` → Header `apikey`).

## Optionen

| Option | Aufwand | Ergebnis in Apple Home |
| --- | --- | --- |
| **A – eigenes Homebridge-Plugin** in diesem Repo | mittel | echte **Markise/Jalousie** mit Prozent-Schieberegler und Live-Position, Siri („Fahr die Markise auf 40 %“) |
| B – generisches HTTP-Plugin (z. B. Taster pro Befehl) | gering | vier Schalter „Auf/Ab/Stopp/My“, keine Position, wirkt provisorisch |
| C – HomeKit direkt auf dem ESP32 (z. B. HomeSpan) | hoch | eigene Firmware nötig, Weboberfläche und Rolling-Code-Verwaltung von ESPSomfy-RTS gehen verloren |

**Empfehlung: Option A.** Ein schlankes Plugin (`homebridge-espsomfy-rts`) bildet die Markise als HomeKit-`WindowCovering` ab:

- `TargetPosition` → `POST /shadeCommand` mit `target`
- `CurrentPosition` / `PositionState` ← WebSocket-Event `shadeState`
- optional ein zusätzlicher Schalter „My-Position“ → `command: "My"`

Hinweis zur Richtung: ESPSomfy-RTS kehrt bei Shades vom Typ *Awning* die Positionsrichtung um (bei der Home-Assistant-Anbindung über `shadeType == awning` bzw. `flipPosition`, siehe `src/MqttDisco.cpp`). Das Plugin muss dieselbe Umrechnung machen, damit „öffnen“ in der Home-App das Ausfahren der Markise bedeutet. Am echten Gerät prüfen.

## Nächste Schritte

1. Entscheidung Option A/B/C
2. Bei A: Plugin-Grundgerüst unter `homebridge/` anlegen, zuerst nur Befehle senden, dann Zustand per WebSocket lesen
3. Plugin auf dem Raspberry Pi in Homebridge installieren und mit der Home-App testen
