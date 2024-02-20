# TilesetParser

find single tile image in folder full of tilesets. It's very common that many tilesets are unorganized and contains unrecognaizable names. With TileParser you can take one tile (for example screenshot from web) and find whitch tileset contains that tile.
To parse large amount of files TilesetParser uses AI (openCV)

---

## Instalation

```
pip install TilesetParser
```

## How to use?

```
tilesetparser /path/to/source/image.bmp /path/to/folder_with_tilesets
```

After parsing every file, preview window will appear. You can browse tilesets that program found similar to the source tile.

Program takes a few arguments:

## Algorithms

By default TilesetParser calculates historgrams for input tile and every tile in tileset. You can use SSIM algorithm, whitch gives far more accurate results, but takes a bit more time.

### positional arguments:

- source_image_path
  > Path to single source tile you need to find
- tiles_folder
  > Path to tileset folder you want to parse

### options:

- -h, --help
  > Show help message and exit
- -s, --size
  > Size of a tile (default: 32)
- -q, --similarity
  > Similarity level for openCV (default: 0.8)
- -e, --extension
  > Extension of the files (default: bmp)
- -t, --tiles_per_tileset
  > How many tiles are in single tileset (default: 12)
- -d, --ssim_algorithm
  > Use SSIM algorithm (default: false)
