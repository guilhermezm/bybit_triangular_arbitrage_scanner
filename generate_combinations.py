import json
import requests

def get_symbols():
    response = requests.get("https://api.bitget.com/api/v2/spot/public/symbols")
    response.raise_for_status()  # Raise an exception for bad status codes
    return response.json()

# Function to generate combinations
def generate_combinations(api_response):
    trading_pairs = [pair for pair in api_response.get('data') if pair['status'] == 'online']
    combinations = []
    passed = False

    for pair_a in trading_pairs:

        for pair_b in trading_pairs:

            if (pair_a['quoteCoin'] == pair_b['baseCoin'] or pair_a['quoteCoin'] == pair_b['quoteCoin'] or pair_a['baseCoin'] == pair_b['baseCoin'] or pair_a['baseCoin'] == pair_b['quoteCoin']) and pair_a != pair_b:

                for pair_c in trading_pairs:

                    if pair_a['baseCoin'] == pair_b['baseCoin']:
                        if (pair_c['baseCoin'] == pair_a['quoteCoin'] and pair_c['quoteCoin'] == pair_b['quoteCoin']):
                            operation = "BSB"
                            type = "baba"
                            initial = pair_a['quoteCoin']
                            intermediary = pair_b['quoteCoin']
                            final = pair_c['baseCoin']
                            passed = True
                        elif (pair_c['quoteCoin'] == pair_a['quoteCoin'] and pair_c['baseCoin'] == pair_b['quoteCoin']):
                            operation = "BSS"
                            type = "baba"
                            initial = pair_a['quoteCoin']
                            intermediary = pair_b['quoteCoin']
                            final = pair_c['quoteCoin']
                            passed = True

                    elif pair_a['baseCoin'] == pair_b['quoteCoin']:
                        if (pair_c['baseCoin'] == pair_a['quoteCoin'] and pair_c['quoteCoin'] == pair_b['baseCoin']):
                            operation = "BBB"
                            type = "baquo"
                            initial = pair_a['quoteCoin']
                            intermediary = pair_b['baseCoin']
                            final = pair_c['baseCoin']
                            passed = True
                        elif (pair_c['quoteCoin'] == pair_a['quoteCoin'] and pair_c['baseCoin'] == pair_b['baseCoin']):
                            operation = "BBS"
                            type = "baquo"
                            initial = pair_a['quoteCoin']
                            intermediary = pair_b['baseCoin']
                            final = pair_c['quoteCoin']
                            passed = True

                    elif pair_a['quoteCoin'] == pair_b['baseCoin']:
                        if (pair_c['baseCoin'] == pair_a['baseCoin'] and pair_c['quoteCoin'] == pair_b['quoteCoin']):
                            operation = "SSB"
                            type = "quoba"
                            initial = pair_a['baseCoin']
                            intermediary = pair_b['quoteCoin']
                            final = pair_c['baseCoin']
                            passed = True
                        elif (pair_c['quoteCoin'] == pair_a['baseCoin'] and pair_c['baseCoin'] == pair_b['quoteCoin']):
                            operation = "SSS"
                            type = "quoba"
                            initial = pair_a['baseCoin']
                            intermediary = pair_b['quoteCoin']
                            final = pair_c['quoteCoin']
                            passed = True

                    elif pair_a['quoteCoin'] == pair_b['quoteCoin']:
                        if (pair_c['baseCoin'] == pair_a['baseCoin'] and pair_c['quoteCoin'] == pair_b['baseCoin']):
                            operation = "SBB"
                            type = "quoquo"
                            initial = pair_a['baseCoin']
                            intermediary = pair_b['baseCoin']
                            final = pair_c['baseCoin']
                            passed = True
                        elif (pair_c['quoteCoin'] == pair_a['baseCoin'] and pair_c['baseCoin'] == pair_b['baseCoin']):
                            operation = "SBS"
                            type = "quoquo"
                            initial = pair_a['baseCoin']
                            intermediary = pair_b['baseCoin']
                            final = pair_c['quoteCoin']
                            passed = True

                    if passed:

                        match_dict = {
                            "n": len(combinations) + 1,
                            "type": type,
                            "operation": operation,
                            "initial": initial,
                            "final": final,
                            "intermediary": intermediary,
                            "a_base": pair_a['baseCoin'],
                            "a_quote": pair_a['quoteCoin'],
                            "a_symbol": pair_a['symbol'],
                            "b_base": pair_b['baseCoin'],
                            "b_quote": pair_b['quoteCoin'],
                            "b_symbol": pair_b['symbol'],
                            "c_base": pair_c['baseCoin'],
                            "c_quote": pair_c['quoteCoin'],
                            "c_symbol": pair_c['symbol'],
                            "combined": [pair_a['symbol'], pair_b['symbol'], pair_c['symbol']]
                        }
                        combinations.append(match_dict)
    return combinations

# Function to save combinations to a JSON file
def save_combinations_to_json(combinations, filename):
    with open(filename, 'w') as json_file:
        json.dump(combinations, json_file, indent=4)

# Main code to fetch data, generate combinations, and save to JSON
api_response = get_symbols()  # Fetch trading pairs from the API
combinations = generate_combinations(api_response)
save_combinations_to_json(combinations, 'combinations.json')
print(f"Combinations saved to 'combinations.json'")
