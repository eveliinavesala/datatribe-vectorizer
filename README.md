# PNG to SVG Converter created for @datatribe-collective-labs

A Python tool to convert PNG logos to SVG format with optional background removal.

## Features

- Convert PNG images to scalable SVG format
- Optional background removal
- Customizable conversion parameters
- Built with `vtracer` (fast Rust-based vectorization)
- Optimized for logos and icons

## Installation

This project uses Poetry for dependency management:

```bash
poetry install
```

## Usage

### Basic Usage

```bash
# Convert with background removal and quality enhancement (default)
poetry run python converter.py input.png output.svg

# Keep the background
poetry run python converter.py input.png output.svg --keep-bg

# Output to a specific directory (auto-generates filename)
poetry run python converter.py input.png --output-dir generated

# Short form
poetry run python converter.py input.png -o generated
```

### Quality Modes

The converter has three quality modes:

#### 1. Standard Mode (Fast)
```bash
poetry run python converter.py logo.png logo.svg --no-enhance
```
- Fastest processing
- Good for simple logos
- No preprocessing

#### 2. Default Mode
```bash
poetry run python converter.py logo.png logo.svg
```
- Balanced quality and speed
- Applies sharpening and contrast enhancement (1.2x)
- Best for most logos

#### 3. Ultra Quality Mode (Recommended)
```bash
poetry run python converter.py logo.png logo.svg --ultra-quality
```
- Maximum quality preprocessing
- Gaussian blur (0.5) + unsharp mask + contrast (1.4x) + color saturation (1.1x)
- Best for production logos
- 2-3x slower but worth it!

### Ultra Quality with Custom Parameters

For absolute best results, combine ultra quality with optimized parameters:

```bash
poetry run python converter.py logo.png logo.svg \
  --ultra-quality \
  --filter-speckle 16 \
  --color-precision 8 \
  --layer-difference 48
```

### Other Options

```bash
# Binary mode (black and white only - for QR codes, line art)
poetry run python converter.py logo.png logo.svg --colormode binary --filter-speckle 16

# Fine-tune individual parameters
poetry run python converter.py logo.png logo.svg \
  --filter-speckle 12 \
  --color-precision 7 \
  --layer-difference 32
```

### Available Options

**Quality Control:**
- `--no-enhance`: Disable quality enhancement (enabled by default)
- `--ultra-quality`: Apply maximum quality preprocessing (slower, best results)

**Background & Color:**
- `--keep-bg`: Keep the background (don't remove it)
- `--colormode {color,binary}`: Color mode (default: color)

**Vectorization Parameters:**
- `--filter-speckle N`: Suppress speckles of size N or smaller, 0-255 (default: 12)
- `--color-precision N`: Number of significant bits for RGB, 1-8 (default: 7)
- `--layer-difference N`: Color difference threshold, 0-255 (default: 32)
- `--corner-threshold N`: Corner detection threshold, 0-180 (default: 60)
- `--length-threshold N`: Curve length threshold (default: 4.0)
- `--max-iterations N`: Maximum iterations for optimization (default: 10)
- `--splice-threshold N`: Splice angle threshold, 0-180 (default: 45)
- `--path-precision N`: Path precision (default: 8)

**Advanced:**
- `--hierarchical {stacked,cutout}`: Hierarchical grouping mode (default: stacked)
- `--mode {spline,polygon,none}`: Conversion mode (default: spline)

## Quality Tips

### Recommended Settings by Use Case

#### Production Logos (Best Quality)
```bash
poetry run python converter.py logo.png logo.svg \
  --ultra-quality \
  --filter-speckle 16 \
  --color-precision 8 \
  --layer-difference 48
```
**Best for:** Final production logos, brand assets  
**Results:** Cleanest edges, best color separation, smallest file size  
**Processing time:** 3-5 seconds

#### General Purpose
```bash
poetry run python converter.py logo.png logo.svg
```
**Best for:** Most logos and icons  
**Results:** Good quality, fast processing  
**Processing time:** 2-3 seconds

#### Quick Conversion
```bash
poetry run python converter.py logo.png logo.svg --no-enhance
```
**Best for:** Testing, previews, simple shapes  
**Results:** Basic quality, fastest processing  
**Processing time:** 1-2 seconds

### Troubleshooting Quality Issues

**Problem: Fuzzy or mixed colors around edges**
- Solution: Use `--ultra-quality --filter-speckle 16 --layer-difference 48`

**Problem: Too many colors/large file size**
- Solution: Reduce `--color-precision 6` or increase `--layer-difference 40`

**Problem: Lost detail in complex areas**
- Solution: Increase `--color-precision 8` and decrease `--filter-speckle 8`

**Problem: Jagged edges**
- Solution: Use `--ultra-quality` and increase `--corner-threshold 90`

### Advanced Tips

For more detailed quality optimization, see [ULTRA_QUALITY.md](ULTRA_QUALITY.md)

## How It Works

1. **Background Removal** (optional): Uses `rembg` to remove the background from the PNG
2. **Vectorization**: Uses `vtracer` to trace the image and convert it to SVG paths
3. **Output**: Saves the resulting SVG file

## Dependencies

- `vtracer`: Raster to vector graphics converter
- `rembg`: Background removal tool
- `Pillow`: Image processing library

## License

MIT
