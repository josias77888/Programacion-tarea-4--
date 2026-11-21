# Programacion-tarea-4--
Programación - Tarea 4 (UNAD)

Curso: Programación (213023) | Universidad: UNAD | Grupo: 213023_17

¿Qué se pedía?

La actividad pedía crear, en equipo de cinco estudiantes, un programa en Python para una empresa 
ficticia llamada Software FJ. La empresa ofrece tres tipos de servicios: reserva de salas, 
alquiler de equipos y asesorías.

El programa debía:

Gestionar clientes, servicios y reservas sin usar base de datos (solo objetos y listas).
Aplicar la programación orientada a objetos: clases abstractas, herencia, polimorfismo y encapsulación.
Manejar errores con excepciones, para que el programa nunca se caiga.
Guardar todos los eventos y errores en un archivo de logs.
Simular mínimo 10 operaciones (algunas correctas y otras con errores a propósito).
¿Qué hace el programa?

Al ejecutarlo, simula 22 operaciones de la empresa y muestra el resultado de cada una en pantalla:

Clientes: registra clientes válidos y rechaza los que tienen datos incorrectos
(correo mal escrito, nombre que no es texto, teléfono con letras, nombre vacío o cliente repetido).
Servicios: crea salas, equipos y asesorías, y rechaza los que tienen datos incorrectos 
(tarifa negativa, datos faltantes).
Reservas: crea, confirma, cancela y procesa reservas (calcula el costo con impuesto y descuento). 
También maneja los casos que fallan: duración inválida, cliente no registrado, reserva que no existe, 
confirmar una reserva cancelada, servicio no disponible y cálculos inconsistentes.
Resumen: muestra al final cuántos clientes, servicios y reservas quedaron registrados.

Cuando algo sale mal, el programa muestra el error, lo guarda en el log y continúa con la siguiente operación. 
Nunca se detiene.

¿Cómo se ejecuta?

Se necesita tener Python 3. Desde la carpeta del proyecto:
```bash
python3 main.py
```
Todo lo que ocurre queda registrado en el archivo `logs/sistema.log`.

## Archivos del proyecto

| Archivo | Qué contiene |
|---|---|
| `main.py` | Programa principal: simula las 22 operaciones |
| `entidad.py` | Clase abstracta base del sistema |
| `cliente.py` | Clase Cliente, con sus validaciones |
| `excepciones.py` | Errores personalizados del sistema |
| `servicio.py` | Clase abstracta Servicio y los tres servicios: sala, equipo y asesoría |
| `reserva.py` | Clase Reserva y sus estados (pendiente, confirmada, cancelada, procesada y fallida) |
| `gestor_general.py` | Administra las listas de clientes, servicios y reservas |
| `sistema_logs.py` | Crea y escribe el archivo de logs |
| `logs/sistema.log` | Registro de eventos y errores |

## Temas aplicados

- **Clases abstractas y herencia:** `Entidad` y `Servicio`, de las que heredan `Cliente`, `ReservaSala`, `AlquilerEquipo` y `Asesoria`.
- **Polimorfismo:** cada servicio calcula su costo y se describe a su manera.
- **Encapsulación:** los datos van privados y se validan antes de guardarse.
- **Métodos sobrecargados:** el costo se puede calcular solo, con impuesto, con descuento o con ambos.
- **Manejo de excepciones:** errores personalizados, `try/except`, `try/except/else`, `try/except/finally` y encadenamiento de excepciones.

Integrantes:

1 Josías Madera Martínez - escogi parte 1 - excepciones.py - 
entidad.py - cliente.py - main.py

2 Juan Diego Seña Madera - escogí parte 4 - sistema_logs.py - gestor_general.py
 
3 Ronald de Hoyos Hoyos - escogí parte 3-
Clase_Reserva 

4 Salome Infante Quiñonez - escogi parte 2 - servicio.py - PDF

Parte que le toca a cada integrante
    1.  Excepciones, clase abstracta base y Cliente
	2.	Clase abstracta Servicio y servicios (salas, equipos, asesorías)
	3.	Clase Reserva
	4.	Sistema de logs y gestor general
	5.	main.py con las 10+ operaciones, README y PDF

