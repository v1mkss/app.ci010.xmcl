# XMCL (X Minecraft Launcher) - Flatpak пакет

Кроссплатформенный лаунчер Minecraft, упакованный как Flatpak для Linux систем.

## 📋 Быстрая установка

### Установка XMCL

#### 📥 Варианты установки

##### Предварительные требования
Убедитесь, что на вашей системе установлен Flatpak. Если нет, посетите [flatpak.org/setup](https://flatpak.org/setup/) для инструкций, специфичных для вашего дистрибутива.

##### **Вариант 1**: Установка из GitHub Releases (Рекомендуется)
Скачайте последнюю версию [XMCL](https://github.com/v1mkss/io.github.voxelum.xmcl/releases/latest).

Для установки выполните:
```sh
flatpak install ./xmcl.flatpak --user
```

##### **Вариант 2**: Сборка из репозитория

###### Сборка и установка
```sh
flatpak-builder --user --install --force-clean build-dir io.xmcl.XMCL.yml
```

### 🚀 Запуск XMCL
Запустите XMCL из меню приложений или используйте следующую команду:
```sh
flatpak run io.github.voxelum.xmcl
```

## 🤝 Содействие
Нашли проблему с этим Flatpak пакетом? Пожалуйста:
- Откройте issue
- Отправьте pull request

XMCL не связан с Mojang или Microsoft.