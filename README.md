# MY Notification

Уведомления для рабочего стола Material You на i3.

## Предпросмотр

Откройте [design/preview.html](design/preview.html) в браузере из локальной копии репозитория. Выберите звук и нажмите «Показать уведомление», чтобы услышать его вместе с анимацией. «Послушать исходник» воспроизводит запись до обработки. Предпросмотр учитывает системную тему и настройку уменьшенного движения.

| Звук | Уведомление | Запись до обработки |
| --- | --- | --- |
| Дерево, короткий стук с тихим вторым ударом | [WAV](audio/wood.wav) | [MP3](audio/source/wood.mp3) |
| Бумага, короткий сухой шорох | [WAV](audio/paper.wav) | [MP3](audio/source/paper.mp3) |
| Капля, мягкий всплеск | [WAV](audio/drop.wav) | [MP3](audio/source/drop.mp3) |

[Редактируемая карточка SVG](design/notification.svg) · [Источники и обработка звука](audio/CREDITS.md)

Тёмная тема использует снимок синей палитры m3. Карточка использует `surfaceContainerHigh`, область иконки — `primaryContainer`, текст — `onSurface` и `onSurfaceVariant`. В демо смещение на 24 px отрабатывает пружина M3 Expressive Fast Spatial за 320 мс. Прозрачность набирается без отскока за 120 мс, а уход занимает 180 мс. Звук вступает примерно через 40 мс после запуска карточки.

[Роли цвета Material 3](https://m3.material.io/styles/color/the-color-system/key-colors-tones) · [Движение Material 3](https://m3.material.io/styles/motion) · [Анатомия уведомления в Android](https://developer.android.com/design/ui/mobile/guides/home-screen/notifications)

## Flake

Послушать звук отдельно в графической сессии:

```sh
nix run github:Kostr2007/MY-notification -- wood
nix run github:Kostr2007/MY-notification -- paper
nix run github:Kostr2007/MY-notification -- drop
```

Для конфигурации m3 на i3 есть [патч подключения](nix/examples/m3-i3.patch). Он добавляет input в системный flake и передаёт его в Home Manager. Функция `my-notification.lib.withM3 pkgs m3Base` дополняет пакет m3 шаблонами Dunst и picom. Во время активации штатный `m3 render` заново генерирует конфиги из текущей палитры и пользовательских настроек. Picom использует кривую, приближающую пружину из макета, и системный масштаб анимаций. Положение, тайм-аут, история и переключатели «Анимации» и «Звук» по-прежнему задаются в m3.

В рабочей копии конфигурации NixOS проверьте, затем примените патч:

```sh
patch --dry-run -p1 < /путь/к/MY-notification/nix/examples/m3-i3.patch
patch -p1 < /путь/к/MY-notification/nix/examples/m3-i3.patch
nix flake lock
```

После активации этой конфигурации можно проверить связку в i3:

```sh
notify-send -a 'Система' -i drive-harddisk 'Резервная копия готова' 'Изменения сохранены на внешнем диске.'
```

[Glass](audio/glass.wav) — текущий звук обычных уведомлений Dunst. Dunst запускает скрипт при показе. Скрипт пропускает «Не беспокоить», служебные уведомления m3 и OSD.

## Редактирование звука

[ForgeSound Engine](https://github.com/Kostr2007/ForgeSound-Engine) позволяет работать с семплами, слоями и огибающими. Для сборки WAV используется Python и FFmpeg из dev shell:

```sh
nix develop -c python3 tools/render-sound.py all
```
