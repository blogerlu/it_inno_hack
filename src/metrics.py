import Levenshtein
from jellyfish import jaro_similarity, ,

def levenshtein_distance(s1: str, s2: str) -> float:
    return Levenshtein.distance(s1, s2)

def jaro_winkler_distance(s1: str, s2: str) -> float:
    return jaro_similarity(s1, s2)
