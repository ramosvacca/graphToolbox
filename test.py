testlist = ['a', 'b']

print(type(testlist))

if type(testlist) == list:
  if len(testlist) == 3:
    print('OH')
  else:
    raise TypeError("Length should be 3")
