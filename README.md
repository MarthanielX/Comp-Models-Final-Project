# Comp-Models-Final-Project

This is Nathaniel Sauerberg and Luna Yee's final project for Professor Anna Rafferty's CS328: Computational Models of Cognition.

## Warnings (HIGH PRIORITY)

Be aware that these models are designed to run on large data, and that the primary data file included in the `/data` directory includes
over 70000 data points. As a result, running the modules on this or other large sets of data will result in **high CPU, RAM, and disk
usage**. For more details on the individual modules:

`matrix_loader`:
- All matrix-creation methods save the matrices created in pickled form in the `/lib` directory. For both full-matrix-creation
methods, the size of these files will exceed 1 GB.

`accessibility_ranker`:
- Both models will have large runtime, and be intensive on RAM and CPU with large input matrices.
- HITS will be particularly intensive on both RAM and CPU, with high runtime. This is because query-independent HITS requires two
instances of matrix multiplication of the square matrix provided. Since matrix multiplication is O(n^3), and this will require 4
separate representations of n-by-n matrices, with two using float as the dtype, RAM will be very active while the model is running.

Due to these inherent faults in model scope, the following are provided in the `/lib` directory:
- `normedItems`: A 1-dimesional ndarray of strings of normed cues. The order of this indexing will be used for matrices and rankings.
- `unnormedItems`: A 1-dimesional ndarray of strings of unnormed targets. The order of this indexing will be used for matrices and 
rankings, after that of `normedItems`.
- `pageRankRankings`: A 1-dimensional ndarray of PageRank rankings produced by the `accessibility_ranker` `pageRank` method on the full
unweighted matrix formed by the provided association data. Rankings appear by the indexed order of `normedItems` + `unnormedItems`.
- `hitsAuthRankings`: As above, but of HITS authority rankings produced by the `accessibility_ranker` `hypertextInducedTopicSearch` method.
- `hitsHubRankings`: As above, but of HITS hub rankings produced by the `accessibility_ranker` `hypertextInducedTopicSearch` method.

## Contents



## Description
