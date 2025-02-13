import requests
import re
print("PubMed Fetcher script is running...")


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
    """Fetch paper details using PubMed IDs."""
    if not pubmed_ids:
        return []
    
    PUBMED_SUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "json"
    }
    
    response = requests.get(PUBMED_SUMMARY_URL, params=params)
    response.raise_for_status()
    
    return response.json().get("result", {})

def identify_non_academic_authors(authors):
    """Identify non-academic authors based on their affiliation."""
    non_academic_authors = []
    companies = []
    
    for author in authors:
        affiliation = author.get("affiliation", "").lower()
        
        if affiliation and not re.search(r"university|college|school|institute|hospital", affiliation):
            non_academic_authors.append(author.get("name", "Unknown"))
            companies.append(affiliation)
    
    return non_academic_authors, companies

def extract_paper_data(query, max_results=10):
    """Fetch papers, filter based on author affiliation, and return structured data."""
    pubmed_ids = fetch_pubmed_ids(query, max_results)
    papers = fetch_paper_details(pubmed_ids)
    
    results = []
    for pmid in pubmed_ids:
        paper = papers.get(pmid, {})
        authors = paper.get("authors", [])
        title = paper.get("title", "N/A")
        pub_date = paper.get("pubdate", "N/A")
        corresponding_email = paper.get("corresponding_author_email", "N/A")
        
        non_academic_authors, companies = identify_non_academic_authors(authors)
        
        if non_academic_authors:
            results.append({
                "PubmedID": pmid,
                "Title": title,
                "Publication Date": pub_date,
                "Non-academic Author(s)": ", ".join(non_academic_authors),
                "Company Affiliation(s)": ", ".join(companies),
                "Corresponding Author Email": corresponding_email
            })
    
    return results


