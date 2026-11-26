# MY Notification

Первый вариант для рабочего стола Material You на i3. Звук **Glass** основан на записи одного удара по стеклу и звучит 420 мс.

## Предпросмотр

Откройте [design/preview.html](design/preview.html) в браузере из локальной копии репозитория. Кнопка «Показать уведомление» запускает появление карточки и звук. Карточку можно закрыть или дождаться, пока она уйдёт сама. Предпросмотр учитывает системную тему и настройку уменьшенного движения.

- [Редактируемая карточка SVG](design/notification.svg)
- [Звук WAV](audio/glass.wav)
- [Автор записи и обработка](audio/CREDITS.md)

Тёмная тема использует снимок синей палитры m3. Карточка использует `surfaceContainerHigh`, область иконки — `primaryContainer`, текст — `onSurface` и `onSurfaceVariant`. В демо смещение на 24 px отрабатывает пружина M3 Expressive Fast Spatial за 320 мс. Прозрачность набирается без отскока за 120 мс, а уход занимает 180 мс. Первый удар начинается примерно через 40 мс после запуска карточки.

[Роли цвета Material 3](https://m3.material.io/styles/color/the-color-system/key-colors-tones) · [Движение Material 3](https://m3.material.io/styles/motion) · [Анатомия уведомления в Android](https://developer.android.com/design/ui/mobile/guides/home-screen/notifications)

## Flake

Послушать звук отдельно в графической сессии:

```sh
nix run github:Kostr2007/MY-notification
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

Glass воспроизводится для обычной срочности. Dunst запускает скрипт при показе. Скрипт пропускает «Не беспокоить», служебные уведомления m3 и OSD.

## Редактирование звука

[ForgeSound Engine](https://github.com/Kostr2007/ForgeSound-Engine) позволяет работать с семплами, слоями и огибающими. Для этого варианта обработка записи и сборка WAV воспроизводятся через Python и FFmpeg из dev shell:

```sh
nix develop -c python3 tools/render-sound.py
```
