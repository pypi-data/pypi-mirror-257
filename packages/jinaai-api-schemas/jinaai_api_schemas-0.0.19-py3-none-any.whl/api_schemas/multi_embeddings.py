from typing import List, Union, Literal

from docarray import BaseDoc, DocList
from docarray.base_doc.doc import BaseDocWithoutId
from docarray.typing import NdArray
from pydantic import Field

from api_schemas.embedding import ExecutorUsage, TextDoc, Usage
from api_schemas.base import BaseInputModel


## Model to be imported by the Executor and used by the Universal API to communicate with it
class MultiEmbeddingsDoc(BaseDoc):
    """Document to be returned by the embedding backend, containing the embedding vector and the token usage for the
    corresponding input texts"""

    embeddings: List[NdArray] = Field(description='A list of embeddings for the text', default=[])
    usage: ExecutorUsage


class MultiEmbeddingsObject(BaseDocWithoutId):
    """Embedding object. OpenAI compatible"""

    object: str = 'embedding'
    index: int = Field(
        description='The index of the embedding output, corresponding to the index in the list of inputs'
    )
    embeddings: List[NdArray] = Field(description='A list of embeddings for the text', default=[])

    class Config(BaseDocWithoutId.Config):
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "object": "embedding",
                "index": 0,
                "embeddings": [[0.1, 0.2, 0.3], [0.5, 0.6, 0.7]],
            }
        }


class TextEmbeddingInput(BaseInputModel):
    """The input to the API for text embedding. OpenAI compatible"""

    input: Union[List[str], str, List[TextDoc], TextDoc] = Field(
        description='List of texts to embed',
    )
    input_type: Literal['query', 'document'] = Field(description='Type of the embedding to compute, query or document',
                                                     default='document')

    @classmethod
    def validate(
            cls,
            value,
    ):
        if 'input' not in value:
            raise ValueError('"input" field missing')
        if 'model' not in value:
            raise ValueError('you must provide a model parameter')
        return cls(**value)

    class Config(BaseDoc.Config):
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "model": "jina-colbert-v1-en",
                "input": ["Hello, world!"],
            },
        }


class ColbertModelEmbeddingsOutput(BaseInputModel):
    """Output of the embedding service"""

    object: str = 'list'
    data: DocList[MultiEmbeddingsDoc] = Field(
        description='A list of Embedding Objects returned by the embedding service'
    )
    usage: Usage = Field(
        description='Total usage of the request. Sums up the usage from each individual input'
    )
