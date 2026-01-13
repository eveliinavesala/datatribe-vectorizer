# Test Quality Comparison

This document shows all test conversions performed with different settings and their results.

## Source Image

**File:** `test_logo.png` (1.3 KB)  
**Description:** Simple test logo with a blue circle, white background, and geometric elements created with PIL

---

## Test Results

### 1. With Background (Baseline)

**File:** `test_logo_with_bg.svg` (2.4 KB)  
**Command:**
```bash
poetry run python converter.py test_logo.png test_logo_with_bg.svg --keep-bg
```

**Parameters:**
- Background removal: Disabled (`--keep-bg`)
- Quality enhancement: Enabled (default)
- Filter speckle: 12 (default)
- Color precision: 7 (default)
- Layer difference: 32 (default)

**Results:**
- Clean conversion with white background preserved
- No artifacts since no background removal
- Good baseline for comparison

---

### 2. Default Settings (No Background)

**File:** `test_logo_no_bg.svg` (15 KB)  
**Command:**
```bash
poetry run python converter.py test_logo.png test_logo_no_bg.svg
```

**Parameters:**
- Background removal: Enabled
- Quality enhancement: Enabled (default)
- Filter speckle: 4 (old default)
- Color precision: 6 (old default)
- Layer difference: 16 (old default)

**Results:**
- Background successfully removed
- Many small artifacts and color variations (114 paths)
- Fuzzy edges around the circle
- Large file size due to many small paths

**Issues:**
- Too many color variations picked up from background removal artifacts
- Low speckle filtering allowed noise through
- Low layer difference created too many color layers

---

### 3. Enhanced Quality

**File:** `test_logo_no_bg_enhanced.svg` (8.7 KB)  
**Command:**
```bash
poetry run python converter.py test_logo.png test_logo_no_bg_enhanced.svg \
  --enhance-quality \
  --filter-speckle 12 \
  --color-precision 7 \
  --layer-difference 32
```

**Parameters:**
- Background removal: Enabled
- Quality enhancement: Enabled
- Filter speckle: 12
- Color precision: 7
- Layer difference: 32

**Results:**
- Much cleaner than default (95 paths vs 114)
- Better edge quality from preprocessing
- Reduced artifacts from higher speckle filtering
- 42% smaller file size than default

**Improvements:**
- Sharpening filter improved edge detection
- Higher speckle filtering removed noise
- Higher layer difference grouped similar colors

---

### 4. High Quality Parameters

**File:** `test_logo_no_bg_hq.svg` (14 KB)  
**Command:**
```bash
poetry run python converter.py test_logo.png test_logo_no_bg_hq.svg \
  --color-precision 8 \
  --filter-speckle 8 \
  --corner-threshold 90 \
  --length-threshold 8.0
```

**Parameters:**
- Background removal: Enabled
- Quality enhancement: Enabled (default)
- Filter speckle: 8
- Color precision: 8
- Layer difference: 32 (default)
- Corner threshold: 90
- Length threshold: 8.0

**Results:**
- High color precision captured more color variations
- Lower speckle filtering kept more detail
- Similar file size to default
- More paths than enhanced version

**Analysis:**
- Higher color precision (8) created more color layers
- Lower speckle filtering (8) kept more small elements
- Not optimal for this use case

---

### 5. Binary Mode

**File:** `test_logo_no_bg_binary.svg` (929 bytes)  
**Command:**
```bash
poetry run python converter.py test_logo.png test_logo_no_bg_binary.svg \
  --colormode binary \
  --filter-speckle 16
```

**Parameters:**
- Background removal: Enabled
- Quality enhancement: Enabled (default)
- Color mode: binary (black and white only)
- Filter speckle: 16

**Results:**
- Smallest file size (929 bytes - 94% smaller than default!)
- Only 6 paths (vs 114 in default)
- Clean, crisp edges
- Lost all color information

**Best for:**
- QR codes, line art, simple icons
- When file size is critical
- When color is not needed

---

### 6. Ultra High Quality Parameters

**File:** `test_logo_ultra_hq.svg` (8.6 KB)  
**Command:**
```bash
poetry run python converter.py test_logo.png test_logo_ultra_hq.svg \
  --filter-speckle 16 \
  --color-precision 8 \
  --layer-difference 48 \
  --corner-threshold 90 \
  --length-threshold 6.0 \
  --max-iterations 20
```

