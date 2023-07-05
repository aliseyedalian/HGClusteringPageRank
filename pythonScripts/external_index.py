#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""External cluster index seen in literature."""
from __future__ import division
import math
import numpy as np

__all__ = (
    'ari',
    'ri',
    'precision',
    'recall',
    'f_measure',
    'folkes_mallows',
    'jaccard',
    'kulczFNski',
    'mc_nemar',
    'phi',
    'rogers_tanimoto',
    'russel_rao',
    'solkal_sneath',
    'solkal_sneath_2',
    'hubert',
    'mirkin',
    'purity',
    'entropy',
    'mi',
    'sg_nmi',
    'fj_nmi',
    'variation_information')


def compute_pairs_count(labels, res):
    """Compute confusion matrix.

    TP the two points belong to the same cluster, according to both P1 and P2
    TN the two points belong to the same cluster according to P1 but not to P2
    FN the two points belong to the same cluster acording to P2 but not to P1
    FP the two points do not belong to the same cluster, according to both P1 and P2
    """
    TP = 0  
    TN = 0
    FN = 0
    FP = 0
    for i in range(len(labels)):
        for j in range(i+1, len(labels)):
            if labels[i] == labels[j] and res[i] == res[j]:
                TP += 1
            if labels[i] != labels[j] and res[i] != res[j]:
                TN += 1
            if labels[i] == labels[j] and res[i] != res[j]:
                FN += 1
            if labels[i] != labels[j] and res[i] == res[j]:
                FP += 1 
    return (TP, TN, FN, FP)


def compute_confusion_matrix(labels,res):
    """Compute confusion matrix M with m_i,j=|C_i inter C'_j|."""
    k = set(labels)
    h = set(res)
    n = len(labels)
    if n != len(res):
        raise ValueError("The two partitions have different size.")
    M = []
    for i in k:
        m_i = []
        C_i = set([index for index, value in enumerate(labels) if value == i])
        for j in h:
            C_j = set([index for index, value in enumerate(res) if value == j])
            m_i.append(len(C_i.intersection(C_j)))
        M.append(m_i)
    
    M = np.array(M).T.tolist()
    return M


def cluster_entropy(labels):
    """Compute the entropy of a clustering."""
    n = len(labels)
    sum = 0
    for i in set(labels):
        C_i = [x for x in labels if x == i]
        p_i = len(C_i)/n
        sum += p_i*math.log(p_i, 2)
    return -1*sum


def ari(labels, res):
    """Compute Hubert and Arabi's Adjusted Rand Index."""
    TP, TN, FN, FP = compute_pairs_count(labels, res)
    return 2*(TP*TN-FN*FP)/((TP+FP)*(FP+TN)+(TP + FN)*(FN + TN))


def ri(labels, res):
    """Compute Rand Index (it is the 'accuracy' on pairs of points, which is invariant to renaming clusters.)."""
    TP, TN, FN, FP = compute_pairs_count(labels, res)
    return (TP+TN)/(TP+TN+FN+FP)


def precision(labels, res):
    """Precision coefficient, portion of points rightly grouped together."""
    TP, TN, FN, FP = compute_pairs_count(labels, res)
    return TP/(TP+FP)


def recall(labels, res):
    """Recall coefficient.

    this is  the proportion of points which are supposed to be grouped together
    according to the reference partition P1 and which are effectively marked
    as such by partition P2.
    """
    TP, TN, FN, FP = compute_pairs_count(labels, res)
    return TP/(TP+FN)


def f_measure(labels, res):
    """F measeure or Czekanowski-Dice index aka Ochiai index."""
    TP, TN, FN, FP = compute_pairs_count(labels, res)
    return (2*TP)/(2*TP+FN+FP)


def folkes_mallows(labels, res):  # noqa:D401
    """Folkes-Mallows index.

    The geometric mean of the Recall and the Precision.
    """
    TP, TN, FN, FP = compute_pairs_count(labels, res)
    return TP/math.sqrt((TP+FN)*(TP+FP))


def jaccard(labels, res):
    """Jaccard index."""
    TP, TN, FN, FP = compute_pairs_count(labels, res)
    return TP/(TP+FN+FP)


def kulczFNski(labels, res):
    """KulczFNski index.

    This is the arithmetic mean of the precision and recall coefficients.
    """
    TP, TN, FN, FP = compute_pairs_count(labels, res)
    return 1/2*(TP/(TP+FP)+TP/(TP+FN))


