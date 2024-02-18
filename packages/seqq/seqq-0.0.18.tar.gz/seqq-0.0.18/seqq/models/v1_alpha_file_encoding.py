from enum import Enum


class V1AlphaFileEncoding(str, Enum):
    FASTA = "FASTA"
    FILE_UNSPECIFIED = "FILE_UNSPECIFIED"
    GENBANK = "GENBANK"

    def __str__(self) -> str:
        return str(self.value)
