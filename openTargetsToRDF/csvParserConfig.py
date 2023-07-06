from rdflib import Literal

lit="C=CCNc1c(O)cc2c(O)c1C[C@@H](C)C[C@H](OC)[C@H](O)[C@@H](C)/C=C(\C)[C@H](OC(N)=O)[C@@H](OC)/C=C\C=C(/C)C(=O)N2.Cl"

print(Literal(lit))