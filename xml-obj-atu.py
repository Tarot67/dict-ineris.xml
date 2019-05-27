import lxml
from bs4 import BeautifulSoup
import re
import sys


class dtdict:
	def __init__(self, descripteur):
		self.extract = None
		self.extract_branch = None
		self.emprise = ["t:emprise", "emprise", "gu22:emprise" ]
		self.descripteur = descripteur
		self.soup = BeautifulSoup(self.descripteur,"lxml")
		self.partie = None
		self.resul = None
		self.dt_origine = None
		self.dict_origine = None
		self.atu_origine = None

	def extraction1(self):
		self.resul = self.soup.find(self.partie).find(self.extract).text
		if self.partie == ["t:dt", "t:partiedt", "dt", "partiedt", "dtliee", "gu22:dt", "gu22:dtliee", "gu22:partiedt" ] and self.extract == ["noconsultationduteleservice", "noconsultationduteleserviceseize", "t:noconsultationduteleservice", "t:noconsultationduteleserviceseize", "gu22:noconsultationduteleserviceseize", "gu22:noconsultationduteleservice" ] and self.resul != None:
			origine = re.search("([0-9]+)([A-Z])(.*)",str(self.resul))
			self.dt_origine = origine.group(2)
			#print(origine.group(2))
			#print(origine.groups())
		if self.partie == ["t:dict", "t:partiedict", "dict", "partiedict", "gu22:dict", "gu22:partiedict" ] and self.extract == ["noconsultationduteleservice", "noconsultationduteleserviceseize", "t:noconsultationduteleservice", "t:noconsultationduteleserviceseize", "gu22:noconsultationduteleservice" ] and self.resul != None:
			origine = re.search("([0-9]+)([A-Z])(.*)",str(self.resul))
			self.dict_origine = origine.group(2)
			#print(origine.group(2))
			#print(origine.groups())

		if self.partie == ["t:atu", "t:partieatu", "atu", "partieatu", "gu22:atu" ] and self.extract == ["noconsultationduteleservice", "noconsultationduteleserviceseize", "t:noconsultationduteleservice", "t:noconsultationduteleserviceseize", "gu22:noconsultationduteleservice" ] and self.resul != None:
			origine = re.search("([0-9]+)([A-Z])(.*)",str(self.resul))
			self.atu_origine = origine.group(2)

	def extraction2(self):
		self.resul = self.soup.find(self.partie).find(self.extract).findChild(self.extract_branch).text

	def extraction3(self):
		#nb_poly = self.soup.find("emprise").findAll("ns2:poslist").__len__()	
		#nb_poly = self.soup.find(self.partie).find(self.extract).findAll(self.extract_branch).__len__()
		nb_poly = self.soup.find(self.partie).find(self.emprise).findAll(self.extract_branch).__len__()
		#print(nb_poly)
		if nb_poly == 1:
			self.resul = self.soup.find(self.partie).find(self.extract).findChild(self.extract_branch).text 
			reponse = re.search('[7][.][0-9]+ [4][8][.][0-9]+',self.resul)
			if reponse:
				traite_liste = re.finditer('[7][.][0-9]+ [4][8][.][0-9]+',self.resul)
				g = [ tt.group(0) for tt in traite_liste ]
				self.resul = [ k.replace(' ',',') for k in g ]
			else:
				traite_liste = re.finditer('[7][.][0-9]+,[4][8][.][0-9]+',self.resul)
				self.resul = [ tt.group(0) for tt in traite_liste ]
		else:
			print("cas multi polygone")
			#self.resul = self.soup.find(self.partie).find(self.extract).findAll(self.extract_branch)
			self.resul = self.soup.find(self.partie).find(self.emprise).findChildren(self.extract_branch)
			traite_liste=re.sub("ns2[:]","",str(self.resul))
			self.resul=traite_liste
			traite_liste = re.sub("<poslist srsdimension=.2.>","",self.resul)
			self.resul=traite_liste
			traite_liste=re.sub("</poslist>","",self.resul)
			self.resul=traite_liste
			traite_liste=re.sub("<gml:coordinates>","",self.resul)
			self.resul=traite_liste
			traite_liste=re.sub("<coordinates>","",self.resul)
			self.resul=traite_liste
			traite_liste=re.sub("</gml:coordinates>","",self.resul)
			self.resul=traite_liste
			traite_liste=re.sub("</coordinates>","",self.resul)
			self.resul=traite_liste
			#self.resul=traite_liste
			self.resul=traite_liste + 'MULTIPOLYGON'
			print("Debug liste poly: " + str(self.resul))
			
	def extraction4(self):
		ma_liste = self.soup.find(self.partie).find(self.extract).findChildren(self.extract_branch)
		#print(ma_liste)
		if len(ma_liste) > 1:
			if re.search("<t:naturedestravaux>", str(ma_liste)):
				ma_sortie = re.sub("<t:naturedestravaux>","",str(ma_liste))
				ma_liste= ma_sortie
				ma_sortie = re.sub("</t:naturedestravaux>","",ma_liste)
				ma_liste = ma_sortie
			elif re.search("<naturedestravaux>", str(ma_liste)):
				ma_sortie = re.sub("<naturedestravaux>","",str(ma_liste))
				ma_liste= ma_sortie
				ma_sortie = re.sub("</naturedestravaux>","",ma_liste)
				ma_liste = ma_sortie
			else:
				ma_sortie = re.sub("<gu22:naturedestravaux>","",str(ma_liste))
				ma_liste= ma_sortie
				ma_sortie = re.sub("</gu22:naturedestravaux>","",ma_liste)
				ma_liste = ma_sortie
			ma_sortie = re.sub("\[","",ma_liste)
			ma_liste = ma_sortie
			ma_sortie = re.sub("\]","",ma_liste)
			ma_liste = ma_sortie
			ma_sortie = re.sub(",","",ma_liste)
			#print("masortie vaut" + ma_sortie)
			self.resul=ma_sortie

		else:
			self.resul = self.soup.find(self.partie).find(self.extract).findChild(self.extract_branch).text


