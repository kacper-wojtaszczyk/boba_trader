from strategy.moving_avarages_neural_network.config import (
    MovingAveragesNeuralNetworkConfig,
)
from strategy.moving_avarages_neural_network.strategy import (
    MovingAveragesNeuralNetworkStrategy,
)


class TestClass:
    def test_one(self) -> None:
        strategy = MovingAveragesNeuralNetworkStrategy(
            MovingAveragesNeuralNetworkConfig(stop_loss=1, take_profit=1)
        )
        assert isinstance(strategy, MovingAveragesNeuralNetworkStrategy)
