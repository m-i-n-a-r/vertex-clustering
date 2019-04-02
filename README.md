# Vertex Clustering

## Status - WIP

## TODO list

#### Passi preliminari ed algoritmi di supporto
- Avere tutte le pagine di un sito in un file (csv, xml)
- Funzione che seleziona casualmente il 20% delle pagine disponibili nel csv sopra
- File che, data una pagina, calcola l'insieme degli shingle e il conseguente vettore di 8 byte
	- Data una pagina prendo tutti i subset di tag (sia aperti che chiusi) di lunghezza l=10
	- Applico a ciascun subset le 8 funzioni di hash (da definire)
	- Prendo il minimo per ciascuna funzione di hash e genero il vettore
	
#### Altro file (principale) che esegue l'algoritmo vero e proprio
- Primo passo
	- Prendo l'insieme delle pagine
	- Per ogni pagina calcolo lo shingle vector 
	- Genero tutti gli shingle vector con corrispondenza di 6/8, 7/8, 8/8 
	- Per ogni shingle vector generato, lo inserisco nella hashtable con punteggio 1, o se già presente incremento il suo punteggio di 1
- Secondo passo
	- Prendo ogni shingle vector con 8/8 in H (che corrisponderà a tutti gli shingle vector delle pagine in input), con punteggio crescente
	- Per ognuno prendiamo da H lo shingle che lo matcha ed ha punteggio massimo
	- Il punteggio dello shingle selezionato resta invariato, il punteggio degli altri shingle che matchano quello in esame è diminuito di un ammontare pari al punteggio dello shingle vector 8/8 in esame 
	- Cancello tutti gli shingle vector mascherati (quindi con 1 o più wildcard) in H con punteggio inferiore ad una soglia prestabilita (20)
- Terzo passo
	- Per ogni shingle vector mascherato v in H creo un cluster vuoto ad esso relativo
	- Ogni pagina p con vettore v viene assegnata al cluster Cv’ dove v’ e il vettore shingle in H che combacia con v ed ha il massimo punteggio
	- Ritorno i cluster con relativo shingle vector e il punteggio associato, e li visualizzo in qualche modo
	
### Testing 
- Run su diversi tipi di siti e calcolo di alcune metriche (coverage)
	
	