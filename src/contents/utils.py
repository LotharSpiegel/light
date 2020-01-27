
def build_breadcrumbs(page_title, page_url, parents):
    breadcrumbs = [(page_title, page_url)]
    for parent in parents:
        breadcrumbs.append((parent[0], parent[1]))
    return breadcrumbs[::-1]