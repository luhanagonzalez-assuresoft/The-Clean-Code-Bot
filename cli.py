import argparse
from core.processor import CodeProcessor

def main():
    parser = argparse.ArgumentParser(
        description="Optimize and document code using SOLID principles"
    )
    
    parser.add_argument("file", help="Path to the input code file")
    parser.add_argument(
        "--output", "-o",
        help="Output file path",
        default="optimized_output.py"
    )

    args = parser.parse_args()

    processor = CodeProcessor()
    processor.process(args.file, args.output)

if __name__ == "__main__":
    main()