def mc_nemar(labels, res):
    """Mc Nemar index."""
    TP, TN, FN, FP = compute_pairs_count(labels, res)
    return (TN-FP)/math.sqrt(TN+FP)


def phi(labels, res):
    """Phi index."""
    TP, TN, FN, FP = compute_pairs_count(labels, res)
    return (TP*TN-FN*FP)/((TP+FN)*(TP+FP)*(FN+TN)*(FP+TN))


def rogers_tanimoto(labels, res):
    """Rogers-Tanimoto index."""
    TP, TN, FN, FP = compute_pairs_count(labels, res)
    return (TP+TN)/(TP+TN+2*(FN + FP))


def russel_rao(labels, res):
    """Russel-Rao index."""
    TP, TN, FN, FP = compute_pairs_count(labels, res)
    return TP/(TP+TN+FN+FP)


def solkal_sneath(labels, res):
    """Solkal_Sneath index, first version."""
    TP, TN, FN, FP = compute_pairs_count(labels, res)
    return TP/(TP+2*(FN+FP))


def solkal_sneath_2(labels, res):
    """Solkal_Sneath index, second version."""
    TP, TN, FN, FP = compute_pairs_count(labels, res)
    return (TP + TN)/(TP + TN + (FN + FP)/2)


def hubert(labels, res):
    """Hubert index."""
    TP, TN, FN, FP = compute_pairs_count(labels, res)
    Nt = TP + TN + FN + FP
    return (Nt*TP-((TP+FN)*(TP+FP)))/math.sqrt((TP+FN)*(TP+FP)*(TN+FN)*(TN+FP))


def mirkin(labels, res):
    """Mirkin metric or Equivalence Mismatch Distance."""
    TP, TN, FN, FP = compute_pairs_count(labels, res)
    return 2 * (FP + FN)


def van_dongen_measure(labels, res):
    """Compute Van Dongen Measure."""
    m = compute_confusion_matrix(labels, res)
    n = len(labels)
    k = len(set(labels))
    h = len(set(res))
    sum_k = 0
    sum_l = 0
    for i in m:
        sum_k += max(i)
    for j in range(h):
        max_i = 0
        for i in range(k):
            if m[i][j] > max_i:
                max_i = m[i][j]
        sum_l += max_i
    print(2*n-sum_k-sum_l)


def purity(labels, res):
    """Purity of a clustering."""
    confusion_matrix = compute_confusion_matrix(labels, res)
    n = len(labels)
    sum = 0
    
    for c in confusion_matrix:
        sum += max(c)
    return sum / n


def entropy(labels, res):
    """Entropy of two clustering."""
    confusion_matrix = compute_confusion_matrix(labels, res)
    n = len(labels)
    sum_E = 0
    for c in confusion_matrix:
        n_j = sum(c)
        sum_j = 0
        for j in c:
            p_ij = j / sum(c)
            if p_ij != 0:
                sum_j += p_ij * math.log(p_ij, 2)
        sum_E -= n_j/n * sum_j
    return sum_E


def mi(labels, res):
    """Compute mutual information."""
    k = set(labels)
    h = set(labels)
    n = len(labels)
    if n != len(res):
        raise ValueError("The two partitions have different size.")
    sum_k = 0
    for i in k:
        C_i = set([index for index, value in enumerate(labels) if value == i])
        p_i = len(C_i)/n
        sum_h = 0
        for j in h:
            C_j = set([index for index, value in enumerate(res) if value == j])
            p_j = len(C_j)/n
            p_ij = len(C_i.intersection(C_j))/n
            if p_ij != 0:
                sum_h += p_ij * math.log((p_ij/(p_i*p_j)), 2)
        sum_k += sum_h
    return sum_k


def sg_nmi(labels, res):
    """Strehl and Glosh Normalized Mutual Information."""
    mutualI = mi(labels, res)
    return mutualI / math.sqrt(cluster_entropy(labels) * cluster_entropy(res))


def fj_nmi(labels, res):
    """Fred and Jain Normalized Mutual Information."""
    mutualI = mi(labels, res)
    return 2 * mutualI / (cluster_entropy(labels) + cluster_entropy(res))


def variation_information(labels, res):
    """Meila Variation of Information."""
    return cluster_entropy(labels) + cluster_entropy(res) - 2 * mi(labels, res)



# res = [1,1,1,2,2,2,3,3]
# labels = ['a','a','b','b','c','c','a','a']
 
# print(compute_pairs_count(labels,res))