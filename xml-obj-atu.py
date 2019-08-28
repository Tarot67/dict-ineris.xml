import lxml
from bs4 import BeautifulSoup
import re
import sys


class dtdict:
	def __init__(self, descripteur):
		self.extract = None
		self.extract_branch = None
		self.emprise = [ i+j if i == '' else i + ':' +j  for i in namespace for j in [ "emprise" ]]
		self.descripteur = descripteur
		self.soup = BeautifulSoup(self.descripteur,"lxml")
		self.partie = None
		self.resul = None
		self.dt_origine = None
		self.dict_origine = None
		self.atu_origine = None

	def extraction1(self):
		self.resul = self.soup.find(self.partie).find(self.extract).text
		if self.partie == [ i+j if i == '' else i + ':' +j  for i in namespace for j in valeur_namespace_dt ] and self.extract == [i+j if i == '' else i + ':' +j  for i in namespace for j in  ["noconsultationduteleservice", "noconsultationduteleserviceseize"]] and self.resul != None:
			origine = re.search("([0-9]+)([A-Z])(.*)",str(self.resul))
			self.dt_origine = origine.group(2)
			#print(origine.group(2))
			#print(origine.groups())
		if self.partie == [ i+j if i == '' else i + ':' +j  for i in namespace for j in valeur_namespace_dict ] and self.extract == [  i+j if i == '' else i + ':' +j  for i in namespace for j in ["noconsultationduteleservice", "noconsultationduteleserviceseize"]] and self.resul != None:
			origine = re.search("([0-9]+)([A-Z])(.*)",str(self.resul))
			self.dict_origine = origine.group(2)
			#print(origine.group(2))
			#print(origine.groups())

		if self.partie == [ i+j if i == '' else i + ':' +j  for i in namespace for j in valeur_namespace_atu ] and self.extract == [ i+j if i == '' else i + ':' +j  for i in namespace for j in ["noconsultationduteleservice", "noconsultationduteleserviceseize"]] and self.resul != None:
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
			traite_liste=re.sub("ns1[:]","",str(self.resul))
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
			for k in [ i+j if i == '' else i + ':' +j  for i in namespace for j in ["naturedestravaux"]]:
				ma_sortie = re.sub("<" + k + ">","",str(ma_liste))
				if str(ma_liste) != ma_sortie:
						ma_liste = ma_sortie
						ma_sortie = re.sub("</" + k + ">","",ma_liste)
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

	
	def extraction5(self):
		ma_liste = self.soup.find(self.partie).find(self.extract).findChildren(self.extract_branch)
		#print(ma_liste)
		if len(ma_liste) > 1:
			for k in [ i+j if i == '' else i + ':' +j  for i in namespace for j in ["techniquesutilisees"]]:
				ma_sortie = re.sub("<" + k + ">","",str(ma_liste))
				if str(ma_liste) != ma_sortie:
						ma_liste = ma_sortie
						ma_sortie = re.sub("</" + k + ">","",ma_liste)
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
		self._PARTIEDT = [ i+j if i == '' else i + ':' +j  for i in namespace for j in valeur_namespace_dt ]
		self._PARTIEDICT = [ i+j if i == '' else i + ':' +j  for i in namespace for j in valeur_namespace_dict ]
		self._PARTIEATU = [ i+j if i == '' else i + ':' +j  for i in namespace for j in valeur_namespace_atu ]
		self._NUM_DICT = [ i+j if i == '' else i + ':' +j  for i in namespace for j in ["noconsultationduteleservice", "noconsultationduteleserviceseize"]]
		self._NUM_DT = [ i+j if i == '' else i + ':' +j  for i in namespace for j in ["noconsultationduteleservice", "noconsultationduteleserviceseize"]]
		self._NUM_ATU = [ i+j if i == '' else i + ':' +j  for i in namespace for j in ["noconsultationduteleservice", "noconsultationduteleserviceseize"]]
		self._SOUSPARTIEATUREPONSE = [ i+j if i == '' else i + ':' +j  for i in namespace for j in [ "chantiertermineouchantieravenir" ]]
		self._ATU_REPONSE = [ i+j if i == '' else i + ':' +j  for i in namespace for j in [ "reponseattenduechantieravenir" ]]
		self._NUM_AFFAIRE_DT = [ i+j if i == '' else i + ':' +j  for i in namespace for j in ["noaffaireduresponsableduprojet" ]]
		self._NUM_AFFAIRE_DICT = [ i+j if i == '' else i + ':' +j  for i in namespace for j in ["noaffairedelexecutantdestravaux" ]]
		self._SOUSPARTIEOEUVRE = ([ i+j if i == '' else i + ':' +j  for i in namespace for j in [ "representantduresponsabledeprojet" ]])
		self._SOUSPARTIEATU = ([ i+j if i == '' else i + ':' +j  for i in namespace for j in [ "personneordonnantlestravauxurgents" ]])
		self._DATEDECLARATION = [ i+j if i == '' else i + ':' +j  for i in namespace for j in ["datedeladeclaration", "date" ]]
		self._DATETRAVAUX = [ i+j if i == '' else i + ':' +j  for i in namespace for j in ["dateprevuepourlecommencementdestravaux", "datedebutdestravaux" ]]
		self._PROJETCAL = [ i+j if i == '' else i + ':' +j  for i in namespace for j in ["projetetsoncalendrier", "travauxetleurcalendrier" ]]
		self._CHAMPMELCONTACT = [ i+j if i == '' else i + ':' +j  for i in namespace for j in [ "courriel" ]]
		self._CHAMPENTREPOEUVRE = [ i+j if i == '' else i + ':' +j  for i in namespace for j in ["denomination", "nom" ]]
		self._CHAMPNUMVOIEOEUVRE = [ i+j if i == '' else i + ':' +j  for i in namespace for j in [ "numero" ]]
		self._CHAMPVOIEOEUVRE = [ i+j if i == '' else i + ':' +j  for i in namespace for j in [ "voie" ]]
		self._CHAMPCPOEUVRE = [ i+j if i == '' else i + ':' +j  for i in namespace for j in [ "codepostal" ]]
		self._CHAMPCOMMUNEOEUVRE = [ i+j if i == '' else i + ':' +j  for i in namespace for j in [ "commune" ]]
		self._CHAMPTELOEUVRE = [ i+j if i == '' else i + ':' +j  for i in namespace for j in [ "tel" ]]
		self._CHAMPFAXOEUVRE = [ i+j if i == '' else i + ':' +j  for i in namespace for j in [ "fax" ]]
		self._CHAMPCONTACT = [ i+j if i == '' else i + ':' +j  for i in namespace for j in ["personneacontacter", "nomdelapersonneacontacter" ]]
		self._CONJOINTE = [ i+j if i == '' else i + ':' +j  for i in namespace for j in ["declarationconjointedtdict" ]]
		self._SOUSPARTIEEXECUTANT = [ i+j if i == '' else i + ':' +j  for i in namespace for j in ["executantdestravaux"]]
		self._CHAMPEMPRISE = [ i+j if i == '' else i + ':' +j  for i in namespace for j in [ "emplacementduprojet", "emplacementdestravaux", "travauxemplacementdureedescription" ]]
		self._CHAMPADDRTRA = [ i+j if i == '' else i + ':' +j  for i in namespace for j in [ "adresse" ]]
		self._CHAMPCPTRA = [ i+j if i == '' else i + ':' +j  for i in namespace for j in [ "cp" ]]
		self._CHAMPCOMMUNETRA = [ i+j if i == '' else i + ':' +j  for i in namespace for j in ["communeprincipale", "commune" ]]
		self._AVANTEMPRISE = ["gml:linearring", "ns2:linearring", "ns1:linearring"]
		self._EMPRISE = ["gml:coordinates", "ns2:coordinates", "gml:poslist", "ns2:poslist", "ns1:poslist" ]
		self._NATURE_TRA = [ i+j if i == '' else i + ':' +j  for i in namespace for j in ["naturedestravaux", "travauxetmoyensmisenoeuvre" ]]
		self._DESCRI_PROJ = [ i+j if i == '' else i + ':' +j  for i in namespace for j in [ "decrivezleprojet", "decrivezlestravaux" ]]
		self._MOYENS_UTIL = [i+j if i == '' else i + ':' +j  for i in namespace for j in [ "techniquesutilisees" ]]

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
			"_CHAMPTELOEUVRE":["extraction2","_SOUSPARTIEOEUVRE"],
			"_CHAMPADDRTRA":["extraction2","_CHAMPEMPRISE"],
			"_CHAMPCOMMUNETRA":["extraction2","_CHAMPEMPRISE"],
			"_DATEDECLARATION":"extraction1",
			"_DATETRAVAUX":["extraction2","_PROJETCAL"],
			"_EMPRISE":["extraction3","_AVANTEMPRISE"],
			"_NATURE_TRA":["extraction4","_PROJETCAL"],
			"_MOYENS_UTIL":["extraction5","_PROJETCAL"],
			"_DESCRI_PROJ":["extraction2","_PROJETCAL"]})

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
			"_CHAMPTELOEUVRE":["extraction2","_SOUSPARTIEEXECUTANT"],
			"_CHAMPADDRTRA":["extraction2","_CHAMPEMPRISE"],
			"_CHAMPCOMMUNETRA":["extraction2","_CHAMPEMPRISE"],
			"_DATEDECLARATION":"extraction1",
			"_DATETRAVAUX":["extraction2","_PROJETCAL"],
			"_EMPRISE":["extraction3","_AVANTEMPRISE"],
			"_NATURE_TRA":["extraction4","_PROJETCAL"],
			"_MOYENS_UTIL":["extraction5","_PROJETCAL"],
			"_DESCRI_PROJ":["extraction2","_PROJETCAL"]})

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
			"_CHAMPTELOEUVRE":["extraction2","_SOUSPARTIEATU"],
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

	#nouvelle technique pour construire les listes
	#de balises j'utilise une liste namespace
	#qui contient tout les namespaces
	#ensuite a l'aide de liste comprehention
	#je construie cette liste dynamiquement
	#evitant ainsi les erreurs! car ces listes
	#commence a etre tres tres longue
	namespace=['t', '', 'gu22', 'gu3','ns3']

	#valeur_namespace_dt=['dt', 'partiedt', 'dtliee']
	valeur_namespace_dt=['dt', 'partiedt']
	valeur_namespace_dict=['dict', 'partiedict']
	valeur_namespace_atu=['atu', 'partieatu']

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
