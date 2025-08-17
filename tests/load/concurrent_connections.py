import requests
from concurrent.futures import as_completed, ThreadPoolExecutor

# exec into the tests container and run `pip install requests`

def fetch_url(url, index):
	try:
		response = requests.get(url, timeout=20) # Add a timeout for robustness
		response.raise_for_status() # Raise an exception for bad status codes
		return index, url, response.text # Or response.json(), etc.
	except requests.exceptions.RequestException as e:
		return index, url, f"Error: {e}"

if __name__ == "__main__":
	url = "http://candid-api-1:8000/test"

	with ThreadPoolExecutor(max_workers=4000) as executor:
		# Submit tasks and map futures to their corresponding URLs
		future_to_url = {executor.submit(fetch_url, url, index): index for index in range(4000)}

		print("waiting for requests", flush=True)

		# Process results as they complete
		for future in as_completed(future_to_url):
			index, url, data = future.result()
			print(f"Finished processing: {index} {url} {data}")