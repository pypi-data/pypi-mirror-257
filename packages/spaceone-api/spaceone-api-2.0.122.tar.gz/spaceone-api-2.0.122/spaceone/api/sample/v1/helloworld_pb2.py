# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/sample/v1/helloworld.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\'spaceone/api/sample/v1/helloworld.proto\x12\x16spaceone.api.sample.v1\"\x1c\n\x0cHelloRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"\x1d\n\nHelloReply\x12\x0f\n\x07message\x18\x01 \x01(\t2e\n\nHelloWorld\x12W\n\tsay_hello\x12$.spaceone.api.sample.v1.HelloRequest\x1a\".spaceone.api.sample.v1.HelloReply\"\x00\x42=Z;github.com/cloudforet-io/api/dist/go/spaceone/api/sample/v1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'spaceone.api.sample.v1.helloworld_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z;github.com/cloudforet-io/api/dist/go/spaceone/api/sample/v1'
  _globals['_HELLOREQUEST']._serialized_start=67
  _globals['_HELLOREQUEST']._serialized_end=95
  _globals['_HELLOREPLY']._serialized_start=97
  _globals['_HELLOREPLY']._serialized_end=126
  _globals['_HELLOWORLD']._serialized_start=128
  _globals['_HELLOWORLD']._serialized_end=229
# @@protoc_insertion_point(module_scope)
