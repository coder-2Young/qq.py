eq = ['0o12', '+', '0o23']
count = 0
if eq[0] != '-':
    sum = int(eq[0], 8)
else:
    sum = 0.0
for i in eq:
    if i == '-':
        sum = sum - int(eq[count + 1], 8)
    elif i == '+':
        sum = sum + int(eq[count + 1], 8)
    count = count + 1
if sum >= 0:
    eq = [str(oct(sum))]
else:
    eq = ['-', str(oct(-sum))]
print(eq)
