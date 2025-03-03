# XMCL (X Minecraft Launcher) - Flatpak-Paket

Ein plattformübergreifender Minecraft-Launcher, der als Flatpak für Linux-Systeme verpackt ist.

## 📋 Schnellinstallation

### XMCL installieren

#### 📥 Installationsoptionen

##### Voraussetzungen
Stellen Sie sicher, dass Flatpak auf Ihrem System installiert ist. Falls nicht, besuchen Sie [flatpak.org/setup](https://flatpak.org/setup/) für distributionsspezifische Anweisungen.

##### Option 1: Installation von GitHub Releases (Empfohlen)
Laden Sie die neueste Version von [XMCL](https://github.com/v1mkss/io.github.voxelum.xmcl/releases/latest) herunter.
Zur Installation führen Sie aus:
```sh
flatpak install ./xmcl.flatpak --user
```

##### Option 2: Aus dem Repository erstellen
###### Erstellen und Installieren
```sh
flatpak-builder --user --install --force-clean build-dir io.xmcl.XMCL.yml
```

### 🚀 XMCL ausführen
Starten Sie XMCL aus Ihrem Anwendungsmenü oder verwenden Sie folgenden Befehl:
```sh
flatpak run io.github.voxelum.xmcl
```

## 🤝 Mitwirken
Ein Problem mit diesem Flatpak-Paket gefunden? Bitte:
- Öffnen Sie ein Issue
- Reichen Sie einen Pull Request ein

XMCL ist nicht mit Mojang oder Microsoft verbunden.