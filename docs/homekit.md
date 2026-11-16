# Anbindung an Apple Home

Vorhandenes Setup: Homebridge auf einem Raspberry Pi, Apple TV als Steuerzentrale, Bedienung über die Home-App. MQTT soll nicht verwendet werden.

## Stand der Recherche (November 2026)

- ESPSomfy-RTS bringt **kein** eigenes HomeKit mit. Offizielle Integrationen gibt es für Home Assistant und MQTT.
- Auf npm gibt es **kein** Homebridge-Plugin speziell für ESPSomfy-RTS.
- ESPSomfy-RTS v2.4.6 (Arduino-Version) stellt eine lokale API bereit:
  - **Befehle:** `http://<gerät>:8081/shadeCommand?shadeId=1&command=up` (auch `down`, `my`, `stop`) oder `…&target=50` für eine Position in Prozent. Alternativ als JSON per POST.
  - **Zustand:** WebSocket `ws://<gerät>:8080`, sendet bei jeder Bewegung ein Event mit Position, Ziel und Richtung.
  - Ist im Web-UI ein PIN oder Passwort gesetzt, braucht jede Anfrage einen API-Schlüssel.
- Beim Wechsel auf den Fork cjkas v4.x laufen API und Events auf Port 80 (`/shadeCommand`, `ws://<gerät>/ws`), siehe [PROTOCOL.md](https://github.com/cjkas/ESPSomfy-RTS/blob/main/docs/PROTOCOL.md). Ein Plugin sollte beide Varianten unterstützen.

## Optionen

| Option | Aufwand | Ergebnis in Apple Home |
| --- | --- | --- |
| **A – eigenes Homebridge-Plugin** in diesem Repo | mittel | echte **Markise/Jalousie** mit Prozent-Schieberegler und Live-Position, Siri („Fahr die Markise auf 40 %“) |
| B – generisches HTTP-Plugin (z. B. Taster pro Befehl) | gering | vier Schalter „Auf/Ab/Stopp/My“, keine Position, wirkt provisorisch |
| C – HomeKit direkt auf dem ESP32 (z. B. HomeSpan) | hoch | eigene Firmware nötig, Weboberfläche und Rolling-Code-Verwaltung von ESPSomfy-RTS gehen verloren |

**Empfehlung: Option A.** Ein schlankes Plugin (`homebridge-espsomfy-rts`) bildet die Markise als HomeKit-`WindowCovering` ab:

- `TargetPosition` → `/shadeCommand` mit `target`
- `CurrentPosition` / `PositionState` ← WebSocket-Events des Geräts
- optional ein zusätzlicher Schalter „My-Position“ → `command=my`

Hinweis zur Richtung: ESPSomfy-RTS kehrt bei Shades vom Typ *Awning* die Positionsrichtung um (im Fork cjkas sichtbar in `src/MqttDisco.cpp`: `shadeType == awning` bzw. `flipPosition`). Das Plugin muss dieselbe Umrechnung machen, damit „öffnen“ in der Home-App das Ausfahren der Markise bedeutet. Am echten Gerät prüfen.

## Nächste Schritte

1. Entscheidung Option A/B/C
2. Bei A: Plugin-Grundgerüst unter `homebridge/` anlegen, zuerst nur Befehle senden, dann Zustand per WebSocket lesen
3. Plugin auf dem Raspberry Pi in Homebridge installieren und mit der Home-App testen
