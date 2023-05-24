properties_list = [
      # Activity environmentalContributions
      {
            'type': 1,
            'name': ['Mitigation summary', 'C1'],
            'domain': ['Mitigation summary', 'B2'],
            'range': ['Mitigation summary', 'C1'],
            'property_prefix': 'has',
            'uri_prefix': ''
      },
      # Activity has bics mapping
      {
            'type': 1,
            'name': ['BICS', 'A1'],
            'domain': ['Mitigation summary', 'B2'],
            'range': ['BICS', 'A1'],
            'property_prefix': 'has',
            'uri_prefix': ''
      },
      # Activity has trbc mapping
      {
            'type': 1,
            'name': ['TRBC', 'A1'],
            'domain': ['Mitigation summary', 'B2'],
            'range': ['TRBC', 'A1'],
            'property_prefix': 'has',
            'uri_prefix': ''
      },
      # activity is part of NaceMacroSector
      {
            'type': 3,
            'name': 'is part of',
            'domain': ['Mitigation summary', 'B2'],
            'range': ['Mitigation summary', 'A2'],
            'uri_prefix': 'dc',
            'property_prefix': ''
      },
      # ClimateChangeMitigation isEnabling Boolean
      {
            'type': 2,
            'name': ['Mitigation summary', 'E3'],
            'domain': ['Mitigation summary', 'C2'],
            'range': 'xsd:boolean',
            'uri_prefix': '',
            'property_prefix': 'is'
      },
      # ClimateChangeMitigation basedOnOwnPerformance Boolean
      {
            'type': 2,
            'name': ['Mitigation summary', 'D3'],
            'domain': ['Mitigation summary', 'C2'],
            'range': 'xsd:boolean',
            'uri_prefix': '',
            'property_prefix': 'based on'
      },
      # EnvironmentalContributions hasTypeOfContribution String
      {
            'type': 2,
            'name': ['Mitigation summary', 'C3'],
            'domain': ['Mitigation summary', 'C1'],
            'range': 'xsd:string',
            'uri_prefix': '',
            'property_prefix': 'has'
      },
      # ClimateChangeMitigation isTransitionActivity Boolean
      {
            'type': 2,
            'name': ['Mitigation summary', 'F3'],
            'domain': ['Mitigation summary', 'C2'],
            'range': 'xsd:boolean',
            'uri_prefix': '',
            'property_prefix': 'is'
      },
      # Activity level2 string
      {
            'type': 2,
            'name': ['Mitigation full data', 'B2'],
            'domain': ['Mitigation summary', 'B2'],
            'range': 'xsd:string',
            'uri_prefix': '',
            'property_prefix': ''
      },
      # Activity level3 string
      {
            'type': 2,
            'name': ['Mitigation full data', 'C2'],
            'domain': ['Mitigation summary', 'B2'],
            'range': 'xsd:string',
            'uri_prefix': '',
            'property_prefix': ''
      },
      # Activity level4 string
      {
            'type': 2,
            'name': ['Mitigation full data', 'D2'],
            'domain': ['Mitigation summary', 'B2'],
            'range': 'xsd:string',
            'uri_prefix': '',
            'property_prefix': ''
      },
      # Activity description
      {
            'type': 3,
            'name': 'description',
            'domain': ['Mitigation summary', 'B2'],
            'range': 'xsd:string',
            'uri_prefix': 'dc',
            'property_prefix': ''
      },
      # Mitigation Criteria hasPrinciple string
      {
            'type': 2,
            'name': ['Mitigation full data', 'G2'],
            'domain': ['Mitigation full data', 'G1'],
            'range': 'xsd:string',
            'uri_prefix': '',
            'property_prefix': 'has'
      },
      # Mitigation Criteria hasMetric&Threshold string
      {
            'type': 2,
            'name': ['Mitigation full data', 'H2'],
            'domain': ['Mitigation full data', 'G1'],
            'range': 'xsd:string',
            'uri_prefix': '',
            'property_prefix': 'has'
      },
      # Mitigation Criteria hasRationale string
      {
            'type': 2,
            'name': ['Mitigation full data', 'I2'],
            'domain': ['Mitigation full data', 'G1'],
            'range': 'xsd:string',
            'uri_prefix': '',
            'property_prefix': 'has'
      },
      # Activity has DNSHassessment
      {
            'type': 1,
            'name': ['Mitigation full data', 'J1'],
            'domain': ['Mitigation full data', 'E2'],
            'range': ['Mitigation full data', 'J1'],
            'uri_prefix': '',
            'property_prefix': 'has'
      },
      # DNSH assessment Summary string
      {
            'type': 3,
            'name': ['Mitigation full data', 'J2'],
            'domain': ['Mitigation full data', 'J1'],
            'range': 'xsd:string',
            'uri_prefix': '',
            'property_prefix': ''
      },
      # DNSH assessment Adaptation string
      {
            'type': 2,
            'name': ['Mitigation full data', 'K2'],
            'domain': ['Mitigation full data', 'J1'],
            'range': 'xsd:string',
            'uri_prefix': '',
            'property_prefix': ''
      },
      # DNSH assessment Water string
      {
            'type': 2,
            'name': ['Mitigation full data', 'L2'],
            'domain': ['Mitigation full data', 'J1'],
            'range': 'xsd:string',
            'uri_prefix': '',
            'property_prefix': 'dnsh on'
      },
      # DNSH assessment Water based on legislation boolean
      {
            'type': 2,
            'name': ['Mitigation full data', 'M2'],
            'domain': ['Mitigation full data', 'J1'],
            'range': 'xsd:boolean',
            'uri_prefix': '',
            'property_prefix': ''
      },
      # DNSH assessment WaterRelevantRegulation string
      {
            'type': 2,
            'name': ['Mitigation full data', 'N2'],
            'domain': ['Mitigation full data', 'J1'],
            'range': 'xsd:string',
            'uri_prefix': '',
            'property_prefix': ''
      },
      # DNSH assessment Circular Economy string
      {
            'type': 2,
            'name': ['Mitigation full data', 'O2'],
            'domain': ['Mitigation full data', 'J1'],
            'range': 'xsd:string',
            'uri_prefix': '',
            'property_prefix': 'dnsh on'
      },
      # DNSH assessment circular economy based on legislation boolean
      {
            'type': 2,
            'name': ['Mitigation full data', 'P2'],
            'domain': ['Mitigation full data', 'J1'],
            'range': 'xsd:boolean',
            'uri_prefix': '',
            'property_prefix': ''
      },
      # DNSH assessment circular economyRelevantRegulation string
      {
            'type': 2,
            'name': ['Mitigation full data', 'Q2'],
            'domain': ['Mitigation full data', 'J1'],
            'range': 'xsd:string',
            'uri_prefix': '',
            'property_prefix': ''
      },
      # DNSH assessment pollution string
      {
            'type': 2,
            'name': ['Mitigation full data', 'R2'],
            'domain': ['Mitigation full data', 'J1'],
            'range': 'xsd:string',
            'uri_prefix': '',
            'property_prefix': 'dnsh on'
      },
      # DNSH assessment pollution based on legislation boolean
      {
            'type': 2,
            'name': ['Mitigation full data', 'S2'],
            'domain': ['Mitigation full data', 'J1'],
            'range': 'xsd:boolean',
            'uri_prefix': '',
            'property_prefix': ''
      },
      # DNSH assessment pollutionRelevantRegulation string
      {
            'type': 2,
            'name': ['Mitigation full data', 'T2'],
            'domain': ['Mitigation full data', 'J1'],
            'range': 'xsd:string',
            'uri_prefix': '',
            'property_prefix': ''
      },
      # DNSH assessment ecosystems string
      {
            'type': 2,
            'name': ['Mitigation full data', 'U2'],
            'domain': ['Mitigation full data', 'J1'],
            'range': 'xsd:string',
            'uri_prefix': '',
            'property_prefix': 'dnsh on'
      },
      # DNSH assessment ecosystems based on legislation boolean
      {
            'type': 2,
            'name': ['Mitigation full data', 'V2'],
            'domain': ['Mitigation full data', 'J1'],
            'range': 'xsd:boolean',
            'uri_prefix': '',
            'property_prefix': ''
      },
      # DNSH assessment ecosystemsRelevantRegulation string
      {
            'type': 2,
            'name': ['Mitigation full data', 'W2'],
            'domain': ['Mitigation full data', 'J1'],
            'range': 'xsd:string',
            'uri_prefix': '',
            'property_prefix': ''
      },
      # aCTIVITY has adaptation criteria
      {
            'type': 1,
            'name': ['Adaptation full data', 'G1'],
            'domain': ['Adaptation full data', 'E2'],
            'range': ['Adaptation full data', 'G1'],
            'uri_prefix': '',
            'property_prefix': 'has'
      },
      # Adaptation criteria has technical screening criteria string
      {
            'type': 2,
            'name': ['Adaptation full data', 'G2'],
            'domain': ['Adaptation full data', 'G1'],
            'range': 'xsd:string',
            'uri_prefix': '',
            'property_prefix': 'has'
      },
      # DNSH has mitigation information
      {
            'type': 2,
            'name': ['Adaptation full data', 'I2'],
            'domain': ['Adaptation full data', 'H1'],
            'range': 'xsd:string',
            'uri_prefix': '',
            'property_prefix': 'has'
      },
      # Adaotation screening criteria explanatio
      {
            'type': 3,
            'name': ['Adaptation screening criteria', 'B2'],
            'domain': ['Adaptation screening criteria', 'B1'],
            'range': 'xsd:string',
            'uri_prefix': '',
            'property_prefix': ''
      },
      # adaptation dc:description
      {
            'type': 3,
            'name': 'description',
            'domain': ['Adaptation screening criteria', 'B1'],
            'range': 'xsd:string',
            'uri_prefix': 'dc',
            'property_prefix': ''
      },
      # Regulation and directive title
      {
            'type': 3,
            'name': 'title',
            'domain': ['Regulation', 'A1'],
            'range': 'xsd:string',
            'uri_prefix': 'dc',
            'property_prefix': ''
      },
      # Regulation and directive comissionWebsite
      {
            'type': 2,
            'name': ['Regulation', 'C3'],
            'domain': ['Regulation', 'A1'],
            'range': 'xsd:anyURI',
            'uri_prefix': '',
            'property_prefix': ''
      },
      # Regulation and directive link
      {
            'type': 2,
            'name': ['Regulation', 'E3'],
            'domain': ['Regulation', 'A1'],
            'range': 'xsd:anyURI',
            'uri_prefix': '',
            'property_prefix': ''
      },
      # BICS mapping has bics code
      {
            'type': 2,
            'name': ['BICS', 'A2'],
            'domain': ['BICS', 'A1'],
            'range': 'xsd:string',
            'uri_prefix': '',
            'property_prefix': ''
      },
      # BICS mapping has bics name
      {
            'type': 2,
            'name': ['BICS', 'C2'],
            'domain': ['BICS', 'A1'],
            'range': 'xsd:string',
            'uri_prefix': '',
            'property_prefix': ''
      },
      # level
      {
            'type': 3,
            'name': ['BICS', 'B2'],
            'domain': ['BICS', 'A1'],
            'range': 'xsd:string',
            'uri_prefix': '',
            'property_prefix': ''
      },
      # TRBC mapping has bics NACE class
      {
            'type': 2,
            'name': ['TRBC', 'C2'],
            'domain': ['TRBC', 'A1'],
            'range': 'xsd:string',
            'uri_prefix': '',
            'property_prefix': ''
      },
      # TRBC mapping has bics NACE class
      {
            'type': 2,
            'name': ['TRBC', 'D2'],
            'domain': ['TRBC', 'A1'],
            'range': 'xsd:string',
            'uri_prefix': '',
            'property_prefix': ''
      },
      # TRBC mapping has TRBC level
      {
            'type': 2,
            'name': ['TRBC', 'E2'],
            'domain': ['TRBC', 'A1'],
            'range': 'xsd:string',
            'uri_prefix': '',
            'property_prefix': ''
      },
      # TRBC mapping has TRBC code
      {
            'type': 2,
            'name': ['TRBC', 'F2'],
            'domain': ['TRBC', 'A1'],
            'range': 'xsd:string',
            'uri_prefix': '',
            'property_prefix': ''
      },
      # TRBC mapping has TRBC description
      {
            'type': 2,
            'name': ['TRBC', 'G2'],
            'domain': ['TRBC', 'A1'],
            'range': 'xsd:string',
            'uri_prefix': '',
            'property_prefix': ''
      },
]

for property in properties_list:
    print(f'  - type: {property["type"]}\n'
          f'    name: {property["name"]}\n'
          f'    domain: {property["domain"]}\n'
          f'    range: {property["range"]}\n'
          f'    uri_prefix: {property["uri_prefix"]}\n'
          f'    property_prefix: {property["property_prefix"]}')