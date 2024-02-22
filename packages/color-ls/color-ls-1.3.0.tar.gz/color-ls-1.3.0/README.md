# colorls

Pure Python implementation of ls command with colors and icons. Inspired from [colorls](https://github.com/athityakumar/colorls). Requires [Nerd Fonts](https://github.com/ryanoasis/nerd-fonts/blob/master/readme.md) for icon/glyphs.

## Installation
`pip install color-ls`

## Usage
```
usage: lx [-h] [-1] [-a] [-B] [-d] [-f] [-F] [-I PATTERN] [-l] [-n] [-R] [--report] [-t [DEPTH]] [--version] [--si] FILE

positional arguments:
  FILE                  List information about the FILEs (the current directory by default).

optional arguments:
  -h, --help            show this help message and exit
  -1                    list items on individual lines
  -a, --all             do not ignore entires starting with .
  -B, --ignore-backups  do not list implied entires ending with ~
  -d, --directory       list directories themselves, not their contents
  -f, --file            list files only, not directories
  -F, --classify        append indicator (one of */=>@|) to entries
  -I PATTERN, --ignore PATTERN
                        do not list implied entries matching shell PATTERN
  -l, --long            use a long listing format
  -n, --numeric-uid-gid
                        like -l, but list numeric user and group IDs
  -R, --recursive       list subdirectories recursively
  --report              brief report about number of files and directories
  -t [DEPTH], --tree [DEPTH]
                        max tree depth
  --version             display current version number and exit
  --si                  display file size in SI units
```
## Requirements
- Python 3.8 or higher
- Nerd Fonts

## License
MIT
