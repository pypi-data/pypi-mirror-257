def list_overlap(list1: list[str], list2: list[str], threshold: float) -> bool:
    if list2:
        overlap = len(set(list1).intersection(set(list2))) / len(list1)
        if overlap >= threshold:
            return True
        else:
            return False
    else:
        return False
    
def list_overlap2(list1: list[int], list2: list[int], threshold: int) -> bool:
    if list2:
        overlap = len(set(list1).intersection(set(list2)))
        if overlap >= threshold:
            return True
        else:
            return False
    else:
        return False

def find_best_address(suburb_name, street_name, number):
    df_temp = db.execute(f"select * from addrtext_with_detail where suburb='{suburb_name}'").df()
    results = df_temp.query(f"addr.str.contains('{street_name}')").query(f"addr.str.contains('{number}')")
    return results

# remove building name from addresses
import polars as pl 

df = pl.read_csv('/home/alex/Desktop/Data/gnaf_nov2023/GNAF_CORE.psv', separator='|', infer_schema_length=10000)

def get_string_length_blah(text):
    if text:
        return len(text)
    else:
        return 0
    
# remove
# load up the course file and remove all the building names from addresses which have them
df = pl.scan_csv('/home/alex/Desktop/Data/gnaf_nov2023/GNAF_CORE.psv', 
                 separator='|', 
                 infer_schema_length=10000)

df = df.with_column(
    df['BUILDING_NAME'].apply(lambda s, a: leng, args=[df['length_column']]).alias('new_column_name')
)

df = df.with_columns(
    df['ADDRESS_LABEL'].apply(lambda s, length: s[length:], args=[df['BUILDING_NAME'].str.lengths()]).alias('new_column_name')
)

df = df.with_columns(
    df['BUILDING_NAME'].apply(lambda s: get_string_length_blah(s), skip_nulls=False).alias('BUILDING_NAME_length')
)

df = df.with_columns(
    df.select(pl.col('BUILDING_NAME').apply(lambda s: get_string_length_blah(s), skip_nulls=False).alias('BUILDING_NAME_length'))
)

df2 = pl.read_csv('/home/alex/Desktop/Data/gnaf_nov2023/gnafid_to_building_name.csv')
df = df.join(df2, left_on='ADDRESS_DETAIL_PID', right_on='ADDRESS_DETAIL_PID', how='left')

## to do: fix up cases where span incorrect
# fix up where number doesn't exist but find closest
# fix up where suburb incorrect but a neighbouring one matches
# include letters in street number
# remove the place name from the address to get better matching

from whereabouts.Matcher import Matcher
from whereabouts.MatcherPipeline import MatcherPipeline
from whereabouts.utils import order_matches, get_unmatched

addresses = ['37a rathmine st fairifeld', 
             '4/19 rathimines st fairifield', 
             '34/121 exhibiotin st melbouren', 
             '13 wikns st burwood east']

matcher1 = Matcher('gnaf_vic', how='standard')
matcher2 = Matcher('gnaf_vic', how='trigram')

matchers = [matcher1, matcher2]

pipeline = MatcherPipeline(matchers)

results = pipeline.geocode(addresses)

jaro_similarity(t2.address, t3.addr) * numeric_overlap(t2.numeric_tokens, t3.numeric_tokens)

def list_overlap(list1: list[str], list2: list[str], threshold: float) -> bool:
    if list2:
        overlap = len(set(list1).intersection(set(list2))) / len(list1)
        if overlap >= threshold:
            return True
        else:
            return False
    else:
        return False
    
def numeric_overlap(input_numerics: list[str], 
                    candidate_numerics: list[str]) -> float:
    num_overlap = len(set(input_numerics).intersection(set(candidate_numerics)))
    fraction_overlap = num_overlap / len(set(input_numerics))
    return fraction_overlap

def bigram_jaccard(input_address: str, candidate_address: str) -> float:
    # bigrams
    bigrams_input = [input_address[n:n+2] for n in range(0, len(input_address) - 1)]
    bigrams_candidate = [candidate_address[n:n+2] for n in range(0, len(candidate_address) - 1)]
    # unigrams
    unigrams_input = [input_address[n:n+1] for n in range(0, len(input_address))]
    unigrams_candidate = [candidate_address[n:n+1] for n in range(0, len(candidate_address))]
    ngrams_input_set = set(bigrams_input).union(unigrams_input)
    ngrams_candidate_set = set(bigrams_candidate).union(unigrams_candidate)
    return len(ngrams_input_set.intersection(ngrams_candidate_set)) / len(ngrams_input_set.union(ngrams_candidate_set))

db.create_function('list_overlap', list_overlap)
db.create_function('numeric_overlap', numeric_overlap)
db.create_function('ngram_jaccard', bigram_jaccard)

test1 = '7/26 LEONARD STREET ASCOT VALUE'
test2 = 'UNIT 7 26 BEAUREPAIRE PDE FOOTSCRAY VIC 3011'
test3 = 'UNIT 7 26 LEONARD CR ASCOT VALE VIC 3032'
