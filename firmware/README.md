# Firmware mit der Arduino IDE

Als Firmware kommt [ESPSomfy-RTS](https://github.com/rstrouse/ESPSomfy-RTS) **v2.4.6** von Robert Strouse zum Einsatz, kompiliert und geflasht mit der **Arduino IDE 2.x**. Die Firmware wird nicht in diesem Repo mitgeliefert.

> [!NOTE]
> **Warum nicht die neueste Version?** Der gepflegte Fork [cjkas/ESPSomfy-RTS](https://github.com/cjkas/ESPSomfy-RTS) (v4.x) lässt sich nur mit PlatformIO bauen. Für die Arduino IDE ist v2.4.6 die passende Version. Sie läuft stabil, hat aber eine bekannte Schwäche: gelegentliche Neustarts durch den Watchdog. Wer später wechseln will, findet in der [Anleitung des Forks](https://github.com/cjkas/ESPSomfy-RTS#install) den Weg über fertige Binärdateien.

## 1. ESP32-Core 2.0.17 installieren

*Werkzeuge → Board → Boardverwalter*, nach **esp32** von Espressif suchen und **Version 2.0.17** installieren.

> [!IMPORTANT]
> Mit Core 3.x kompiliert ESPSomfy-RTS v2.4.6 **nicht** (getestet mit 3.3.12: 348 Fehler). Die Arduino IDE hält immer nur eine Core-Version vor. Andere ESP32-Projekte, die Core 3.x brauchen, laufen nach dem Downgrade erst wieder, wenn im Boardverwalter zurückgewechselt wird.

Falls *esp32* im Boardverwalter fehlt: Unter *Einstellungen → Zusätzliche Boardverwalter-URLs* diese Adresse eintragen:

```
https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
```

## 2. Bibliotheken installieren

*Werkzeuge → Bibliotheken verwalten*, jeweils **genau diese Version** wählen:

| Bibliothek | Autor | Version |
| --- | --- | --- |
| ArduinoJson | Benoit Blanchon | **6.21.5** (nicht 7.x) |
| PubSubClient | Nick O'Leary | **2.8.0** |
| SmartRC-CC1101-Driver-Lib | LSatan | **2.5.7** |
| WebSockets | Markus Sattler | **2.4.0** |

Die Versionen entsprechen denen, mit denen ESPSomfy-RTS seine offiziellen Releases baut.

## 3. Quellcode holen

1. [ESPSomfy-RTS v2.4.6 als ZIP](https://github.com/rstrouse/ESPSomfy-RTS/archive/refs/tags/v2.4.6.zip) herunterladen und entpacken.
2. Den entpackten Ordner in **`SomfyController`** umbenennen. Die Arduino IDE verlangt, dass der Ordner so heißt wie die `.ino`-Datei.
3. `SomfyController/SomfyController.ino` in der Arduino IDE öffnen.

Per Git geht es auch:

```sh
git clone --branch v2.4.6 --depth 1 https://github.com/rstrouse/ESPSomfy-RTS.git SomfyController
```

## 4. Board einstellen

| Einstellung (*Werkzeuge*) | Wert |
| --- | --- |
| Board | **ESP32 Dev Module** |
| Partition Scheme | **Default 4MB with spiffs (1.2MB APP/1.5MB SPIFFS)** |
| Flash Mode | QIO |
| Upload Speed | 921600 |
| Port | `/dev/cu.usbserial-…` bzw. `/dev/cu.SLAB_USBtoUART` |

Erscheint kein Port: ein Datenkabel statt eines reinen Ladekabels verwenden und ggf. den Treiber für den USB-Seriell-Chip (CP210x oder CH340) installieren.

## 5. Sketch hochladen

**Hochladen** (→) klicken. Hängt der Upload bei `Connecting…`, die **BOOT**-Taste am DevKit gedrückt halten, bis der Schreibvorgang startet.

## 6. Weboberfläche hochladen (LittleFS)

Die Weboberfläche liegt im Ordner `SomfyController/data/` und muss einmalig als LittleFS-Dateisystem auf den ESP32.

1. Das Plugin [arduino-littlefs-upload](https://github.com/earlephilhower/arduino-littlefs-upload/releases) herunterladen (`.vsix`-Datei).
2. Die Datei nach `~/.arduinoIDE/plugins/` kopieren (Ordner bei Bedarf anlegen) und die Arduino IDE neu starten.
3. Den **seriellen Monitor schließen**.
4. `⌘ ⇧ P` drücken und **Upload LittleFS to Pico/ESP8266/ESP32** wählen.

<details>
<summary>Alternative ohne Plugin: fertiges Image per esptool</summary>

`SomfyController.littlefs.bin` aus dem [Release v2.4.6](https://github.com/rstrouse/ESPSomfy-RTS/releases/tag/v2.4.6) laden und an die Adresse der SPIFFS-Partition des Default-Schemas schreiben:

```sh
esptool.py --chip esp32 --port /dev/cu.usbserial-0001 write_flash 0x290000 SomfyController.littlefs.bin
```
</details>

## 7. WLAN einrichten

1. Seriellen Monitor mit **115200 Baud** öffnen und den ESP32 per **EN**-Taste neu starten.
2. Der ESP32 öffnet das WLAN **`ESPSomfy RTS`**. Damit verbinden und `http://192.168.4.1` aufrufen.
3. Unter *Settings → Network* das Heim-WLAN eintragen. Nach dem Neustart zeigt der serielle Monitor die neue IP-Adresse.
4. Im Router eine **feste IP** für den ESP32 vergeben. Homebridge braucht später eine stabile Adresse.

## CC1101 konfigurieren

Im Web-UI unter *Settings → Radio → Transceiver* die Pins passend zur [Verdrahtung](../README.md#verdrahtung) für **ein Breadboard** eintragen:

| Feld | GPIO |
| --- | --- |
| SCLK | **33** |
| CSN | **25** |
| MOSI | **32** |
| MISO | **35** |
| TX | **26** (GDO0) |
| RX | **34** (GDO2) |
| Frequency | **433,42 MHz** |
| Protocol | RTS |
| Bit Length | 56 |
| Enable Radio | an |

Speichern. Wird der CC1101 nicht erkannt: MISO/MOSI vertauscht, CSN falsch oder fehlende 3,3-V-Versorgung.

> [!TIP]
> Die Markise mit der Telis bedienen und unter *Logs* prüfen, ob die Funktelegramme ankommen. Damit sind Frequenz und RX-Leitung bestätigt, bevor angelernt wird.

## Backups

Nach dem Anlernen über *Settings → System → Firmware → Backup* ein Backup ziehen und lokal unter `firmware/backups/` ablegen. Der Ordner steht in `.gitignore`, weil Backups WLAN-Zugangsdaten und Rolling Codes enthalten und nicht ins öffentliche Repo gehören.

> [!CAUTION]
> Das Backup enthält den Rolling-Code-Zähler. Wird später ein **altes** Backup mit niedrigerem Zähler eingespielt, ignoriert der Motor die Befehle, bis der Zähler aufgeholt hat oder neu angelernt wird. Immer das neueste Backup verwenden.

> [!WARNING]
> Markisen, Rolling Codes und Einstellungen liegen im LittleFS-Dateisystem. Ein erneuter **LittleFS-Upload** löscht sie. Vorher immer ein Backup ziehen und danach wieder einspielen.
