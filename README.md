# Vertex Clustering

## Status - WIP

## TODO list
#### Passi preliminari ed algoritmi di supporto
- [ ] Avere tutte le pagine di un sito in un file (csv, xml)
- [ ] Funzione che seleziona casualmente il 20% delle pagine disponibili nel csv sopra
- [X] File che, data una pagina, calcola l'insieme degli shingle e il conseguente vettore di 8 byte
	- [X] Data una pagina prendo tutti i subset di tag (sia aperti che chiusi) di lunghezza l=10
	- [X] Applico a ciascun subset le 8 funzioni di hash (da definire)
	- [X] Prendo il minimo per ciascuna funzione di hash e genero il vettore
- [X] Funzione per verificare il match tra due shingle vectors (dove uno dei due può contenere wildcard)
	
#### Altro file (principale) che esegue l'algoritmo vero e proprio
- [x] Primo passo
	- [x] Prendo l'insieme delle pagine
	- [x] Per ogni pagina calcolo lo shingle vector (funzione ausiliaria) 
	- [x] Genero tutti gli shingle vector con corrispondenza di 6/8, 7/8, 8/8 
	- [x] Per ogni shingle vector generato, lo inserisco nella hashtable con punteggio 1, o se già presente incremento il suo punteggio di 1
- [x] Secondo passo
	- [x] Prendo ogni shingle vector con 8/8 in H (che corrisponderà a tutti gli shingle vector delle pagine in input), con punteggio crescente
	- [x] Per ognuno prendiamo da H lo shingle che lo matcha ed ha punteggio massimo
	- [x] Il punteggio dello shingle selezionato resta invariato, il punteggio degli altri shingle che matchano quello in esame è diminuito di un ammontare pari al punteggio dello shingle vector 8/8 in esame 
	- [x] Cancello tutti gli shingle vector mascherati (quindi con 1 o più wildcard) in H con punteggio inferiore ad una soglia prestabilita (20)
- [x] Terzo passo
	- [x] Per ogni shingle vector mascherato v in H creo un cluster vuoto ad esso relativo
	- [x] Ogni pagina p con vettore v viene assegnata al cluster Cv’ dove v’ e il vettore shingle in H che combacia con v ed ha il massimo punteggio
	- [x] Ritorno i cluster con relativo shingle vector e il punteggio associato, e li visualizzo in qualche modo (grafico e json salvati in locale)
	
### Testing 
- [ ] Run su diversi tipi di siti e calcolo di alcune metriche (coverage)
	
	