class const_dtdict:
	def __init__(self):
		self._PARTIEDT = ["t:dt", "t:partiedt", "dt", "partiedt", "dtliee", "gu22:dt", "gu22:dtliee", "gu22:partiedt" ]
		self._PARTIEDICT = ["t:dict", "t:partiedict", "dict", "partiedict", "gu22:dict", "gu22:partiedict" ]
		self._PARTIEATU = ["t:atu", "t:partieatu", "atu", "partieatu", "gu22:atu" ]
		self._NUM_DICT = ["noconsultationduteleservice", "noconsultationduteleserviceseize", "t:noconsultationduteleservice", "t:noconsultationduteleserviceseize", "gu22:noconsultationduteleservice" ]
		self._NUM_DT = ["noconsultationduteleservice", "noconsultationduteleserviceseize", "t:noconsultationduteleservice", "t:noconsultationduteleserviceseize", "gu22:noconsultationduteleserviceseize", "gu22:noconsultationduteleservice" ]
		self._NUM_ATU =["noconsultationduteleservice", "noconsultationduteleserviceseize", "t:noconsultationduteleservice", "t:noconsultationduteleserviceseize", "gu22:noconsultationduteleservice" ]
		self._SOUSPARTIEATUREPONSE = [ "t:chantiertermineouchantieravenir", "chantiertermineouchantieravenir" , "gu22:chantiertermineouchantieravenir" ]
		self._ATU_REPONSE = [ "t:reponseattenduechantieravenir", "reponseattenduechantieravenir", "gu22:reponseattenduechantieravenir" ]

		self._NUM_AFFAIRE_DT = ["noaffaireduresponsableduprojet","t:noaffaireduresponsableduprojet", "gu22:noaffaireduresponsableduprojet" ]
		self._NUM_AFFAIRE_DICT = ["noaffairedelexecutantdestravaux","t:noaffairedelexecutantdestravaux", "noaffairedelexecutantdestravaux", "gu22:noaffairedelexecutantdestravaux" ]
		self._SOUSPARTIEOEUVRE = (["t:representantduresponsabledeprojet", "gu22:representantduresponsabledeprojet", "representantduresponsabledeprojet"])
		self._SOUSPARTIEATU = (["t:personneordonnantlestravauxurgents", "gu22:personneordonnantlestravauxurgents", "personneordonnantlestravauxurgents"])
		self._DATEDECLARATION = ["datedeladeclaration","t:datedeladeclaration","gu22:datedeladeclaration", "date", "t:date", "gu22:date" ]
		self._DATETRAVAUX = ["dateprevuepourlecommencementdestravaux","t:dateprevuepourlecommencementdestravaux","gu22:dateprevuepourlecommencementdestravaux", "datedebutdestravaux", "t:datedebutdestravaux", "gu22:datedebutdestravaux" ]
		self._PROJETCAL = ["projetetsoncalendrier", "travauxetleurcalendrier","t:travauxetleurcalendrier","t:projetetsoncalendrier","gu22:projetetsoncalendrier", "gu22:travauxetleurcalendrier" ]
		self._CHAMPMELCONTACT = ["t:courriel", "courriel", "gu22:courriel" ]
		self._CHAMPENTREPOEUVRE = ["denomination","t:denomination", "gu22:denomination", "gu22:nom", "t:nom", "nom" ]
		self._CHAMPNUMVOIEOEUVRE = ["t:numero", "numero", "gu22:numero" ]
		self._CHAMPVOIEOEUVRE = ["t:voie", "voie", "gu22:voie" ]
		self._CHAMPCPOEUVRE = ["t:codepostal", "codepostal", "gu22:codepostal" ]
		self._CHAMPCOMMUNEOEUVRE = ["t:commune", "commune", "gu22:commune" ]
		self._CHAMPTELOEUVRE = ["t:tel", "tel", "gu22:tel" ]
		self._CHAMPFAXOEUVRE = ["t:fax", "fax", "gu22:fax" ]
		self._CHAMPCONTACT = (["t:personneacontacter", "personneacontacter",
					"nomdelapersonneacontacter","t:nomdelapersonneacontacter", "gu22:nomdelapersonneacontacter", "gu22:personneacontacter" ])
		self._CONJOINTE = ["declarationconjointedtdict","t:declarationconjointedtdict", "gu22:declarationconjointedtdict" ]
		self._SOUSPARTIEEXECUTANT = (["t:executantdestravaux", 
                        "executantdestravaux", "gu22:executantdestravaux" ])
		self._CHAMPEMPRISE = (["t:emplacementduprojet", "emplacementduprojet",
                 "t:emplacementdestravaux", "emplacementdestravaux", "gu22:emplacementdestravaux", "gu22:emplacementduprojet", "travauxemplacementdureedescription", "t:travauxemplacementdureedescription", "gu22:travauxemplacementdureedescription" ])
		self._CHAMPADDRTRA = ["t:adresse", "adresse", "gu22:adresse" ]
		self._CHAMPCPTRA = ["t:cp", "cp", "gu22:cp" ]
		self._CHAMPCOMMUNETRA = ["t:communeprincipale", "communeprincipale", "gu22:communeprincipale", "commune", "t:commune", "gu22:commune" ]
		self._AVANTEMPRISE = ["gml:linearring", "ns2:linearring"]
		self._EMPRISE = ["gml:coordinates", "ns2:coordinates", "gml:poslist", "ns2:poslist"]
		self._NATURE_TRA = (["naturedestravaux", "t:naturedestravaux", "gu22:naturedestravaux",
				"travauxetmoyensmisenoeuvre", "t:travauxetmoyensmisenoeuvre", "gu22:travauxetmoyensmisenoeuvre" ])

