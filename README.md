# Objetivo

El objetivo de este proyecto es aprender a modelar un problema en CNF, y a usar un SAT solver para resolverlo, así como traducir la salida del SAT solver a un formato legible.
No solo se evaluará que la implementación funcione, sino la eficiencia de su traducción a CNF del problema.

# Problema a resolver

Imagine que se está organizando un torneo, y se le pide realizar un programa que encuentre una asignación de fecha y hora en la que los juegos van a ocurrir. Las reglas son las siguientes:

1. Todos los participantes deben jugar dos veces con cada uno de los otros participantes, una como "visitantes" y la otra como "locales". Esto significa que, si hay 10 equipos, cada equipo jugará 18 veces.
1. Dos juegos no pueden ocurrir al mismo tiempo.
1. Un participante puede jugar a lo sumo una vez por día.
1. Un participante no puede jugar de "visitante" en dos días consecutivos, ni de "local" dos días seguidos.
1. Todos los juegos deben empezar en horas "en punto" (por ejemplo, las 13:00:00 es una hora válida pero las 13:30:00 no).
1. Todos los juegos deben ocurrir entre una fecha inicial y una fecha final especificadas. Pueden ocurrir juegos en dichas fechas.
1. Todos los juegos deben ocurrir entre un rango de horas especificado, el cuál será fijo para todos los días del torneo.
1. A efectos prácticos, todos los juegos tienen una duración de dos horas.

# Formato de entrada

Su sistema debe recibir un JSON con el siguiente formato (asuma que siempre recibirá el formato correcto):

```
{
  "tournament_name": String. Nombre del torneo,
  "start_date": String. Fecha de inicio del torneo en formato ISO 8601,
  "end_date": String. Fecha de fin del torneo en formato ISO 8601,
  "start_time": String. Hora a partir de la cuál pueden ocurrir los juegos en cada día, en formato ISO 8601,
  "end_time": String. Hora hasta la cuál pueden ocurrir los juegos en cada día, en formato ISO 8601,
  "participants": [String]. Lista con los nombres de los participantes en el torneo
}
```

Asuma que todas las horas vienen sin zona horaria especificada, y asuma por lo tanto que su zona horaria es UTC.

# Actividad 1

Deben crear una traducción del problema a formato CNF, y luego deben crear un programa, en el lenguaje de programación que sea de su agrado, que traduzca cualquier JSON en el formato propuesto a la representación del problema en formato [DIMACS CNF](https://people.sc.fsu.edu/~jburkardt/data/cnf/cnf.html)

# Actividad 2

Usando la transformación creada en la parte anterior, los archvios en formato DIMACS CNF pueden ser usados como entrada para el SAT solver [Glucose](https://www.labri.fr/perso/lsimon/glucose/). Debe crear un programa, en el lenguaje de programación que sea de su agrado, que traduzca la salida de Glucose al resolver el problema en un archivo con el mismo nombre del torneo y extensión `.ics`, en formato de [iCalendar](https://en.wikipedia.org/wiki/ICalendar) de manera que sea posible agregar la asignación de los juegos a un gestor de calendarios. Para ello puede usar cualquier librería que considere necesaria. Los eventos del calendario deben tener ocurrir a la hora que fue asignada cumpliendo todas las reglas dadas, y deben indicar quiénes son los participantes en el juego, quién es el "local" y quién es el "visitante".

# Actividad 3

Debe crear un cliente que maneje todo el proceso. Es decir, reciba un JSON en el formato de entrada, ejecute el programa que lo transforma en CNF, introduzca el resultado  en Glucose, y se asegure de que se cree el archivo .ics con la respuesta, o falle en caso de ser UNSAT. Debe generar casos de prueba fáciles y difíciles, y medir el rendimiento de su solución.

# Entrega

Deben tener un repositorio con todo el código usado y un informe que describa su solución, sus resultados experimentales, así como instrucciones específicas para ejecutar todo el proceso.

# Como correr el programa
En primer lugar se debe instalar las dependencias (libreria ics)

```bash
pip3 install -r requirements.txt
```

Luego
```bash
python3 manager.py <testcase.json>
```

Durante la ejecucion se muestra por terminal la ejecucion del SAT solver GLUCOSE.

En caso de que se encuentre solucion, se genera un archivo <tournament_name>.ics con el calendario del torneo.

# Programas
* manager.py: orquestador recibe como unico argumento el nombre del archivo que contiene una representacion correcta de un torneo en json, y corre los subprogramas para generar en caso de ser posible un archivo <tournament_name>.ics con el calendario del torneo.
* jsonToCNF.py: recibe como unico argumento el nombre del archivo que contiene una representacion correcta de un torneo en json, e imprime su representacion en formato cnf.
* cnfToICS.py: recibe como unico argumento el nombre del archivo que contiene una representacion correcta de un torneo en json, y lee el archivo `glucoseResult.txt`. Si el glucose encontro una solucion crea un archivo <tournament_name>.ics.

# Representacion CNF
Cada variable contiene: dia, hora, equipo local y visitante, representando un posible partido del torneo. Esta se calcula con la funcion `calcVar` en el archivo `jsonToCNF.py`, para hacer el proceso inverso existe la funcion `varCalc` en el archivo `cnfToICS.py`.

Para cumplir con las reglas especificadas:

1. Dados dos equipos `a`, `b` siendo `a` local y `b` visitante, existen dos tipos de clausura: una para asegurar que haya al menos un juego entre ellos y otra para asegurar que haya a lo sumo uno. Linea 80 archivo `jsonToCNF.py`.

1. Dado un dia `a` y una hora `b`: a lo sumo uno de todos los partidos posibles en ese dia y hora es posible. Linea 27 archivo `jsonToCNF.py`.

1. Dado un equipo `a` y un dia `b`: a lo sumo uno de todos los partidos posibles en el dia `b` donde `a` es visitante o local es posible. Linea  64 archivo `jsonToCNF.py`.

1. Dado un equipo `a`: se verifica que si un partido ocurre en el dia `c` con `a` como visitante, no ocurra un partido en el dia `c`+1 con `a` como visitante, y se realiza un procedimiento analogo con `a` como local. Linea 41 archivo `jsonToCNF.py`.

1. Al principio se ajusta el start_time y el end_time para comenzar en la primera y ultima hora en punto en el rango dado.

1. Se calculo el numero de dias tomando la diferencia entre el start_date y end_date.

1. Se calcula el numero de horas disponible con la diferencia de start_time y el end_time (ajustadas previamente). 

1. Una vez calculado el horario disponible, se divide el numero de horas entre dos, obteniendo el numero maximo de partidos por dia.

# Resultados obtenidos

| Caso | # Variables | # Clausulas | CPU Time (s) | Result |
|:---:|:---:|:---:|:---:|:---:|
| easy | 8100 | 1364130 | 8.4 | U |
| easy2 | 132 | 1878 | 6.8 | U |
| medium | 66430 | 19692309 | 12.6 | S |
| medium2 | 78260 | 29525860 | 20.54 | S |
| medium3 | 89544 | 45194786 | 32.4735 | S |
| medium4 | 76076 | 60941062 | 42.66 | S |
| hard | 240 | 4940 | 205.377 | U |
| hard2 | 260 | 5490 | 1594.53 | I |

I = INDETERMINATE
S = SATISFIABLE
U = UNSATISFIABLE