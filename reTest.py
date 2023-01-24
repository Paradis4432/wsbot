import re 

t = ["1300costo/2900venta/800cada uno", "1400costo/3000Venta/800cada uno"]

for i in t:
    datos = [int(s) for s in re.findall(r'\d+', i)]
    print(datos)
