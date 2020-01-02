# nbt-tools
Read/modify NBT files. Extra tools to modify core NBT files in a very popular blocky game.

```
usage: main.py [-h] [--loglevel {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
               [--version] --src-path SRC_PATH [--unpacked-nbt]
               (--nbt | --chunk-relocator | --map-gen | --region)
               [--output-dir OUTPUT_DIR] [--point1 POINT1] [--point2 POINT2]
               [--dest-point DEST_POINT] [--dest-path DEST_PATH]

NBT File Manipulation

optional arguments:
  -h, --help            show this help message and exit
  --loglevel {DEBUG,INFO,WARNING,ERROR,CRITICAL}
  --version             show program's version number and exit
  --src-path SRC_PATH   Src path for nbt file(s)
  --unpacked-nbt        Use this option for region files, or nbt files that
                        aren't gzipped
  --nbt
  --chunk-relocator
  --map-gen
  --region

Map to Image Generator:
  Image files will be generated from all the map_*.dat files

  --output-dir OUTPUT_DIR
                        dir path of where map images will be saved

Chunk Relocator:
  Move chunk files from one save to another with an x,z offset

  --point1 POINT1       (x,z) of one corner
  --point2 POINT2       (x,z) of opposite corner
  --dest-point DEST_POINT
                        (x,z) destination of chunks
  --dest-path DEST_PATH
                        Dest path for nbt file(s)
```
