from datetime import time

from nautilus_trader.core.rust.common import LogColor
from nautilus_trader.core.rust.model import PriceType, AggregationSource, OrderSide
from nautilus_trader.indicators.average.ma_factory import MovingAverageFactory
from nautilus_trader.indicators.average.moving_average import MovingAverage
from nautilus_trader.model.data import BarType, BarSpecification, BarAggregation, Bar
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.trading import Strategy

from strategy.moving_avarages_neural_network.config import MovingAveragesNeuralNetworkConfig


class MovingAveragesNeuralNetworkStrategy(Strategy):
    def __init__(self, config: MovingAveragesNeuralNetworkConfig) -> None:
        super().__init__(config)

        ma_factory = MovingAverageFactory()

        self.instrument_id: InstrumentId = InstrumentId.from_str(config.instrument_id)
        self.stop_loss: int = config.stop_loss
        self.take_profit: int = config.take_profit
        self.trailing_stop: int = config.trailing_stop
        self.trailing_step: int = config.trailing_step
        self.volume: float = config.volume
        self.open_positions_limit: int = config.open_positions_limit
        self.p1: float = config.p1
        self.p2: float = config.p2
        self.p3: float = config.p3
        self.q1: float = config.q1
        self.q2: float = config.q2
        self.q3: float = config.q3
        self.k1: float = config.k1
        self.k2: float = config.k2
        self.k3: float = config.k3
        self.start_time: time = config.start_time
        self.end_time: time = config.end_time
        self.h1_ma_indicator: MovingAverage = ma_factory.create(config.h1_ma_period, config.ma_type)
        self.h4_ma_indicator: MovingAverage = ma_factory.create(config.h4_ma_period, config.ma_type)
        self.d1_ma_indicator: MovingAverage = ma_factory.create(config.d1_ma_period, config.ma_type)

    def on_start(self) -> None:
        self.register_indicator_for_bars(
            BarType(
                self.instrument_id, BarSpecification(1, BarAggregation.HOUR, PriceType.MID), AggregationSource.EXTERNAL
            ),
            self.h1_ma_indicator,
        )
        self.register_indicator_for_bars(
            BarType(
                self.instrument_id, BarSpecification(4, BarAggregation.HOUR, PriceType.MID), AggregationSource.EXTERNAL
            ),
            self.h4_ma_indicator,
        )
        self.register_indicator_for_bars(
            BarType(
                self.instrument_id, BarSpecification(1, BarAggregation.DAY, PriceType.MID), AggregationSource.EXTERNAL
            ),
            self.d1_ma_indicator,
        )

    def on_stop(self) -> None:
        self.cancel_all_orders(self.instrument_id)

    def on_bar(self, bar: Bar) -> None:
        if not self.indicators_initialized():
            self.log.info(
                f"Waiting for indicators to warm up",
                color=LogColor.BLUE,
            )
            return  # Wait for indicators to warm up...

        if bar.is_single_price():
            # Implies no market information for this bar
            return
        if self.end_time < self.clock.utc_now().time < self.start_time:
            return

        h1_value: float = self.h1_ma_indicator.value
        h4_value: float = self.h4_ma_indicator.value
        d1_value: float = self.d1_ma_indicator.value

        n1: float = h1_value * self.p1
        n2: float = h4_value * self.q1
        n3: float = d1_value * self.k1

        if n1 > 0.0 and n2 > 0.0 and n3 > 0.0:
            self.submit_order(
                self.order_factory.market(
                    instrument_id=self.instrument_id,
                    order_side=OrderSide.BUY,
                    quantity=self.volume,
                )
            )
        if n1 > 0.0 and n2 < 0.0 and n3 < 0.0:
            self.submit_order(
                self.order_factory.market(
                    instrument_id=self.instrument_id,
                    order_side=OrderSide.SELL,
                    quantity=self.volume,
                )
            )