**Parameters:**
- Background removal: Enabled
- Quality enhancement: Enabled (default)
- Filter speckle: 16
- Color precision: 8
- Layer difference: 48
- Corner threshold: 90
- Length threshold: 6.0
- Max iterations: 20

**Results:**
- Very clean output
- High speckle filtering removed artifacts
- High layer difference grouped colors well
- Similar size to enhanced version

**Analysis:**
- Good balance of quality and file size
- High layer difference (48) compensated for high color precision (8)

---

### 7. Ultra Quality Mode (NEW)

**File:** `test_logo_ultra.svg` (6.3 KB)  
**Command:**
```bash
poetry run python converter.py test_logo.png test_logo_ultra.svg \
  --ultra-quality \
  --filter-speckle 16 \
  --color-precision 8 \
  --layer-difference 48
```

**Parameters:**
- Background removal: Enabled
- Quality enhancement: Ultra mode (`--ultra-quality`)
- Filter speckle: 16
- Color precision: 8
- Layer difference: 48

**Ultra Quality Preprocessing:**
- Gaussian blur (0.5 radius) - noise reduction
- Unsharp mask (radius=2, percent=150) - edge enhancement
- Contrast enhancement (1.4x)
- Color saturation (1.1x)

**Results:**
- **Best overall quality**
- Cleanest edges (only 9 paths!)
- Smallest file size among color versions (6.3 KB)
- 58% smaller than default
- 27% smaller than enhanced

**Why it's better:**
- Gaussian blur removed noise before vectorization
- Unsharp mask created crisp edge definition
- Enhanced contrast improved color separation
- Aggressive filtering removed all artifacts

---

### 8. Default with New Settings

**File:** `test_logo_default_new.svg` (8.7 KB)  
**Command:**
```bash
poetry run python converter.py test_logo.png test_logo_default_new.svg
```

**Parameters (New Defaults):**
- Background removal: Enabled
- Quality enhancement: Enabled
- Filter speckle: 12 (improved from 4)
- Color precision: 7 (improved from 6)
- Layer difference: 32 (improved from 16)

**Results:**
- Same quality as enhanced version
- Now the default behavior
- Good balance for most use cases

---

## Summary Comparison

| File | Size | Paths | Quality | Speed | Best For |
|------|------|-------|---------|-------|----------|
| test_logo_with_bg.svg | 2.4 KB | 9 | 4/5 | Fast | Logos with backgrounds |
| test_logo_no_bg.svg | 15 KB | 114 | 2/5 | Fast | Old defaults (poor) |
| test_logo_no_bg_enhanced.svg | 8.7 KB | 95 | 4/5 | Medium | General purpose |
| test_logo_no_bg_hq.svg | 14 KB | ~100 | 3/5 | Medium | Not optimal |
| test_logo_no_bg_binary.svg | 929 B | 6 | 5/5 | Fast | B&W logos, QR codes |
| test_logo_ultra_hq.svg | 8.6 KB | ~90 | 4/5 | Slow | Good balance |
| **test_logo_ultra.svg** | **6.3 KB** | **9** | **5/5** | **Slow** | **Production logos** |
| test_logo_default_new.svg | 8.7 KB | 95 | 4/5 | Medium | Default (good) |

## Recommendations

### Winner: Ultra Quality Mode
```bash
poetry run python converter.py logo.png logo.svg \
  --ultra-quality \
  --filter-speckle 16 \
  --color-precision 8 \
  --layer-difference 48
```

**Why:**
- Best edge quality
- Smallest file size for color output
- Fewest paths (cleaner SVG)
- Worth the extra processing time

### Runner-up: Default (Enhanced)
```bash
poetry run python converter.py logo.png logo.svg
```

**Why:**
- Good quality out of the box
- Fast processing
- No parameter tuning needed

### Special Case: Binary Mode
```bash
poetry run python converter.py logo.png logo.svg --colormode binary --filter-speckle 16
```

**Why:**
- Smallest file size (94% reduction!)
- Perfect for simple logos
- Only use when color isn't needed
