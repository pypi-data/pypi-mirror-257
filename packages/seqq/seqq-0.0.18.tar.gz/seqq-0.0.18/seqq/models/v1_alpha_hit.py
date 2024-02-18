from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="V1AlphaHit")


@_attrs_define
class V1AlphaHit:
    """Hit is a single hit from a Search.

    Attributes:
        saccver (Union[Unset, str]): Subject accession version.
        pident (Union[Unset, float]): Percentage of identical matches.
        length (Union[Unset, str]): Alignment length.
        mismatch (Union[Unset, str]): Number of mismatches.
        gapopen (Union[Unset, str]): Number of gap openings.
        qstart (Union[Unset, str]): Start of alignment in search.
        qend (Union[Unset, str]): End of alignment in search.
        sstart (Union[Unset, str]): Start of alignment in subject.
        send (Union[Unset, str]): End of alignment in subject.
        evalue (Union[Unset, float]): Expect value.
        bitscore (Union[Unset, float]): Bit score.
    """

    saccver: Union[Unset, str] = UNSET
    pident: Union[Unset, float] = UNSET
    length: Union[Unset, str] = UNSET
    mismatch: Union[Unset, str] = UNSET
    gapopen: Union[Unset, str] = UNSET
    qstart: Union[Unset, str] = UNSET
    qend: Union[Unset, str] = UNSET
    sstart: Union[Unset, str] = UNSET
    send: Union[Unset, str] = UNSET
    evalue: Union[Unset, float] = UNSET
    bitscore: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        saccver = self.saccver

        pident = self.pident

        length = self.length

        mismatch = self.mismatch

        gapopen = self.gapopen

        qstart = self.qstart

        qend = self.qend

        sstart = self.sstart

        send = self.send

        evalue = self.evalue

        bitscore = self.bitscore

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if saccver is not UNSET:
            field_dict["saccver"] = saccver
        if pident is not UNSET:
            field_dict["pident"] = pident
        if length is not UNSET:
            field_dict["length"] = length
        if mismatch is not UNSET:
            field_dict["mismatch"] = mismatch
        if gapopen is not UNSET:
            field_dict["gapopen"] = gapopen
        if qstart is not UNSET:
            field_dict["qstart"] = qstart
        if qend is not UNSET:
            field_dict["qend"] = qend
        if sstart is not UNSET:
            field_dict["sstart"] = sstart
        if send is not UNSET:
            field_dict["send"] = send
        if evalue is not UNSET:
            field_dict["evalue"] = evalue
        if bitscore is not UNSET:
            field_dict["bitscore"] = bitscore

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        saccver = d.pop("saccver", UNSET)

        pident = d.pop("pident", UNSET)

        length = d.pop("length", UNSET)

        mismatch = d.pop("mismatch", UNSET)

        gapopen = d.pop("gapopen", UNSET)

        qstart = d.pop("qstart", UNSET)

        qend = d.pop("qend", UNSET)

        sstart = d.pop("sstart", UNSET)

        send = d.pop("send", UNSET)

        evalue = d.pop("evalue", UNSET)

        bitscore = d.pop("bitscore", UNSET)

        v1_alpha_hit = cls(
            saccver=saccver,
            pident=pident,
            length=length,
            mismatch=mismatch,
            gapopen=gapopen,
            qstart=qstart,
            qend=qend,
            sstart=sstart,
            send=send,
            evalue=evalue,
            bitscore=bitscore,
        )

        v1_alpha_hit.additional_properties = d
        return v1_alpha_hit

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
