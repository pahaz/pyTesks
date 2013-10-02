# -*- encoding: utf-8 -*-

from collections import Counter
import re

# Статистическая информация "Информация о результатах борьбы с организованной преступностью"
data = open('od9.csv').read()
c = Counter([e[0] for e in re.findall(r'\d+$', data, re.MULTILINE) if len(e) > 0 and e[0] != '0'])
length = sum(c.values())

for i in range(1, 10):
    print('%s: %0.2f' % (i, c[str(i)] * 100.0 / length))

