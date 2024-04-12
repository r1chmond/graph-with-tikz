## Contents

- [Graph With Tikz](#graph-with-tikz)
- [Installation instruction](#installation-instructions)
- [Installing TexLive](#installing-texlive)
- [Known Issues](#known-issues)
- [References](#references)

## Graph With Tikz (Flowcharts)

This app allows users to generate TikZ code for flowcharts from a JSON file. The TikZ code can then be integrated into your LaTeX document for creating sophisticated diagrams and illustrations.


## Installation instructions

```
$ virtualenv venv

linux or maxOS
$ source venv/bin/activate

windows
$ source venv/Scripts/activate
```

Install all required packages:

```
$ pip3 install -r requirements.txt
```

## Installing TexLive

To be able to compile the tikz code, users are required to install TexLive. See below for further information:

For linux or windows visit - https://eu.mirrors.cicku.me/ctan/systems/texlive/tlnet/

For macOS visit - https://www.tug.org/mactex/mactex-download.html

## Known Issues

Linux:
If using the copy button gives an error, ensure that you have "xclip" installed

```
$ sudo apt install xclip
```

## References

ICONS:
https://www.flaticon.com/free-icon/add-file_1091916?term=add+file&page=1&position=7&origin=search&related_id=1091916
https://www.flaticon.com/free-icon/tex_5105637?term=tex&page=1&position=9&origin=search&related_id=5105637
https://www.flaticon.com/free-icon/export_8828334?term=export&page=1&position=15&origin=search&related_id=8828334
https://www.flaticon.com/free-icon/broom_9742093?term=clear&page=1&position=2&origin=search&related_id=9742093
https://www.flaticon.com/free-icon/copy_1620767?term=copy&page=1&position=7&origin=search&related_id=1620767

CODE:
https://docs.python.org/3/library/tk.html

LITERATURE:
http://www.tcs.uni-luebeck.de/downloads/papers/2011/2011-10-14-configurable-graph-drawing-algorithms-jannis-pohlmann.pdf
refer to bibliography in report