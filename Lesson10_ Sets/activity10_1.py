s={'q','w',1,2,3,5}
t={'a','b',1,4,6,7,'q'}

#union
result = s.union(t)
#print(result)

#intersection
result = s.intersection(t)
#print(result)

#difference
result =s.difference(t)
#print('s diff t' ,result)
result =t.difference(s)
#print('t diff s' ,result)

#symmetric difference
result =s.symmetric_difference(t)
print(result)