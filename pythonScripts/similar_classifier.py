import os

def read_clusters(fn:str) -> list:
    clusters_file = open(fn, 'r')
    clusters = clusters_file.readlines()
    clusters_file.close()
    return clusters

def jaccard_similarity(c1:list, c2:list):
    # Convert the lists to sets for easier comparison
    s1 = set(c1)
    s2 = set(c2)
    # Calculate the Jaccard similarity by taking the length of the intersection of the sets
    # and dividing it by the length of the union of the sets
    return float(len(s1.intersection(s2)) / len(s1.union(s2)))

def count_similar_cluster_in_target(cluster:str,target_clusters, jaccard=0.7):
    count = 0
    cluster = cluster[1:-2].replace('\'','').replace(' ','').split(',')
    for t_cluster in target_clusters:
        t_cluster = t_cluster[1:-2].replace('\'','').replace(' ','').split(',')
        if jaccard_similarity(cluster,t_cluster) > jaccard:
            count += 1
    return count

def similar_classifier(input_clusters_file):   
    input_clusters = read_clusters(input_clusters_file)
    js = 0.2
    uc_nonibd_clusters = read_clusters(f'../results/result_clusters_raw/Sum_samples/distinct_UC_nonIBD_js{js}.txt')
    uc_cd_clusters = read_clusters(f'../results/result_clusters_raw/Sum_samples/distinct_UC_CD_js{js}.txt')
    cd_nonibd_clusters = read_clusters(f'../results/result_clusters_raw/Sum_samples/distinct_CD_nonIBD_js{js}.txt')
    cd_uc_clusters = read_clusters(f'../results/result_clusters_raw/Sum_samples/distinct_CD_UC_js{js}.txt')
    nonibd_uc_clusters = read_clusters(f'../results/result_clusters_raw/Sum_samples/distinct_nonIBD_UC_js{js}.txt')
    nonibd_cd_clusters = read_clusters(f'../results/result_clusters_raw/Sum_samples/distinct_nonIBD_CD_js{js}.txt')
    uc_nonibd_count = 0
    uc_cd_count = 0 
    cd_nonibd_count = 0
    cd_uc_count = 0
    nonibd_cd_count = 0
    nonibd_uc_count = 0
    js = 0.8
    for c in input_clusters:
        uc_nonibd_count += count_similar_cluster_in_target(c,uc_nonibd_clusters,js)#/len(uc_nonibd_clusters)
        uc_cd_count += count_similar_cluster_in_target(c,uc_cd_clusters,js)#/len(uc_cd_clusters)
        cd_nonibd_count += count_similar_cluster_in_target(c,cd_nonibd_clusters,js)#/len(cd_nonibd_clusters)
        cd_uc_count += count_similar_cluster_in_target(c,cd_uc_clusters,js)#/len(cd_uc_clusters)
        nonibd_cd_count += count_similar_cluster_in_target(c,nonibd_cd_clusters,js)#/len(nonibd_cd_clusters)
        nonibd_uc_count += count_similar_cluster_in_target(c,nonibd_uc_clusters,js)#/len(nonibd_uc_clusters)

    print('uc_nonibd:',round(uc_nonibd_count,3),'\n'
          'uc_cd:',round(uc_cd_count,3),'\n',
          '----------> uc =',round(uc_cd_count,3)+round(uc_nonibd_count,3),'\n'

          'cd_nonibd:',round(cd_nonibd_count,3),'\n',
          'cd_uc:',round(cd_uc_count,3),'\n',
          '----------> cd =',round(cd_nonibd_count,3)+round(cd_uc_count,3),'\n'

          'nonibd_uc:',round(nonibd_uc_count,3),'\n',
          'nonibd_cd:',round(nonibd_cd_count,3),'\n',
          '----------> nonibd=', round(nonibd_uc_count,3)+round(nonibd_cd_count,3),'\n',
          '-----------------------------------------------'
          )
    
directory = "../results/result_clusters_raw/UC_samples/"
files = sorted(os.listdir(directory))

for f in files: 
    print(f)
    similar_classifier(input_clusters_file=directory+f)
