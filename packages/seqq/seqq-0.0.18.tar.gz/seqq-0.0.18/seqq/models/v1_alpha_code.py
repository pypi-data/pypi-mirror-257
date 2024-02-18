from enum import Enum


class V1AlphaCode(str, Enum):
    CODE_UNSPECIFIED = "CODE_UNSPECIFIED"
    NUCLEIC = "NUCLEIC"
    PROTEIN = "PROTEIN"

    def __str__(self) -> str:
        return str(self.value)
