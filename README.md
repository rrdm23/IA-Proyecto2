# IA-Proyecto2

Instituto Tecnológico de Costa Rica

Escuela de Ingeniería en Computación

IC-6200 Inteligencia Artificial

Proyecto #2 – Connect 4 Genético

Informe técnico

Profesor:
Juan Esquivel Rodríguez, Ph. D. 

Estudiante:
Randall Delgado Miranda

Grupo #2

II Semestre 2018

<h3>Algoritmo de detección de gane y bloqueo</h3>

Los agentes son capaces de determinar si una partida puede potencialmente terminar, ya sea a favor o en contra de ellos. Es decir, a la hora de ejecutar su turno, pueden analizar si hay una posible jugada que les permita ganar actualmente, o por el contrario, identifican que el otro jugador o agente puede ganar en el siguiente turno.
	Para esto, se diseñó un algoritmo que revisa únicamente los espacios jugables, es decir, los siete espacios que haya en las columnas para el tablero actual. Ambos algoritmos (ejecución de movida final y bloqueo de oponente) siguen la misma lógica, lo que cambiará es quién tiene la posibilidad de ganar (al final, se decidirá por poner la ficha en el espacio si se detecta cualquiera de las situaciones).

Aquí se presenta un pseudocódigo del algoritmo diseñado (en español):

    funcion REVISAR-SITUACION-GANE (tablero, columna-revisada, jugador-a-ganar) 
        retorna un resultado de revisión (y lo ejecuta si es el caso)
        entradas: tablero, el tablero actual de juego
                  columna-revisada, la columna donde se desea jugar
                  jugador-a-ganar, un número que determina cuál color de ficha revisar
    
        fila-actual ← tablero.OBTENER-ESPACIO-COLUMNA(columna-revisada)
        tablero-temporal ← CREAR-COPIA(tablero)
        temp-num-agente ← Agente.num-jugador
        Agente.num-jugador ← jugador-a-ganar
        Agente.JUGAR(tablero-temporal, columna-revisada)
    
        fichas-horizontales ← REVISION-HORIZONTAL(tablero-temporal, fila-actual, jugador-a-ganar)
        hay-linea-horizontal ← LARGO(fichas-horizontales) == 4 
            && (columna-revisada - 1) está en fichas-horizontales
            && tablero.ES-POSIBLE-JUGAR(fila-actual, columna-revisada - 1)

        hay-linea-vertical = REVISION-VERTICAL(tablero-temporal, columna-revisada - 1, jugador-a-ganar)

        fichas-diagonales ← REVISION-DIAGONAL(tablero-temporal, fila-actual, columna-revisada - 1, jugador-a-ganar)
        hay-linea-diagonal ← LARGO(fichas-diagonales) == 4 \
            && (columna-revisada - 1) está en fichas-diagonales \
            && tablero.ES-POSIBLE-JUGAR(fila-actual, columna-revisada - 1)

        fichas-anti_diagonales ← REVISION-ANTI-DIAGONAL(tablero-temporal, fila-actual, columna-revisada – 1, jugador-a-ganar)
        hay_linea_anti_diagonal ← LARGO(fichas-anti-diagonales) == 4 \
            && (columna-revisada - 1) está en fichas-anti-diagonales \
            && tablero.ES-POSIBLE-JUGAR(fila-actual, columna-revisada - 1)

        Agente.num-jugador ← temp-num-agente
        si hay_linea_horizontal || hay_linea_vertical || hay_linea_diagonal || hay_linea_anti_diagonal entonces
            Agente.JUGAR(tablero, columna-revisada)
            retornar VERDADERO
        retornar FALSO

Este algoritmo luego se aplica por columna, únicamente en los “topes” de cada columna, es decir, sólo se realiza el chequeo en los 7 espacios donde se puede poner la ficha. Además, mediante el parámetro jugador-a-ganar, puede revisar tanto sus propias jugadas de victoria (las cuales tienen prioridad), como las necesarias para bloquear el gane.

<h3>Diseño de movimiento genérico</h3>

Incluso si ya cada agente está muy seguro de qué hacer cuando hay una jugada crucial en el tablero, es importante también saber qué es lo mejor en casos donde las jugadas son “neutras”, o mejor dicho, donde una jugada inmediata no acabará la partida. A esto se le llamará el algoritmo general del juego.

Para este caso, se planteó que lo mejor es tomar entre una decisión u otra de manera libre (siguiendo las “sugerencias” de columnas por cada movimiento genérico), bajo 4 criterios probabilísticos de ejecución diferentes, como se verá en las características a continuación:

<h4>Característica 1: Centro o extremos?</h4>

