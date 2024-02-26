---
title: "Clustering vectors in higher dimensions"
date: "2024-02-25"
tags: 
  - "ML"
  - "clustering"
  - "embeddings"
  - "high-dimensions"
---

## Objective

Determine whether we can understand which are the concepts in a delimited portion of high-dimensional space.

## Context

We are analyzing a corpus of 600k sentences from the Asian Development Bank public documents.
These documents have been split into sentences and vectorized using the OpenAI word embeddings API.
The resulting vectors, along with the sentence text and the paper uid, have been stored in a table called sentencev.

## Process

We select a random point in the space. We compute the closest points in this vector space to constritute a sub-corpus.
We compute the frequency of words in the sub-corpus. We evaluate the effectiveness of the process.

## Conclusion

It is possible, using L2 distance, to get a list of the closest sentences to a given sentence, even in high dimensions space.
For research purposes, we arbitrally chose a distance of 0.1 as the threshold for similarity.
Experimental analysis of the L2 distance in pgvector shows that the distance between a vector and itself is 0. All other vectors have a distance greater than 0.5.
Visual inspection confirms that the sentences are semantically close, even at the bigger distances (ie. 0.1).
The sentences are scattered across a set of papers, which is expected.
The word frequency over the corpus, once the stopwords have been disposed, shows that the most frequent words across the corpus capture the semantics of the sentences.
The performances of the L2 distance algorithm can be improved.

## Next steps

Cluster all the points in the vector space.
Randomly choose a point in the space, not yet categorized.
Analyze the distribution of points in the clusters. Determine the number of clusters. Determine a threshold below which it is not worth to continue the clusterization.

## References

[L2 distance is meaningless it in higher dimensions spaces](https://stats.stackexchange.com/questions/99171/why-is-euclidean-distance-not-a-good-metric-in-high-dimensions/) (where n > 9)

[How to cluster in higher dimensions](https://towardsdatascience.com/how-to-cluster-in-high-dimensions-4ef693bacc6)

## SQL Instructions


```sql
-- `sentencev` table structure: uid, text, paper_uid, vector
SELECT uid FROM sentencev
ORDER BY RANDOM()
LIMIT 1;

-- analyze the distance of all other vectors from the current one
SELECT 
    other_vectors.uid,
    target_vector.vector <-> other_vectors.vector AS distance
FROM 
    sentencev AS other_vectors,
    (SELECT vector FROM sentencev WHERE uid = 'a4d09d88-6e93-565f-02aa-b2ca230216a1') AS target_vector
ORDER BY 
    distance
LIMIT 100;

-- how many sentences and papers are included in the given subspace?
SELECT count(*), count(distinct(paper_uid))
FROM sentencev
WHERE vector <-> (SELECT vector FROM sentencev where uid = '8af34aad-512c-2d77-d9bd-c5cc25224494') < 0.6;

-- visual inspection: are the sentences semantically close?
WITH 
    vector1 AS (SELECT uid, vector FROM sentencev WHERE uid = '8af34aad-512c-2d77-d9bd-c5cc25224494')
SELECT text, paper_uid, uid, vector <-> (SELECT vector FROM vector1) as distance
FROM sentencev
WHERE vector <-> (SELECT vector FROM vector1) < 0.6
ORDER BY distance;

-- count the most frequent words across the sentences; defect: stopwords
WITH
    texts AS (SELECT uid, text
    FROM sentencev
    WHERE vector <-> (SELECT vector FROM sentencev where uid = '8af34aad-512c-2d77-d9bd-c5cc25224494') < 0.6
)
SELECT 
    word,
    COUNT(*) AS frequency
FROM 
    (SELECT regexp_split_to_table(text, E'\\s+') AS word FROM texts) AS words
GROUP BY 
    word
ORDER BY 
    frequency DESC;

--
CREATE TABLE
    texts_1 AS (SELECT uid, text, paper_uid
    FROM sentencev
    WHERE vector <-> (SELECT vector FROM sentencev where uid = '8af34aad-512c-2d77-d9bd-c5cc25224494') < 0.6)

-- advantage: no more stop words, defect: training is now train
SELECT 
    word,
    COUNT(*) AS frequency
FROM 
    (SELECT unnest(tsvector_to_array(to_tsvector('english', text))) AS word FROM texts_1) AS words
GROUP BY 
    word
ORDER BY 
    frequency DESC;
```

## Sample


```plain text
word,frequency
train,579
employ,444
worker,398
skill,335
educ,308
job,239
inform,221
women,216
work,191
least,175
labor,134
sector,125
survey,122
increas,115
peopl,109
school,107
countri,106
report,105
baselin,105
particip,104
level,101
self,100
formal,98
graduat,96
program,95
industri,95
year,92
higher,91
10,90
base,89
also,84
figur,84
develop,84
employe,83
learn,82
high,82
workforc,82
famili,80
provid,80
self-employ,80
household,79
tvet,79
technic,78
receiv,78
occup,77
20,76
share,74
busi,74
firm,73
```

<br/>

## Involving GitHub Copilot

Represent the first 50 terms on the list with a sentence

### **GitHub Copilot**

Here's a sentence that includes the first 50 terms from your list:

"The train program aims to employ workers and enhance their skills through education and job training. It provides information to women about work opportunities, targeting at least 175 labor sector companies. The survey shows an increase in people attending school across the country. The report and baseline data indicate that participants at all levels, including the self-employed, formal graduates, and those in the industry, have seen improvements over the years. Higher education, especially in the 10-base system, also figures prominently in the development of employees. Learning opportunities for the high workforce, families, and the self-employed are provided in households. TVET (Technical and Vocational Education and Training) has received a significant share of attention, with 78 occupations covered. 20 businesses and firms are actively involved in the program."

<br/>

