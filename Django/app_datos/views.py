from django.shortcuts import render
import numpy as np  

class estudiantes:
    def __init__(self, nombre, ramo,seccion):
        self.nombre = nombre
        self.ramo = ramo
        self.seccion = seccion
    def __str__(self):
        return f"{self.nombre} - {self.ramo}"
    
# Genera 20 notas aleatorias entre 1.0 y 7.0 con un decimal

nombres = [
    "Ana", "Luis", "María", "Carlos", "Lucía", "Javier", "Sofía", "Andrés", "Elena", "Miguel",
    "Laura", "Diego", "Valeria", "Fernando", "Camila", "Pablo", "Isabella", "Daniel", "Gabriela", "José"
]

ramos = ["TVD", "BD", "POO", "ML", "AWS"]

secciones = ["A", "B", "C", "D", "E"]

apellidos = [
    "García", "López", "Martínez", "Rodríguez", "Pérez", "Gómez", "Sánchez", "Díaz", "Fernández", "Ruiz",
    "Morales", "Torres", "Ramírez", "Flores", "Vargas", "Castro", "Romero", "Suárez", "Ortega", "Herrera"]

estudiantes_lista = []

for nombre in nombres:
    for apellido in apellidos:
            notasr1 = {"nota1": np.round(np.random.uniform(1.0, 7.0), 1),"nota2": np.round(np.random.uniform(1.0, 7.0), 1),"nota3": np.round(np.random.uniform(1.0, 7.0), 1)}
            notasr2 = {"nota1": np.round(np.random.uniform(1.0, 7.0), 1),"nota2": np.round(np.random.uniform(1.0, 7.0), 1),"nota3": np.round(np.random.uniform(1.0, 7.0), 1)}
            notasr3 = {"nota1": np.round(np.random.uniform(1.0, 7.0), 1),"nota2": np.round(np.random.uniform(1.0, 7.0), 1),"nota3": np.round(np.random.uniform(1.0, 7.0), 1)}
            notasr4 = {"nota1": np.round(np.random.uniform(1.0, 7.0), 1),"nota2": np.round(np.random.uniform(1.0, 7.0), 1),"nota3": np.round(np.random.uniform(1.0, 7.0), 1)}
            notasr5 = {"nota1": np.round(np.random.uniform(1.0, 7.0), 1),"nota2": np.round(np.random.uniform(1.0, 7.0), 1),"nota3": np.round(np.random.uniform(1.0, 7.0), 1)}
            estudiantes_lista.append(estudiantes(f"{nombre} {apellido}",{ramos[0]: notasr1, ramos[1]: notasr2,
            ramos[2]: notasr3, ramos[3]: notasr4,
            ramos[4]: notasr5}, np.random.choice(secciones)))

def base(request):
    return render(request, 'base.html')
def total_alumnos(request):
    total = len(estudiantes_lista)
    return render(request, 'total_alumnos.html', {'total': total })
def totalSeccion(request):
    total_por_seccion = {seccion: 0 for seccion in secciones}
    for i in estudiantes_lista:
        total_por_seccion[i.seccion] += 1


    valores = list(total_por_seccion.values())
    nombres_secciones = list(total_por_seccion.keys())

    return render(request, 'total_secciones.html', {
        'totalSeccion': valores,
        'secciones': nombres_secciones
    })

def totalNotas1(request):
    promedios =np.array([0,0,0,0,0])
    for i in estudiantes_lista:
        for ramo in ramos:
            promedios[ramos.index(ramo)] += i.ramo[ramo]["nota1"]
    promedios = list(promedios / len(estudiantes_lista))
    return render(request, 'notas1.html', {'promedios': promedios, 'ramos': ramos})

def promedioTVD(request):
    promedio=np.array([0,0,0,0,0])
    total_por_seccion = np.array([0,0,0,0,0])
    for i in estudiantes_lista:

        promedio[secciones.index(i.seccion)] += i.ramo["TVD"]["nota1"]
        total_por_seccion[secciones.index(i.seccion)] += 1
    promedio = [round(float(i),2) for i in (promedio / total_por_seccion)]
    print(promedio)
    return render(request, 'promedio_tvd.html', {'promedio': promedio, 'secciones': secciones})