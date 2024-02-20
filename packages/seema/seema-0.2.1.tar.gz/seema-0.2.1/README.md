# Seema
Khmer, Lao, Myanmar, and Thai word segmentation/breaking library in Python written in Rust

# Example

```
>>> from seema import Seema
>>> Seema("words_th.txt", "thai_cluster_rules.txt")
>>> s.segment_into_strings("ไก่จิกเด็ก")
['ไก่', 'จิก', 'เด็ก']
```

words_th.txt and thai_cluster_rules.txt can be downloaded from https://codeberg.org/mekong-lang/chamkho/src/branch/main/data.
