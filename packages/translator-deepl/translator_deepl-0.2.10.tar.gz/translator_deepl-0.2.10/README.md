# SRTranslator

## Install

[PyPI](https://pypi.org/project/srtranslator/)

```bash
pip install srtranslator
```

## Usage in Blender

[tin2tin](https://github.com/tin2tin) has made this [blender addon](https://github.com/tin2tin/import_subtitles). Check it out.

## Usage from script

Import stuff

```python
import os
from srtranslator import SrtFile
from srtranslator.translators.deepl_api import DeeplApi
from srtranslator.translators.deepl_handler import DeeplTranslator
from srtranslator.translators.translatepy import TranslatePy
```

Initialize translator. It can be any translator, even your own, check the docs, there are instructions per translator and how to create your own.

```python
translator = DeeplTranslator() # or TranslatePy() or DeeplApi(api_key)
```

Load, translate and save. For multiple recursive files in folder, check `examples folder`

```python
filepath = "./filepath/to/srt"
srt = SrtFile(filepath)
srt.translate(translator, "en", "es")

# Making the result subtitles prettier
srt.wrap_lines()

srt.save(f"{os.path.splitext(filepath)[0]}_translated.srt")
```

Quit translator

```python
translator.quit()
```

## Usage from GUI

[KryptoST](https://github.com/KryptoST) has made a graphical user interface. You can check it out [here](https://github.com/KryptoST/SRTranslatorGUI)

## Usage command line

```bash
python -m srtranslator ./filepath/to/srt -i SRC_LANG -o DEST_LANG
```

## Advanced usage

```
usage: __main__.py [-h] [-i SRC_LANG] [-o DEST_LANG] [-v] [-vv] [-s] [-w WRAP_LIMIT] [-t {deepl-scrap,translatepy,deepl-api}] [--auth AUTH] path

Translate an .STR file

positional arguments:
  path                  File to translate

options:
  -h, --help            show this help message and exit
  -i SRC_LANG, --src-lang SRC_LANG
                        Source language. Default: auto
  -o DEST_LANG, --dest-lang DEST_LANG
                        Destination language. Default: es (spanish)
  -v, --verbose         Increase output verbosity
  -vv, --debug          Increase output verbosity for debugging
  -s, --show-browser    Show browser window
  -w WRAP_LIMIT, --wrap-limit WRAP_LIMIT
                        Number of characters -including spaces- to wrap a line of text. Default: 50
  -t {deepl-scrap,translatepy,deepl-api}, --translator {deepl-scrap,translatepy,deepl-api}
                        Built-in translator to use
  --auth AUTH           Api key if needed on translator
```
