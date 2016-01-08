import urllib2

def add_page_to_index(index, url, page_content):
    list_content = page_content.split()
    for i in list_content:
        #case 1: i already in index
        if i not in index:
            index[i] = set()
            
        #case 2: i not in index, insert i to index
    
        #finally: add url to index[i]
        index[i].add(url)

def get_page(url):
    try:  
        response = urllib2.urlopen(url)
    except:
        return ""
    page = response.read()
    return page
    
def get_all_links(page, domain):
    url_set = set()
    start_pos = 0
    end_pos = -1
    while end_pos < len(page):
        start_link = page.find('<a href=', end_pos + 1)
        if start_link < 0:
            break
        start_pos = page.find('"', start_link)
        end_pos = page.find('"', start_pos + 1)
        url = page[start_pos + 1:end_pos]
        if url.find(domain) >= 0:
            url_set.add(url)
    return url_set

def crawl_web(seed, max_page, domain):
    to_crawl = {seed}
    crawled = set()
    graph = {}  # <url>, [list of pages it links to]
    index = {}                   
    while to_crawl:
        url = to_crawl.pop()
        if url not in crawled:
            content = get_page(url)           
            add_page_to_index(index, url, content) 
            outlinks = get_all_links(content, domain)
            graph[url] = outlinks
            to_crawl = to_crawl.union(outlinks)
            crawled.add(url)
            if len(crawled)>=max_page:
                break            
    return index, graph
            
def compute_ranks(graph):
    d = 0.8 # damping factor
    numloops = 100 

    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages

    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            for node in graph:
                if page in graph[node]:
                    newrank = newrank +d * (ranks[node] / len(graph[node]))
                    
            newranks[page] = newrank
        ranks = newranks
    return ranks
    
def print_links_in_relevance(seed, topN, domain):
    graph = {}  # <url>, [list of pages it links to]
    index = {}
    ranks = {}
    max_page = 20 
    index, graph = crawl_web(seed, max_page, domain)
    ranks = compute_ranks(graph)
    print list(reversed(sorted(ranks)))[0:topN]
     
#test    
print_links_in_relevance("http://nus.edu.sg", 10, "nus.edu")  



