# Hanziart

Hanzi (Chinese characters) version of `asciiart`.

ASCII art uses monospaced keyboard characters, originally limited to those encoded by the ASCII standard, in place of pixels to draw raster images. The intensity of a given pixel is approximated by the visual density of the ASCII character.

Chinese characters, or *hanzi*, also known by their Japanese name *kanji*, present an even wider variety of characters to use for ASCII art.

For an example, see `apple40.txt`. Best viewed in a text editor with line-wrapping turned off.

As a proxy for their visual density, we shall use the *stroke count* of a character. Stroke count data are provided in [Unihan database](https://www.unicode.org/reports/tr38/) produced by the Unicode consortium.

## Source data

You will need to download [Unihan data (zip archive)](http://www.unicode.org/Public/UCD/latest/ucd/Unihan.zip) from Unicode. The file we need is `Unihan_DictionaryLikeData.txt` within the `Unihan.zip` archive.

## Dependencies

Written in Python3. Requires the following libraries: scikit-image (`skimage`), `scipy`, `matplotlib`, `numpy`, `argparse`, `csv`, `random`, `re`, `collections`.

## Usage

```bash
python3 hanziart.py --image photo.jpeg
python3 hanziart.py --image photo.jpeg --gradelevel 2 # Use characters up to grade level 2
python3 hanziart.py --help # Help message
```

The only required argument is the path to the image file. Assumes that `Unihan_DictionaryLikeData.txt` is in the current folder by default. Use `--help` option to see all options and their defaults.

## To do list

Some ideas for future development

 * Measure the visual density of each character, instead of using stroke count as a proxy.
 * Match the visual pattern of a character to the image, e.g. characters with strong diagonal elements better approximate part of an image with diagonal texture.
 * Use n-grams from actual written text, to better simulate readable text.
