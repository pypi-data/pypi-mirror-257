from dicee import KGE
model_byte = KGE(path="Experiments/2024-02-06 14-38-33.916157")

triples = [("concept_mlconference_nyc", "concept:atdate", "concept_date_n2000"),
           ("concept_transportation_increase", "concept:atdate", "concept_dateliteral_n2006"),
           ("concept_city_nj", "concept:locationlocatedwithinlocation", "concept_country_usa"),
          ("concept_aiconference_nyc", "concept:atdate", "concept_date_n2000"),
           ("concept_transportation_decrease", "concept:atdate", "concept_dateliteral_n2024"),
           ("concept_city_nj", "concept:locationlocatedwithinlocation", "concept_countryusa")
           ]

for (h, r, t) in triples:
    print(h, r, t)
    try:
        print("Keci", model.predict(h=h, r=r, t=t))
    except KeyError as e:
        print("Cannot compute score")
    print("Inductive Keci", model_byte.predict(h=h, r=r, t=t))
    print()
