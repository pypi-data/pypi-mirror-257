# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/repository/v1/repository.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n+spaceone/api/repository/v1/repository.proto\x12\x1aspaceone.api.repository.v1\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1cgoogle/api/annotations.proto\"A\n\x0fRepositoryQuery\x12\x15\n\rrepository_id\x18\x01 \x01(\t\x12\x17\n\x0frepository_type\x18\x02 \x01(\t\"`\n\x0eRepositoryInfo\x12\x15\n\rrepository_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x17\n\x0frepository_type\x18\x03 \x01(\t\x12\x10\n\x08\x65ndpoint\x18\x04 \x01(\t\"d\n\x10RepositoriesInfo\x12;\n\x07results\x18\x01 \x03(\x0b\x32*.spaceone.api.repository.v1.RepositoryInfo\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05\x32\x9b\x01\n\nRepository\x12\x8c\x01\n\x04list\x12+.spaceone.api.repository.v1.RepositoryQuery\x1a,.spaceone.api.repository.v1.RepositoriesInfo\")\x82\xd3\xe4\x93\x02#\"\x1e/repository/v1/repository/list:\x01*BAZ?github.com/cloudforet-io/api/dist/go/spaceone/api/repository/v1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'spaceone.api.repository.v1.repository_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z?github.com/cloudforet-io/api/dist/go/spaceone/api/repository/v1'
  _globals['_REPOSITORY'].methods_by_name['list']._options = None
  _globals['_REPOSITORY'].methods_by_name['list']._serialized_options = b'\202\323\344\223\002#\"\036/repository/v1/repository/list:\001*'
  _globals['_REPOSITORYQUERY']._serialized_start=164
  _globals['_REPOSITORYQUERY']._serialized_end=229
  _globals['_REPOSITORYINFO']._serialized_start=231
  _globals['_REPOSITORYINFO']._serialized_end=327
  _globals['_REPOSITORIESINFO']._serialized_start=329
  _globals['_REPOSITORIESINFO']._serialized_end=429
  _globals['_REPOSITORY']._serialized_start=432
  _globals['_REPOSITORY']._serialized_end=587
# @@protoc_insertion_point(module_scope)
