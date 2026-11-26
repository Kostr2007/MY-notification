# Источники звуков

## Дерево, бумага и капля

В `source/` лежат публичные HQ MP3 с Freesound без дополнительной обработки. На страницах авторов также доступны оригиналы в WAV или AIFF. Лицензия всех трёх записей — [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/).

| Файл | Автор и запись | Обработка |
| --- | --- | --- |
| `wood.wav` | [Stiff wooden tap, Raclure](https://freesound.org/people/Raclure/sounds/405550/) | Более низкий тон, мягче верхние частоты и тихий второй удар через 84 мс. 280 мс. |
| `paper.wav` | [paper - crumple 02.wav, Anthousai](https://freesound.org/people/Anthousai/sounds/398897/) | Короткий участок шороха, немного ускоренный и сглаженный по краям. 205 мс. |
| `drop.wav` | [Water drop / Splash, bxyorna](https://freesound.org/people/bxyorna/sounds/410335/) | Убран фон перед всплеском, слегка поднят тон и приглушён хвост. 265 мс. |

Готовые файлы — моно PCM 48 кГц, 16 бит. В браузере исходники звучат на половине амплитуды, чтобы резкие пики не мешали сравнению.

## Glass

Исходная запись удара по стеклу `impactGlass_medium_001.ogg` из набора Kenney Impact Sounds, [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). В `source/kenney-glass-clink.wav` хранится WAV-конверсия из JingleScript.

- [Оригинальный набор Kenney](https://kenney.nl/assets/impact-sounds)
- [Документация конверсии JingleScript](https://github.com/receptron/jinglescript/blob/main/samples/sfx/SOURCES.md)

В `glass.wav` сигнал отфильтрован и мягко затухает. Второй, тихий призвук получен из того же удара повышением тона примерно на пять полутонов. Тайминг от начала показа карточки: первый удар на 40 мс, призвук на 123 мс, конец на 420 мс. Пик −15 dBFS, PCM 48 кГц, 16 бит, моно.
