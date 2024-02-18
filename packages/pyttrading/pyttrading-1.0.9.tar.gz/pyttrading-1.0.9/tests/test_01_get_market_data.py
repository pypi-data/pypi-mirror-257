

import pyttrading as pytrade
from pyttrading.models import ExperimentMessage


def test_get_market_data(pass_test :bool = False):
    data = pytrade.get_market_data_from_playground(symbols=['TNA'], is_crypto=False)

    if len(data) > 200:
        pass_test = True
        
    assert pass_test
    
def test_get_market_crypto(pass_test :bool = False):
    pass_test = False
    data = pytrade.get_market_data_from_playground(symbols=['AVAX/USD'], is_crypto=True)

    if len(data) > 200:
        pass_test = True

    assert pass_test