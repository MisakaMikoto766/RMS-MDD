
from argparse import ArgumentParser
import time
from Bio import Entrez
import json



def search(query, max_num_articles):
    "Retrieve the ids of first `max_num_articles` based on the provided query"
    handle = Entrez.esearch(db='pubmed', 
                            sort='relevance', 
                            retmax=max_num_articles,
                            retmode='xml', 
                            term=query)
    results = Entrez.read(handle)
    return results


def fetch_details(id_list):
    """
    Fetch the metadata of PubMed articles based on their IDs
    """
    ids = ','.join(id_list)
    handle = Entrez.efetch(db='pubmed', 
                        retmode='xml', 
                        id=ids)
    results = Entrez.read(handle)
    return results


def get_pubmed_data(
    symptom_list: list, 
    output_json_file: str, 
    start_date: str, 
    end_date: str, 
    email: str = '', 
    max_num_articles: int = 10000
):
    """
    Download the first `max_num_articles` pubmed abstracts for each symptom keyword in `symptom_list`
    published between `start_date` and `end_date`.
    
    Parameters: 
    ----------
    symptom_list: List of symptoms to query
    output_json_file: Path to the JSON file where to store the downloaded articles
    start_date: Start date, in the format of "%Y/%m/%d", for the PubMed article search based on their publication date.
    end_date: End date, in the format of "%Y/%m/%d", for the PubMed article search based on their publication date.
    """
    # Always provide your email when using Entrez
    Entrez.email = email

    result = {}
    start_time = time.time()
    

    for index, symptom in enumerate(symptom_list):
        symptom_start_time = time.time()

        query = f'("{symptom}"[Title/Abstract]) AND ({start_date}[Date - Publication] : {end_date}[Date - Publication])'

        results = search(query, max_num_articles=max_num_articles)
        id_list = results['IdList']

        if not id_list:
            print(f"No articles found for symptom: {symptom}")
            continue


        papers = fetch_details(id_list)
        

        count = 0  
        for i, paper in enumerate(papers['PubmedArticle']):
            abstract = paper['MedlineCitation']['Article'].get('Abstract')
            date = paper['MedlineCitation']['Article']['ArticleDate']
            if abstract and date:
                result_key = f"{symptom}_{i}"  
                result[result_key] = {
                    "symptom": symptom,
                    "article_title": paper['MedlineCitation']['Article']['ArticleTitle'],
                    "article_abstract": abstract['AbstractText'][0],
                    "pub_date": {
                        "year": paper['MedlineCitation']['Article']['ArticleDate'][0]['Year'],
                        "month": paper['MedlineCitation']['Article']['ArticleDate'][0]['Month'],
                        "day": paper['MedlineCitation']['Article']['ArticleDate'][0]['Day'],
                    }
                }
                count += 1


        elapsed_time = time.time() - symptom_start_time
        print(f"Symptom '{symptom}': {count} articles found, time taken: {elapsed_time:.2f} seconds")


    print(f"Total {len(result)} PubMed articles were downloaded in {time.time() - start_time:.2f} seconds")

    with open(output_json_file, 'w') as f:
        f.write(json.dumps(list(result.values()), indent=2))



def get_args():
    parser = ArgumentParser()
    parser.add_argument(
        "--symptom_file",
        type=str,
        default=" ",
        help="Path to the text file containing symptom keywords, one per line",
    )
    parser.add_argument(
        "--output_json",
        type=str,
        default=" ",
        help="Path to the JSON file where to store the downloaded articles",
    )
    parser.add_argument(
        "--start_date",
        type=str,
        default="2020/01/01",
        help="Start date for the PubMed search",
    )
    parser.add_argument(
        "--end_date",
        type=str,
        default="2024/09/28",
        help="End date for the PubMed search",
    )
    parser.add_argument(
        "--num_articles",
        type=int,
        default=50,
        help="The number of articles to retrieve per symptom",
    )
    args = parser.parse_args()
    return args


def read_symptoms(file_path):
    """
    Read symptom keywords from a text file, one per line.
    """
    with open(file_path, 'r') as f:
        return [line.strip() for line in f.readlines() if line.strip()]


if __name__ == "__main__":
    args = get_args()
    
    symptoms = read_symptoms(args.symptom_file)
    
    get_pubmed_data(
        symptom_list=symptoms, 
        output_json_file=args.output_json, 
        start_date=args.start_date, 
        end_date=args.end_date, 
        max_num_articles=args.num_articles
    )
