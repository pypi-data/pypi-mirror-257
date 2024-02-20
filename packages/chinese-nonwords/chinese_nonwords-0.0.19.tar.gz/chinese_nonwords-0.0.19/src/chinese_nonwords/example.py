from chinese_nonwords import ChineseNonwords

cnw = ChineseNonwords(2, 18, 100, 300, 3, 6, N=10, random_state=42)
my_cnw = cnw.generate_words()

print(my_cnw)
