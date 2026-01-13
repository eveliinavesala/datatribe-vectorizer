# Quality Comparison Results

## Test Results for Different Conversion Settings

### File Sizes
| Version | Size | Description |
|---------|------|-------------|
| test_logo_no_bg_binary.svg | 929 bytes | Binary mode with speckle filtering |
| test_logo_with_bg.svg | 2.4 KB | Original with background |
| test_logo_no_bg_enhanced.svg | 8.7 KB | Enhanced quality with preprocessing |
| test_logo_no_bg_hq.svg | 14 KB | High quality color mode |
| test_logo_no_bg.svg | 15 KB | Default settings |

### Recommendations

#### Best for Simple Logos (Recommended)
**Binary Mode** - Cleanest output, smallest file size
```bash
poetry run python converter.py logo.png logo.svg --colormode binary --filter-speckle 16
```
- Clean, crisp edges
- Smallest file size (929 bytes vs 15 KB)
- No color artifacts
- Only works well for logos with solid colors

#### Best for Multi-Color Logos
**Enhanced Quality Mode (Default)** - Good balance of quality and file size
```bash
poetry run python converter.py logo.png logo.svg \
  --filter-speckle 12 \
  --color-precision 7 \
  --layer-difference 32
```
- Preserves multiple colors
- Reduces artifacts through preprocessing (enabled by default)
- Moderate file size (8.7 KB)
- Better edge quality than standard mode

#### For Logos with Background (No Removal Needed)
**Keep Background Mode** - Best when background is part of the design
```bash
poetry run python converter.py logo.png logo.svg --keep-bg
```
- No artifacts from background removal
- Smallest file for colored logos
- Preserves original composition

## Key Parameters Explained

### `--filter-speckle N`
Removes small isolated pixels/artifacts. Higher values = more aggressive filtering.
- Default: 4
- For background removal: 12-16 recommended
- For clean images: 4-8

### `--color-precision N`
Bits of precision for RGB colors. Lower = fewer colors = cleaner output.
- Default: 6 (64 color levels per channel)
- For logos: 5-7 recommended
- For photos: 7-8

### `--layer-difference N`
Color threshold for grouping similar colors together.
- Default: 16
- Higher values (24-32) = more aggressive color grouping
- Lower values (8-16) = more color fidelity

### `--colormode binary`
Converts to pure black and white (no grays).
- Best for: Simple logos, icons, line art
- Not suitable for: Gradients, photos, multi-color designs

### `--no-enhance`
Disables quality enhancement preprocessing (enabled by default).
- Default behavior: Applies sharpening + contrast (1.2x) enhancement
- Use `--no-enhance` for: Fastest processing, simple shapes
- Use `--ultra-quality` for: Maximum quality with Gaussian blur + unsharp mask + contrast (1.4x) + color saturation (1.1x)
