import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.search_state import SearchState
from ..models.v1_alpha_code import V1AlphaCode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.rpc_status import RpcStatus
    from ..models.v1_alpha_blastn import V1AlphaBlastn
    from ..models.v1_alpha_blastp import V1AlphaBlastp
    from ..models.v1_alpha_hit import V1AlphaHit
    from ..models.v1_alpha_tblastn import V1AlphaTblastn
    from ..models.v1_alpha_tblastx import V1AlphaTblastx


T = TypeVar("T", bound="V1AlphaSearch")


@_attrs_define
class V1AlphaSearch:
    """A Search of the Sequences in a Collection.

    On creation, Searches direct seqq to start a query against a Collection using a chosen `program`. On reads, Searches
    contain the results of the query, including its current `state` and any `hits`.

        Attributes:
            query (str): The sequence of nucleoties or amino acids to search the Collection for.
            name (Union[Unset, str]): The globally unique name of the Serach. Format is
                `collections/{collection_id}/searches/{search_id}`.
            code (Union[Unset, V1AlphaCode]): Code is the type of sequence.

                 - CODE_UNSPECIFIED: CODE_UNSPECIFIED is the default value.
                 - NUCLEIC: NUCLEIC is a nucleic acid sequence.
                 - PROTEIN: PROTEIN is an amino acid sequence.
            prefix (Union[Unset, str]): An optional "/" separated prefix to limit searches to.
            query_time (Union[Unset, datetime.datetime]): The time a search start is started.
            query_duration (Union[Unset, str]): The duration of a search from start to completion.
            hits (Union[Unset, List['V1AlphaHit']]): A list of hits from the Search. This is only set when `state` is
                `SUCCEEDED`.
            state (Union[Unset, SearchState]): The current state of the Search.

                 - STATE_UNSPECIFIED: STATE_UNSPECIFIED is the default value.
                 - RUNNING: RUNNING is the search is running.
                 - SUCCEEDED: SUCCEEDED is the search succeeded.
                 - FAILED: FAILED is the search failed.
            error (Union[Unset, RpcStatus]): The `Status` type defines a logical error model that is suitable for
                different programming environments, including REST APIs and RPC APIs. It is
                used by [gRPC](https://github.com/grpc). Each `Status` message contains
                three pieces of data: error code, error message, and error details.

                You can find out more about this error model and how to work with it in the
                [API Design Guide](https://cloud.google.com/apis/design/errors).
            blastn (Union[Unset, V1AlphaBlastn]): Blastn is a blastn search.
            blastp (Union[Unset, V1AlphaBlastp]): Blastp is a blastp search.
            blastx (Union[Unset, V1AlphaBlastp]): Blastp is a blastp search.
            tblastn (Union[Unset, V1AlphaTblastn]): Tblastn is a tblastn search.
            tblastx (Union[Unset, V1AlphaTblastx]): Tblastx is a tblastx search.
    """

    query: str
    name: Union[Unset, str] = UNSET
    code: Union[Unset, V1AlphaCode] = UNSET
    prefix: Union[Unset, str] = UNSET
    query_time: Union[Unset, datetime.datetime] = UNSET
    query_duration: Union[Unset, str] = UNSET
    hits: Union[Unset, List["V1AlphaHit"]] = UNSET
    state: Union[Unset, SearchState] = UNSET
    error: Union[Unset, "RpcStatus"] = UNSET
    blastn: Union[Unset, "V1AlphaBlastn"] = UNSET
    blastp: Union[Unset, "V1AlphaBlastp"] = UNSET
    blastx: Union[Unset, "V1AlphaBlastp"] = UNSET
    tblastn: Union[Unset, "V1AlphaTblastn"] = UNSET
    tblastx: Union[Unset, "V1AlphaTblastx"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        query = self.query

        name = self.name

        code: Union[Unset, str] = UNSET
        if not isinstance(self.code, Unset):
            code = self.code.value

        prefix = self.prefix

        query_time: Union[Unset, str] = UNSET
        if not isinstance(self.query_time, Unset):
            query_time = self.query_time.isoformat()

        query_duration = self.query_duration

        hits: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.hits, Unset):
            hits = []
            for hits_item_data in self.hits:
                hits_item = hits_item_data.to_dict()
                hits.append(hits_item)

        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        error: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.error, Unset):
            error = self.error.to_dict()

        blastn: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.blastn, Unset):
            blastn = self.blastn.to_dict()

        blastp: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.blastp, Unset):
            blastp = self.blastp.to_dict()

        blastx: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.blastx, Unset):
            blastx = self.blastx.to_dict()

        tblastn: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.tblastn, Unset):
            tblastn = self.tblastn.to_dict()

        tblastx: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.tblastx, Unset):
            tblastx = self.tblastx.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "query": query,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if code is not UNSET:
            field_dict["code"] = code
        if prefix is not UNSET:
            field_dict["prefix"] = prefix
        if query_time is not UNSET:
            field_dict["queryTime"] = query_time
        if query_duration is not UNSET:
            field_dict["queryDuration"] = query_duration
        if hits is not UNSET:
            field_dict["hits"] = hits
        if state is not UNSET:
            field_dict["state"] = state
        if error is not UNSET:
            field_dict["error"] = error
        if blastn is not UNSET:
            field_dict["blastn"] = blastn
        if blastp is not UNSET:
            field_dict["blastp"] = blastp
        if blastx is not UNSET:
            field_dict["blastx"] = blastx
        if tblastn is not UNSET:
            field_dict["tblastn"] = tblastn
        if tblastx is not UNSET:
            field_dict["tblastx"] = tblastx

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.rpc_status import RpcStatus
        from ..models.v1_alpha_blastn import V1AlphaBlastn
        from ..models.v1_alpha_blastp import V1AlphaBlastp
        from ..models.v1_alpha_hit import V1AlphaHit
        from ..models.v1_alpha_tblastn import V1AlphaTblastn
        from ..models.v1_alpha_tblastx import V1AlphaTblastx

        d = src_dict.copy()
        query = d.pop("query")

        name = d.pop("name", UNSET)

        _code = d.pop("code", UNSET)
        code: Union[Unset, V1AlphaCode]
        if isinstance(_code, Unset):
            code = UNSET
        else:
            code = V1AlphaCode(_code)

        prefix = d.pop("prefix", UNSET)

        _query_time = d.pop("queryTime", UNSET)
        query_time: Union[Unset, datetime.datetime]
        if isinstance(_query_time, Unset):
            query_time = UNSET
        else:
            query_time = isoparse(_query_time)

        query_duration = d.pop("queryDuration", UNSET)

        hits = []
        _hits = d.pop("hits", UNSET)
        for hits_item_data in _hits or []:
            hits_item = V1AlphaHit.from_dict(hits_item_data)

            hits.append(hits_item)

        _state = d.pop("state", UNSET)
        state: Union[Unset, SearchState]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = SearchState(_state)

        _error = d.pop("error", UNSET)
        error: Union[Unset, RpcStatus]
        if isinstance(_error, Unset):
            error = UNSET
        else:
            error = RpcStatus.from_dict(_error)

        _blastn = d.pop("blastn", UNSET)
        blastn: Union[Unset, V1AlphaBlastn]
        if isinstance(_blastn, Unset):
            blastn = UNSET
        else:
            blastn = V1AlphaBlastn.from_dict(_blastn)

        _blastp = d.pop("blastp", UNSET)
        blastp: Union[Unset, V1AlphaBlastp]
        if isinstance(_blastp, Unset):
            blastp = UNSET
        else:
            blastp = V1AlphaBlastp.from_dict(_blastp)

        _blastx = d.pop("blastx", UNSET)
        blastx: Union[Unset, V1AlphaBlastp]
        if isinstance(_blastx, Unset):
            blastx = UNSET
        else:
            blastx = V1AlphaBlastp.from_dict(_blastx)

        _tblastn = d.pop("tblastn", UNSET)
        tblastn: Union[Unset, V1AlphaTblastn]
        if isinstance(_tblastn, Unset):
            tblastn = UNSET
        else:
            tblastn = V1AlphaTblastn.from_dict(_tblastn)

        _tblastx = d.pop("tblastx", UNSET)
        tblastx: Union[Unset, V1AlphaTblastx]
        if isinstance(_tblastx, Unset):
            tblastx = UNSET
        else:
            tblastx = V1AlphaTblastx.from_dict(_tblastx)

        v1_alpha_search = cls(
            query=query,
            name=name,
            code=code,
            prefix=prefix,
            query_time=query_time,
            query_duration=query_duration,
            hits=hits,
            state=state,
            error=error,
            blastn=blastn,
            blastp=blastp,
            blastx=blastx,
            tblastn=tblastn,
            tblastx=tblastx,
        )

        v1_alpha_search.additional_properties = d
        return v1_alpha_search

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
