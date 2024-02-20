# Package description

This package is developed based on [`strokes`](https://pypi.org/project/strokes/) and [`pinyin`](https://pypi.org/project/pinyin/). Use this package to generate Chinese disyllabic nonwords. 


### Installation
```python
from chinese_nonwords import ChineseNonwords
```

The `ChineseNonwords` function takes in the following arguments, in the following order:
- stroke_min, stroke_max (min: 1; max: 25):
    - the minimum and maximum number of stroke a character has 
- num_nei_min, num_nei_max (min: 8; max: 307): 
    - the minimum and maximum number of phonological neighborhood a character has 
- logfreq_min, logfreq_max (min: 0; max: 6.31): 
    - the minimum and maximum number of frequency (log) of a character 
- N: 
    - the number of disyllabic words to be generated (default=10)
- random_state: 
    - random state for sampling (default=42)

### Usage
#### Generate disyllabic nonwords
```python
from chinese_nonwords import ChineseNonwords
cnw = ChineseNonwords.generate_nonwords(stroke_min=2, 
                                        stroke_max=18, 
                                        num_nei_min=20, 
                                        num_nei_max=300, 
                                        logfreq_min=4, 
                                        logfreq_max=6, 
                                        N=10, 
                                        random_state=42)
```
Once specified, the run the `generate_nonwords()` function to get a tabulated list of nonwords. The pinyin of these nonwords were cross-checked with the [SUBTLEX-CH][1] to make sure it does not appear in the given list of known disyllabic words. The frequency information is extracted from [SUBTLEX-CH][1], stroke count from the [`strokes`](https://pypi.org/project/strokes/) package, and the rest of the lexical properties from [`Mandarin-Neighborhood-Statistics`](https://github.com/karlneergaard/Mandarin-Neighborhood-Statistics).

Note that the length of the output is not always the same as specified (N), as there are nonwords that are phonologically similar to real disyllabic words, which are excluded. To generate another list with the same arguments, change `random_state` to a different value. 

```
print(cnw)
+----+----------+----------+-------------+-------------+------------+------------+--------+--------+-----------------+-----------------+
|    | Char-1   | Char-2   |   Logfreq-1 |   Logfreq-2 |   Stroke-1 |   Stroke-2 |   HD-1 |   HD-2 |   NumNeighbor-1 |   NumNeighbor-2 |
+====+==========+==========+=============+=============+============+============+========+========+=================+=================+
|  0 | 求       | 查       |        4.36 |        4.49 |          7 |          9 |      9 |      6 |             219 |             219 |
+----+----------+----------+-------------+-------------+------------+------------+--------+--------+-----------------+-----------------+
|  1 | 名       | 空       |        4.64 |        4.19 |          6 |          8 |      7 |      1 |             219 |             277 |
+----+----------+----------+-------------+-------------+------------+------------+--------+--------+-----------------+-----------------+
|  2 | 妈       | 何       |        4.9  |        4.58 |          6 |          7 |      3 |     12 |             278 |             219 |
+----+----------+----------+-------------+-------------+------------+------------+--------+--------+-----------------+-----------------+
|  3 | 法       | 比       |        4.78 |        4.71 |          8 |          4 |      2 |      5 |             261 |             262 |
+----+----------+----------+-------------+-------------+------------+------------+--------+--------+-----------------+-----------------+
|  4 | 乐       | 到       |        4.42 |        5.46 |          5 |          8 |      9 |      8 |             304 |             305 |
+----+----------+----------+-------------+-------------+------------+------------+--------+--------+-----------------+-----------------+
|  5 | 表       | 但       |        4.5  |        5.09 |          8 |          7 |      4 |     10 |             260 |             305 |
+----+----------+----------+-------------+-------------+------------+------------+--------+--------+-----------------+-----------------+
```

#### Generate disyllabic words
Similarly, you can use the `generate_words()` function to generate a list of disyllabic words that meet the specification. 
```python
from chinese_nonwords import ChineseNonwords
cw = ChineseNonwords.generate_words(stroke_min=2, 
                                    stroke_max=18, 
                                    num_nei_min=100, 
                                    num_nei_max=300, 
                                    logfreq_min=3, 
                                    logfreq_max=6, 
                                    N=10, 
                                    random_state=42)
```

The output is in the same format as the nonword list. 

```
print(cw)
+----+--------+-----------+---------------------+----------+----------------+
|    | word   |   logfreq |   homophone_density |   stroke |   num_neighbor |
+====+========+===========+=====================+==========+================+
|  0 | 思考   |      3.08 |                 8   |      7.5 |          268.5 |
+----+--------+-----------+---------------------+----------+----------------+
|  1 | 家里   |      3.66 |                11   |      8.5 |          270   |
+----+--------+-----------+---------------------+----------+----------------+
|  2 | 迷人   |      3.03 |                 6.5 |      5.5 |          219.5 |
+----+--------+-----------+---------------------+----------+----------------+
|  3 | 交给   |      3.25 |                 7.5 |      7.5 |          268   |
+----+--------+-----------+---------------------+----------+----------------+
|  4 | 工具   |      3.02 |                13.5 |      5.5 |          291.5 |
+----+--------+-----------+---------------------+----------+----------------+
|  5 | 多久   |      3.64 |                 5   |      4.5 |          240   |
+----+--------+-----------+---------------------+----------+----------------+
|  6 | 理解   |      3.71 |                 6.5 |     12   |          262   |
+----+--------+-----------+---------------------+----------+----------------+
|  7 | 情绪   |      3.16 |                 7   |     11   |          262.5 |
+----+--------+-----------+---------------------+----------+----------------+
|  8 | 天气   |      3.1  |                 7.5 |      4   |          291.5 |
+----+--------+-----------+---------------------+----------+----------------+
|  9 | 酒吧   |      3.47 |                 3.5 |      8.5 |          136.5 |
+----+--------+-----------+---------------------+----------+----------------+
```

##### References
[1] [SUBTLEX-CH](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0010729&ref=https://githubhelp.com): Cai, Q., & Brysbaert, M. (2010). SUBTLEX-CH: Chinese word and character frequencies based on film subtitles. PloS one, 5(6), e10729.