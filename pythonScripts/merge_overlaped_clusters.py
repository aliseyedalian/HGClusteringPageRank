# c1 = ['C20175', 'C05859', 'C16142', 'C20120', 'C20119', 'C17432', 'C04146', 'C04216', 'C00353', 'C03428', 'C01230', 'C00129', 'C15672', 'C00341', 'C20345', 'C00448', 'C04590']
# c2 = ['C21684', 'C05859', 'C16142', 'C20120', 'C20119', 'C04146', 'C17432', 'C04216', 'C00353', 'C03428', 'C01230', 'C00129', 'C15672', 'C00341', 'C20345', 'C00448', 'C04590']

import os


def jaccard_similarity(c1, c2):
    # Convert the lists to sets for easier comparison
    s1 = set(c1)
    s2 = set(c2)
    # Calculate the Jaccard similarity by taking the length of the intersection of the sets
    # and dividing it by the length of the union of the sets
    return float(len(s1.intersection(s2)) / len(s1.union(s2)))


def merge_overlaped_clusters(file_in_path: str, file_out_path: str, js=0.5):
    with open(file_in_path, 'r') as file_in:
        lines = file_in.readlines()
    file_out = open(file_out_path, "w")
    nc = len(lines)
    seen = []
    for i in range(nc):
        if i not in seen:
            ci = lines[i].replace('[', '').replace(']', '').replace('\n', '').split(', ')
            to_merge_clusters = [ci]
            seen.append(i)
            if i != nc-1:
                for j in range(i+1, nc):
                    if j not in seen:
                        cj = lines[j].replace('[', '').replace(']', '').replace('\n', '').split(', ')
                        if jaccard_similarity(ci, cj) >= js:
                            to_merge_clusters.append(cj)
                            seen.append(j)
            merged = set()
            for c in to_merge_clusters:
                merged = merged.union(set(c))
       
            if len(merged) > 2:
                file_out.write(str(list(merged))+"\n")
    file_out.close()

js = 0.7 # merge clusters with more than 0.7 jaccard similarity.
directory = "../results/cd_results/"
files = os.listdir(directory)
for fn in files:
    fn = directory + fn
    print(fn)
    merge_overlaped_clusters(file_in_path=fn, 
                            file_out_path=fn[:-4]+f'_merged_{str(js)}.txt'
                            ,js = js)
