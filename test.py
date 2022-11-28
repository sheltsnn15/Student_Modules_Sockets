my_dictionary_v1 = {
    "SOFT8023": [["lo1", "lo2", "lo3"], ["prog1", "prog2"], ["assess1", "assess2"]],
    "SOFT8009": [["lo1", "lo2", "lo3"], ["prog1", "prog2"], ["assess1", "assess2"]]
}

my_dictionary_v2 = {
    "SOFT8023": {
        "learning_outcomes": ["lo1", "lo2", "lo3"],
        "assessments": ["prog1", "prog2"],
        "programmes": ["assess1", "assess2"]
    },
    "SOFT8009": {
        "learning_outcomes": ["lo1", "lo2", "lo3"],
        "assessments": ["prog1", "prog2"],
        "programmes": ["assess1", "assess2"]
    }
}

print(my_dictionary_v1.get("SOFT8023")[0][0])
print(my_dictionary_v2.get("SOFT8009").get("learning_outcomes")[0])