En este caso, se tiene como base que el agente toma una decisión aleatoria, en la cual determina si juega en los extremos o en el centro. El pseudocódigo correspondiente es el siguiente:

    funcion MOVIMIENTO-GENERICO-1 () 
        retorna una lista con un rango de columnas

        movimiento-a-decidir ← FLOTANTE-ALEATORIO(0, 1)
        rango-columnas ← []
        si movimiento-a-decidir <= Agente.prob-movimiento-1 entonces
            rango-columnas ← [2, 3, 4]
        de lo contrario
            rango-columnas ← [2, 3, 4]
        retornar rango-columnas

<h4>Característica 2: Espacios o consecutivos?</h4>

El siguiente tipo de movimiento genérico consiste en, dado que existe una ficha propia puesta, se podrá tomar el camino de poner una ficha a la par, con el fin de seguir una secuencia, o por el contrario, se buscará ubicar una ficha de la manera más alejada posible, con el fin de “confundir” al otro agente. El pseudocódigo de este movimiento es el siguiente:

    funcion MOVIMIENTO-GENERICO-2 (tablero) 
        retorna una lista con un rango de columnas
        entrada: tablero, el tablero actual del juego
    
        movimiento-a-decidir ← FLOTANTE-ALEATORIO(0, 1)
        rango-columnas ← []
        para columna en RANGO(0, 7)
            fila ← tablero.OBTENER-ESPACIO-COLUMNA(columna)
            si fila != 5 entonces
                fila ← fila + 1
            ficha-a-revisar = tablero.OBTENER-POSICION(fila, columna)
            si movimiento-a-decidir <= Agente.prob-movimiento-2 entonces
                si ficha-a-revisar == Agente.num-jugador entonces
                    rango-columnas.AÑADIR(columna)
                    si columna != 6 
                            && tablero.ES-POSIBLE-JUGAR(fila, columna + 1) entonces
                        rango-columnas.AÑADIR(columna + 1)
                    si columna != 0
                            && tablero.ES-POSIBLE-JUGAR(fila, columna - 1) entonces
                        rango-columnas.AÑADIR(columna - 1)
            de lo contrario
                si ficha-a-revisar == Agente.num-jugador entonces
                    si !(columna está en [5, 6]) 
                            && tablero.ES-POSIBLE-JUGAR(fila, columna + 1)
                            && tablero.ES-POSIBLE-JUGAR(fila, columna + 2) entonces
                        rango-columnas.AÑADIR(columna + 2)
                        si columna != 4 && tablero.ES-POSIBLE-JUGAR(fila, columna + 3) entonces
                            si (columna <= 2 && tablero.OBTENER-POSICION(fila, columna + 4) != Agente.num-jugador) 
                                    || columna == 3 entonces
                                rango-columnas.AÑADIR(columna + 3)
                    si !(columna está en [0, 1]) 
                            && tablero.ES-POSIBLE-JUGAR(fila, columna - 1)
                            && tablero.ES-POSIBLE-JUGAR(fila, columna - 2) entonces
                        rango-columnas.AÑADIR(columna - 2)
                        si columna != 2
                                && tablero.ES-POSIBLE-JUGAR(fila, columna - 3) entonces
                            si (columna >= 4
                                    && tablero.OBTENER-POSICION(fila, columna - 4) != Agente.num-jugador) 
                                    || columna == 3 entonces
                                rango-columnas.AÑADIR(columna – 3)
        retornar rango-columnas

<h4>Característica 3: Columnas más llenas o más vacías (tope o fondo)?</h4>

Este tipo de estrategia consiste en identificar cuáles columnas poseen más fichas. Se decidirá si se opta por llenar las columnas más altas, o primero buscar los “huecos” o espacios más bajos en el tablero. El pseudocódigo de esta sección se adjunta a continuación:

    funcion MOVIMIENTO-GENERICO-3 (tablero) 
        retorna una lista con un rango de columnas
        entrada: tablero, el tablero actual del juego

        movimiento-a-decidir ← FLOTANTE-ALEATORIO(0, 1)
        rango-columnas ← []
        si movimiento-a-decidir <= Agente.prob-movimiento-3 entonces
            espacios-altos ← tablero.OBTENER-ESPACIOS-ALTOS()
            rango-columnas.AÑADIR(espacios-altos)
        de lo contrario
            rango-columnas.AÑADIR(espacios-bajos)
        retornar rango-columnas

<h4>Característica 4: Cubrir al oponente encima o jugar al lado de él?</h4>

