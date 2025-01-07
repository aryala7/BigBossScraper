# Flask Scrapy Caching Application

This project is a web scraping and caching application built with Flask and Scrapy. It fetches product information from two different websites, caches the data, and serves it through a web interface. The cache is updated periodically to ensure the data remains fresh.

## Features

- Scrapes product data (images and titles) from two websites.
- Caches scraped data locally to reduce redundant network requests.
- Background thread for periodic cache updates.
- Flask-based web interface to display the data.
- Organized and modular codebase for maintainability.

## Prerequisites

- Python 3.7+
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/aryala7/flask-scrapy-caching.git
   cd flask-scrapy-caching
   ```

2. Set up a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate # On Windows, use venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the application:
   ```bash
   python app.py
   ```

2. Open your browser and navigate to `http://127.0.0.1:5000/` to view the application.

## Project Structure

```
.
├── app.py                 # Main Flask application
├── cache_manager.py       # Handles data scraping and caching logic
├── templates/             # HTML templates for the web interface
├── static/                # Static assets (CSS, JS, images)
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

## Endpoints

### `/`
- Displays a random sample of 20 products from each category.

### `/category/<name>`
- Displays all products for a specified category (`glas` or `fliese`).

## Configuration

- **Cache expiration**: The cache is updated every 15 minutes by default. You can modify `CACHE_EXPIRATION` in `cache_manager.py` to change this interval.

## Development

### Adding a New Feature
1. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
2. Make your changes and commit them:
   ```bash
   git commit -am "Add new feature"
   ```
3. Push the branch and create a pull request:
   ```bash
   git push origin feature-name
   ```

### Testing
Currently, there are no automated tests included. You can add tests using frameworks like `pytest` or `unittest`.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributions

Contributions are welcome! Feel free to open issues or submit pull requests with improvements or fixes.

## Acknowledgments

- **Flask**: For providing a lightweight web framework.
- **Scrapy**: For its powerful web scraping capabilities.
- **Requests**: For handling HTTP requests.

