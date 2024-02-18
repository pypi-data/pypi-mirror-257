from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict
import uuid
from config import Config 
config = Config()
import pyttrading as pytrade


start_date, end_date, now_ny =  pytrade.utils.get_datetime_now_trade(delay_minutes=int(config.delay_minutes))

class Trade(BaseModel):
    symbol: str = "TNA"
    start_date: str = str(start_date)
    end_date: str = str(end_date)
    is_crypto: bool = False
    interval: str = '4h'
    time_amount: int = 10
    indicators: list = [
                        "boll_ub",
                        "boll_lb",
                        "close_10_sma",
                        "close_12_ema",
                        "close_16_ema"
                        ]

db: Dict[int, Trade] = {}

class ExperimentMessage(Trade):
    tag: str = "algo"
    intervals: list = [
        '1h',
        '2h',
        '4h',
        '6h',
        '8h',
    ]
    start_date: str = '9/1/2023'
    end_date: str = '1/5/2024'
    strategies_list: list = [
        'rsi',
        'sma',
        'dummy',
        'ema'
    ]