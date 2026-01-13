# Organizing Generated Files

By default, the converter saves SVG files to the same location you specify. To keep your project organized, you can use the `--output-dir` (or `-o`) flag to automatically save all generated SVGs to a specific directory. Please first create a directory called `generated` in the root of your project.

## Using Output Directory

### Basic Usage

```bash
# Saves to generated/logo.svg
poetry run python converter.py logo.png -o generated

# Saves to output/icon.svg
poetry run python converter.py icon.png --output-dir output
```

The converter will:
1. Create the directory if it doesn't exist
2. Use the input filename (with .svg extension) as the output filename
3. Save the file to the specified directory

### Batch Processing Example

```bash
# Process multiple files to the same output directory
for file in logos/*.png; do
    poetry run python converter.py "$file" -o generated
done
```

This will convert all PNG files in the `logos/` directory and save them to `generated/`.

### Gitignore

The project includes a `.gitignore` file that excludes:
- `generated/` directory
- All `.svg` files (except specific test files)
- Build artifacts and virtual environments

This keeps your repository clean while allowing you to generate as many SVGs as needed locally.

## Directory Structure

```
PNGtoSVG/
├── converter.py          # Main script
├── generated/            # Auto-generated SVGs (gitignored)
│   ├── logo1.svg
│   ├── logo2.svg
│   └── icon.svg
├── test_logo.png         # Test input
└── README.md
```
