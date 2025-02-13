import requests
import re
from lxml import etree

def fetch_pubmed_ids(query, max_results=10):
    """Fetch PubMed IDs matching the query from PubMed."""
    PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json"
    }
    
    response = requests.get(PUBMED_SEARCH_URL, params=params)
    response.raise_for_status()
    
    return response.json().get("esearchresult", {}).get("idlist", [])

def fetch_paper_details(pubmed_ids):
    """Fetch full paper details including author affiliations, emails, and publication date."""
    if not pubmed_ids:
        return {}

    PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "xml"
    }

    response = requests.get(PUBMED_FETCH_URL, params=params)
    response.raise_for_status()
    
    root = etree.fromstring(response.content)
    papers = {}

    for article in root.findall(".//PubmedArticle"):
        pmid = article.findtext(".//PMID")
        title = article.findtext(".//ArticleTitle", "N/A")

        # Extract publication date (ensure it's properly formatted)
        pub_date_element = article.find(".//PubDate")
        if pub_date_element is not None:
            year = pub_date_element.findtext("Year", "N/A")
            month = pub_date_element.findtext("Month", "")
            day = pub_date_element.findtext("Day", "")
            pub_date = f"{year}-{month}-{day}".strip("-")
        else:
            pub_date = "N/A"

        authors = []
        corresponding_author_email = "N/A"

        for author in article.findall(".//Author"):
            first_name = author.findtext("ForeName", "").strip()
            last_name = author.findtext("LastName", "").strip()
            name = f"{first_name} {last_name}".strip()

            affiliation = author.findtext(".//AffiliationInfo/Affiliation", "").strip()
            affiliation = affiliation.capitalize()  # Ensure proper capitalization

            email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", affiliation)
            if email_match and corresponding_author_email == "N/A":
                corresponding_author_email = email_match.group(0)  # Extract email

            if name:
                authors.append({"name": name, "affiliation": affiliation})

        papers[pmid] = {
            "title": title,
            "publication_date": pub_date,
            "authors": authors,
            "corresponding_author_email": corresponding_author_email  # Store email
        }

    return papers

def identify_non_academic_authors(authors):
    """Identify non-academic authors based on their affiliation."""
    non_academic_authors = []
    companies = []
    
    for author in authors:
        affiliation = author.get("affiliation", "").lower()
        
        if affiliation and not re.search(r"university|college|school|institute|hospital", affiliation):
            non_academic_authors.append(author.get("name", "Unknown"))
            companies.append(affiliation.capitalize())  # Ensure proper case
    
    return non_academic_authors, companies

def extract_paper_data(query, max_results=10):
    """Fetch, filter, and format paper data."""
    pubmed_ids = fetch_pubmed_ids(query, max_results)
    papers = fetch_paper_details(pubmed_ids)

    results = []
    for pmid in pubmed_ids:
        paper = papers.get(pmid, {})
        authors = paper.get("authors", [])

        print(f"\n📌 PMID: {pmid} - Authors Found: {authors}")  # Debugging line

        non_academic_authors, companies = identify_non_academic_authors(authors)

        if non_academic_authors:
            results.append({
                "PubmedID": pmid,
                "Title": paper.get("title", "N/A"),
                "Publication Date": paper.get("publication_date", "N/A"),
                "Non-academic Author(s)": ", ".join(non_academic_authors),
                "Company Affiliation(s)": ", ".join(companies),
                "Corresponding Author Email": paper.get("corresponding_author_email", "N/A")
            })

    return results
