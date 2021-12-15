import re

worf  = "Период: февраль  2014 года"
pattern = '(\W|^)Период:(\W|$)'

# print(re.match(r'pattern',worf))
print(re.match(r'Период', worf).group())