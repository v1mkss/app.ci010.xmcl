# XMCL (X Minecraft Launcher) - Flatpak пакет

Крос-платформний лаунчер Minecraft, упакований як Flatpak для Linux систем.

## 📋 Швидка інсталяція

### Встановлення XMCL

#### 📥 Варіанти встановлення

##### Передумови
Переконайтеся, що на вашій системі встановлено Flatpak. Якщо ні, відвідайте [flatpak.org/setup](https://flatpak.org/setup/) для інструкцій, що відповідають вашому дистрибутиву.

##### **Варіант 1**: Встановлення з GitHub Releases (Рекомендовано)
Завантажте останню версію [XMCL](https://github.com/v1mkss/io.github.voxelum.xmcl/releases/latest).

Для встановлення виконайте:
```sh
flatpak install ./xmcl.flatpak --user
```

##### **Варіант 2**: Збірка з репозиторію

###### Збірка та встановлення
```sh
flatpak-builder --user --install --force-clean build-dir io.xmcl.XMCL.yml
```

### 🚀 Запуск XMCL
Запустіть XMCL з меню додатків або використовуйте наступну команду:
```sh
flatpak run io.github.voxelum.xmcl
```

## 🤝 Сприяння
Знайшли проблему з цим Flatpak пакетом? Будь ласка:
- Відкрийте issue
- Надішліть pull request

XMCL не пов'язаний з Mojang або Microsoft.