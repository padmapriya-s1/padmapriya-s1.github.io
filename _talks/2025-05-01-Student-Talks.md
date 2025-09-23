---
title: "Student Talks"
collection: talks
type: "Talk"
permalink: /talks/2025-05-01-Student-Talks
venue: "Online"
date: 2025-05-01
location: ""
---

One of the canonical worst-case NP-Hard problems is to find the maximum independent set (MIS) in a graph. One way to cope with NP-Hardness is to devise approximation algorithms where the goal is to guarantee a solution within a small fraction of the optimal one. But MIS is notoriously hard in the sense that it does not have even a good approximation algorithm. In fact, it is not possible to do so, as it is known that for any constant $$\epsilon > 0$$ it is NP-Hard (unless NP = ZPP) to approximate MIS to within $$n^{1-\epsilon}$$[3] (This means the $$\frac{\text{OPT(MIS)}}{\text{MIS given by algo}}$$ is as large as $$n^{1-\epsilon}$$).

Coloring and the independent set problem go hand in hand. One can think of coloring as "packing" a graph with as few independent sets as possible. No surprise, coloring is as hard as well. Similar to MIS, it is known that one cannot approximate the minimum number of colors needed to color the graph to within $$n^{1-\epsilon}$$ for any constant $$\epsilon > 0$$[1]. In fact, even if you are given that the graph is 3-colorable, the best known coloring algorithm requires $$O(n^{0.19747})$$ colors[4]. To make things worse, it is known to be NP-hard to color a 3-colorable graph using even 4 colors![2]

In this talk, we will see a powerful technique called semidefinite programming that gives a polynomial-time approximation algorithm to a 3-colorable graph with $$\tilde{O}(n^{1/4})$$ colors.

### References

[1] Uriel Feige and Joe Kilian. Zero knowledge and the chromatic number. J.Comput. Syst. Sci., 57(2):187–199, October 1998.
[2] Venkatesan Guruswami and Sanjeev Khanna. On the hardness of 4-coloring a 3-colorable graph. SIAM Journal on Discrete Mathematics, 18(1):30–40, 2004.
[3] Johan H˚astad. Clique is hard to approximate within n 1- ε. 1999.
[4] Ken-ichi Kawarabayashi, Mikkel Thorup, and Hirotaka Yoneda. Better coloring of 3-colorable graphs. In Proceedings of the 56th Annual ACM Symposium on Theory of Computing, pages 331–339, 2024.
