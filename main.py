import serpapi
import pandas as pd
import os
import time

# Your API key and search parameters
api_key = "1c3d078851f1e09f81d67ae7fdab94def91d925e3704b0f765ca4e9b2b331df4"
query = "food sovereignity"

# Pagination settings
results_per_page = 20  # Max for Google Scholar
total_pages_to_fetch = 100  # Or use a while loop until no more results
start_index = 0

# Store all results
all_results = []
current_page = 0

print(f"Starting to fetch up to {total_pages_to_fetch} pages...")

while current_page < total_pages_to_fetch:
  try:
    # Perform search with pagination
    client = serpapi.Client(api_key=api_key)
    results = client.search({
      "engine": "google_scholar",
      "q": query,
      "hl": "en",
      "start": start_index,  # Pagination parameter
      "num": results_per_page
    })

    # Extract organic results
    organic_results = results.get("organic_results", [])

    if not organic_results:
      print(f"No more results found at page {current_page + 1}")
      break

    # Add current page results
    for result in organic_results:
      result['page_number'] = current_page + 1
      result['page_position'] = start_index + result.get('position', 0)
      all_results.append(result)

    print(f"✅ Page {current_page + 1}: Retrieved {len(organic_results)} results (Total: {len(all_results)})")

    # Check if there's a next page
    pagination = results.get("serpapi_pagination", {})
    if "next" not in pagination:
      print("No more pages available")
      break

    # Update for next page
    start_index += results_per_page
    current_page += 1

    # Be respectful - add delay between requests
    time.sleep(1)

  except Exception as e:
    print(f"❌ Error on page {current_page + 1}: {e}")
    break

print(f"\n📊 Total results collected: {len(all_results)}")

# Save to Excel in your specified directory
if all_results:
  # Extract relevant fields
  results_data = []
  for result in all_results:
    row = {
      'Page Number': result.get('page_number', ''),
      'Position': result.get('page_position', ''),
      'Title': result.get('title', ''),
      'Link': result.get('link', ''),
      'Snippet': result.get('snippet', ''),
      'Publication Info': result.get('publication_info', {}).get('summary', ''),
      'Cited By Count': result.get('inline_links', {}).get('cited_by', {}).get('total', 0),
      'Cited By Link': result.get('inline_links', {}).get('cited_by', {}).get('link', ''),
      'Versions Count': result.get('inline_links', {}).get('versions', {}).get('total', 0),
      'Versions Link': result.get('inline_links', {}).get('versions', {}).get('link', ''),
      'Result ID': result.get('result_id', ''),
    }
    results_data.append(row)

  # Save to Excel
  df = pd.DataFrame(results_data)
  target_directory = "/Users/wemigliari/Documents/Pós-Doutorado & Doutorado/Pós-Doc/Articles"
  filename = "food_sovereignity_lapo.xlsx"
  full_path = os.path.join(target_directory, filename)

  os.makedirs(target_directory, exist_ok=True)
  df.to_excel(full_path, index=False)

  print(f"\n✅ Results saved to: {full_path}")
  print(f"📈 Total papers: {len(results_data)}")
  print(f"📄 Total pages: {len(set([r['Page Number'] for r in results_data]))}")
else:
  print("No results were collected")
