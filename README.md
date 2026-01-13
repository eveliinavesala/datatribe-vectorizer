# PNG to SVG Converter

A Python tool to convert PNG logos to SVG format with optional background removal.

## Features

- 🎨 Convert PNG images to scalable SVG format
- 🔲 Optional background removal
- ⚙️ Customizable conversion parameters
- 🚀 Built with `vtracer` (fast Rust-based vectorization)
- 🎯 Optimized for logos and icons

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

# Disable quality enhancement for faster processing
poetry run python converter.py input.png output.svg --no-enhance
```

### Advanced Options

```bash
# Use binary color mode (black and white only - for QR codes, line art)
poetry run python converter.py logo.png logo.svg --colormode binary

# Fine-tune quality settings
poetry run python converter.py logo.png logo.svg \
  --filter-speckle 16 \
  --color-precision 8 \
  --layer-difference 24
```

### Available Options

- `--keep-bg`: Keep the background (don't remove it)
- `--enhance-quality`: Apply preprocessing (sharpening, contrast) to improve vectorization
- `--colormode {color,binary}`: Color mode (default: color)
- `--hierarchical {stacked,cutout}`: Hierarchical grouping mode (default: stacked)
- `--mode {spline,polygon,none}`: Conversion mode (default: spline)
- `--filter-speckle N`: Suppress speckles of size N or smaller, 0-255 (default: 4)
- `--color-precision N`: Number of significant bits for RGB, 1-8 (default: 6)
- `--layer-difference N`: Color difference threshold, 0-255 (default: 16)
- `--corner-threshold N`: Corner detection threshold, 0-180 (default: 60)
- `--length-threshold N`: Curve length threshold (default: 4.0)
- `--max-iterations N`: Maximum iterations for optimization (default: 10)
- `--splice-threshold N`: Splice angle threshold, 0-180 (default: 45)
- `--path-precision N`: Path precision (default: 8)

## Quality Tips

### For Logos with Background Removal

Background removal can sometimes introduce artifacts around edges. Here are strategies to improve quality:

**1. Use Binary Mode for Simple Logos**
```bash
poetry run python converter.py logo.png logo.svg --colormode binary --filter-speckle 16
```
Binary mode works best for logos with solid colors and produces much smaller files.

**2. Increase Speckle Filtering**
```bash
poetry run python converter.py logo.png logo.svg --filter-speckle 12
```
Higher values (8-16) remove more noise and artifacts from background removal.

**3. Reduce Color Precision**
```bash
poetry run python converter.py logo.png logo.svg --color-precision 5 --layer-difference 32
```
Lower precision groups similar colors together, reducing fuzzy edges.

**4. Use Quality Enhancement**
```bash
poetry run python converter.py logo.png logo.svg --enhance-quality --filter-speckle 12
```
Applies sharpening and contrast enhancement before vectorization.

**5. Combine Multiple Settings**
```bash
poetry run python converter.py logo.png logo.svg \
  --enhance-quality \
  --filter-speckle 12 \
  --color-precision 7 \
  --layer-difference 32
```

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
# datatribe-vectorizer
