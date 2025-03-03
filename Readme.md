# XMCL (X Minecraft Launcher) - Flatpak Package

A cross-platform Minecraft launcher packaged as Flatpak for Linux systems.

## 📋 Quick Installation

### Install XMCL

#### 📥 Installation Options

##### Prerequisites
Ensure Flatpak is installed on your system. If not, visit [flatpak.org/setup](https://flatpak.org/setup/) for distribution-specific instructions.

##### **Option 1**: Install from GitHub Releases (Recommended)
Download the latest release of [XMCL](https://github.com/v1mkss/io.github.voxelum.xmcl/releases/latest).

To install, run:
```sh
flatpak install ./xmcl.flatpak --user
```

##### **Option 2**: Build from Repository

###### Build and Install
```sh
flatpak-builder --user --install --force-clean build-dir io.xmcl.XMCL.yml
```

### 🚀 Running XMCL
Launch XMCL from your application menu or use the following command:
```sh
flatpak run io.github.voxelum.xmcl
```

## 🤝 Contributing
Found an issue with this Flatpak package? Please:
- Open an issue
- Submit a pull request

XMCL is not affiliated with Mojang or Microsoft.