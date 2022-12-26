s = "Martina iturbe Luna biocca Camila dongiovanni Julieta dominici Jeronimo ballestrin"

ss = s.split()
print(ss)
sss = [" ".join(ss[i:i+2]) for i in range(0, len(ss), 2)]
s1 = []
for i in range(0,len(ss), 2):
    s1.append(ss[i] + " " + ss[i+1])
    
print(s1)