En este último movimiento general, el agente tomará en cuenta las fichas de su oponente. Puede tomar el camino de colocar fichas sobre las de él, o por el contrario colocarlas a uno de los lados. El pseudocódigo de esta parte es el siguiente:

    funcion MOVIMIENTO-GENERICO-4 (tablero) 
        retorna una lista con un rango de columnas
        entrada: tablero, el tablero actual del juego

        movimiento-a-decidir ← FLOTANTE-ALEATORIO(0, 1)
        rango-columnas ← []
        para columna en RANGO(0, 7)
            fila ← tablero.OBTENER-ESPACIO-COLUMNA(columna)
            si fila == 5 entonces
                continuar
            ficha-a-revisar ← tablero.OBTENER-POSICION(fila + 1, columna)
            si ficha-a-revisar != Agente.num-jugador entonces
                si movimiento-a-decidir <= Agente.prob-movimiento-4 entonces
                    rango-columnas.AÑADIR(columna)
                de lo contrario
                    si columna != 0 && tablero.ES-POSIBLE-JUGAR(fila + 1, columna – 1) entonces
                        si !(columna – 1 está en rango-columnas):
                            rango-columnas.AÑADIR(columna – 1)
                    si columna != 6 && tablero.ES-POSIBLE-JUGAR(fila + 1, columna + 1) entonces
                        si !(columna + 1 está en rango-columnas):
                            rango-columnas.AÑADIR(columna + 1)
        retornar rango-columnas

<h3>Algoritmos genéticos</h3>

Para determinar los “mejores” agentes para un juego de 4 en línea, se diseñó un algoritmo genético para establecer una ley de “el más fuerte y capaz de adaptarse sobrevive”. Por esta razón, con base en una población inicial de agentes con valores aleatorios, se determinó que la manera de identificar quiénes son más aptos (función de fitness / adaptabilidad) sería mediante el número de victorias obtenido contra los demás agentes. Al brindar un número inicial de población, un número de generaciones a crear, y el número de agentes más aptos a mantenerse, se procederá a ejecutar el algoritmo genético, el cual se detendrá al llegar al número especificado de generación.

<h4>Operación de cruce</h4>

La operación de cruce es aquella que permite crear nuevos agentes a partir de dos “padres”, como si se tratara de seres vivos. En este caso, a la hora de cruzar, se toman los valores de los agentes padres con la intención de simular “genes” o “cromosomas”, al tomar la mitad de cada padre y crear un agente con una combinación nueva de valores. Al cruzarse, se genera un “agente hijo”, el cual toma los valores decimales de los movimientos genéricos 1 y 3 de un agente, contra los valores de los movimientos genéricos 2 y 4 del otro (recordar que los números de movimientos genéricos se explicaron en la sección anterior).

Para cruzar los N agentes más aptos entre sí, se realiza de forma “elitista”, es decir, se toma el mejor agente y se cruza con el segundo más apto, el tercero con el cuarto, y así sucesivamente. Se espera que el número N de individuos más aptos sea par, pero si no es el caso, el agente menos apto de todos no se cruzará y pasará a la siguiente generación.

<h4>Operación de mutación</h4>

Respecto a la mutación, resulta similar a la vida real, donde una especie muta de manera espontánea y evoluciona constantemente. Para este caso, una vez que los agentes padres se han cruzado, hay una pequeña probabilidad en los agentes hijos de que uno de sus parámetros para los movimientos genéricos “mute”, que equivale a generar un nuevo valor aleatorio entre 0 y 1 para determinar la nueva probabilidad. Esto asegura variabilidad en las “especies”.

Nota: Para ejecutar el programa de consola, es necesario seguir un formato como el mostrado aquí (sólo los números están sujetos a cambio):

python MainGenetics.py --gen_number:20 --pop_number:20 --next_gen_agents:80

<h3>Programa interactivo</h3>

Además del programa de consola que permite obtener un agente a partir de una población generada aleatoriamente, existe otro que permitirá tanto jugar contra un agente pasado por parámetro, como indicar dos parámetros de agente y hacer que jueguen entre sí.

<h4>Formato de parámetros de ejecución</h4>

El string del agente retornado por la consola del algoritmo genético debe de verse con un formato similar a este (sin espacios, únicamente las comas como separadores):

0.923072380453,0.594874591925,0.977029031199,0.471895098323

<h3>Apéndice: Manual de usuario</h3>

<h4>Instalación y ejecución</h4>

Se asume que el usuario tiene como mínimo la versión 3 de Python instalada, que incluye pip por defecto. Para clonar de GitHub el proyecto, se puede ejecutar el siguiente comando (ya sea en Linux, en el Bash de Git de Windows, etc.):

git clone https://github.com/rrdm23/IA-Proyecto2.git

Otra opción es ingresar directamente a la página, donde se puede ver directamente esta información:

https://github.com/rrdm23/IA-Proyecto2

Con el IDE PyCharm, el proyecto es perfectamente ejecutable, sin embargo, para aquellos que no lo posean, pueden ejecutar su IDE de preferencia en la carpeta raíz del proyecto.
