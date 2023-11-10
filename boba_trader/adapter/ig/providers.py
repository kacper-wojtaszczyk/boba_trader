from typing import Optional

from nautilus_trader.common.providers import InstrumentProvider
from nautilus_trader.model.identifiers import InstrumentId


class FxcmInstrumentProvider(InstrumentProvider):
    """
    An example template of an ``InstrumentProvider`` showing the minimal methods which
    must be implemented for an integration to be complete.
    """

    async def load_all_async(self, filters: Optional[dict] = None) -> None:
        raise NotImplementedError("method must be implemented in the subclass")  # pragma: no cover

    async def load_ids_async(
        self,
        instrument_ids: list[InstrumentId],
        filters: Optional[dict] = None,
    ) -> None:
        raise NotImplementedError("method must be implemented in the subclass")  # pragma: no cover

    async def load_async(self, instrument_id: InstrumentId, filters: Optional[dict] = None):
        raise NotImplementedError("method must be implemented in the subclass")  # pragma: no cover