class descrit_toi_DT:
	def __init__(self):
		self.liste_dt = ({"_NUM_DT":"extraction1",
			"_NUM_AFFAIRE_DT":"extraction1",
			"_CHAMPENTREPOEUVRE":["extraction2","_SOUSPARTIEOEUVRE"],
			"_CHAMPNUMVOIEOEUVRE":["extraction2","_SOUSPARTIEOEUVRE"],
			"_CHAMPVOIEOEUVRE":["extraction2","_SOUSPARTIEOEUVRE"],
			"_CHAMPCPOEUVRE":["extraction2","_SOUSPARTIEOEUVRE"],
			"_CHAMPCOMMUNEOEUVRE":["extraction2","_SOUSPARTIEOEUVRE"],
			"_CHAMPCONTACT":["extraction2","_SOUSPARTIEOEUVRE"],
			"_CHAMPMELCONTACT":["extraction2","_SOUSPARTIEOEUVRE"],
			"_CHAMPADDRTRA":["extraction2","_CHAMPEMPRISE"],
			"_CHAMPCOMMUNETRA":["extraction2","_CHAMPEMPRISE"],
			"_DATEDECLARATION":"extraction1",
			"_DATETRAVAUX":["extraction2","_PROJETCAL"],
			"_EMPRISE":["extraction3","_AVANTEMPRISE"],
			"_NATURE_TRA":["extraction4","_PROJETCAL"]})

