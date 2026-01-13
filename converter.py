#!/usr/bin/env python3
"""
PNG to SVG Converter - Enhanced version with post-processing
Converts PNG images to SVG format with optional background removal.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Optional

try:
    import vtracer
    from rembg import remove
    from PIL import Image, ImageFilter, ImageEnhance
except ImportError as e:
    print(f"Error: Missing required dependency: {e}")
    print("Please run: poetry install")
    sys.exit(1)


def preprocess_image(img: Image.Image, enhance_edges: bool = True, ultra_quality: bool = False) -> Image.Image:
    """
    Preprocess image to improve vectorization quality.
    
    Args:
        img: Input PIL Image
        enhance_edges: Whether to enhance edges
        ultra_quality: Apply maximum quality preprocessing
    
    Returns:
        Processed PIL Image
    """
    # Convert to RGBA if not already
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    if enhance_edges:
        if ultra_quality:
            # Ultra quality mode: more aggressive preprocessing
            # First, apply slight gaussian blur to reduce noise
            img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
            
            # Apply unsharp mask for better edge definition
            img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
            
            # Enhance contrast more aggressively
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.4)
            
            # Enhance color saturation slightly
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.1)
        else:
            # Standard quality mode
            # Slightly sharpen the image to get cleaner edges
            img = img.filter(ImageFilter.SHARPEN)
            
            # Enhance contrast slightly
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.2)
    
    return img


def convert_to_svg(
    input_path: str,
    output_path: str,
    remove_background: bool = True,
    colormode: str = "color",
    hierarchical: str = "stacked",
    mode: str = "spline",
    filter_speckle: int = 12,
    color_precision: int = 7,
    layer_difference: int = 32,
    corner_threshold: int = 60,
    length_threshold: float = 4.0,
    max_iterations: int = 10,
    splice_threshold: int = 45,
    path_precision: int = 8,
    enhance_quality: bool = True,
    ultra_quality: bool = False,
) -> None:
    """
    Convert a PNG image to SVG format.
    
    Args:
        input_path: Path to the input PNG file
        output_path: Path to save the output SVG file
        remove_background: Whether to remove the background before conversion
        colormode: Color mode ('color' or 'binary')
        hierarchical: Hierarchical grouping ('stacked' or 'cutout')
        mode: Conversion mode ('spline', 'polygon', 'none')
        filter_speckle: Suppress speckles of this size or smaller (0-255)
        color_precision: Number of significant bits for RGB (1-8)
        layer_difference: Color difference threshold (0-255)
        corner_threshold: Corner detection threshold (0-180)
        length_threshold: Curve length threshold
        max_iterations: Maximum iterations for optimization
        splice_threshold: Splice angle threshold (0-180)
        path_precision: Path precision
        enhance_quality: Apply preprocessing to improve quality
        ultra_quality: Apply maximum quality preprocessing (slower)
    """
    
    # Validate input file
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Process the image
    temp_file = None
    try:
        # Open the image
        img = Image.open(input_path)
        
        # Remove background if requested
        if remove_background:
            print(f"Removing background from {input_path}...")
            img_no_bg = remove(img)
            
            # Preprocess if quality enhancement is enabled
            if enhance_quality:
                img_no_bg = preprocess_image(img_no_bg, ultra_quality=ultra_quality)
            
            # Save to temporary file for vtracer processing
            temp_file = input_path.replace('.png', '_temp.png')
            img_no_bg.save(temp_file)
            processing_file = temp_file
        else:
            if enhance_quality:
                img = preprocess_image(img, enhance_edges=False, ultra_quality=ultra_quality)
                temp_file = input_path.replace('.png', '_temp.png')
                img.save(temp_file)
                processing_file = temp_file
            else:
                processing_file = input_path
        
        # Convert to SVG using vtracer
        print(f"Converting {processing_file} to SVG...")
        vtracer.convert_image_to_svg_py(
            processing_file,
            output_path,
            colormode=colormode,
            hierarchical=hierarchical,
            mode=mode,
            filter_speckle=filter_speckle,
            color_precision=color_precision,
            layer_difference=layer_difference,
            corner_threshold=corner_threshold,
            length_threshold=length_threshold,
            max_iterations=max_iterations,
            splice_threshold=splice_threshold,
            path_precision=path_precision,
        )
        
        print(f"✓ Successfully converted to {output_path}")
        
    except Exception as e:
        print(f"Error during conversion: {e}")
        raise
    
    finally:
        # Clean up temporary file
        if temp_file and os.path.exists(temp_file):
            os.remove(temp_file)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Convert PNG images to SVG format with optional background removal",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert with background removal (default)
  python converter.py input.png output.svg
  
  # Keep the background
  python converter.py input.png output.svg --keep-bg
  
  # High quality conversion with preprocessing
  python converter.py input.png output.svg --enhance-quality
  
  # Use binary color mode
  python converter.py input.png output.svg --colormode binary
  
  # Adjust quality settings
  python converter.py input.png output.svg --color-precision 8 --filter-speckle 2
        """
    )
    
    parser.add_argument(
        "input",
        help="Path to input PNG file"
    )
    
    parser.add_argument(
        "output",
        nargs="?",
        help="Path to output SVG file (optional if --output-dir is specified)"
    )
    
    parser.add_argument(
        "-o", "--output-dir",
        help="Output directory for generated SVG files (default: current directory)"
    )
    
    parser.add_argument(
        "--keep-bg",
        action="store_true",
        help="Keep the background (don't remove it)"
    )
    
    parser.add_argument(
        "--no-enhance",
        action="store_true",
        help="Disable quality enhancement preprocessing (enabled by default)"
    )
    
    parser.add_argument(
        "--ultra-quality",
        action="store_true",
        help="Apply maximum quality preprocessing (slower, best results)"
    )
    
    parser.add_argument(
        "--colormode",
        choices=["color", "binary"],
        default="color",
        help="Color mode (default: color)"
    )
    
    parser.add_argument(
        "--hierarchical",
        choices=["stacked", "cutout"],
        default="stacked",
        help="Hierarchical grouping mode (default: stacked)"
    )
    
    parser.add_argument(
        "--mode",
        choices=["spline", "polygon", "none"],
        default="spline",
        help="Conversion mode (default: spline)"
    )
    
    parser.add_argument(
        "--filter-speckle",
        type=int,
        default=12,
        help="Suppress speckles of this size or smaller, 0-255 (default: 12)"
    )
    
    parser.add_argument(
        "--color-precision",
        type=int,
        default=7,
        help="Number of significant bits for RGB, 1-8 (default: 7)"
    )
    
    parser.add_argument(
        "--layer-difference",
        type=int,
        default=32,
        help="Color difference threshold, 0-255 (default: 32)"
    )
    
    parser.add_argument(
        "--corner-threshold",
        type=int,
        default=60,
        help="Corner detection threshold, 0-180 (default: 60)"
    )
    
    parser.add_argument(
        "--length-threshold",
        type=float,
        default=4.0,
        help="Curve length threshold (default: 4.0)"
    )
    
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=10,
        help="Maximum iterations for optimization (default: 10)"
    )
    
    parser.add_argument(
        "--splice-threshold",
        type=int,
        default=45,
        help="Splice angle threshold, 0-180 (default: 45)"
    )
    
    parser.add_argument(
        "--path-precision",
        type=int,
        default=8,
        help="Path precision (default: 8)"
    )
    
    args = parser.parse_args()
    
    # Determine output path
    if args.output_dir:
        # Create output directory if it doesn't exist
        os.makedirs(args.output_dir, exist_ok=True)
        
        # Generate output filename from input filename
        input_basename = os.path.basename(args.input)
        output_filename = os.path.splitext(input_basename)[0] + '.svg'
        output_path = os.path.join(args.output_dir, output_filename)
    elif args.output:
        output_path = args.output
    else:
        print("Error: Either output path or --output-dir must be specified", file=sys.stderr)
        sys.exit(1)
    
    try:
        convert_to_svg(
            input_path=args.input,
            output_path=output_path,
            remove_background=not args.keep_bg,
            colormode=args.colormode,
            hierarchical=args.hierarchical,
            mode=args.mode,
            filter_speckle=args.filter_speckle,
            color_precision=args.color_precision,
            layer_difference=args.layer_difference,
            corner_threshold=args.corner_threshold,
            length_threshold=args.length_threshold,
            max_iterations=args.max_iterations,
            splice_threshold=args.splice_threshold,
            path_precision=args.path_precision,
            enhance_quality=not args.no_enhance,
            ultra_quality=args.ultra_quality,
        )
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
