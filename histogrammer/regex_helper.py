import re 

def find_belle_group(string: str) -> str:
    tree_search = re.compile(r'(\S+)\_[pP]$')
    match = tree_search.search(string)
    if match:
        return str(match.group(1))
    else: 
        return None