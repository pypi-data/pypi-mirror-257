# flitz-compress

`flitz-compress` is a simple zip-compression plugin for the
[flitz file manager](https://pypi.org/project/flitz/).

## Installation

```bash
pip install flitz-compress
```

## Usage

As soon as it's integrated, the plugin is automatically detected by flitz.
Then the context menu item `COMPRESS` becomes available which can be used in the
flitz settings `~/.flitz.yml`:

```
context_menu:
- CREATE_FOLDER
- CREATE_FILE
- RENAME
- COMPRESS
- PROPERTIES
```
