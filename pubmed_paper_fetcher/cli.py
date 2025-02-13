import argparse
import json
import pandas as pd
from pubmed_paper_fetcher.pubmed_fetcher import extract_paper_data

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", type=str, help="Search query for PubMed")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("-f", "--file", type=str, help="Filename to save results as CSV")

    args = parser.parse_args()

    if args.debug:
        print(f"Debug Mode: Querying PubMed for '{args.query}'")

    results = extract_paper_data(args.query, max_results=10)

    if not results:
        print("No relevant papers found.")
        return

    if args.file:
        df = pd.DataFrame(results)
        df.to_csv(args.file, index=False)
        print(f"Results saved to {args.file}")
    else:
        print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
