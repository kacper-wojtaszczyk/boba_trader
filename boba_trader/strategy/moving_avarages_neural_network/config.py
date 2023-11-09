from datetime import time

from nautilus_trader.indicators.average.moving_average import MovingAverageType
from nautilus_trader.trading.strategy import StrategyConfig


class MovingAveragesNeuralNetworkConfig(StrategyConfig):
    stop_loss: int
    take_profit: int
    trailing_stop: int
    trailing_step: int
    volume: int
    open_positions_limit: int
    ma_type: MovingAverageType
    h1_ma_period: int
    h1_ma_shift: int
    h4_ma_period: int
    h4_ma_shift: int
    d1_ma_period: int
    d1_ma_shift: int
    p1: float
    p2: float
    p3: float
    q1: float
    q2: float
    q3: float
    k1: float
    k2: float
    k3: float
    start_time: time
    end_time: time
