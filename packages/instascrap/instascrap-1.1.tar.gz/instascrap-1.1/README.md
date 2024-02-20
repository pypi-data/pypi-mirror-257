# instascrap

**instascrap** is a Python module for scraping Instagram profile data.

## Installation

You can install instascrap via pip:

`pip install instascrap`

## Usage

```python
from instascrap import InstaScraper

# Create an instance of InstaScraper
scraper = InstaScraper()

# Define input data
input_data = {"usernames": ["yousseifmuhammed"]}

# Run the scraper
results = scraper.Scraper(input_data)

# Print the results
for item in results:
    print(item)
```