class descrit_toi_DICT:
	def __init__(self):
		self.liste_dict = ({"_NUM_DICT":"extraction1",
			"_NUM_AFFAIRE_DICT":"extraction1", 
			"_CHAMPENTREPOEUVRE":["extraction2","_SOUSPARTIEEXECUTANT"],
			"_CHAMPNUMVOIEOEUVRE":["extraction2","_SOUSPARTIEEXECUTANT"],
			"_CHAMPVOIEOEUVRE":["extraction2","_SOUSPARTIEEXECUTANT"],
			"_CHAMPCPOEUVRE":["extraction2","_SOUSPARTIEEXECUTANT"],
			"_CHAMPCOMMUNEOEUVRE":["extraction2","_SOUSPARTIEEXECUTANT"],
			"_CHAMPCONTACT":["extraction2","_SOUSPARTIEEXECUTANT"],
			"_CHAMPMELCONTACT":["extraction2","_SOUSPARTIEEXECUTANT"],
			"_CHAMPADDRTRA":["extraction2","_CHAMPEMPRISE"],
			"_CHAMPCOMMUNETRA":["extraction2","_CHAMPEMPRISE"],
			"_DATEDECLARATION":"extraction1",
			"_DATETRAVAUX":["extraction2","_PROJETCAL"],
			"_EMPRISE":["extraction3","_AVANTEMPRISE"],
			"_NATURE_TRA":["extraction4","_PROJETCAL"]})

class descrit_toi_ATU:
     def __init__(self):
                self.liste_atu = ({"_NUM_ATU":"extraction1",
			"_ATU_REPONSE":["extraction2","_SOUSPARTIEATUREPONSE"],
                        "_CHAMPENTREPOEUVRE":["extraction2","_SOUSPARTIEATU"],
                        "_CHAMPNUMVOIEOEUVRE":["extraction2","_SOUSPARTIEATU"],
                        "_CHAMPVOIEOEUVRE":["extraction2","_SOUSPARTIEATU"],
                        "_CHAMPCPOEUVRE":["extraction2","_SOUSPARTIEATU"],
                        "_CHAMPCOMMUNEOEUVRE":["extraction2","_SOUSPARTIEATU"],
                        "_CHAMPCONTACT":["extraction2","_SOUSPARTIEATU"],
                        "_CHAMPMELCONTACT":["extraction2","_SOUSPARTIEATU"],
                        "_CHAMPADDRTRA":["extraction2","_CHAMPEMPRISE"],
                        "_CHAMPCOMMUNETRA":["extraction2","_CHAMPEMPRISE"],
                        "_DATEDECLARATION":"extraction1",
                        "_DATETRAVAUX":["extraction2","_CHAMPEMPRISE"],
                        "_EMPRISE":["extraction3","_AVANTEMPRISE"],
                        "_NATURE_TRA":["extraction2","_CHAMPEMPRISE"]})

