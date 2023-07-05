def jaccard_similarity(c1:list, c2:list):
    # Convert the lists to sets for easier comparison
    s1 = set(c1)
    s2 = set(c2)
    # Calculate the Jaccard similarity by taking the length of the intersection of the sets
    # and dividing it by the length of the union of the sets
    return float(len(s1.intersection(s2)) / len(s1.union(s2)))

def have_similar_cluster_in_target(cluster:str,target_clusters, jaccard):
    cluster = cluster[1:-2].replace('\'','').replace(' ','').split(',')
    for target_cluster in target_clusters:
        target_cluster = target_cluster[1:-2].replace('\'','').replace(' ','').split(',')
        if jaccard_similarity(cluster,target_cluster) > jaccard:
            return True
    return False

def distinct_clusters(input_clusters_file:str,target_clusters_file:str,output_file:str, jaccard=0.5):
    # find and save every cluster from input_clusters which doesn't have even one
    # similar cluster in target_clusters.
    input_clusters_file = open(input_clusters_file,"r")
    input_clusters = input_clusters_file.readlines()
    input_clusters_file.close()

    target_clusters_file = open(target_clusters_file,"r")
    target_clusters = target_clusters_file.readlines()
    target_clusters_file.close()

    output = open(output_file, 'w')
    for in_cluster in input_clusters:
        if not have_similar_cluster_in_target(in_cluster,target_clusters, jaccard):
            in_cluster = in_cluster[1:-2].replace('\'','').replace(' ','').split(',')
            if len(in_cluster):
                output.write(str(in_cluster)+"\n")
    output.close()

js = 0.1  
pairs = [('CD','UC'),('CD', 'nonIBD'), 
         ('UC', 'CD'), ('UC', 'nonIBD'),
          ('nonIBD', 'CD'), ('nonIBD', 'UC') ]
for pair in pairs:
    distinct_clusters(input_clusters_file=f"../results/result_clusters_raw/Sum_samples/clusters_SumSample_{pair[0]}.txt",
                    target_clusters_file=f"../results/result_clusters_raw/Sum_samples/clusters_SumSample_{pair[1]}.txt",
                    output_file = f"../results/result_clusters_raw/Sum_samples/distinct_{pair[0]}_{pair[1]}_js{js}.txt",jaccard=js
                    )


