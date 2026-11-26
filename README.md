# MY Notification

Уведомления для рабочего стола Material You на i3.

## Предпросмотр

Откройте [design/preview.html](design/preview.html) в браузере из локальной копии репозитория. Выберите звук и нажмите «Показать уведомление», чтобы услышать его вместе с анимацией. «Послушать исходник» воспроизводит запись до обработки. Предпросмотр учитывает системную тему и настройку уменьшенного движения.

| Звук | Уведомление | Запись до обработки |
| --- | --- | --- |
| Калимба, короткий подъём на большую терцию | [WAV](audio/kalimba.wav) | [MP3](audio/source/kalimba.mp3) |
| Пианино, мягкий нисходящий ответ | [WAV](audio/piano.wav) | [MP3](audio/source/piano.mp3) |
| Нейлоновая струна, щипок и более высокий отзвук | [WAV](audio/nylon.wav) | [MP3](audio/source/nylon.mp3) |
| Дерево, короткий стук с тихим вторым ударом | [WAV](audio/wood.wav) | [MP3](audio/source/wood.mp3) |
| Бумага, короткий сухой шорох | [WAV](audio/paper.wav) | [MP3](audio/source/paper.mp3) |
| Капля, мягкий всплеск | [WAV](audio/drop.wav) | [MP3](audio/source/drop.mp3) |

[Редактируемая карточка SVG](design/notification.svg) · [Источники и обработка звука](audio/CREDITS.md)

Тёмная тема использует снимок синей палитры m3. Карточка использует `surfaceContainerHigh`, область иконки — `primaryContainer`, текст — `onSurface` и `onSurfaceVariant`. В демо смещение на 24 px отрабатывает пружина M3 Expressive Fast Spatial за 320 мс. Прозрачность набирается без отскока за 120 мс, а уход занимает 180 мс. Звук вступает примерно через 40 мс после запуска карточки.

[Роли цвета Material 3](https://m3.material.io/styles/color/the-color-system/key-colors-tones) · [Движение Material 3](https://m3.material.io/styles/motion) · [Анатомия уведомления в Android](https://developer.android.com/design/ui/mobile/guides/home-screen/notifications)

## Что делает звуки Pixel узнаваемыми

**Materia** — тема Freedesktop на основе библиотеки Google Material Sound, опубликованная до Material 3. В сборке тема сопоставляет входящее сообщение `message-new-instant` с `notification_high-intensity`, а диалог с вопросом — с `notification_simple-01`. Поэтому при оценке обычного уведомления я сравнил оба файла и дополнительно взял штатные сигналы Pixel. [Materia Sound Theme](https://github.com/nana-4/materia-sound-theme/tree/10d30e9a01af4dec6a9cf94317c9536fec5a24f4) · [Карта событий Materia](https://github.com/nana-4/materia-sound-theme/blob/10d30e9a01af4dec6a9cf94317c9536fec5a24f4/material_product_sounds/meson.build)

Команда Pixel записывает бытовые звуки и использует их вместе с музыкальными и цифровыми тембрами. Примеры Google включают звук закрывающегося ящика и звук риса, высыпаемого на сковороду. Для уведомлений дизайнеры рекомендуют короткий, различимый сигнал, который легко услышать много раз за день. Попкорн послужил образом для музыкального жеста `Popcorn`. [Процесс команды Pixel](https://blog.google/products-and-platforms/devices/pixel/google-pixel-sound-design/) · [Дизайн звуков первого Pixel](https://design.google/library/creating-consistency-one-pixel-at-a-time) · [Интервью с Конором О’Салливаном](https://design.google/library/google-pixel-sound-design-ux-conor-osullivan)

Для запуска Material 3 и Pixel 6 в 2021 году Google создал коллекцию Material Adventures. В ней команда шире экспериментировала с текстурами и жанрами. В той же статье дизайнеры описывают, как уменьшают заметность звуков по мере того, как событие становится привычнее и чаще. [Good Vibrations, Google Design](https://design.google/library/ux-sound-haptic-material-design)

| Референс | Длина файла | Активное звучание | Наблюдение |
| --- | ---: | ---: | --- |
| Materia Simple 01 | 817 мс | ≈200 мс | Один компактный акцент |
| Materia High Intensity | 1 289 мс | ≈560 мс | Более длинный спад после акцента |
| Pixel Popcorn | 1 589 мс | ≈590 мс | Два акцента примерно на 50 и 140 мс, второй светлее |
| Pixel Eureka | 1 102 мс | ≈645 мс | Два акцента примерно на 45 и 150 мс, у второго выше главный спектральный пик |

Измерения сделаны на декодированных монофайлах. Активное звучание — от первого до последнего 5-мс окна с RMS выше −35 дБ относительно самого громкого окна файла. Моменты акцентов оценены по росту энергии. Файлы Pixel взяты из архива системных звуков для анализа. [Архив Pixel Sounds](https://3.onj.me/phonetones/unzipped/Google/%21%20Google%20Sounds/Pixel%20Sounds/notifications/)

В новых вариантах я сохранил атаку живой записи, из неё же сделал вторую, более тихую ноту через 82–112 мс и дал ей плавно затихнуть. Первый импульс звучит примерно через 40 мс после начала анимации карточки. Калимба поднимается на терцию, пианино спускается на тон, а нейлоновая струна отвечает квинтой. Это даёт общую форму и три разных контура. [Записи и обработка](audio/CREDITS.md)

## Flake

Послушать звук отдельно в графической сессии:

```sh
nix run github:Kostr2007/MY-notification -- kalimba
nix run github:Kostr2007/MY-notification -- piano
nix run github:Kostr2007/MY-notification -- nylon
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
