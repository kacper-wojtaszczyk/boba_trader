import datetime
from datetime import time

from nautilus_trader.common.clock import TestClock, LiveClock
from nautilus_trader.core.nautilus_pyo3 import OmsType
from nautilus_trader.core.rust.model import PriceType, AggregationSource
from nautilus_trader.indicators.average.moving_average import MovingAverageType
from nautilus_trader.indicators.average.sma import SimpleMovingAverage
from nautilus_trader.model.data import Bar, BarType, BarSpecification, BarAggregation
from nautilus_trader.model.identifiers import TraderId, InstrumentId, ClientId
from nautilus_trader.model.objects import Price, Quantity
from nautilus_trader.test_kit.stubs.component import TestComponentStubs
from nautilus_trader.test_kit.stubs.identifiers import TestIdStubs

from strategy.moving_avarages_neural_network.config import MovingAveragesNeuralNetworkConfig
from strategy.moving_avarages_neural_network.strategy import MovingAveragesNeuralNetworkStrategy


class TestClass:
    def test_init(self) -> None:
        instrument_id: str = "EURUSD.IG"
        stop_loss: int = 1
        take_profit: int = 1
        trailing_stop: int = 1
        trailing_step: int = 1
        volume: float = 1
        open_positions_limit: int = 5
        ma_type: MovingAverageType = MovingAverageType.SIMPLE
        h1_ma_period: int = 1
        h4_ma_period: int = 2
        d1_ma_period: int = 3
        p1: float = 0.1
        p2: float = 0.1
        p3: float = 0.1
        q1: float = 0.1
        q2: float = 0.1
        q3: float = 0.1
        k1: float = 0.1
        k2: float = 0.1
        k3: float = 0.1
        start_time: time = time()
        end_time: time = time()

        strategy: MovingAveragesNeuralNetworkStrategy = self.get_strategy(
            instrument_id,
            stop_loss,
            take_profit,
            trailing_stop,
            trailing_step,
            volume,
            open_positions_limit,
            ma_type,
            h1_ma_period,
            h4_ma_period,
            d1_ma_period,
            p1,
            p2,
            p3,
            q1,
            q2,
            q3,
            k1,
            k2,
            k3,
            start_time,
            end_time,
        )

        assert isinstance(strategy, MovingAveragesNeuralNetworkStrategy)
        assert instrument_id == strategy.instrument_id.value
        assert stop_loss == strategy.stop_loss
        assert take_profit == strategy.take_profit
        assert trailing_stop == strategy.trailing_stop
        assert trailing_step == strategy.trailing_step
        assert volume == strategy.volume
        assert open_positions_limit == strategy.open_positions_limit
        assert isinstance(strategy.h1_ma_indicator, SimpleMovingAverage)
        assert isinstance(strategy.h4_ma_indicator, SimpleMovingAverage)
        assert isinstance(strategy.d1_ma_indicator, SimpleMovingAverage)
        assert h1_ma_period == strategy.h1_ma_indicator.period
        assert h4_ma_period == strategy.h4_ma_indicator.period
        assert d1_ma_period == strategy.d1_ma_indicator.period
        assert p1 == strategy.p1
        assert p2 == strategy.p2
        assert p3 == strategy.p3
        assert q1 == strategy.q1
        assert q2 == strategy.q2
        assert q3 == strategy.q3
        assert k1 == strategy.k1
        assert k2 == strategy.k2
        assert k3 == strategy.k3
        assert start_time == strategy.start_time
        assert end_time == strategy.end_time

    def test_on_start(self) -> None:
        h1_ma_period: int = 1
        h4_ma_period: int = 2
        d1_ma_period: int = 3
        strategy: MovingAveragesNeuralNetworkStrategy = self.get_strategy(
            h1_ma_period=h1_ma_period, h4_ma_period=h4_ma_period, d1_ma_period=d1_ma_period
        )

        strategy.start()

        assert 3 == len(strategy.registered_indicators)
        assert h1_ma_period == strategy.registered_indicators[0].period
        assert h4_ma_period == strategy.registered_indicators[1].period
        assert d1_ma_period == strategy.registered_indicators[2].period

    def test_on_bar(self) -> None:
        instrument_id: str = "EURUSD.IG"
        strategy: MovingAveragesNeuralNetworkStrategy = self.get_strategy()
        strategy.start()
        for i in range(48):
            bar = Bar(
                BarType(
                    InstrumentId.from_str(instrument_id),
                    BarSpecification(1, BarAggregation.HOUR, PriceType.MID),
                    AggregationSource.EXTERNAL,
                ),
                Price(1.075, 5),
                Price(1.076, 5),
                Price(1.073, 5),
                Price(1.074, 5),
                Quantity(1000, 0),
                self.clock.timestamp_ns(),
                self.clock.timestamp_ns(),
            )
            strategy.handle_bar(bar)
            self.clock.advance_time(self.clock.timestamp_ns() + 1000000000 * 60 * 60)

        assert True

    def get_strategy(
        self,
        instrument_id: str = "EURUSD.IG",
        stop_loss: int = 1,
        take_profit: int = 1,
        trailing_stop: int = 1,
        trailing_step: int = 1,
        volume: float = 1,
        open_positions_limit: int = 5,
        ma_type: MovingAverageType = MovingAverageType.SIMPLE,
        h1_ma_period: int = 1,
        h4_ma_period: int = 1,
        d1_ma_period: int = 1,
        p1: float = 0.1,
        p2: float = 0.1,
        p3: float = 0.1,
        q1: float = 0.1,
        q2: float = 0.1,
        q3: float = 0.1,
        k1: float = 0.1,
        k2: float = 0.1,
        k3: float = 0.1,
        start_time: time = time(22),
        end_time: time = time(2),
    ) -> MovingAveragesNeuralNetworkStrategy:
        self.clock = TestClock()
        self.clock.set_time(1672567200000000000)

        strategy: MovingAveragesNeuralNetworkStrategy = MovingAveragesNeuralNetworkStrategy(
            MovingAveragesNeuralNetworkConfig(
                instrument_id=instrument_id,
                stop_loss=stop_loss,
                take_profit=take_profit,
                trailing_stop=trailing_stop,
                trailing_step=trailing_step,
                volume=volume,
                open_positions_limit=open_positions_limit,
                ma_type=ma_type,
                h1_ma_period=h1_ma_period,
                h4_ma_period=h4_ma_period,
                d1_ma_period=d1_ma_period,
                p1=p1,
                p2=p2,
                p3=p3,
                q1=q1,
                q2=q2,
                q3=q3,
                k1=k1,
                k2=k2,
                k3=k3,
                start_time=start_time,
                end_time=end_time,
                external_order_claims=None,
                manage_contingent_orders=False,
                manage_gtd_expiry=False,
                oms_type=OmsType.HEDGING,
                order_id_tag="100001",
                strategy_id="MovingAveragesNeuralNetworkStrategy",
            )
        )

        strategy.register(
            TraderId("TESTER-000"),
            TestComponentStubs.portfolio(),
            TestComponentStubs.msgbus(),
            TestComponentStubs.cache(),
            self.clock,
            TestComponentStubs.logger(),
        )

        return strategy
