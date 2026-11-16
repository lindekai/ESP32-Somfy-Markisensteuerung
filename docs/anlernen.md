# ESP32 an der Markise anlernen

Der ESP32 wird am Somfy-Motor als **zusätzliche Fernbedienung** angemeldet. Die Telis 1 RTS Pure bleibt dabei unverändert nutzbar.

## Voraussetzungen

- Firmware geflasht und CC1101 konfiguriert ([firmware/](../firmware/README.md))
- Telis-Fernbedienung funktioniert, Batterie ist frisch
- ESP32 steht während des Anlernens in der Nähe der Markise (Reichweite erst danach testen)

## Ablauf

1. **Markise im Web-UI anlegen:** *Shades → Add Shade*, Typ **Awning**, Name z. B. „Markise“, Protokoll RTS. ESPSomfy-RTS vergibt eine eigene Fernbedienungsadresse.
2. **Fahrzeiten eintragen:** Laufzeit ganz auf und ganz ab mit der Stoppuhr messen (Telis, Auf → Endlage, Ab → Endlage) und in Sekunden eintragen. Daraus berechnet ESPSomfy-RTS Prozentpositionen.
3. **Motor in den Programmiermodus setzen:** Auf der Rückseite der Telis die **PROG**-Taste mit einem Stift ca. **2–3 Sekunden** drücken, bis die Markise kurz ruckelt (kurz auf/ab).
4. **Innerhalb von ca. 2 Minuten** im Web-UI beim Shade auf **Pair Shade** bzw. **Prog** klicken. Die Markise ruckelt erneut – der ESP32 ist angelernt.
5. Im Web-UI bestätigen, dass das Pairing erfolgreich war.
6. **Telis verknüpfen** (empfohlen): Beim Shade *Link Remote* wählen und eine Taste auf der Telis drücken. Dann folgt ESPSomfy-RTS auch Fahrten, die mit der Original-Fernbedienung ausgelöst werden.
7. **Backup ziehen** (siehe [firmware/](../firmware/README.md#backups)).

> [!WARNING]
> Im Programmiermodus wirkt PROG als Umschalter: Sendet ein **bereits angelernter** Sender PROG, wird er wieder **abgemeldet**. Pair Shade also nur einmal auslösen und nicht wiederholen, wenn die Markise schon geruckelt hat. Den Motor nicht durch Strom-Aus/-Ein zurücksetzen – ein Werksreset kann alle angelernten Sender löschen.

## Testprotokoll (Phase 3)

| Test | Erwartung | Ergebnis |
| --- | --- | --- |
| Auf | fährt in obere Endlage | |
| Ab | fährt in untere Endlage | |
| Stopp während der Fahrt | bleibt stehen | |
| My im Stillstand | fährt auf My-Position | |
| Position 50 % | stoppt etwa in der Mitte | |
| Telis bedienen | Web-UI zeigt neue Position | |
| Reichweite vom geplanten Montageort | Befehle kommen zuverlässig an (10 × hintereinander) | |
| Reichweite durch Fenster/Wand | dito | |

## Reichweite

- Antenne senkrecht ausrichten und nicht durch Metall (Gehäuse, Fensterrahmen, Heizkörper) abschirmen.
- Bei schlechtem Empfang: Montageort näher an die Markise, Spiralantenne gegen eine λ/4-Drahtantenne (≈ 17,3 cm bei 433 MHz) tauschen.
- Die Sendeleistung lässt sich im Web-UI unter *Settings → Radio* anpassen.
