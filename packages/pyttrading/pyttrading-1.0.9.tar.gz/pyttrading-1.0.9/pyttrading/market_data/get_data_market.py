from .opensearch_collector import OpensearchCollector
import os

def get_market_data_from_playground(
        symbols: list = ['TNA', 'SPY'],
        opensearch_host :str = os.getenv('URL_OPENSEARCH', 'http://localhost:9200'),
        playground_host :str = os.getenv('URL_PLAYGROUND', 'http://localhost:5001'), 
        start_date :str = '9/1/2023', 
        end_date: str = '1/5/2024',
        interval: str = "1h",
        is_crypto: bool = False
    ):

    collector = OpensearchCollector(
            url_opensearch=opensearch_host,
            url_playground=playground_host,
    )

    data =  collector.market_data(
            symbols=symbols,
            start_date=start_date,
            end_date=end_date,
            interval=interval, 
            is_crypto=is_crypto
        )

    return data