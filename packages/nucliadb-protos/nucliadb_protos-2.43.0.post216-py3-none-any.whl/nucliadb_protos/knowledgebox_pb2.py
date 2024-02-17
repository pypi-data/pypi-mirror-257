# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: nucliadb_protos/knowledgebox.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from nucliadb_protos import utils_pb2 as nucliadb__protos_dot_utils__pb2

from nucliadb_protos.utils_pb2 import *

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\"nucliadb_protos/knowledgebox.proto\x12\x0cknowledgebox\x1a\x1bnucliadb_protos/utils.proto\",\n\x0eKnowledgeBoxID\x12\x0c\n\x04slug\x18\x01 \x01(\t\x12\x0c\n\x04uuid\x18\x02 \x01(\t\"\x96\x01\n\x0cKnowledgeBox\x12\x0c\n\x04slug\x18\x01 \x01(\t\x12\x0c\n\x04uuid\x18\x02 \x01(\t\x12\x38\n\x06status\x18\x03 \x01(\x0e\x32(.knowledgebox.KnowledgeBoxResponseStatus\x12\x30\n\x06\x63onfig\x18\x04 \x01(\x0b\x32 .knowledgebox.KnowledgeBoxConfig\"\xe9\x01\n\x12KnowledgeBoxConfig\x12\r\n\x05title\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\x1b\n\x0f\x65nabled_filters\x18\x03 \x03(\tB\x02\x18\x01\x12\x1c\n\x10\x65nabled_insights\x18\x04 \x03(\tB\x02\x18\x01\x12\x0c\n\x04slug\x18\x05 \x01(\t\x12\x1b\n\x0f\x64isable_vectors\x18\x06 \x01(\x08\x42\x02\x18\x01\x12\x19\n\x11migration_version\x18\x07 \x01(\x03\x12.\n\x0frelease_channel\x18\x08 \x01(\x0e\x32\x15.utils.ReleaseChannel\"\xc4\x02\n\x0fKnowledgeBoxNew\x12\x0c\n\x04slug\x18\x01 \x01(\t\x12\x30\n\x06\x63onfig\x18\x02 \x01(\x0b\x32 .knowledgebox.KnowledgeBoxConfig\x12\x11\n\tforceuuid\x18\x03 \x01(\t\x12+\n\nsimilarity\x18\x04 \x01(\x0e\x32\x17.utils.VectorSimilarity\x12\x1d\n\x10vector_dimension\x18\x05 \x01(\x05H\x00\x88\x01\x01\x12\x1e\n\x11\x64\x65\x66\x61ult_min_score\x18\x06 \x01(\x02H\x01\x88\x01\x01\x12.\n\x0frelease_channel\x18\x07 \x01(\x0e\x32\x15.utils.ReleaseChannel\x12\x17\n\x0flearning_config\x18\x08 \x01(\tB\x13\n\x11_vector_dimensionB\x14\n\x12_default_min_score\"a\n\x17NewKnowledgeBoxResponse\x12\x38\n\x06status\x18\x01 \x01(\x0e\x32(.knowledgebox.KnowledgeBoxResponseStatus\x12\x0c\n\x04uuid\x18\x02 \x01(\t\"$\n\x12KnowledgeBoxPrefix\x12\x0e\n\x06prefix\x18\x01 \x01(\t\"b\n\x12KnowledgeBoxUpdate\x12\x0c\n\x04slug\x18\x01 \x01(\t\x12\x0c\n\x04uuid\x18\x02 \x01(\t\x12\x30\n\x06\x63onfig\x18\x03 \x01(\x0b\x32 .knowledgebox.KnowledgeBoxConfig\"d\n\x1aUpdateKnowledgeBoxResponse\x12\x38\n\x06status\x18\x01 \x01(\x0e\x32(.knowledgebox.KnowledgeBoxResponseStatus\x12\x0c\n\x04uuid\x18\x02 \x01(\t\"\x18\n\x16GCKnowledgeBoxResponse\"V\n\x1a\x44\x65leteKnowledgeBoxResponse\x12\x38\n\x06status\x18\x01 \x01(\x0e\x32(.knowledgebox.KnowledgeBoxResponseStatus\"\x1d\n\x1b\x43leanedKnowledgeBoxResponse\"B\n\x05Label\x12\r\n\x05title\x18\x02 \x01(\t\x12\x0f\n\x07related\x18\x03 \x01(\t\x12\x0c\n\x04text\x18\x04 \x01(\t\x12\x0b\n\x03uri\x18\x05 \x01(\t\"\xe0\x01\n\x08LabelSet\x12\r\n\x05title\x18\x01 \x01(\t\x12\r\n\x05\x63olor\x18\x02 \x01(\t\x12#\n\x06labels\x18\x03 \x03(\x0b\x32\x13.knowledgebox.Label\x12\x10\n\x08multiple\x18\x04 \x01(\x08\x12\x31\n\x04kind\x18\x05 \x03(\x0e\x32#.knowledgebox.LabelSet.LabelSetKind\"L\n\x0cLabelSetKind\x12\r\n\tRESOURCES\x10\x00\x12\x0e\n\nPARAGRAPHS\x10\x01\x12\r\n\tSENTENCES\x10\x02\x12\x0e\n\nSELECTIONS\x10\x03\"\x87\x01\n\x06Labels\x12\x34\n\x08labelset\x18\x01 \x03(\x0b\x32\".knowledgebox.Labels.LabelsetEntry\x1aG\n\rLabelsetEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12%\n\x05value\x18\x02 \x01(\x0b\x32\x16.knowledgebox.LabelSet:\x02\x38\x01\"L\n\x06\x45ntity\x12\r\n\x05value\x18\x02 \x01(\t\x12\x12\n\nrepresents\x18\x04 \x03(\t\x12\x0e\n\x06merged\x18\x03 \x01(\x08\x12\x0f\n\x07\x64\x65leted\x18\x05 \x01(\x08\"D\n\x14\x45ntitiesGroupSummary\x12\r\n\x05title\x18\x02 \x01(\t\x12\r\n\x05\x63olor\x18\x03 \x01(\t\x12\x0e\n\x06\x63ustom\x18\x04 \x01(\x08\"\xc1\x01\n\rEntitiesGroup\x12;\n\x08\x65ntities\x18\x01 \x03(\x0b\x32).knowledgebox.EntitiesGroup.EntitiesEntry\x12\r\n\x05title\x18\x02 \x01(\t\x12\r\n\x05\x63olor\x18\x03 \x01(\t\x12\x0e\n\x06\x63ustom\x18\x04 \x01(\x08\x1a\x45\n\rEntitiesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12#\n\x05value\x18\x02 \x01(\x0b\x32\x14.knowledgebox.Entity:\x02\x38\x01\"0\n\x15\x44\x65letedEntitiesGroups\x12\x17\n\x0f\x65ntities_groups\x18\x01 \x03(\t\"\xaf\x01\n\x0e\x45ntitiesGroups\x12I\n\x0f\x65ntities_groups\x18\x01 \x03(\x0b\x32\x30.knowledgebox.EntitiesGroups.EntitiesGroupsEntry\x1aR\n\x13\x45ntitiesGroupsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12*\n\x05value\x18\x02 \x01(\x0b\x32\x1b.knowledgebox.EntitiesGroup:\x02\x38\x01\"\xf3\x03\n\x19\x45ntityGroupDuplicateIndex\x12T\n\x0f\x65ntities_groups\x18\x01 \x03(\x0b\x32;.knowledgebox.EntityGroupDuplicateIndex.EntitiesGroupsEntry\x1a&\n\x10\x45ntityDuplicates\x12\x12\n\nduplicates\x18\x01 \x03(\t\x1a\xe1\x01\n\x15\x45ntityGroupDuplicates\x12]\n\x08\x65ntities\x18\x01 \x03(\x0b\x32K.knowledgebox.EntityGroupDuplicateIndex.EntityGroupDuplicates.EntitiesEntry\x1ai\n\rEntitiesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12G\n\x05value\x18\x02 \x01(\x0b\x32\x38.knowledgebox.EntityGroupDuplicateIndex.EntityDuplicates:\x02\x38\x01\x1at\n\x13\x45ntitiesGroupsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12L\n\x05value\x18\x02 \x01(\x0b\x32=.knowledgebox.EntityGroupDuplicateIndex.EntityGroupDuplicates:\x02\x38\x01\"K\n\tVectorSet\x12\x11\n\tdimension\x18\x01 \x01(\x05\x12+\n\nsimilarity\x18\x02 \x01(\x0e\x32\x17.utils.VectorSimilarity\"\x96\x01\n\nVectorSets\x12<\n\nvectorsets\x18\x01 \x03(\x0b\x32(.knowledgebox.VectorSets.VectorsetsEntry\x1aJ\n\x0fVectorsetsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12&\n\x05value\x18\x02 \x01(\x0b\x32\x17.knowledgebox.VectorSet:\x02\x38\x01\" \n\x0cTermSynonyms\x12\x10\n\x08synonyms\x18\x01 \x03(\t\"\x86\x01\n\x08Synonyms\x12\x30\n\x05terms\x18\x01 \x03(\x0b\x32!.knowledgebox.Synonyms.TermsEntry\x1aH\n\nTermsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12)\n\x05value\x18\x02 \x01(\x0b\x32\x1a.knowledgebox.TermSynonyms:\x02\x38\x01\"\xb7\x01\n\x15SemanticModelMetadata\x12\x34\n\x13similarity_function\x18\x01 \x01(\x0e\x32\x17.utils.VectorSimilarity\x12\x1d\n\x10vector_dimension\x18\x02 \x01(\x05H\x00\x88\x01\x01\x12\x1e\n\x11\x64\x65\x66\x61ult_min_score\x18\x03 \x01(\x02H\x01\x88\x01\x01\x42\x13\n\x11_vector_dimensionB\x14\n\x12_default_min_score\"\x8c\x01\n\x0fKBConfiguration\x12\x16\n\x0esemantic_model\x18\x02 \x01(\t\x12\x18\n\x10generative_model\x18\x03 \x01(\t\x12\x11\n\tner_model\x18\x04 \x01(\t\x12\x1b\n\x13\x61nonymization_model\x18\x05 \x01(\t\x12\x17\n\x0fvisual_labeling\x18\x06 \x01(\t*K\n\x1aKnowledgeBoxResponseStatus\x12\x06\n\x02OK\x10\x00\x12\x0c\n\x08\x43ONFLICT\x10\x01\x12\x0c\n\x08NOTFOUND\x10\x02\x12\t\n\x05\x45RROR\x10\x03P\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'nucliadb_protos.knowledgebox_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _KNOWLEDGEBOXCONFIG.fields_by_name['enabled_filters']._options = None
  _KNOWLEDGEBOXCONFIG.fields_by_name['enabled_filters']._serialized_options = b'\030\001'
  _KNOWLEDGEBOXCONFIG.fields_by_name['enabled_insights']._options = None
  _KNOWLEDGEBOXCONFIG.fields_by_name['enabled_insights']._serialized_options = b'\030\001'
  _KNOWLEDGEBOXCONFIG.fields_by_name['disable_vectors']._options = None
  _KNOWLEDGEBOXCONFIG.fields_by_name['disable_vectors']._serialized_options = b'\030\001'
  _LABELS_LABELSETENTRY._options = None
  _LABELS_LABELSETENTRY._serialized_options = b'8\001'
  _ENTITIESGROUP_ENTITIESENTRY._options = None
  _ENTITIESGROUP_ENTITIESENTRY._serialized_options = b'8\001'
  _ENTITIESGROUPS_ENTITIESGROUPSENTRY._options = None
  _ENTITIESGROUPS_ENTITIESGROUPSENTRY._serialized_options = b'8\001'
  _ENTITYGROUPDUPLICATEINDEX_ENTITYGROUPDUPLICATES_ENTITIESENTRY._options = None
  _ENTITYGROUPDUPLICATEINDEX_ENTITYGROUPDUPLICATES_ENTITIESENTRY._serialized_options = b'8\001'
  _ENTITYGROUPDUPLICATEINDEX_ENTITIESGROUPSENTRY._options = None
  _ENTITYGROUPDUPLICATEINDEX_ENTITIESGROUPSENTRY._serialized_options = b'8\001'
  _VECTORSETS_VECTORSETSENTRY._options = None
  _VECTORSETS_VECTORSETSENTRY._serialized_options = b'8\001'
  _SYNONYMS_TERMSENTRY._options = None
  _SYNONYMS_TERMSENTRY._serialized_options = b'8\001'
  _globals['_KNOWLEDGEBOXRESPONSESTATUS']._serialized_start=3564
  _globals['_KNOWLEDGEBOXRESPONSESTATUS']._serialized_end=3639
  _globals['_KNOWLEDGEBOXID']._serialized_start=81
  _globals['_KNOWLEDGEBOXID']._serialized_end=125
  _globals['_KNOWLEDGEBOX']._serialized_start=128
  _globals['_KNOWLEDGEBOX']._serialized_end=278
  _globals['_KNOWLEDGEBOXCONFIG']._serialized_start=281
  _globals['_KNOWLEDGEBOXCONFIG']._serialized_end=514
  _globals['_KNOWLEDGEBOXNEW']._serialized_start=517
  _globals['_KNOWLEDGEBOXNEW']._serialized_end=841
  _globals['_NEWKNOWLEDGEBOXRESPONSE']._serialized_start=843
  _globals['_NEWKNOWLEDGEBOXRESPONSE']._serialized_end=940
  _globals['_KNOWLEDGEBOXPREFIX']._serialized_start=942
  _globals['_KNOWLEDGEBOXPREFIX']._serialized_end=978
  _globals['_KNOWLEDGEBOXUPDATE']._serialized_start=980
  _globals['_KNOWLEDGEBOXUPDATE']._serialized_end=1078
  _globals['_UPDATEKNOWLEDGEBOXRESPONSE']._serialized_start=1080
  _globals['_UPDATEKNOWLEDGEBOXRESPONSE']._serialized_end=1180
  _globals['_GCKNOWLEDGEBOXRESPONSE']._serialized_start=1182
  _globals['_GCKNOWLEDGEBOXRESPONSE']._serialized_end=1206
  _globals['_DELETEKNOWLEDGEBOXRESPONSE']._serialized_start=1208
  _globals['_DELETEKNOWLEDGEBOXRESPONSE']._serialized_end=1294
  _globals['_CLEANEDKNOWLEDGEBOXRESPONSE']._serialized_start=1296
  _globals['_CLEANEDKNOWLEDGEBOXRESPONSE']._serialized_end=1325
  _globals['_LABEL']._serialized_start=1327
  _globals['_LABEL']._serialized_end=1393
  _globals['_LABELSET']._serialized_start=1396
  _globals['_LABELSET']._serialized_end=1620
  _globals['_LABELSET_LABELSETKIND']._serialized_start=1544
  _globals['_LABELSET_LABELSETKIND']._serialized_end=1620
  _globals['_LABELS']._serialized_start=1623
  _globals['_LABELS']._serialized_end=1758
  _globals['_LABELS_LABELSETENTRY']._serialized_start=1687
  _globals['_LABELS_LABELSETENTRY']._serialized_end=1758
  _globals['_ENTITY']._serialized_start=1760
  _globals['_ENTITY']._serialized_end=1836
  _globals['_ENTITIESGROUPSUMMARY']._serialized_start=1838
  _globals['_ENTITIESGROUPSUMMARY']._serialized_end=1906
  _globals['_ENTITIESGROUP']._serialized_start=1909
  _globals['_ENTITIESGROUP']._serialized_end=2102
  _globals['_ENTITIESGROUP_ENTITIESENTRY']._serialized_start=2033
  _globals['_ENTITIESGROUP_ENTITIESENTRY']._serialized_end=2102
  _globals['_DELETEDENTITIESGROUPS']._serialized_start=2104
  _globals['_DELETEDENTITIESGROUPS']._serialized_end=2152
  _globals['_ENTITIESGROUPS']._serialized_start=2155
  _globals['_ENTITIESGROUPS']._serialized_end=2330
  _globals['_ENTITIESGROUPS_ENTITIESGROUPSENTRY']._serialized_start=2248
  _globals['_ENTITIESGROUPS_ENTITIESGROUPSENTRY']._serialized_end=2330
  _globals['_ENTITYGROUPDUPLICATEINDEX']._serialized_start=2333
  _globals['_ENTITYGROUPDUPLICATEINDEX']._serialized_end=2832
  _globals['_ENTITYGROUPDUPLICATEINDEX_ENTITYDUPLICATES']._serialized_start=2448
  _globals['_ENTITYGROUPDUPLICATEINDEX_ENTITYDUPLICATES']._serialized_end=2486
  _globals['_ENTITYGROUPDUPLICATEINDEX_ENTITYGROUPDUPLICATES']._serialized_start=2489
  _globals['_ENTITYGROUPDUPLICATEINDEX_ENTITYGROUPDUPLICATES']._serialized_end=2714
  _globals['_ENTITYGROUPDUPLICATEINDEX_ENTITYGROUPDUPLICATES_ENTITIESENTRY']._serialized_start=2609
  _globals['_ENTITYGROUPDUPLICATEINDEX_ENTITYGROUPDUPLICATES_ENTITIESENTRY']._serialized_end=2714
  _globals['_ENTITYGROUPDUPLICATEINDEX_ENTITIESGROUPSENTRY']._serialized_start=2716
  _globals['_ENTITYGROUPDUPLICATEINDEX_ENTITIESGROUPSENTRY']._serialized_end=2832
  _globals['_VECTORSET']._serialized_start=2834
  _globals['_VECTORSET']._serialized_end=2909
  _globals['_VECTORSETS']._serialized_start=2912
  _globals['_VECTORSETS']._serialized_end=3062
  _globals['_VECTORSETS_VECTORSETSENTRY']._serialized_start=2988
  _globals['_VECTORSETS_VECTORSETSENTRY']._serialized_end=3062
  _globals['_TERMSYNONYMS']._serialized_start=3064
  _globals['_TERMSYNONYMS']._serialized_end=3096
  _globals['_SYNONYMS']._serialized_start=3099
  _globals['_SYNONYMS']._serialized_end=3233
  _globals['_SYNONYMS_TERMSENTRY']._serialized_start=3161
  _globals['_SYNONYMS_TERMSENTRY']._serialized_end=3233
  _globals['_SEMANTICMODELMETADATA']._serialized_start=3236
  _globals['_SEMANTICMODELMETADATA']._serialized_end=3419
  _globals['_KBCONFIGURATION']._serialized_start=3422
  _globals['_KBCONFIGURATION']._serialized_end=3562
# @@protoc_insertion_point(module_scope)
