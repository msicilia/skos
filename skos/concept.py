

class SKOSConcept():
	"""
	Concepts in SKOS are the units of thought, ideas, meanings,
	or (categories of) objects and events which underlie 
	many knowledge organization systems.
	"""
	def __init__(self, uri, endpoint):
		"""
		Creates the concept based on traversable URI identifying it.
		"""
		self.uri = uri
		self.endpoint = endpoint

	def get_preflabels(self):
		""" 
		Preferred lexical label(s). Only one, but may be translated. 
		
		Returns:
			A list of tuples ("label", "lang").
			Languages represented as ISO codes.		
		"""
		q1 = '''
			 PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
			 SELECT ?lbl
			 { '''
		q = (q1 + '<' + self.uri + '>' + '''
			skos:prefLabel ?lbl.
			}
			'''
			)

		self.endpoint.setQuery(q)
		ret = self.endpoint.query().convert()

		if ret["results"]["bindings"]:
			self.pref_labels = []
			for row in ret["results"]["bindings"]:
				self.pref_labels.append([row["lbl"]["value"], 
										 row["lbl"]["xml:lang"]])
		else:
			self.pref_labels = None
		return self.pref_labels


	def get_altlabels(self):
		""" Synonyms, near-synonyms, abbreviations and acronyms.
			
			Returns:
			A list of tuples ("label", "lang").
			Languages represented as ISO codes.	

		"""
		q1 = '''
			 PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
			 SELECT ?lbl
			 { '''
		q = (q1 + '<' + self.uri + '>' + '''
			skos:altLabel ?lbl.
			}
			'''
			)

		self.endpoint.setQuery(q)
		ret = self.endpoint.query().convert()

		if ret["results"]["bindings"]:
			self.alt_labels = []
			for row in ret["results"]["bindings"]:
				self.alt_labels.append([row["lbl"]["value"], 
										 row["lbl"]["xml:lang"]])
		else:
			self.alt_labels = None
		return self.alt_labels

	def get_hiddenlabels(self):
		"""  Accessible to applications performing text-based indexing 
		     and search operations, but would not like that label to 
		     be visible otherwise.


		"""
		q1 = '''
			 PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
			 SELECT ?lbl
			 { '''
		q = (q1 + '<' + self.uri + '>' + '''
			skos:hiddenLabel ?lbl.
			}
			'''
			)

		self.endpoint.setQuery(q)
		ret = self.endpoint.query().convert()

		if ret["results"]["bindings"]:
			self.hidden_labels = []
			for row in ret["results"]["bindings"]:
				self.hidden_labels.append([row["lbl"]["value"], 
										 row["lbl"]["xml:lang"]])
		else:
			self.hidden_labels = None
		return self.hidden_labels


	def get_concepts(self, prop):
		"""
			Returns a list of concepts related by property prop. 
		"""
		q = ('''
			 PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
			 SELECT ?c
			 { 
			     ?c a skos:Concept .
			     <'''+ self.uri +'> '+ prop + ' ?c.}'
			)
		self.endpoint.setQuery(q)
		ret = self.endpoint.query().convert()
		if ret["results"]["bindings"]:
			r = []
			for result in ret["results"]["bindings"]:
				r.append(SKOSConcept(result["c"]["value"], self.endpoint))
			return r
		else:
			return None
	

	def get_narrower(self):
		"""
			Returns a list of skos:narrower concepts. 
		"""
		return self.get_concepts("skos:narrower")

	def get_related(self):
		"""
			Returns a list of skos:related concepts. 
		"""
		return self.get_concepts("skos:related")

	def get_broader(self):
		"""
			Returns a list of skos:broader concepts. 
		"""
		return self.get_concepts("skos:broader")