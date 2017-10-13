import multiprocessing
import requests
import sys
import threading
from timeit import Timer

final_results=[]
def request_item(item_id):
    try:
        print  threading.currentThread().getName()
        r = requests.get("http://hn.algolia.com/api/v1/items/%s" % item_id)
        print  threading.currentThread().getName()
        final_results.append(r.json())
        return r.json()
    except requests.RequestException:
        return None


def request_sequential(number_range):
    sys.stdout.write("Requesting sequentially...\n")

    articles = []
    for item_id in number_range:
        articles.append(request_item(item_id))
    return articles
    sys.stdout.write("done.\n")

def request_concurrent(number_range):
    sys.stdout.write("Requesting in parallel...\n")
    jobs=[]
    for i in range(4):
        t = threading.Thread(target=request_item, args=(number_range,))
        jobs.append(t)
        t.start()
    for t in jobs:
        t.join()
    sys.stdout.write("done.\n")


if __name__ == '__main__':

    number_range=range(20)
    number_threads=multiprocessing.cpu_count()

    t = Timer(lambda: request_sequential(number_range))
    print "Completed sequential in %s seconds." % t.timeit(1)
    print "--------------------------------------"

    t = Timer(lambda: request_concurrent(number_range))
    print "Completed using threads in %s seconds." % t.timeit(1)
