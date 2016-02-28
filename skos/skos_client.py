"""Queries against a SPARQL endpoint using SKOS schema.

	The SKOS schema can be found here:
	https://www.w3.org/TR/2009/REC-skos-reference-20090818/

	It allows for navigational traversal of the concept graph.
	It hides the underlying SPARQL queries.
"""

from SPARQLWrapper import SPARQLWrapper, JSON

from concept import SKOSConcept

class SKOSEndpoint():
	"""
	Wraps a SPARQL endpoint, assuming it is using SKOS.
	"""

	def __init__(self, url):
		"""
		Sends a ping query to the endpoint.
		"""
		self.endpoint = SPARQLWrapper(url)
		self.endpoint.setQuery("""ASK {}""")
		self.endpoint.setReturnFormat(JSON)
		results = self.endpoint.query().convert()
		assert results["boolean"], "Endpoint error, did not resolve ASK{}"


	def query_concept(self, label,
		              include_alt=False,
		              lang="en"):
		"""
		Queries concepts based on labels.
		Args:
			label: the query string to query for.
			include_alt: use also altLabel(s)
			lang: filter a single language (ISO code, default English).
		Returns:
			The first exact match for the concept or None
		"""
		if not include_alt:
			return self.query_concept_aux(label, "skos:prefLabel")
		else:
			return self.query_concept_aux(label, "skos:prefLabel") + self.query_concept_aux(label, "skos:altLabel")

	def query_concept_aux(self, label,
		              	  property,
		              	  lang="en"):
		"""
		Queries concepts based on labels.
		Args:
			label: the query string to query for.
			property: the SKOS property to use
			lang: filter a single language (ISO code, default English).
		Returns:
			The first exact match for the concept or None
		"""
		# Get the URI of the skos:Concept
		q = ('''
			 PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
			 SELECT ?c
			 {
			     ?c a skos:Concept .
			     ?c ''' + property + ' "' + label + '"@'+lang+'.}'
			)
		self.endpoint.setQuery(q)
		try :
			ret = self.endpoint.query().convert()
			# If the list of bindings is nonempty, it has rows returned:
			if ret["results"]["bindings"]:
				cpts = []
				for row in ret["results"]["bindings"]:
					cpts.append(SKOSConcept(row["c"]["value"],
					           self.endpoint))
				return cpts
			else:
				return None

		except Exception as e:
			print e
			print "Something went wrong looking for concept: " + label