if __name__ == '__main__':
	#print('toto' ,len(sys.argv))
	#print(sys.argv[-1:])
	#for arg  in sys.argv:
	value = sys.argv[-1:][0]
	descripteur = open(value)
	
	newfile=value + ".txt"

	sortie = open(newfile,"w")

	#INSTANCE DE CLASSE
	jst = dtdict(descripteur)
	jstconst = const_dtdict()
	jstdecritdt = descrit_toi_DT()
	jstdecritdict = descrit_toi_DICT()
	jstdecritatu = descrit_toi_ATU()

	#print('partie DT')

	sortie.write("PARTIE:DT#")

	for g in jstdecritdt.liste_dt:
		jst.partie = jstconst._PARTIEDT
		if isinstance(jstdecritdt.liste_dt[g],list):
			jst.extract = getattr(jstconst,jstdecritdt.liste_dt[g][1])
			jst.extract_branch = getattr(jstconst,g)
			tmp = jstdecritdt.liste_dt[g][0]
			#print("DEBUG: jst.extract:" + str(jst.extract) + " jst.extract_branch : " + str(jst.extract_branch) + " tmp vaut: " + tmp)
		else:
			jst.extract = getattr(jstconst,g)
			tmp = jstdecritdt.liste_dt[g]
			#print("DEBUG: jst.extract:" + str(jst.extract) + " tmp vaut: " + tmp)
			
					
		try:
			getattr(jst,tmp)()
			#print("resultat: " + str(jst.resul))
			if jst.resul:
				#sortie.write(g + ":" + str(jst.resul) + "#")
				sortie.write(g + ":" + str(jst.resul) + "#")
			else:
				sortie.write(g + ":#")
		except AttributeError:
			#print("le champ " + g + " n existe pas")
			sortie.write(g + ":#")
	sortie.write("ORIGINE:")
	if jst.dt_origine != None:
		sortie.write(jst.dt_origine + "#")
	else:
		sortie.write("#")

	#print('\npartie DICT')

	sortie.write("\nPARTIE:DICT#")

	for g in jstdecritdict.liste_dict:
		jst.partie = jstconst._PARTIEDICT
		if isinstance(jstdecritdict.liste_dict[g],list):
			jst.extract = getattr(jstconst,jstdecritdict.liste_dict[g][1])
			jst.extract_branch = getattr(jstconst,g)
			tmp = jstdecritdict.liste_dict[g][0]
			#print("DEBUG: jst.extract:" + str(jst.extract) + " jst.extract_branch : " + str(jst.extract_branch) + " tmp vaut: " + tmp)
		else:
			jst.extract = getattr(jstconst,g)
			tmp = jstdecritdict.liste_dict[g]
			#print("DEBUG: jst.extract:" + str(jst.extract) + " tmp vaut: " + tmp)

		try:
			getattr(jst,tmp)()
			#print("resultat: " + str(jst.resul))
			if jst.resul:
				sortie.write(g + ":" + str(jst.resul) + "#")
			else:
				sortie.write(g +  ":#")
		except AttributeError:
			#print("le champ " + g + " n existe pas")
			sortie.write(g + ":#")

	sortie.write("ORIGINE:")
	if jst.dict_origine != None:
		sortie.write(jst.dict_origine + "#")
	else:
		sortie.write("#")

	sortie.write("\nPARTIE:ATU#")

	for g in jstdecritatu.liste_atu:
                jst.partie = jstconst._PARTIEATU
                if isinstance(jstdecritatu.liste_atu[g],list):
                        jst.extract = getattr(jstconst,jstdecritatu.liste_atu[g][1])
                        jst.extract_branch = getattr(jstconst,g)
                        tmp = jstdecritatu.liste_atu[g][0]
                        #print("DEBUG: jst.extract:" + str(jst.extract) + " jst.extract_branch : " + str(jst.extract_branch) + " tmp vaut: " + tmp)
                else:
                        jst.extract = getattr(jstconst,g)
                        tmp = jstdecritatu.liste_atu[g]
                        #print("DEBUG: jst.extract:" + str(jst.extract) + " tmp vaut: " + tmp)

                try:
                        getattr(jst,tmp)()
                        #print("resultat: " + str(jst.resul))
                        if jst.resul:
                                sortie.write(g + ":" + str(jst.resul) + "#")
                        else:
                                sortie.write(g +  ":#")
                except AttributeError:
                        #print("le champ " + g + " n existe pas")
                        sortie.write(g + ":#")

	sortie.write("ORIGINE:")
	if jst.atu_origine != None:
                sortie.write(jst.atu_origine + "#")
	else:
                sortie.write("#")

sortie.close()
descripteur.close()
