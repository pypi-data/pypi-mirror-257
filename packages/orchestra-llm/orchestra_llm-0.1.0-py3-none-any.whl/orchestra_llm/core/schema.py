# from pydantic import BaseModel
from langchain_core.load.serializable import Serializable
from abc import ABC
from typing import Any, List

# class Schema(BaseModel, ABC):
    

#     def __init__(self, **kwargs: Any) -> None:
#         super().__init__(**kwargs)


#     def to_json(self) -> dict:

#         lc_kwargs = {
#             k: getattr(self, k, v)
#             for k, v in self._lc_kwargs.items()
#             if not (self.__exclude_fields__ or {}).get(k, False)  # type: ignore
#         }

#         return lc_kwargs

class RouteSchema(Serializable):

    path: str
    composer: Any
    input_schema: Any
    name: str

    def __init__(self, **kwargs: Any) -> None:
        """Pass page_content in as positional or named arg."""
        super().__init__(**kwargs)

    @classmethod
    def is_lc_serializable(cls) -> bool:
        """Return whether this class is serializable."""
        return True

    @classmethod
    def get_lc_namespace(cls) -> List[str]:
        """Get the namespace of the langchain object."""
        return ["langchain", "schema", "document"]