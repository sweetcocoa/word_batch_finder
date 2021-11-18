import requests
from collections import OrderedDict
from bs4 import BeautifulSoup


def search_daum_dic(query_keyword):
    dic_url = """http://dic.daum.net/search.do?q={0}"""
    r = requests.get(dic_url.format(query_keyword))
    soup = BeautifulSoup(r.text, "html.parser")
    result_means = soup.find_all(attrs={"class": "list_search"})
    result = parse_result(result_means)
    return query_keyword, result


def parse_result(result_means):
    for elem in result_means:
        text = elem.get_text().strip()
        if text:
            result = text.split("\n")
        break
    return result


def _queries_to_results(queries):
    results = dict()
    fails = list()
    for _query in queries:
        query = _query.strip()
        if len(query) > 0:
            try:
                query, result = search_daum_dic(query)
                results[query] = result
            except:
                fails.append(query)
    return results, fails


def queries_to_results(queries, n_retry=1):
    results, fails = _queries_to_results(queries)
    # 가끔 단어뜻 있는데 실패하는거있길래 재시도
    for i in range(n_retry):
        _results, fails = _queries_to_results(fails)
        results.update(_results)

    ordered_results = OrderedDict()
    for query in queries:
        if query in results:
            ordered_results[query] = results[query]
        else:
            ordered_results[query] = ["!!검색_오류!!"]

    return ordered_results, fails
