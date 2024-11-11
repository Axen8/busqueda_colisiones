import pandas as pd
import matplotlib.pyplot as plt

resumen = []
bits = []
contr = []

with open("estadistica.txt", "r") as f:
    for n,line in enumerate(f):
        print(line,n)
        line = line[1:-2]
        if n == 0:
            for word in line.split( ','):
                resumen.append(word)
        elif n == 1:
            for word in line.split( ','):
                bits.append(int(word))
        elif n == 2:
            for word in line.split( ','):
                contr.append(int(word))
            
f.close()

data = {
    'Función de resumen': resumen,
    'Bits': bits,
    'Contraseñas encontradas': contr
}

df = pd.DataFrame(data)

plt.figure(figsize=(10, 6))

for resumen in df['Función de resumen'].unique():
    subset = df[df['Función de resumen'] == resumen]
    plt.plot(subset['Bits'], subset['Contraseñas encontradas'], marker='o', label=resumen)

plt.xlabel('Bits')
plt.ylabel('Colisiones encontradas')
plt.title('Colisiones encontradas por función de resumen y cantidad de bits')
plt.legend(title='Función de resumen')
plt.grid(True)

plt.show()
