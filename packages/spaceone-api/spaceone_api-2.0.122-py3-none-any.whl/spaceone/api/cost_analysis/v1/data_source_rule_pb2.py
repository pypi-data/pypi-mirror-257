# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/cost_analysis/v1/data_source_rule.proto
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
from spaceone.api.core.v2 import query_pb2 as spaceone_dot_api_dot_core_dot_v2_dot_query__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n4spaceone/api/cost_analysis/v1/data_source_rule.proto\x12\x1dspaceone.api.cost_analysis.v1\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1cgoogle/api/annotations.proto\x1a spaceone/api/core/v2/query.proto\"G\n\x17\x44\x61taSourceRuleCondition\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\x12\x10\n\x08operator\x18\x03 \x01(\t\"+\n\tMatchRule\x12\x0e\n\x06source\x18\x01 \x01(\t\x12\x0e\n\x06target\x18\x02 \x01(\t\"\xef\x01\n\x15\x44\x61taSourceRuleActions\x12\x16\n\x0e\x63hange_project\x18\x01 \x01(\t\x12?\n\rmatch_project\x18\x02 \x01(\x0b\x32(.spaceone.api.cost_analysis.v1.MatchRule\x12G\n\x15match_service_account\x18\x03 \x01(\x0b\x32(.spaceone.api.cost_analysis.v1.MatchRule\x12\x34\n\x13\x61\x64\x64_additional_info\x18\x04 \x01(\x0b\x32\x17.google.protobuf.Struct\"0\n\x15\x44\x61taSourceRuleOptions\x12\x17\n\x0fstop_processing\x18\x01 \x01(\x08\"\xcd\x04\n\x1b\x43reateDataSourceRuleRequest\x12\x16\n\x0e\x64\x61ta_source_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12J\n\nconditions\x18\x03 \x03(\x0b\x32\x36.spaceone.api.cost_analysis.v1.DataSourceRuleCondition\x12J\n\x11\x63onditions_policy\x18\x04 \x01(\x0e\x32/.spaceone.api.cost_analysis.v1.ConditionsPolicy\x12\x45\n\x07\x61\x63tions\x18\x05 \x01(\x0b\x32\x34.spaceone.api.cost_analysis.v1.DataSourceRuleActions\x12\x45\n\x07options\x18\x06 \x01(\x0b\x32\x34.spaceone.api.cost_analysis.v1.DataSourceRuleOptions\x12%\n\x04tags\x18\x07 \x01(\x0b\x32\x17.google.protobuf.Struct\x12`\n\x0eresource_group\x18\x14 \x01(\x0e\x32H.spaceone.api.cost_analysis.v1.CreateDataSourceRuleRequest.ResourceGroup\x12\x14\n\x0cworkspace_id\x18\x15 \x01(\t\"C\n\rResourceGroup\x12\x17\n\x13RESOURCE_GROUP_NONE\x10\x00\x12\n\n\x06\x44OMAIN\x10\x01\x12\r\n\tWORKSPACE\x10\x02\"\x95\x03\n\x1bUpdateDataSourceRuleRequest\x12\x1b\n\x13\x64\x61ta_source_rule_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12J\n\nconditions\x18\x03 \x03(\x0b\x32\x36.spaceone.api.cost_analysis.v1.DataSourceRuleCondition\x12J\n\x11\x63onditions_policy\x18\x04 \x01(\x0e\x32/.spaceone.api.cost_analysis.v1.ConditionsPolicy\x12\x45\n\x07\x61\x63tions\x18\x05 \x01(\x0b\x32\x34.spaceone.api.cost_analysis.v1.DataSourceRuleActions\x12\x45\n\x07options\x18\x06 \x01(\x0b\x32\x34.spaceone.api.cost_analysis.v1.DataSourceRuleOptions\x12%\n\x04tags\x18\x07 \x01(\x0b\x32\x17.google.protobuf.Struct\"N\n ChangeDataSourceRuleOrderRequest\x12\x1b\n\x13\x64\x61ta_source_rule_id\x18\x01 \x01(\t\x12\r\n\x05order\x18\x02 \x01(\x05\"4\n\x15\x44\x61taSourceRuleRequest\x12\x1b\n\x13\x64\x61ta_source_rule_id\x18\x01 \x01(\t\"\xa3\x02\n\x13\x44\x61taSourceRuleQuery\x12*\n\x05query\x18\x01 \x01(\x0b\x32\x1b.spaceone.api.core.v2.Query\x12\x1b\n\x13\x64\x61ta_source_rule_id\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12N\n\trule_type\x18\x04 \x01(\x0e\x32;.spaceone.api.cost_analysis.v1.DataSourceRuleQuery.RuleType\x12\x14\n\x0cworkspace_id\x18\x15 \x01(\t\x12\x16\n\x0e\x64\x61ta_source_id\x18\x16 \x01(\t\"7\n\x08RuleType\x12\x12\n\x0eRULE_TYPE_NONE\x10\x00\x12\x0b\n\x07MANAGED\x10\x01\x12\n\n\x06\x43USTOM\x10\x02\"\x96\x06\n\x12\x44\x61taSourceRuleInfo\x12\x1b\n\x13\x64\x61ta_source_rule_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12M\n\trule_type\x18\x03 \x01(\x0e\x32:.spaceone.api.cost_analysis.v1.DataSourceRuleInfo.RuleType\x12\r\n\x05order\x18\x04 \x01(\x05\x12J\n\nconditions\x18\x05 \x03(\x0b\x32\x36.spaceone.api.cost_analysis.v1.DataSourceRuleCondition\x12J\n\x11\x63onditions_policy\x18\x06 \x01(\x0e\x32/.spaceone.api.cost_analysis.v1.ConditionsPolicy\x12\x45\n\x07\x61\x63tions\x18\x07 \x01(\x0b\x32\x34.spaceone.api.cost_analysis.v1.DataSourceRuleActions\x12\x45\n\x07options\x18\x08 \x01(\x0b\x32\x34.spaceone.api.cost_analysis.v1.DataSourceRuleOptions\x12%\n\x04tags\x18\t \x01(\x0b\x32\x17.google.protobuf.Struct\x12W\n\x0eresource_group\x18\x14 \x01(\x0e\x32?.spaceone.api.cost_analysis.v1.DataSourceRuleInfo.ResourceGroup\x12\x11\n\tdomain_id\x18\x15 \x01(\t\x12\x14\n\x0cworkspace_id\x18\x16 \x01(\t\x12\x16\n\x0e\x64\x61ta_source_id\x18\x17 \x01(\t\x12\x12\n\ncreated_at\x18\x1f \x01(\t\"C\n\rResourceGroup\x12\x17\n\x13RESOURCE_GROUP_NONE\x10\x00\x12\n\n\x06\x44OMAIN\x10\x01\x12\r\n\tWORKSPACE\x10\x02\"7\n\x08RuleType\x12\x12\n\x0eRULE_TYPE_NONE\x10\x00\x12\x0b\n\x07MANAGED\x10\x01\x12\n\n\x06\x43USTOM\x10\x02\"n\n\x13\x44\x61taSourceRulesInfo\x12\x42\n\x07results\x18\x01 \x03(\x0b\x32\x31.spaceone.api.cost_analysis.v1.DataSourceRuleInfo\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05\"O\n\x17\x44\x61taSourceRuleStatQuery\x12\x34\n\x05query\x18\x01 \x01(\x0b\x32%.spaceone.api.core.v2.StatisticsQuery*:\n\x10\x43onditionsPolicy\x12\x08\n\x04NONE\x10\x00\x12\x07\n\x03\x41LL\x10\x01\x12\x07\n\x03\x41NY\x10\x02\x12\n\n\x06\x41LWAYS\x10\x03\x32\x97\t\n\x0e\x44\x61taSourceRule\x12\xad\x01\n\x06\x63reate\x12:.spaceone.api.cost_analysis.v1.CreateDataSourceRuleRequest\x1a\x31.spaceone.api.cost_analysis.v1.DataSourceRuleInfo\"4\x82\xd3\xe4\x93\x02.\")/cost-analysis/v1/data-source-rule/create:\x01*\x12\xad\x01\n\x06update\x12:.spaceone.api.cost_analysis.v1.UpdateDataSourceRuleRequest\x1a\x31.spaceone.api.cost_analysis.v1.DataSourceRuleInfo\"4\x82\xd3\xe4\x93\x02.\")/cost-analysis/v1/data-source-rule/update:\x01*\x12\xbe\x01\n\x0c\x63hange_order\x12?.spaceone.api.cost_analysis.v1.ChangeDataSourceRuleOrderRequest\x1a\x31.spaceone.api.cost_analysis.v1.DataSourceRuleInfo\":\x82\xd3\xe4\x93\x02\x34\"//cost-analysis/v1/data-source-rule/change-order:\x01*\x12\x8c\x01\n\x06\x64\x65lete\x12\x34.spaceone.api.cost_analysis.v1.DataSourceRuleRequest\x1a\x16.google.protobuf.Empty\"4\x82\xd3\xe4\x93\x02.\")/cost-analysis/v1/data-source-rule/delete:\x01*\x12\xa1\x01\n\x03get\x12\x34.spaceone.api.cost_analysis.v1.DataSourceRuleRequest\x1a\x31.spaceone.api.cost_analysis.v1.DataSourceRuleInfo\"1\x82\xd3\xe4\x93\x02+\"&/cost-analysis/v1/data-source-rule/get:\x01*\x12\xa2\x01\n\x04list\x12\x32.spaceone.api.cost_analysis.v1.DataSourceRuleQuery\x1a\x32.spaceone.api.cost_analysis.v1.DataSourceRulesInfo\"2\x82\xd3\xe4\x93\x02,\"\'/cost-analysis/v1/data-source-rule/list:\x01*\x12\x8b\x01\n\x04stat\x12\x36.spaceone.api.cost_analysis.v1.DataSourceRuleStatQuery\x1a\x17.google.protobuf.Struct\"2\x82\xd3\xe4\x93\x02,\"\'/cost-analysis/v1/data-source-rule/stat:\x01*BDZBgithub.com/cloudforet-io/api/dist/go/spaceone/api/cost_analysis/v1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'spaceone.api.cost_analysis.v1.data_source_rule_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'ZBgithub.com/cloudforet-io/api/dist/go/spaceone/api/cost_analysis/v1'
  _globals['_DATASOURCERULE'].methods_by_name['create']._options = None
  _globals['_DATASOURCERULE'].methods_by_name['create']._serialized_options = b'\202\323\344\223\002.\")/cost-analysis/v1/data-source-rule/create:\001*'
  _globals['_DATASOURCERULE'].methods_by_name['update']._options = None
  _globals['_DATASOURCERULE'].methods_by_name['update']._serialized_options = b'\202\323\344\223\002.\")/cost-analysis/v1/data-source-rule/update:\001*'
  _globals['_DATASOURCERULE'].methods_by_name['change_order']._options = None
  _globals['_DATASOURCERULE'].methods_by_name['change_order']._serialized_options = b'\202\323\344\223\0024\"//cost-analysis/v1/data-source-rule/change-order:\001*'
  _globals['_DATASOURCERULE'].methods_by_name['delete']._options = None
  _globals['_DATASOURCERULE'].methods_by_name['delete']._serialized_options = b'\202\323\344\223\002.\")/cost-analysis/v1/data-source-rule/delete:\001*'
  _globals['_DATASOURCERULE'].methods_by_name['get']._options = None
  _globals['_DATASOURCERULE'].methods_by_name['get']._serialized_options = b'\202\323\344\223\002+\"&/cost-analysis/v1/data-source-rule/get:\001*'
  _globals['_DATASOURCERULE'].methods_by_name['list']._options = None
  _globals['_DATASOURCERULE'].methods_by_name['list']._serialized_options = b'\202\323\344\223\002,\"\'/cost-analysis/v1/data-source-rule/list:\001*'
  _globals['_DATASOURCERULE'].methods_by_name['stat']._options = None
  _globals['_DATASOURCERULE'].methods_by_name['stat']._serialized_options = b'\202\323\344\223\002,\"\'/cost-analysis/v1/data-source-rule/stat:\001*'
  _globals['_CONDITIONSPOLICY']._serialized_start=3034
  _globals['_CONDITIONSPOLICY']._serialized_end=3092
  _globals['_DATASOURCERULECONDITION']._serialized_start=210
  _globals['_DATASOURCERULECONDITION']._serialized_end=281
  _globals['_MATCHRULE']._serialized_start=283
  _globals['_MATCHRULE']._serialized_end=326
  _globals['_DATASOURCERULEACTIONS']._serialized_start=329
  _globals['_DATASOURCERULEACTIONS']._serialized_end=568
  _globals['_DATASOURCERULEOPTIONS']._serialized_start=570
  _globals['_DATASOURCERULEOPTIONS']._serialized_end=618
  _globals['_CREATEDATASOURCERULEREQUEST']._serialized_start=621
  _globals['_CREATEDATASOURCERULEREQUEST']._serialized_end=1210
  _globals['_CREATEDATASOURCERULEREQUEST_RESOURCEGROUP']._serialized_start=1143
  _globals['_CREATEDATASOURCERULEREQUEST_RESOURCEGROUP']._serialized_end=1210
  _globals['_UPDATEDATASOURCERULEREQUEST']._serialized_start=1213
  _globals['_UPDATEDATASOURCERULEREQUEST']._serialized_end=1618
  _globals['_CHANGEDATASOURCERULEORDERREQUEST']._serialized_start=1620
  _globals['_CHANGEDATASOURCERULEORDERREQUEST']._serialized_end=1698
  _globals['_DATASOURCERULEREQUEST']._serialized_start=1700
  _globals['_DATASOURCERULEREQUEST']._serialized_end=1752
  _globals['_DATASOURCERULEQUERY']._serialized_start=1755
  _globals['_DATASOURCERULEQUERY']._serialized_end=2046
  _globals['_DATASOURCERULEQUERY_RULETYPE']._serialized_start=1991
  _globals['_DATASOURCERULEQUERY_RULETYPE']._serialized_end=2046
  _globals['_DATASOURCERULEINFO']._serialized_start=2049
  _globals['_DATASOURCERULEINFO']._serialized_end=2839
  _globals['_DATASOURCERULEINFO_RESOURCEGROUP']._serialized_start=1143
  _globals['_DATASOURCERULEINFO_RESOURCEGROUP']._serialized_end=1210
  _globals['_DATASOURCERULEINFO_RULETYPE']._serialized_start=1991
  _globals['_DATASOURCERULEINFO_RULETYPE']._serialized_end=2046
  _globals['_DATASOURCERULESINFO']._serialized_start=2841
  _globals['_DATASOURCERULESINFO']._serialized_end=2951
  _globals['_DATASOURCERULESTATQUERY']._serialized_start=2953
  _globals['_DATASOURCERULESTATQUERY']._serialized_end=3032
  _globals['_DATASOURCERULE']._serialized_start=3095
  _globals['_DATASOURCERULE']._serialized_end=4270
# @@protoc_insertion_point(module_scope)
