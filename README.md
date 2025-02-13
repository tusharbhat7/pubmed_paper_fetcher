PubMed Paper Fetcher

📌 Overview

This project fetches research papers from PubMed based on a user-specified query and filters papers with at least one author affiliated with a pharmaceutical or biotech company. The results are saved as a CSV file.

🚀 Features

Fetch research papers from PubMed using their API.

Identify authors affiliated with non-academic institutions (pharmaceutical/biotech companies).

Export results to a CSV file.

Command-line interface for easy querying.

🛠️ Installation

1️⃣ Clone the Repository

git clone https://github.com/YOUR_USERNAME/pubmed_paper_fetcher.git
cd pubmed_paper_fetcher

2️⃣ Install Dependencies Using Poetry

Make sure you have Poetry installed.

poetry install

⚡ Usage

Basic Query

poetry run get-papers-list "cancer treatment"

Enable Debug Mode

poetry run get-papers-list "cancer treatment" -d

Save Results to a CSV File

poetry run get-papers-list "cancer treatment" -f results.csv

📚 Project Structure

pubmed_paper_fetcher/
│── pubmed_fetcher.py    # Fetches research papers
│── cli.py               # CLI implementation
│── __init__.py          # Package initialization
│
├── poetry.lock
├── pyproject.toml       # Poetry configuration
└── README.md            # Documentation

🔧 Tools & Dependencies

Python 3.8+

Poetry (Dependency Management)

Requests (For making API calls)

Pandas (For handling CSV files)

LXML (For XML parsing)

💜 License

MIT License

🤝 Contributing

Pull requests are welcome! If you find any issues, feel free to open an issue.

