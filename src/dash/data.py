import sys
sys.path.append('..')
from consumer.api_consumer import DataLoader


dl = DataLoader()
states = dl.get_all_states_with_codes()
codes = {value: key for key, value in states.items()}
states = [{'label': key.title(), 'value': value} for key, value in states.items()]