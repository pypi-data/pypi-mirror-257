"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import google.protobuf.timestamp_pb2
import nucliadb_protos.utils_pb2
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions
from nucliadb_protos.utils_pb2 import (
    COSINE as COSINE,
    DOT as DOT,
    EXPERIMENTAL as EXPERIMENTAL,
    ExtractedText as ExtractedText,
    Relation as Relation,
    RelationMetadata as RelationMetadata,
    RelationNode as RelationNode,
    ReleaseChannel as ReleaseChannel,
    STABLE as STABLE,
    Security as Security,
    UserVector as UserVector,
    UserVectorSet as UserVectorSet,
    UserVectors as UserVectors,
    UserVectorsList as UserVectorsList,
    Vector as Vector,
    VectorObject as VectorObject,
    VectorSimilarity as VectorSimilarity,
    Vectors as Vectors,
)

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class TextInformation(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TEXT_FIELD_NUMBER: builtins.int
    LABELS_FIELD_NUMBER: builtins.int
    text: builtins.str
    @property
    def labels(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    def __init__(
        self,
        *,
        text: builtins.str = ...,
        labels: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["labels", b"labels", "text", b"text"]) -> None: ...

global___TextInformation = TextInformation

@typing_extensions.final
class IndexMetadata(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    MODIFIED_FIELD_NUMBER: builtins.int
    CREATED_FIELD_NUMBER: builtins.int
    @property
    def modified(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Tantivy doc & para"""
    @property
    def created(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Tantivy doc & para"""
    def __init__(
        self,
        *,
        modified: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        created: google.protobuf.timestamp_pb2.Timestamp | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["created", b"created", "modified", b"modified"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["created", b"created", "modified", b"modified"]) -> None: ...

global___IndexMetadata = IndexMetadata

@typing_extensions.final
class ShardId(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ID_FIELD_NUMBER: builtins.int
    id: builtins.str
    def __init__(
        self,
        *,
        id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["id", b"id"]) -> None: ...

global___ShardId = ShardId

@typing_extensions.final
class ShardIds(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    IDS_FIELD_NUMBER: builtins.int
    @property
    def ids(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___ShardId]: ...
    def __init__(
        self,
        *,
        ids: collections.abc.Iterable[global___ShardId] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["ids", b"ids"]) -> None: ...

global___ShardIds = ShardIds

@typing_extensions.final
class ShardCreated(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class _DocumentService:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _DocumentServiceEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[ShardCreated._DocumentService.ValueType], builtins.type):  # noqa: F821
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        DOCUMENT_V0: ShardCreated._DocumentService.ValueType  # 0
        DOCUMENT_V1: ShardCreated._DocumentService.ValueType  # 1
        DOCUMENT_V2: ShardCreated._DocumentService.ValueType  # 2

    class DocumentService(_DocumentService, metaclass=_DocumentServiceEnumTypeWrapper): ...
    DOCUMENT_V0: ShardCreated.DocumentService.ValueType  # 0
    DOCUMENT_V1: ShardCreated.DocumentService.ValueType  # 1
    DOCUMENT_V2: ShardCreated.DocumentService.ValueType  # 2

    class _ParagraphService:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _ParagraphServiceEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[ShardCreated._ParagraphService.ValueType], builtins.type):  # noqa: F821
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        PARAGRAPH_V0: ShardCreated._ParagraphService.ValueType  # 0
        PARAGRAPH_V1: ShardCreated._ParagraphService.ValueType  # 1

    class ParagraphService(_ParagraphService, metaclass=_ParagraphServiceEnumTypeWrapper): ...
    PARAGRAPH_V0: ShardCreated.ParagraphService.ValueType  # 0
    PARAGRAPH_V1: ShardCreated.ParagraphService.ValueType  # 1

    class _VectorService:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _VectorServiceEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[ShardCreated._VectorService.ValueType], builtins.type):  # noqa: F821
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        VECTOR_V0: ShardCreated._VectorService.ValueType  # 0
        VECTOR_V1: ShardCreated._VectorService.ValueType  # 1

    class VectorService(_VectorService, metaclass=_VectorServiceEnumTypeWrapper): ...
    VECTOR_V0: ShardCreated.VectorService.ValueType  # 0
    VECTOR_V1: ShardCreated.VectorService.ValueType  # 1

    class _RelationService:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _RelationServiceEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[ShardCreated._RelationService.ValueType], builtins.type):  # noqa: F821
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        RELATION_V0: ShardCreated._RelationService.ValueType  # 0
        RELATION_V1: ShardCreated._RelationService.ValueType  # 1
        RELATION_V2: ShardCreated._RelationService.ValueType  # 2

    class RelationService(_RelationService, metaclass=_RelationServiceEnumTypeWrapper): ...
    RELATION_V0: ShardCreated.RelationService.ValueType  # 0
    RELATION_V1: ShardCreated.RelationService.ValueType  # 1
    RELATION_V2: ShardCreated.RelationService.ValueType  # 2

    ID_FIELD_NUMBER: builtins.int
    DOCUMENT_SERVICE_FIELD_NUMBER: builtins.int
    PARAGRAPH_SERVICE_FIELD_NUMBER: builtins.int
    VECTOR_SERVICE_FIELD_NUMBER: builtins.int
    RELATION_SERVICE_FIELD_NUMBER: builtins.int
    id: builtins.str
    document_service: global___ShardCreated.DocumentService.ValueType
    paragraph_service: global___ShardCreated.ParagraphService.ValueType
    vector_service: global___ShardCreated.VectorService.ValueType
    relation_service: global___ShardCreated.RelationService.ValueType
    def __init__(
        self,
        *,
        id: builtins.str = ...,
        document_service: global___ShardCreated.DocumentService.ValueType = ...,
        paragraph_service: global___ShardCreated.ParagraphService.ValueType = ...,
        vector_service: global___ShardCreated.VectorService.ValueType = ...,
        relation_service: global___ShardCreated.RelationService.ValueType = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["document_service", b"document_service", "id", b"id", "paragraph_service", b"paragraph_service", "relation_service", b"relation_service", "vector_service", b"vector_service"]) -> None: ...

global___ShardCreated = ShardCreated

@typing_extensions.final
class ShardCleaned(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DOCUMENT_SERVICE_FIELD_NUMBER: builtins.int
    PARAGRAPH_SERVICE_FIELD_NUMBER: builtins.int
    VECTOR_SERVICE_FIELD_NUMBER: builtins.int
    RELATION_SERVICE_FIELD_NUMBER: builtins.int
    document_service: global___ShardCreated.DocumentService.ValueType
    paragraph_service: global___ShardCreated.ParagraphService.ValueType
    vector_service: global___ShardCreated.VectorService.ValueType
    relation_service: global___ShardCreated.RelationService.ValueType
    def __init__(
        self,
        *,
        document_service: global___ShardCreated.DocumentService.ValueType = ...,
        paragraph_service: global___ShardCreated.ParagraphService.ValueType = ...,
        vector_service: global___ShardCreated.VectorService.ValueType = ...,
        relation_service: global___ShardCreated.RelationService.ValueType = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["document_service", b"document_service", "paragraph_service", b"paragraph_service", "relation_service", b"relation_service", "vector_service", b"vector_service"]) -> None: ...

global___ShardCleaned = ShardCleaned

@typing_extensions.final
class ResourceID(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SHARD_ID_FIELD_NUMBER: builtins.int
    UUID_FIELD_NUMBER: builtins.int
    shard_id: builtins.str
    uuid: builtins.str
    def __init__(
        self,
        *,
        shard_id: builtins.str = ...,
        uuid: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["shard_id", b"shard_id", "uuid", b"uuid"]) -> None: ...

global___ResourceID = ResourceID

@typing_extensions.final
class Shard(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    METADATA_FIELD_NUMBER: builtins.int
    SHARD_ID_FIELD_NUMBER: builtins.int
    FIELDS_FIELD_NUMBER: builtins.int
    PARAGRAPHS_FIELD_NUMBER: builtins.int
    SENTENCES_FIELD_NUMBER: builtins.int
    @property
    def metadata(self) -> global___ShardMetadata: ...
    shard_id: builtins.str
    fields: builtins.int
    paragraphs: builtins.int
    sentences: builtins.int
    def __init__(
        self,
        *,
        metadata: global___ShardMetadata | None = ...,
        shard_id: builtins.str = ...,
        fields: builtins.int = ...,
        paragraphs: builtins.int = ...,
        sentences: builtins.int = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["metadata", b"metadata"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["fields", b"fields", "metadata", b"metadata", "paragraphs", b"paragraphs", "sentences", b"sentences", "shard_id", b"shard_id"]) -> None: ...

global___Shard = Shard

@typing_extensions.final
class EmptyResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___EmptyResponse = EmptyResponse

@typing_extensions.final
class EmptyQuery(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___EmptyQuery = EmptyQuery

@typing_extensions.final
class Position(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    INDEX_FIELD_NUMBER: builtins.int
    START_FIELD_NUMBER: builtins.int
    END_FIELD_NUMBER: builtins.int
    PAGE_NUMBER_FIELD_NUMBER: builtins.int
    START_SECONDS_FIELD_NUMBER: builtins.int
    END_SECONDS_FIELD_NUMBER: builtins.int
    index: builtins.int
    start: builtins.int
    end: builtins.int
    page_number: builtins.int
    """For pdfs/documents only"""
    @property
    def start_seconds(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]:
        """For multimedia only"""
    @property
    def end_seconds(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
    def __init__(
        self,
        *,
        index: builtins.int = ...,
        start: builtins.int = ...,
        end: builtins.int = ...,
        page_number: builtins.int = ...,
        start_seconds: collections.abc.Iterable[builtins.int] | None = ...,
        end_seconds: collections.abc.Iterable[builtins.int] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["end", b"end", "end_seconds", b"end_seconds", "index", b"index", "page_number", b"page_number", "start", b"start", "start_seconds", b"start_seconds"]) -> None: ...

global___Position = Position

@typing_extensions.final
class SentenceMetadata(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    POSITION_FIELD_NUMBER: builtins.int
    @property
    def position(self) -> global___Position: ...
    def __init__(
        self,
        *,
        position: global___Position | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["position", b"position"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["position", b"position"]) -> None: ...

global___SentenceMetadata = SentenceMetadata

@typing_extensions.final
class VectorSentence(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    VECTOR_FIELD_NUMBER: builtins.int
    METADATA_FIELD_NUMBER: builtins.int
    @property
    def vector(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.float]: ...
    @property
    def metadata(self) -> global___SentenceMetadata: ...
    def __init__(
        self,
        *,
        vector: collections.abc.Iterable[builtins.float] | None = ...,
        metadata: global___SentenceMetadata | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["metadata", b"metadata"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["metadata", b"metadata", "vector", b"vector"]) -> None: ...

global___VectorSentence = VectorSentence

@typing_extensions.final
class ParagraphMetadata(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    POSITION_FIELD_NUMBER: builtins.int
    @property
    def position(self) -> global___Position: ...
    def __init__(
        self,
        *,
        position: global___Position | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["position", b"position"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["position", b"position"]) -> None: ...

global___ParagraphMetadata = ParagraphMetadata

@typing_extensions.final
class IndexParagraph(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing_extensions.final
    class SentencesEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        @property
        def value(self) -> global___VectorSentence: ...
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: global___VectorSentence | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["value", b"value"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

    START_FIELD_NUMBER: builtins.int
    END_FIELD_NUMBER: builtins.int
    LABELS_FIELD_NUMBER: builtins.int
    SENTENCES_FIELD_NUMBER: builtins.int
    FIELD_FIELD_NUMBER: builtins.int
    SPLIT_FIELD_NUMBER: builtins.int
    INDEX_FIELD_NUMBER: builtins.int
    REPEATED_IN_FIELD_FIELD_NUMBER: builtins.int
    METADATA_FIELD_NUMBER: builtins.int
    start: builtins.int
    """Start end position in field text"""
    end: builtins.int
    """Start end position in field text"""
    @property
    def labels(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """Paragraph specific labels"""
    @property
    def sentences(self) -> google.protobuf.internal.containers.MessageMap[builtins.str, global___VectorSentence]:
        """key is full id for vectors"""
    field: builtins.str
    split: builtins.str
    """split were it belongs"""
    index: builtins.int
    repeated_in_field: builtins.bool
    @property
    def metadata(self) -> global___ParagraphMetadata: ...
    def __init__(
        self,
        *,
        start: builtins.int = ...,
        end: builtins.int = ...,
        labels: collections.abc.Iterable[builtins.str] | None = ...,
        sentences: collections.abc.Mapping[builtins.str, global___VectorSentence] | None = ...,
        field: builtins.str = ...,
        split: builtins.str = ...,
        index: builtins.int = ...,
        repeated_in_field: builtins.bool = ...,
        metadata: global___ParagraphMetadata | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["metadata", b"metadata"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["end", b"end", "field", b"field", "index", b"index", "labels", b"labels", "metadata", b"metadata", "repeated_in_field", b"repeated_in_field", "sentences", b"sentences", "split", b"split", "start", b"start"]) -> None: ...

global___IndexParagraph = IndexParagraph

@typing_extensions.final
class VectorSetID(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SHARD_FIELD_NUMBER: builtins.int
    VECTORSET_FIELD_NUMBER: builtins.int
    @property
    def shard(self) -> global___ShardId: ...
    vectorset: builtins.str
    def __init__(
        self,
        *,
        shard: global___ShardId | None = ...,
        vectorset: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["shard", b"shard"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["shard", b"shard", "vectorset", b"vectorset"]) -> None: ...

global___VectorSetID = VectorSetID

@typing_extensions.final
class VectorSetList(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SHARD_FIELD_NUMBER: builtins.int
    VECTORSET_FIELD_NUMBER: builtins.int
    @property
    def shard(self) -> global___ShardId: ...
    @property
    def vectorset(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    def __init__(
        self,
        *,
        shard: global___ShardId | None = ...,
        vectorset: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["shard", b"shard"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["shard", b"shard", "vectorset", b"vectorset"]) -> None: ...

global___VectorSetList = VectorSetList

@typing_extensions.final
class IndexParagraphs(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing_extensions.final
    class ParagraphsEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        @property
        def value(self) -> global___IndexParagraph: ...
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: global___IndexParagraph | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["value", b"value"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

    PARAGRAPHS_FIELD_NUMBER: builtins.int
    @property
    def paragraphs(self) -> google.protobuf.internal.containers.MessageMap[builtins.str, global___IndexParagraph]:
        """id of the paragraph f"{self.rid}/{field_key}/{paragraph.start}-{paragraph.end}" """
    def __init__(
        self,
        *,
        paragraphs: collections.abc.Mapping[builtins.str, global___IndexParagraph] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["paragraphs", b"paragraphs"]) -> None: ...

global___IndexParagraphs = IndexParagraphs

@typing_extensions.final
class Resource(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class _ResourceStatus:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _ResourceStatusEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[Resource._ResourceStatus.ValueType], builtins.type):  # noqa: F821
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        PROCESSED: Resource._ResourceStatus.ValueType  # 0
        EMPTY: Resource._ResourceStatus.ValueType  # 1
        ERROR: Resource._ResourceStatus.ValueType  # 2
        DELETE: Resource._ResourceStatus.ValueType  # 3
        PENDING: Resource._ResourceStatus.ValueType  # 4
        BLOCKED: Resource._ResourceStatus.ValueType  # 5
        EXPIRED: Resource._ResourceStatus.ValueType  # 6

    class ResourceStatus(_ResourceStatus, metaclass=_ResourceStatusEnumTypeWrapper): ...
    PROCESSED: Resource.ResourceStatus.ValueType  # 0
    EMPTY: Resource.ResourceStatus.ValueType  # 1
    ERROR: Resource.ResourceStatus.ValueType  # 2
    DELETE: Resource.ResourceStatus.ValueType  # 3
    PENDING: Resource.ResourceStatus.ValueType  # 4
    BLOCKED: Resource.ResourceStatus.ValueType  # 5
    EXPIRED: Resource.ResourceStatus.ValueType  # 6

    @typing_extensions.final
    class TextsEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        @property
        def value(self) -> global___TextInformation: ...
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: global___TextInformation | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["value", b"value"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

    @typing_extensions.final
    class ParagraphsEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        @property
        def value(self) -> global___IndexParagraphs: ...
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: global___IndexParagraphs | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["value", b"value"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

    @typing_extensions.final
    class VectorsEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        @property
        def value(self) -> nucliadb_protos.utils_pb2.UserVectors: ...
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: nucliadb_protos.utils_pb2.UserVectors | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["value", b"value"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

    @typing_extensions.final
    class VectorsToDeleteEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        @property
        def value(self) -> nucliadb_protos.utils_pb2.UserVectorsList: ...
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: nucliadb_protos.utils_pb2.UserVectorsList | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["value", b"value"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

    RESOURCE_FIELD_NUMBER: builtins.int
    METADATA_FIELD_NUMBER: builtins.int
    TEXTS_FIELD_NUMBER: builtins.int
    LABELS_FIELD_NUMBER: builtins.int
    STATUS_FIELD_NUMBER: builtins.int
    PARAGRAPHS_FIELD_NUMBER: builtins.int
    PARAGRAPHS_TO_DELETE_FIELD_NUMBER: builtins.int
    SENTENCES_TO_DELETE_FIELD_NUMBER: builtins.int
    RELATIONS_FIELD_NUMBER: builtins.int
    SHARD_ID_FIELD_NUMBER: builtins.int
    VECTORS_FIELD_NUMBER: builtins.int
    VECTORS_TO_DELETE_FIELD_NUMBER: builtins.int
    SECURITY_FIELD_NUMBER: builtins.int
    @property
    def resource(self) -> global___ResourceID: ...
    @property
    def metadata(self) -> global___IndexMetadata: ...
    @property
    def texts(self) -> google.protobuf.internal.containers.MessageMap[builtins.str, global___TextInformation]:
        """Doc index
        Tantivy doc filled by field allways full
        """
    @property
    def labels(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """Key is RID/FIELDID

        Document labels always serialized full
        """
    status: global___Resource.ResourceStatus.ValueType
    """Tantivy doc"""
    @property
    def paragraphs(self) -> google.protobuf.internal.containers.MessageMap[builtins.str, global___IndexParagraphs]:
        """Paragraph
        Paragraphs by field
        """
    @property
    def paragraphs_to_delete(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    @property
    def sentences_to_delete(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    @property
    def relations(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[nucliadb_protos.utils_pb2.Relation]:
        """Relations"""
    shard_id: builtins.str
    @property
    def vectors(self) -> google.protobuf.internal.containers.MessageMap[builtins.str, nucliadb_protos.utils_pb2.UserVectors]:
        """vectorset is the key"""
    @property
    def vectors_to_delete(self) -> google.protobuf.internal.containers.MessageMap[builtins.str, nucliadb_protos.utils_pb2.UserVectorsList]:
        """Vectorset prefix vector id"""
    @property
    def security(self) -> nucliadb_protos.utils_pb2.Security: ...
    def __init__(
        self,
        *,
        resource: global___ResourceID | None = ...,
        metadata: global___IndexMetadata | None = ...,
        texts: collections.abc.Mapping[builtins.str, global___TextInformation] | None = ...,
        labels: collections.abc.Iterable[builtins.str] | None = ...,
        status: global___Resource.ResourceStatus.ValueType = ...,
        paragraphs: collections.abc.Mapping[builtins.str, global___IndexParagraphs] | None = ...,
        paragraphs_to_delete: collections.abc.Iterable[builtins.str] | None = ...,
        sentences_to_delete: collections.abc.Iterable[builtins.str] | None = ...,
        relations: collections.abc.Iterable[nucliadb_protos.utils_pb2.Relation] | None = ...,
        shard_id: builtins.str = ...,
        vectors: collections.abc.Mapping[builtins.str, nucliadb_protos.utils_pb2.UserVectors] | None = ...,
        vectors_to_delete: collections.abc.Mapping[builtins.str, nucliadb_protos.utils_pb2.UserVectorsList] | None = ...,
        security: nucliadb_protos.utils_pb2.Security | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_security", b"_security", "metadata", b"metadata", "resource", b"resource", "security", b"security"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_security", b"_security", "labels", b"labels", "metadata", b"metadata", "paragraphs", b"paragraphs", "paragraphs_to_delete", b"paragraphs_to_delete", "relations", b"relations", "resource", b"resource", "security", b"security", "sentences_to_delete", b"sentences_to_delete", "shard_id", b"shard_id", "status", b"status", "texts", b"texts", "vectors", b"vectors", "vectors_to_delete", b"vectors_to_delete"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_security", b"_security"]) -> typing_extensions.Literal["security"] | None: ...

global___Resource = Resource

@typing_extensions.final
class ShardMetadata(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    KBID_FIELD_NUMBER: builtins.int
    RELEASE_CHANNEL_FIELD_NUMBER: builtins.int
    kbid: builtins.str
    release_channel: nucliadb_protos.utils_pb2.ReleaseChannel.ValueType
    def __init__(
        self,
        *,
        kbid: builtins.str = ...,
        release_channel: nucliadb_protos.utils_pb2.ReleaseChannel.ValueType = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["kbid", b"kbid", "release_channel", b"release_channel"]) -> None: ...

global___ShardMetadata = ShardMetadata

@typing_extensions.final
class NodeMetadata(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing_extensions.final
    class ShardMetadata(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KBID_FIELD_NUMBER: builtins.int
        LOAD_SCORE_FIELD_NUMBER: builtins.int
        kbid: builtins.str
        load_score: builtins.float
        def __init__(
            self,
            *,
            kbid: builtins.str = ...,
            load_score: builtins.float = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["kbid", b"kbid", "load_score", b"load_score"]) -> None: ...

    @typing_extensions.final
    class ShardsEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        @property
        def value(self) -> global___NodeMetadata.ShardMetadata: ...
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: global___NodeMetadata.ShardMetadata | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["value", b"value"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

    LOAD_SCORE_FIELD_NUMBER: builtins.int
    SHARD_COUNT_FIELD_NUMBER: builtins.int
    SHARDS_FIELD_NUMBER: builtins.int
    NODE_ID_FIELD_NUMBER: builtins.int
    PRIMARY_NODE_ID_FIELD_NUMBER: builtins.int
    load_score: builtins.float
    shard_count: builtins.int
    @property
    def shards(self) -> google.protobuf.internal.containers.MessageMap[builtins.str, global___NodeMetadata.ShardMetadata]: ...
    node_id: builtins.str
    primary_node_id: builtins.str
    def __init__(
        self,
        *,
        load_score: builtins.float = ...,
        shard_count: builtins.int = ...,
        shards: collections.abc.Mapping[builtins.str, global___NodeMetadata.ShardMetadata] | None = ...,
        node_id: builtins.str = ...,
        primary_node_id: builtins.str | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_primary_node_id", b"_primary_node_id", "primary_node_id", b"primary_node_id"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_primary_node_id", b"_primary_node_id", "load_score", b"load_score", "node_id", b"node_id", "primary_node_id", b"primary_node_id", "shard_count", b"shard_count", "shards", b"shards"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_primary_node_id", b"_primary_node_id"]) -> typing_extensions.Literal["primary_node_id"] | None: ...

global___NodeMetadata = NodeMetadata
