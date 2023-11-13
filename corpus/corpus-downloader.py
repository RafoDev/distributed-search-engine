#!/usr/bin/env python3

from utils import *
import PyPDF2
from config import *
import io
import warnings
warnings.filterwarnings('ignore')

s3_client = boto3.client("s3")


def store_pdf(pid, content):
    filename = "corpus/pdf/"+pid+".pdf"
    s3_client.put_object(Bucket=bucket_name, Key=filename, Body=content)


def store_bytes_in_txt(pid, content):

    filename = "corpus/txt/"+pid + ".txt"
    try:
        with io.BytesIO(content) as f:
            reader = PyPDF2.PdfReader(f)
            text = ''
            for page in reader.pages:
                text += page.extract_text() + '\n'
            
            stemmed_text = preproccess(text)
            s3_client.put_object(Bucket=bucket_name, Key=filename, Body=stemmed_text)
        return True
    except:
        return False


def store_string_in_txt(pid, string):
    filename = "corpus/txt/"+pid + ".txt"
    stemmed_string = preproccess(string)
    s3_client.put_object(Bucket=bucket_name, Key=filename, Body=stemmed_string)

    return filename


if __name__ == "__main__":
    metadata = ""

    graph = json_to_graph("json/final_graph.json")
    pids = list(graph.nodes())

    j = 0

    for i in range(0, len(pids), 100):
        pids_segment = pids[i:i+100]

        print("** ", i, " ", i+100, " **")
        url = "https://api.semanticscholar.org/graph/v1/paper/batch"
        params = {
            'fields': 'title,citationCount,authors,year,abstract,openAccessPdf'}
        json = {"ids": pids_segment}

        response = requests.post(url, params=params, json=json)
        if response:
            papers = response.json()
            for paper in papers:
                print("*** ", j, " ***")
                pid = paper["paperId"]
                title = "None" if not paper["title"] else paper["title"]
                authors = ""
                if paper["authors"]:
                    for author in paper["authors"]:
                        authors += author["name"] + ","
                else:
                    authors = "None"

                year = "None" if not paper["year"] else paper["year"]
                citationCount = "None" if not paper["citationCount"] else paper["citationCount"]
                abstract = "None" if not paper["abstract"] else paper["abstract"]
                pdf_url = "None"

                if paper["openAccessPdf"] and paper["openAccessPdf"]["url"]:
                    url = paper["openAccessPdf"]["url"]
                    headers = {
                        'user-agent': 'requests/2.0.0'
                    }
                    response = requests.get(
                        url, headers=headers, verify=False, timeout=5)

                    if response:
                        if response.headers["content-type"] != "application/pdf":
                            store_pdf(pid, response.content)
                            print("- pdf stored")
                            pdf_url = url
                            valid_pdf = store_bytes_in_txt(
                                pid, response.content)
                            if not valid_pdf:
                                store_string_in_txt(pid, abstract)
                                pdf_url = "None"
                                print("- abstract stored")
                        else:
                            store_string_in_txt(pid, abstract)
                            print("- abstract stored")

                    else:
                        store_string_in_txt(pid, abstract)
                        print("- abstract stored")
                else:
                    store_string_in_txt(pid, abstract)
                    print("- abstract stored")

                metadata += str(pid) + "\t" + title + "\t" + authors + "\t" + str(year) + \
                    "\t" + str(citationCount) + "\t" + \
                    pdf_url + "\t" + abstract.replace('\n', '') + "\n"

                j += 1

        else:
            print("ERROR WHEN DOWNLOADING METADATA OF PAPERS")


    metadata_filename = "metadata/meta.txt"

    s3_client.put_object(Bucket=bucket_name, Key=metadata_filename, Body=metadata)
