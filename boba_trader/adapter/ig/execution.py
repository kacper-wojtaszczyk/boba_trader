from typing import Optional

import pandas as pd

from nautilus_trader.execution.messages import CancelAllOrders
from nautilus_trader.execution.messages import CancelOrder
from nautilus_trader.execution.messages import ModifyOrder
from nautilus_trader.execution.messages import QueryOrder
from nautilus_trader.execution.messages import SubmitOrder
from nautilus_trader.execution.messages import SubmitOrderList
from nautilus_trader.execution.reports import OrderStatusReport
from nautilus_trader.execution.reports import PositionStatusReport
from nautilus_trader.execution.reports import TradeReport
from nautilus_trader.live.execution_client import LiveExecutionClient
from nautilus_trader.model.identifiers import ClientOrderId
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.model.identifiers import VenueOrderId


class FxcmLiveExecutionClient(LiveExecutionClient):
    """
    An example of a ``LiveExecutionClient`` highlighting the method requirements.

    +--------------------------------------------+-------------+
    | Method                                     | Requirement |
    +--------------------------------------------+-------------+
    | _connect                                   | required    |
    | _disconnect                                | required    |
    | reset                                      | optional    |
    | dispose                                    | optional    |
    +--------------------------------------------+-------------+
    | _submit_order                              | required    |
    | _submit_order_list                         | required    |
    | _modify_order                              | required    |
    | _cancel_order                              | required    |
    | _cancel_all_orders                         | required    |
    | generate_order_status_report               | required    |
    | generate_order_status_reports              | required    |
    | generate_trade_reports                     | required    |
    | generate_position_status_reports           | required    |
    +--------------------------------------------+-------------+

    """

    async def _connect(self) -> None:
        raise NotImplementedError("method must be implemented in the subclass")  # pragma: no cover

    async def _disconnect(self) -> None:
        raise NotImplementedError("method must be implemented in the subclass")  # pragma: no cover

    def reset(self) -> None:
        raise NotImplementedError("method must be implemented in the subclass")  # pragma: no cover

    def dispose(self) -> None:
        raise NotImplementedError("method must be implemented in the subclass")  # pragma: no cover

    # -- EXECUTION REPORTS ------------------------------------------------------------------------

    async def generate_order_status_report(
        self,
        instrument_id: InstrumentId,
        client_order_id: Optional[ClientOrderId] = None,
        venue_order_id: Optional[VenueOrderId] = None,
    ) -> Optional[OrderStatusReport]:
        raise NotImplementedError("method must be implemented in the subclass")  # pragma: no cover

    async def generate_order_status_reports(
        self,
        instrument_id: Optional[InstrumentId] = None,
        start: Optional[pd.Timestamp] = None,
        end: Optional[pd.Timestamp] = None,
        open_only: bool = False,
    ) -> list[OrderStatusReport]:
        raise NotImplementedError("method must be implemented in the subclass")  # pragma: no cover

    async def generate_trade_reports(
        self,
        instrument_id: Optional[InstrumentId] = None,
        venue_order_id: Optional[VenueOrderId] = None,
        start: Optional[pd.Timestamp] = None,
        end: Optional[pd.Timestamp] = None,
    ) -> list[TradeReport]:
        raise NotImplementedError("method must be implemented in the subclass")  # pragma: no cover

    async def generate_position_status_reports(
        self,
        instrument_id: Optional[InstrumentId] = None,
        start: Optional[pd.Timestamp] = None,
        end: Optional[pd.Timestamp] = None,
    ) -> list[PositionStatusReport]:
        raise NotImplementedError("method must be implemented in the subclass")  # pragma: no cover

    # -- COMMAND HANDLERS -------------------------------------------------------------------------

    async def _submit_order(self, command: SubmitOrder) -> None:
        raise NotImplementedError("method must be implemented in the subclass")  # pragma: no cover

    async def _submit_order_list(self, command: SubmitOrderList) -> None:
        raise NotImplementedError("method must be implemented in the subclass")  # pragma: no cover

    async def _modify_order(self, command: ModifyOrder) -> None:
        raise NotImplementedError("method must be implemented in the subclass")  # pragma: no cover

    async def _cancel_order(self, command: CancelOrder) -> None:
        raise NotImplementedError("method must be implemented in the subclass")  # pragma: no cover

    async def _cancel_all_orders(self, command: CancelAllOrders) -> None:
        raise NotImplementedError("method must be implemented in the subclass")  # pragma: no cover

    async def _query_order(self, command: QueryOrder) -> None:
        raise NotImplementedError("method must be implemented in the subclass")  # pragma: no cover
