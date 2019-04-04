#dato lo shingle vector "shingle_vec" genera tutti gli shingle vector 6/8 e 7/8 e ritorna un dict shingle:0
# che contiene tutti gli elementi
def generate_6_7_from_8_shingleVec(shingle_vec):
	
	#inizializzo il dict finale e un dict temporaneo per gli shingle 7/8
	H={}
	HTemp={}
	
	shingle_dict={shingle_vec:0}
	
	#per ogni shingle 8/8 copio elemento per elemento sostituendo un elemento per posizione con la wind card
	# e aggiungo il risultato nel dict temporaneo
	for key in shingle_dict:
		for m in range(8):
			a= ()
			for n in range(8):
				if  m != n:
					a= a + (key[n],)
				else :
					a= a+ ("*",)
			HTemp[a]=0
	
	#per ogni shingle 7/8 copio elemento per elemento sostituendo un elemento per posizione con la wind card
	# e aggiungo il risultato nel dict finale
	for key in HTemp.keys():
		for m in range(8):
			a= ()
			for n in range(8):
				if  m != n:
					a= a + (key[n],)
				else :
					a= a+ ("*",)
			H[a]=0
				
	#aggiungo lo shingle 8/8 al dict finale
	H[shingle_vec]=0
	return H
	
#dato il dict finale shingle:punteggio "H" conta le occorrenze degli shingle del dict shingle:0 "a"
#se non presente lo inserisce con punteggio 1, altrimenti incrementa il punteggio
def dict_shingle_occurencies(H,a):
	
	for key in a:
		x = H.get(key)
		if x==None:
			H[key]=1
		else:
			y=H.get(key)
			y=y+1
			H[key]=y
	return H
	
#dict di shingle:url di prova
shingle_dict = {(0,1,2,3,4,5,6,7):"blabla",(0,1,2,3,4,5,6,9):"blabla"};
#inizializzazione dict H shingle:punteggio
H={}

#itero sul set si shingles richiamando prima la funzione di generazione degli shingle 6/8 e 7/8
# e poi quella che calcola il punteggio ritornando un dict shingle:punteggio
for x in shingle_dict:
	a = generate_6_7_from_8_shingleVec(x)
	H = dict_shingle_occurencies(H,a)