"""
Command-line interface for Synthetic Generator.
"""

import sys
import argparse

# Import web module directly to avoid circular imports


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Synthetic Generator - Synthetic Data Generator for Machine Learning",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  synthetic-generator web                         # Start web UI
  synthetic-generator generate --template customer_data --rows 1000 --out data.parquet
  synthetic-generator generate --in real.csv --rows 5000 --out synthetic.csv
  synthetic-generator web --port 8080            # Start web UI on port 8080
  synthetic-generator web --host 0.0.0.0         # Start web UI accessible from network
		""",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Web UI command
    web_parser = subparsers.add_parser("web", help="Start the web interface")
    web_parser.add_argument(
        "--host", default="0.0.0.0", help="Host to bind to (default: 0.0.0.0)"
    )
    web_parser.add_argument(
        "--port", type=int, default=8000, help="Port to bind to (default: 8000)"
    )
    web_parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    # Generate command (quick path)
    gen_parser = subparsers.add_parser(
        "generate", help="Generate data quickly (template, schema, or by fitting)"
    )
    gen_parser.add_argument(
        "--template",
        help="Built-in template name (e.g., customer_data, ecommerce_data)",
    )
    gen_parser.add_argument(
        "--schema", help="Path to schema JSON file (alternative to --template)"
    )
    gen_parser.add_argument(
        "--in",
        dest="in_path",
        help="Path to real data (CSV/JSON/Parquet/Excel) to fit from",
    )
    gen_parser.add_argument(
        "--rows",
        type=int,
        default=1000,
        help="Number of rows to generate (default: 1000)",
    )
    gen_parser.add_argument("--seed", type=int, help="Optional random seed")
    gen_parser.add_argument(
        "--out", required=True, help="Output file path (.csv, .parquet)"
    )

    args = parser.parse_args()

    if args.command == "web":
        # Import web module directly to avoid circular imports
        from .web import run_app

        run_app(host=args.host, port=args.port, debug=args.debug)
    elif args.command == "generate":
        # Lazy import quick API
        import json
        from .quick import dataset, fit as quick_fit

        if args.in_path:
            model = quick_fit(args.in_path)
            df = model.sample(args.rows, seed=args.seed)
        else:
            loaded_schema = None
            if args.schema:
                with open(args.schema, "r", encoding="utf-8") as f:
                    loaded_schema = json.load(f)
            df = dataset(
                template=args.template,
                schema=loaded_schema,
                rows=args.rows,
                seed=args.seed,
            )

        # Save
        out_path = args.out
        if out_path.lower().endswith(".parquet"):
            df.to_parquet(out_path, index=False)
        elif out_path.lower().endswith(".csv"):
            df.to_csv(out_path, index=False)
        else:
            df.to_csv(out_path, index=False)
        print(f"Wrote {len(df):,} rows to {out_path}")
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
