from nautilus_trader.trading import Strategy

from strategy.moving_avarages_neural_network.config import (
    MovingAveragesNeuralNetworkConfig,
)


class MovingAveragesNeuralNetworkStrategy(Strategy):
    def __init__(self, config: MovingAveragesNeuralNetworkConfig) -> None:
        super().__init__(config)

    def on_start(self):
        pass
