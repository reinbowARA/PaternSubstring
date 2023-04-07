from SubString import Substring

txt = "ABAAABCD"
pat = "ABC"
Substring.searchBM(txt, pat)
Substring.searchRK(pat, txt, 101)
Substring.KMPSearch(pat,txt)
Substring.searchEA(pat,txt)