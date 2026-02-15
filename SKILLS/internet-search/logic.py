import os
import sys
import argparse
from tavily import TavilyClient
from dotenv import load_dotenv

# --- Configuration ---
current_script_dir = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(current_script_dir, "..", ".."))
load_dotenv(os.path.join(BASE_DIR, ".env"))

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

def perform_search(query: str, search_depth: str = "smart"):
    if not TAVILY_API_KEY:
        print("ERROR: TAVILY_API_KEY not found in .env file.")
        sys.exit(1)

    client = TavilyClient(api_key=TAVILY_API_KEY)
    
    try:
        response = client.search(query=query, search_depth=search_depth, max_results=5)
        results = response.get("results", [])
        
        if not results:
            print(f"No results found for: {query}")
            return

        print(f"
--- Search Results for: {query} ---")
        for i, res in enumerate(results, 1):
            print(f"
[{i}] {res.get('title')}")
            print(f"URL: {res.get('url')}")
            print(f"Content: {res.get('content')[:500]}...")
            
    except Exception as e:
        print(f"CRITICAL ERROR during search: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Holisto Internet Search (Tavily)")
    parser.add_argument("query", type=str, help="The search query")
    parser.add_argument("--depth", type=str, choices=["basic", "smart"], default="smart", help="Search depth")
    
    args = parser.parse_args()
    perform_search(args.query, args.depth)

if __name__ == "__main__":
    main()
