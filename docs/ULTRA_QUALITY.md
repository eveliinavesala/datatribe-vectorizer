# Ultra Quality Conversion Guide

## Maximum Quality Settings

For the absolute best quality SVG output, use the `--ultra-quality` flag combined with optimized parameters:

```bash
poetry run python converter.py input.png output.svg \
  --ultra-quality \
  --filter-speckle 16 \
  --color-precision 8 \
  --layer-difference 48
```

## What Ultra Quality Does

The `--ultra-quality` flag applies advanced image preprocessing:

1. **Gaussian Blur (0.5 radius)** - Reduces noise and artifacts from background removal
2. **Unsharp Mask (radius=2, percent=150, threshold=3)** - Enhances edge definition and sharpness
3. **Contrast Enhancement (1.4x)** - Makes edges more distinct for better vectorization
4. **Color Saturation (1.1x)** - Slightly boosts colors for better color separation

**Note:** Quality enhancement is enabled by default. Use `--no-enhance` to disable all preprocessing for fastest conversion.

## Parameter Recommendations by Use Case

### For Logos (Best Quality)
```bash
poetry run python converter.py logo.png logo.svg \
  --ultra-quality \
  --filter-speckle 16 \
  --color-precision 8 \
  --layer-difference 48 \
  --corner-threshold 90 \
  --length-threshold 6.0 \
  --max-iterations 20
```

**Results:**
- Cleanest edges
- Best color separation
- Smallest file size for quality level
- Slower processing (~2-3x longer)

### For Icons (Balanced)
```bash
poetry run python converter.py icon.png icon.svg \
  --filter-speckle 12 \
  --color-precision 7 \
  --layer-difference 32
```

**Results:**
- Good quality
- Fast processing
- Default settings work well

### For Complex Illustrations
```bash
poetry run python converter.py illustration.png illustration.svg \
  --ultra-quality \
  --filter-speckle 8 \
  --color-precision 8 \
  --layer-difference 24
```

**Results:**
- Preserves more color detail
- Better for gradients
- Larger file size

## Quality vs File Size Trade-offs

| Setting | Effect on Quality | Effect on File Size |
|---------|------------------|---------------------|
| `--ultra-quality` | Better edges | Smaller (cleaner paths) |
| `--filter-speckle 16` | Cleaner output | Smaller (fewer artifacts) |
| `--color-precision 8` | More colors | Larger (more layers) |
| `--layer-difference 48` | Fewer colors | Smaller (fewer layers) |

## Processing Time

- **Standard mode**: ~1-2 seconds
- **Enhanced mode** (default): ~2-3 seconds
- **Ultra quality mode**: ~3-5 seconds

The extra processing time is worth it for production logos!
