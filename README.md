# Test Suite for LLM Analysis Quiz Agent

24 test cases across 6 categories (4 tests each).

## Test Categories

1. **Web Scraping** (4 tests) - Multi-page navigation, dynamic content, forms, pagination
2. **API Sourcing** (4 tests) - Large JSON files, nested data, time-series, massive datasets
3. **Cleansing** (4 tests) - PDF extraction, text parsing, CSV cleaning, multi-page PDFs
4. **Processing** (4 tests) - Base64 decoding, date normalization, joins, nested JSON
5. **Analysis** (4 tests) - Weighted averages, percentiles, rolling sums, trimmed means
6. **Visualization** (4 tests) - Chart reading, image analysis, time-series spikes, pie charts

## Structure

Each test has:
- `index.html` - Task instructions and submission URL
- `generate_data.py` - Script to create test data files

## Usage

### Generate Test Data

```bash
cd tests/web_scraping/test_1
python generate_data.py
```

### Run Tests

Each test directory can be served as a static website. The agent should:
1. Visit `index.html`
2. Read instructions
3. Generate/download required data files
4. Solve the task
5. Submit answer to the URL specified in `index.html`

## Expected Answers

See each test's `generate_data.py` for the expected answer printed at the end.

## Notes

- Data files are NOT included - run `generate_data.py` to create them
- All generators use deterministic patterns for reproducible results
- Large files (>1MB) are generated to test performance
- PDF generation requires `reportlab` library



