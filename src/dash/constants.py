column_dt = {
    'delta.confirmed': 'Daily Confimed Cases',
    'delta7.confirmed': 'Daily Confirmed Cases (7 Day Average)',
    'total.confirmed': 'Total Confirmed Cases',
    'delta.recovered': 'Daily Recovered',
    'delta7.recovered': 'Daily Recovered (7 Day Average)',
    'total.recovered': 'Total Recovered', 
    'delta.deceased': 'Daily Deceased', 
    'delta.tested': 'Daily Tested',
    'delta7.deceased': 'Daily Deceased (7 Day Average)',
    'delta7.tested': 'Daily Tested (7 Day Average)',
    'total.deceased': 'Total Deceased',
    'total.tested': 'Total Tested',
    'delta.other': 'Daily (Other)',
    'delta7.other': 'Daily (Other) (7 Day Average)',
    'total.other': 'Total Other',
    'delta.vaccinated1': 'Daily Vaccinated 1',
    'delta7.vaccinated1': 'Daily Vaccinated 1 (7 Day Average)',
    'total.vaccinated1': 'Total Vaccinated 1',
    'delta.vaccinated2': 'Daily Vaccinated 2',
    'delta7.vaccinated2': 'Daily Vaccinated 2 (7 Day Average)',
    'total.vaccinated2': 'Total Vaccinated 2',
    # 'delta.tpr': 'Test Positivity Rate (%)',
    # 'delta.cfr': 'Case Fatality Rate (%)'
}

dt_column = {
    v: k for k, v in column_dt.items()
}

dt_column_dd = [{
    'label': value, 'value': key
} for key, value in column_dt.items()]