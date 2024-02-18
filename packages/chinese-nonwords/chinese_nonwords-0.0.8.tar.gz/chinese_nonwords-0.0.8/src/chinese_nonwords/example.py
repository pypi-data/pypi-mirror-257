from chinese_nonwords import ChineseNonwords

cnw = ChineseNonwords(2, 15, 100, 200, 2, 6, N=10, random_state=42)
my_cnw = cnw.generate()

print(my_cnw)
