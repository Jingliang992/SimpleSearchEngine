"""
import urllib2
response = urllib2.urlopen('http://python.org/')
page = response.read()
start_link = page.find('<a href=')
start_quote = page.find('"', start_link)
end_quote = page.find('"', start_quote + 1)
url = page[start_quote + 1:end_quote]
print url

page = page[end_quote:]
start_link = page.find('<a href=')
start_quote = page.find('"', start_link)
end_quote = page.find('"', start_quote + 1)
url = page[start_quote + 1:end_quote]
print url

page = page[end_quote:]
start_link = page.find('<a href=')
start_quote = page.find('"', start_link)
end_quote = page.find('"', start_quote + 1)
url = page[start_quote + 1:end_quote]
print url

def bigger(x, y):
    if x < y:
       x = y
    return x

   
print bigger(3, 7)


def mystr(a):
    a = "sb"
    
a = "bs"
mystr(a)
print a

ljl = {"height":160, "weight":120}
print ljl["height"]
ljl['IQ']=0
print ljl['IQ']
course = ["math","english"]
print course[0]

days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
print days_in_month[0]

mixed_up = ['apple', 3, 'oranges', 27,
                     [1, 2, ['alpha', 'beta']]]

print mixed_up[4][2][0][0]
"""
s="yellow"
print s[0]

#my_dict = {"search":["google.com","baidu.com"], "shopping":["amazon.com", "taobao.com"]}
"""
my_list = [["search":["google.com","baidu.com"]], ["shopping":["amazon.com", "taobao.com"]]

def look_by_list(kw):
    global my_list
    for i in my_list:
        if i[0] == kw:
            return i[1]
    return []

def look_by_dict(index, kw):
    if kw in index:
        return index[kw]
    else:
        return None
"""       
def add_page_to_index(index, url, page_content):
    list_content = page_content.split()
    for i in list_content:
        #case 1: i already in index
        if i not in index:
            index[i] = set()
            
        #case 2: i not in index, insert i to index
    
        #finally: add url to index[i]
        index[i].add(url)
"""
my_dict = {}
add_page_to_index(my_dict, "google.com", "search me me")
add_page_to_index(my_dict, "jianlong.com", "niubi handsome smart rich tall slim")
print my_dict
print look_by_dict(my_dict, "niubi")

s = set()
a = {1, 2, 3, "string"}
s = s.union(a)
print s
"""
import urllib2

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
"""
def crawl_web(seed):
    to_crawl = {seed}
    crawled = set()
    while to_crawl:
        url = to_crawl.pop()
        if url not in crawled:
            to_crawl = to_crawl.union(get_all_links(get_page(url)))
            crawled.add(url)
            print url
        



crawl_web("http://cuda.io")
"""

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
            
 

def lookup(index, keyword):
    if keyword in index:
            return index[keyword]
    return None 

"""
def popularity(t,p):
    if t == 0:  # base case, at time step 0
        return 1 # the score is always 1 
    else:
        score = 0
        for f in friends(p): # summing over the friends
            score = score + popularity(t-1,f) # adding the popularity at the time step before
        return score
"""

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
    
index, graph = crawl_web("http://nus.edu.sg", 20, "nus.edu")  
ranks = compute_ranks(graph)