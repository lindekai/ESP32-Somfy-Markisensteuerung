# Firmware

Als Firmware kommt [ESPSomfy-RTS](https://github.com/cjkas/ESPSomfy-RTS) zum Einsatz, und zwar der gepflegte Fork von **cjkas** (ab v4.0). Das Original von [rstrouse](https://github.com/rstrouse/ESPSomfy-RTS) wird seit August 2024 nicht mehr weiterentwickelt; der Fork behebt u. a. zufällige Neustarts (Watchdog) und bündelt Web-UI, API und Events auf Port 80.

Die Firmware wird **nicht** in diesem Repo mitgeliefert, sondern direkt aus dem offiziellen Release geflasht.

## Flashen (Erstinstallation per USB)

1. Aus dem [aktuellen Release](https://github.com/cjkas/ESPSomfy-RTS/releases/latest) die Datei `SomfyController.onboard.esp32.bin.zip` laden und entpacken. Sie enthält das komplette Image (Bootloader, Partitionen, Firmware, Web-UI).
2. ESP32-DevKit per Micro-USB anschließen. Falls kein serieller Port erscheint: USB-Treiber für den USB-Seriell-Chip des Boards installieren (meist CP2102 oder CH340).
3. Flashen, z. B. mit `esptool`:

   ```sh
   pipx install esptool        # oder: pip install esptool
   ls /dev/cu.*                # Port finden, z. B. /dev/cu.usbserial-0001
   esptool --chip esp32 --port /dev/cu.usbserial-0001 --baud 460800 \
     write-flash 0x0 SomfyController.onboard.esp32.bin
   ```

   Den genauen Dateinamen und die Offset-Angabe aus der [Firmware-Anleitung im Wiki](https://github.com/cjkas/ESPSomfy-RTS/wiki/Installing-the-Firmware) übernehmen, falls sie vom Beispiel abweichen. Hängt der Upload bei „Connecting…“, die **BOOT**-Taste am DevKit gedrückt halten.

4. Nach dem Neustart spannt der ESP32 ein WLAN `ESPSomfy RTS` auf. Damit verbinden, im Browser `http://192.168.4.1` öffnen, Heim-WLAN eintragen.
5. Danach ist das Gerät im Heimnetz erreichbar. Im Router eine **feste IP** vergeben – Homebridge braucht später eine stabile Adresse.

Spätere Updates laufen über die Weboberfläche (`SomfyController.ino.esp32.bin` und `SomfyController.littlefs.esp32.bin`).

## CC1101 konfigurieren

Im Web-UI unter *Settings → Radio* die Pins entsprechend der [Verdrahtung](../README.md#verdrahtung) eintragen:

| Einstellung | Wert |
| --- | --- |
| Radio | CC1101 |
| SCK | 18 |
| CSN | 5 |
| MOSI | 23 |
| MISO | 19 |
| TX Pin (GDO0) | 26 |
| RX Pin (GDO2) | 17 |
| Frequenz | **433,42 MHz** |
| Protokoll | RTS (56 bit) |
| Radio aktiviert | ja |

Speichern. Im Status sollte der CC1101 anschließend als erkannt angezeigt werden. Wird er nicht erkannt: Verdrahtung (vor allem MISO/MOSI vertauscht) und 3,3-V-Versorgung prüfen.

> [!TIP]
> Die Markise mit der Telis-Fernbedienung bedienen und im Web-UI unter *Logs* bzw. *Frames* nachsehen, ob die Funkbefehle empfangen werden. Das bestätigt Frequenz und RX-Verdrahtung, bevor angelernt wird.

## Backups

Nach dem Anlernen ein Backup über das Web-UI ziehen (`/backup`) und lokal unter `firmware/backups/` ablegen. Der Ordner steht in `.gitignore`, weil Backups WLAN-Zugangsdaten und Rolling Codes enthalten und nicht ins öffentliche Repo gehören.

> [!CAUTION]
> Das Backup enthält den Rolling-Code-Zähler. Wird später ein **altes** Backup mit niedrigerem Zähler eingespielt, ignoriert der Motor die Befehle, bis der Zähler wieder aufgeholt hat oder neu angelernt wird. Immer das neueste Backup verwenden.
