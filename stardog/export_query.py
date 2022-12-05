import stardog

fileNameDRUGS='/media/newbuntu/rdfal/drugs_DRUGS.ttl'
fileNameINTERACTIONS='/media/newbuntu/rdfal/drugs_INTERACTIONS.ttl'
fileNameRXNORM_DRON='/media/newbuntu/rdfal/drugs_RXNORM_DRON_2.ttl'
fileNameSTARDRUGS_dronSPO='/media/newbuntu/rdfal/DRON_spo.ttl'
fileNameSTARDRUGS_rxnormSPO='/media/newbuntu/rdfal/RXNORM_spo.ttl'


conn_details = {
  'endpoint': 'http://localhost:4322',
  'username': 'admin',
  'password': 'admin'
}
query_DRUGS = """
prefix dsch: <http://schema.rdfal.co/#>

prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix pathway: <http://smpdb.ca/view/>
prefix uniprot: <https://www.uniprot.org/uniprotkb/>
prefix mainonto: <urn:stardog:drugs:>
prefix db: <https://go.drugbank.com/drugs/>

CONSTRUCT {
    
    ?drugB rdfs:label ?name ;
           a mainonto:Drug ;
           mainonto:has_drugbank_id ?drugBankId.
    
    ?drugBankId rdfs:label ?drugBidString; a mainonto:id .
    
    ?drugB mainonto:has_description ?drugBdesc .
    
    ?drugBdesc rdfs:label ?description ; a mainonto:description .
               
    ?drugB mainonto:ASSOCIATED_WITH ?targetB  .
    ?targetB a mainonto:Protein ;
             rdfs:label ?targetString ;
             mainonto:has_uniprot_id ?targetBId.    

    ?drugB mainonto:ANNOTATED_IN_PATHWAY ?pathwayB .
    ?pathwayB a mainonto:Pathway ;
              rdfs:label ?pathwayString ;
              mainonto:has_smpdb_id ?pathwayBId.
           
    ?drugB mainonto:has_group ?drugBgroup .
    ?drugBgroup a mainonto:group ; rdf:value ?groupB . 
           
    ?drugB  mainonto:has_kingdom ?drugBking .
    ?drugBking rdfs:label ?kingdom ; a mainonto:kingdom .
    
    ?drugB  mainonto:has_superclass ?drugBsuperclass .
    ?drugBsuperclass rdfs:label ?superclass ; a mainonto:superclass .
    
    ?drugB mainonto:has_class ?drugBclass .
    ?drugBclass rdfs:label ?class ; a mainonto:class .
      
    ?drugB mainonto:has_subclass ?drugBsubclass .
    ?drugBsubclass rdfs:label ?subclass ; a mainonto:subclass .
    
    ?drugB mainonto:has_indication ?drugBindication .
    ?drugBindication rdfs:label ?indication ; a mainonto:indication .
    
    ?drugB mainonto:has_pharmacodynamics ?drugBpharmacodynamics .
    ?drugBpharmacodynamics rdfs:label ?pharmacodinamics ; a mainonto:pharmacodynamics .
    
    ?drugB mainonto:has_toxicity ?drugBtoxicity .
    ?drugBtoxicity rdfs:label ?toxicity ; a mainonto:toxicity .
    
    ?drugB mainonto:has_absorption ?drugBabsorption .
    ?drugBabsorption rdfs:label ?absorption ; a mainonto:absorption .
        
}

FROM stardog:context:all
{

?drug dsch:name ?name ; a dsch:Drug ;
      dsch:groups ?group .

      OPTIONAL {?drug dsch:description ?description }
      OPTIONAL {?drug dsch:ANNOTATED_IN_PATHWAY ?pathway .}

      OPTIONAL {?drug dsch:ASSOCIATED_WITH ?target .}

      OPTIONAL {?drug dsch:kingdom ?kingdom }
      OPTIONAL {?drug dsch:superclass ?superclass }
      OPTIONAL {?drug dsch:class ?class }
      OPTIONAL {?drug dsch:subclass ?subclass }
      OPTIONAL {?drug dsch:indication ?indication }
      OPTIONAL {?drug dsch:pharmacodynamics ?pharmacodinamics }
      OPTIONAL {?drug dsch:toxicity ?toxicity }
      OPTIONAL {?drug dsch:absorption ?absorption }
      #OPTIONAL {<<?drug dsch:INTERACTS_WITH ?otherDrug>> dsch:interaction_type ?tObj .}

BIND (IRI(replace(str(?otherDrug), str(drid:), str(db:)))  AS ?otherDrugB)

#BIND (IRI(CONCAT(str(<urn:stardog:drugs:>), str(replace(?name," ","_"))))  AS ?drugB)
BIND (IRI(CONCAT(str(<urn:stardog:drugs:>), str(replace(str(?drug), str(drid:DB), str("")))))  AS ?drugB)


BIND (IRI(replace(str(?drug), str(drid:), str(db:)))  AS ?drugBankId)
BIND (replace(str(?drug), str(drid:), str(""))  AS ?drugBidString)

BIND (replace(str(?pathway), str(drid:), str("")) AS ?pathwayString)
BIND (IRI(CONCAT(str(<urn:stardog:pathway:>), str(?pathwayString)))  AS ?pathwayB)
BIND (IRI(replace(str(?pathway), str(drid:), str(pathway:)))  AS ?pathwayBId)

BIND (replace(str(?target), str(drid:), str("")) AS ?targetString)
BIND (IRI(CONCAT(str(<urn:stardog:protein:>), str(?targetString)))  AS ?targetB)
BIND (IRI(replace(str(?target), str(drid:), str(uniprot:)))  AS ?targetBId) 

BIND (IRI(replace(str(?group), str(dsch:), str(<urn:stardog:drugs:>))) AS ?groupB)





BIND(IF(exists{?drug dsch:description ?description} , IRI((CONCAT(STR( ?drugB ), "/description") )) , ?none) AS ?drugBdesc) .
BIND(IF(exists{?drug dsch:groups ?group}, IRI((CONCAT(STR( ?drugB ), "/group") )), ?none) AS ?drugBgroup ) .
BIND(IF(exists{?drug dsch:kingdom ?kingdom}, IRI((CONCAT(STR( ?drugB ), "/kingdom") )), ?none) AS ?drugBking ) .
BIND(IF(exists{?drug dsch:superclass ?superclass}, IRI((CONCAT(STR( ?drugB ), "/superclass") )), ?none) AS ?drugBsuperclass ) .
BIND(IF(exists{?drug dsch:class ?class}, IRI((CONCAT(STR( ?drugB ), "/class") )), ?none) AS ?drugBclass ) .
BIND(IF(exists{?drug dsch:subclass ?subclass}, IRI((CONCAT(STR( ?drugB ), "/subclass") )), ?none) AS ?drugBsubclass ) .
BIND(IF(exists{?drug dsch:indication ?indication}, IRI((CONCAT(STR( ?drugB ), "/indication") )), ?none) AS ?drugBindication ) .
BIND(IF(exists{?drug dsch:pharmacodynamics ?pharmacodinamics}, IRI((CONCAT(STR( ?drugB ), "/pharmacodynamics") )), ?none) AS ?drugBpharmacodynamics ) .
BIND(IF(exists{?drug dsch:toxicity ?toxicity}, IRI((CONCAT(STR( ?drugB ), "/toxicity") )), ?none) AS ?drugBtoxicity ) .
BIND(IF(exists{?drug dsch:absorption ?absorption}, IRI((CONCAT(STR( ?drugB ), "/absorption") )), ?none) AS ?drugBabsorption ) .


#VALUES ?drug {drid:DB00162}
    
}
"""
query_INTERACTIONS = """
prefix dsch: <http://schema.rdfal.co/#>
prefix db: <https://go.drugbank.com/drugs/>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix mainonto: <urn:stardog:drugs:>

CONSTRUCT {
        
         [] a mainonto:INTERACTS_WITH ;
         mainonto:int_start ?drugB ;
         mainonto:int_end ?otherDrugB ;
         mainonto:interaction_type ?tObj . 

}

FROM stardog:context:all
{

<<?drug dsch:INTERACTS_WITH ?otherDrug>> dsch:interaction_type ?tObj .

?drug dsch:name ?name .
?otherDrug dsch:name ?otherDrugName

BIND (IRI(CONCAT(str(<urn:stardog:drugs:>), str(replace(str(?otherDrug), str(drid:DB), str("")))))  AS ?otherDrugB)
BIND (IRI(CONCAT(str(<urn:stardog:drugs:>), str(replace(str(?drug), str(drid:DB), str("")))))  AS ?drugB)


#VALUES ?drug {drid:DB00162}
    
}
"""
query_RxNorm_DRUGS = """
#prefix drunt: <urn:stardog:drugs:>

CONSTRUCT
{ ?drugB <http://www.w3.org/2004/02/skos/core#prefLabel> ?drugName ;
         ?rxp ?rxo ; a <urn:stardog:drugs:Drug> ; <urn:stardog:drugs:externalId> ?drug, ?prop ;
         <http://www.geneontology.org/formats/oboInOwl#hasDbXref> ?propName ;
         rdfs:label ?stripped_title ;
         ?dronp ?drono .
  
        ?rxo <urn:stardog:drugs:externalId> ?rxoExternalId .
        ?drono <urn:stardog:drugs:externalId> ?dronoExternalId .
  
  #?rxo ?rxop ?rxoo .
  #?rxp ?rxpp ?rxpo .

  #?drono ?dronop ?dronoo .
  #?dronp ?dronpp ?dronpo .

}

FROM stardog:context:all

{

    ?drug <http://www.w3.org/2004/02/skos/core#prefLabel> ?drugName ;
          ?rxp ?rxo2 .
    
    OPTIONAL {?rxo2 a owl:Class . ?rxo2 <http://www.w3.org/2004/02/skos/core#prefLabel> ?rxoName}
    
    BIND (STR(?drugName)  AS ?stripped_title) 

    BIND(IF(exists{?rxo2 a owl:Class . ?rxo2 <http://www.w3.org/2004/02/skos/core#prefLabel> ?rxoName} , 
        IRI(CONCAT(str(<urn:stardog:drugs:>), REPLACE(STR(?rxoName)," ","_"))), ?rxo2) AS ?rxo) .
    BIND(IF(exists{?rxo2 a owl:Class . ?rxo2 <http://www.w3.org/2004/02/skos/core#prefLabel> ?rxoName} , 
        ?rxo2, ?none) AS ?rxoExternalId) .

    FILTER (?drugName != ?rxo2)

    SERVICE <db://dron>
    { GRAPH stardog:context:all 
        {

        ?prop <http://www.geneontology.org/formats/oboInOwl#hasDbXref> ?propName ;
              rdfs:label ?stripped_title ;
              ?dronp ?drono2 .
        
        OPTIONAL {?drono2 a owl:Class . ?drono2 rdfs:label ?dronoName}
        
        BIND (IRI(CONCAT(str(<urn:stardog:drugs:>), REPLACE(?stripped_title," ","_"))) AS ?drugB)

        BIND(IF(exists{?drono2 a owl:Class . ?drono2 rdfs:label ?dronoName} , 
            IRI(CONCAT(str(<urn:stardog:drugs:>), REPLACE(STR(?dronoName)," ","_"))), ?drono2) AS ?drono) .

        BIND(IF(exists{?drono2 a owl:Class . ?drono2 rdfs:label ?dronoName} , 
            ?drono2, ?none) AS ?dronoExternalId) .

        FILTER (?propName != ?drono2 && ?stripped_title != ?drono2)

        } 
    } 

}
"""
query_dron_spo = """
prefix drunt: <urn:stardog:drugs:>

CONSTRUCT {?o_A ?p ?o . ?o <http://www.w3.org/2004/02/skos/core#prefLabel> ?oName . }
#SELECT DISTINCT ?o_AexId ?p ?o
FROM stardog:context:all

{
    ?s_A ?p_A ?o_A .
    ?o_A drunt:externalId ?o_AexId
   
   
   FILTER NOT EXISTS {?o_A a owl:Class}


SERVICE <db://dron>
    { GRAPH stardog:context:all 
        {

        ?s ?p ?o .

        FILTER (?s = ?o_AexId)

        }

    }

} LIMIT 150000
"""
query_rxnorm_spo = """
#prefix drunt: <urn:stardog:drugs:>

CONSTRUCT {?o_A ?p ?o . ?o <http://www.w3.org/2004/02/skos/core#prefLabel> ?oName . }
#SELECT DISTINCT ?o_AexId ?p ?o
FROM stardog:context:all

{
    ?s_A ?p_A ?o_A .
    ?o_A <urn:stardog:drugs:externalId> ?o_AexId
   
   
   FILTER NOT EXISTS {?o_A a owl:Class}


SERVICE <db://rxnorm>
    { GRAPH stardog:context:all 
        {

        ?s ?p ?o .

        FILTER (?s = ?o_AexId)

        }

    }

} LIMIT 150000
"""


with stardog.Connection('rx-dron', **conn_details) as conn:
    exportDataDRUGS = conn.graph(query_rxnorm_spo, content_type='text/turtle', limit=150000000, timeout=0)
    file = open(fileNameSTARDRUGS_rxnormSPO, 'w+')
    file.write(exportDataDRUGS.decode("utf-8"))

    # exportData_INTERACTIONS = conn.graph(query_INTERACTIONS, content_type='text/turtle', limit=150000000, timeout=0)
    # file = open(fileNameINTERACTIONS, 'w+')
    # file.write(exportData_INTERACTIONS.decode("utf-8"))

