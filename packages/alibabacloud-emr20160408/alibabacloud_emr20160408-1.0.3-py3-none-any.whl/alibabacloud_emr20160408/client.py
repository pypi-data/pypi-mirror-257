# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from typing import Dict
from Tea.core import TeaCore

from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_endpoint_util.client import Client as EndpointUtilClient
from alibabacloud_emr20160408 import models as emr_20160408_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_openapi_util.client import Client as OpenApiUtilClient


class Client(OpenApiClient):
    """
    *\
    """
    def __init__(
        self, 
        config: open_api_models.Config,
    ):
        super().__init__(config)
        self._endpoint_rule = 'regional'
        self._endpoint_map = {
            'cn-beijing': 'emr.aliyuncs.com',
            'cn-hangzhou': 'emr.aliyuncs.com',
            'cn-shanghai': 'emr.aliyuncs.com',
            'cn-shenzhen': 'emr.aliyuncs.com',
            'ap-southeast-1': 'emr.aliyuncs.com',
            'us-west-1': 'emr.aliyuncs.com',
            'cn-hangzhou-finance': 'emr.aliyuncs.com',
            'cn-shenzhen-finance-1': 'emr.aliyuncs.com',
            'cn-shanghai-finance-1': 'emr.aliyuncs.com'
        }
        self.check_config(config)
        self._endpoint = self.get_endpoint('emr', self._region_id, self._endpoint_rule, self._network, self._suffix, self._endpoint_map, self._endpoint)

    def get_endpoint(
        self,
        product_id: str,
        region_id: str,
        endpoint_rule: str,
        network: str,
        suffix: str,
        endpoint_map: Dict[str, str],
        endpoint: str,
    ) -> str:
        if not UtilClient.empty(endpoint):
            return endpoint
        if not UtilClient.is_unset(endpoint_map) and not UtilClient.empty(endpoint_map.get(region_id)):
            return endpoint_map.get(region_id)
        return EndpointUtilClient.get_endpoint_rules(product_id, region_id, endpoint_rule, network, suffix)

    def add_cluster_service_with_options(
        self,
        request: emr_20160408_models.AddClusterServiceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.AddClusterServiceResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.comment):
            query['Comment'] = request.comment
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.service):
            query['Service'] = request.service
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='AddClusterService',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.AddClusterServiceResponse(),
            self.call_api(params, req, runtime)
        )

    async def add_cluster_service_with_options_async(
        self,
        request: emr_20160408_models.AddClusterServiceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.AddClusterServiceResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.comment):
            query['Comment'] = request.comment
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.service):
            query['Service'] = request.service
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='AddClusterService',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.AddClusterServiceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def add_cluster_service(
        self,
        request: emr_20160408_models.AddClusterServiceRequest,
    ) -> emr_20160408_models.AddClusterServiceResponse:
        runtime = util_models.RuntimeOptions()
        return self.add_cluster_service_with_options(request, runtime)

    async def add_cluster_service_async(
        self,
        request: emr_20160408_models.AddClusterServiceRequest,
    ) -> emr_20160408_models.AddClusterServiceResponse:
        runtime = util_models.RuntimeOptions()
        return await self.add_cluster_service_with_options_async(request, runtime)

    def add_scaling_config_item_v2with_options(
        self,
        request: emr_20160408_models.AddScalingConfigItemV2Request,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.AddScalingConfigItemV2Response:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.config_item_information):
            query['ConfigItemInformation'] = request.config_item_information
        if not UtilClient.is_unset(request.config_item_type):
            query['ConfigItemType'] = request.config_item_type
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.scaling_group_biz_id):
            query['ScalingGroupBizId'] = request.scaling_group_biz_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='AddScalingConfigItemV2',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.AddScalingConfigItemV2Response(),
            self.call_api(params, req, runtime)
        )

    async def add_scaling_config_item_v2with_options_async(
        self,
        request: emr_20160408_models.AddScalingConfigItemV2Request,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.AddScalingConfigItemV2Response:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.config_item_information):
            query['ConfigItemInformation'] = request.config_item_information
        if not UtilClient.is_unset(request.config_item_type):
            query['ConfigItemType'] = request.config_item_type
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.scaling_group_biz_id):
            query['ScalingGroupBizId'] = request.scaling_group_biz_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='AddScalingConfigItemV2',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.AddScalingConfigItemV2Response(),
            await self.call_api_async(params, req, runtime)
        )

    def add_scaling_config_item_v2(
        self,
        request: emr_20160408_models.AddScalingConfigItemV2Request,
    ) -> emr_20160408_models.AddScalingConfigItemV2Response:
        runtime = util_models.RuntimeOptions()
        return self.add_scaling_config_item_v2with_options(request, runtime)

    async def add_scaling_config_item_v2_async(
        self,
        request: emr_20160408_models.AddScalingConfigItemV2Request,
    ) -> emr_20160408_models.AddScalingConfigItemV2Response:
        runtime = util_models.RuntimeOptions()
        return await self.add_scaling_config_item_v2with_options_async(request, runtime)

    def clone_flow_with_options(
        self,
        request: emr_20160408_models.CloneFlowRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.CloneFlowResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CloneFlow',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.CloneFlowResponse(),
            self.call_api(params, req, runtime)
        )

    async def clone_flow_with_options_async(
        self,
        request: emr_20160408_models.CloneFlowRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.CloneFlowResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CloneFlow',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.CloneFlowResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def clone_flow(
        self,
        request: emr_20160408_models.CloneFlowRequest,
    ) -> emr_20160408_models.CloneFlowResponse:
        runtime = util_models.RuntimeOptions()
        return self.clone_flow_with_options(request, runtime)

    async def clone_flow_async(
        self,
        request: emr_20160408_models.CloneFlowRequest,
    ) -> emr_20160408_models.CloneFlowResponse:
        runtime = util_models.RuntimeOptions()
        return await self.clone_flow_with_options_async(request, runtime)

    def clone_flow_job_with_options(
        self,
        request: emr_20160408_models.CloneFlowJobRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.CloneFlowJobResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CloneFlowJob',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.CloneFlowJobResponse(),
            self.call_api(params, req, runtime)
        )

    async def clone_flow_job_with_options_async(
        self,
        request: emr_20160408_models.CloneFlowJobRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.CloneFlowJobResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CloneFlowJob',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.CloneFlowJobResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def clone_flow_job(
        self,
        request: emr_20160408_models.CloneFlowJobRequest,
    ) -> emr_20160408_models.CloneFlowJobResponse:
        runtime = util_models.RuntimeOptions()
        return self.clone_flow_job_with_options(request, runtime)

    async def clone_flow_job_async(
        self,
        request: emr_20160408_models.CloneFlowJobRequest,
    ) -> emr_20160408_models.CloneFlowJobResponse:
        runtime = util_models.RuntimeOptions()
        return await self.clone_flow_job_with_options_async(request, runtime)

    def create_cluster_host_group_with_options(
        self,
        request: emr_20160408_models.CreateClusterHostGroupRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.CreateClusterHostGroupResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.comment):
            query['Comment'] = request.comment
        if not UtilClient.is_unset(request.host_group_name):
            query['HostGroupName'] = request.host_group_name
        if not UtilClient.is_unset(request.host_group_params):
            query['HostGroupParams'] = request.host_group_params
        if not UtilClient.is_unset(request.host_group_type):
            query['HostGroupType'] = request.host_group_type
        if not UtilClient.is_unset(request.pay_type):
            query['PayType'] = request.pay_type
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_group_id):
            query['SecurityGroupId'] = request.security_group_id
        if not UtilClient.is_unset(request.vswitch_id):
            query['VswitchId'] = request.vswitch_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateClusterHostGroup',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.CreateClusterHostGroupResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_cluster_host_group_with_options_async(
        self,
        request: emr_20160408_models.CreateClusterHostGroupRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.CreateClusterHostGroupResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.comment):
            query['Comment'] = request.comment
        if not UtilClient.is_unset(request.host_group_name):
            query['HostGroupName'] = request.host_group_name
        if not UtilClient.is_unset(request.host_group_params):
            query['HostGroupParams'] = request.host_group_params
        if not UtilClient.is_unset(request.host_group_type):
            query['HostGroupType'] = request.host_group_type
        if not UtilClient.is_unset(request.pay_type):
            query['PayType'] = request.pay_type
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_group_id):
            query['SecurityGroupId'] = request.security_group_id
        if not UtilClient.is_unset(request.vswitch_id):
            query['VswitchId'] = request.vswitch_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateClusterHostGroup',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.CreateClusterHostGroupResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_cluster_host_group(
        self,
        request: emr_20160408_models.CreateClusterHostGroupRequest,
    ) -> emr_20160408_models.CreateClusterHostGroupResponse:
        runtime = util_models.RuntimeOptions()
        return self.create_cluster_host_group_with_options(request, runtime)

    async def create_cluster_host_group_async(
        self,
        request: emr_20160408_models.CreateClusterHostGroupRequest,
    ) -> emr_20160408_models.CreateClusterHostGroupResponse:
        runtime = util_models.RuntimeOptions()
        return await self.create_cluster_host_group_with_options_async(request, runtime)

    def create_cluster_template_with_options(
        self,
        request: emr_20160408_models.CreateClusterTemplateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.CreateClusterTemplateResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auto_renew):
            query['AutoRenew'] = request.auto_renew
        if not UtilClient.is_unset(request.bootstrap_action):
            query['BootstrapAction'] = request.bootstrap_action
        if not UtilClient.is_unset(request.client_token):
            query['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.cluster_type):
            query['ClusterType'] = request.cluster_type
        if not UtilClient.is_unset(request.config):
            query['Config'] = request.config
        if not UtilClient.is_unset(request.configurations):
            query['Configurations'] = request.configurations
        if not UtilClient.is_unset(request.data_disk_encrypted):
            query['DataDiskEncrypted'] = request.data_disk_encrypted
        if not UtilClient.is_unset(request.data_disk_kmskey_id):
            query['DataDiskKMSKeyId'] = request.data_disk_kmskey_id
        if not UtilClient.is_unset(request.deposit_type):
            query['DepositType'] = request.deposit_type
        if not UtilClient.is_unset(request.eas_enable):
            query['EasEnable'] = request.eas_enable
        if not UtilClient.is_unset(request.emr_ver):
            query['EmrVer'] = request.emr_ver
        if not UtilClient.is_unset(request.high_availability_enable):
            query['HighAvailabilityEnable'] = request.high_availability_enable
        if not UtilClient.is_unset(request.host_group):
            query['HostGroup'] = request.host_group
        if not UtilClient.is_unset(request.init_custom_hive_meta_db):
            query['InitCustomHiveMetaDb'] = request.init_custom_hive_meta_db
        if not UtilClient.is_unset(request.instance_generation):
            query['InstanceGeneration'] = request.instance_generation
        if not UtilClient.is_unset(request.io_optimized):
            query['IoOptimized'] = request.io_optimized
        if not UtilClient.is_unset(request.is_open_public_ip):
            query['IsOpenPublicIp'] = request.is_open_public_ip
        if not UtilClient.is_unset(request.key_pair_name):
            query['KeyPairName'] = request.key_pair_name
        if not UtilClient.is_unset(request.log_path):
            query['LogPath'] = request.log_path
        if not UtilClient.is_unset(request.machine_type):
            query['MachineType'] = request.machine_type
        if not UtilClient.is_unset(request.master_pwd):
            query['MasterPwd'] = request.master_pwd
        if not UtilClient.is_unset(request.meta_store_conf):
            query['MetaStoreConf'] = request.meta_store_conf
        if not UtilClient.is_unset(request.meta_store_type):
            query['MetaStoreType'] = request.meta_store_type
        if not UtilClient.is_unset(request.net_type):
            query['NetType'] = request.net_type
        if not UtilClient.is_unset(request.option_soft_ware_list):
            query['OptionSoftWareList'] = request.option_soft_ware_list
        if not UtilClient.is_unset(request.period):
            query['Period'] = request.period
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_group_id):
            query['SecurityGroupId'] = request.security_group_id
        if not UtilClient.is_unset(request.security_group_name):
            query['SecurityGroupName'] = request.security_group_name
        if not UtilClient.is_unset(request.ssh_enable):
            query['SshEnable'] = request.ssh_enable
        if not UtilClient.is_unset(request.tag):
            query['Tag'] = request.tag
        if not UtilClient.is_unset(request.template_name):
            query['TemplateName'] = request.template_name
        if not UtilClient.is_unset(request.use_custom_hive_meta_db):
            query['UseCustomHiveMetaDb'] = request.use_custom_hive_meta_db
        if not UtilClient.is_unset(request.use_local_meta_db):
            query['UseLocalMetaDb'] = request.use_local_meta_db
        if not UtilClient.is_unset(request.user_defined_emr_ecs_role):
            query['UserDefinedEmrEcsRole'] = request.user_defined_emr_ecs_role
        if not UtilClient.is_unset(request.v_switch_id):
            query['VSwitchId'] = request.v_switch_id
        if not UtilClient.is_unset(request.vpc_id):
            query['VpcId'] = request.vpc_id
        if not UtilClient.is_unset(request.zone_id):
            query['ZoneId'] = request.zone_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateClusterTemplate',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.CreateClusterTemplateResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_cluster_template_with_options_async(
        self,
        request: emr_20160408_models.CreateClusterTemplateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.CreateClusterTemplateResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auto_renew):
            query['AutoRenew'] = request.auto_renew
        if not UtilClient.is_unset(request.bootstrap_action):
            query['BootstrapAction'] = request.bootstrap_action
        if not UtilClient.is_unset(request.client_token):
            query['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.cluster_type):
            query['ClusterType'] = request.cluster_type
        if not UtilClient.is_unset(request.config):
            query['Config'] = request.config
        if not UtilClient.is_unset(request.configurations):
            query['Configurations'] = request.configurations
        if not UtilClient.is_unset(request.data_disk_encrypted):
            query['DataDiskEncrypted'] = request.data_disk_encrypted
        if not UtilClient.is_unset(request.data_disk_kmskey_id):
            query['DataDiskKMSKeyId'] = request.data_disk_kmskey_id
        if not UtilClient.is_unset(request.deposit_type):
            query['DepositType'] = request.deposit_type
        if not UtilClient.is_unset(request.eas_enable):
            query['EasEnable'] = request.eas_enable
        if not UtilClient.is_unset(request.emr_ver):
            query['EmrVer'] = request.emr_ver
        if not UtilClient.is_unset(request.high_availability_enable):
            query['HighAvailabilityEnable'] = request.high_availability_enable
        if not UtilClient.is_unset(request.host_group):
            query['HostGroup'] = request.host_group
        if not UtilClient.is_unset(request.init_custom_hive_meta_db):
            query['InitCustomHiveMetaDb'] = request.init_custom_hive_meta_db
        if not UtilClient.is_unset(request.instance_generation):
            query['InstanceGeneration'] = request.instance_generation
        if not UtilClient.is_unset(request.io_optimized):
            query['IoOptimized'] = request.io_optimized
        if not UtilClient.is_unset(request.is_open_public_ip):
            query['IsOpenPublicIp'] = request.is_open_public_ip
        if not UtilClient.is_unset(request.key_pair_name):
            query['KeyPairName'] = request.key_pair_name
        if not UtilClient.is_unset(request.log_path):
            query['LogPath'] = request.log_path
        if not UtilClient.is_unset(request.machine_type):
            query['MachineType'] = request.machine_type
        if not UtilClient.is_unset(request.master_pwd):
            query['MasterPwd'] = request.master_pwd
        if not UtilClient.is_unset(request.meta_store_conf):
            query['MetaStoreConf'] = request.meta_store_conf
        if not UtilClient.is_unset(request.meta_store_type):
            query['MetaStoreType'] = request.meta_store_type
        if not UtilClient.is_unset(request.net_type):
            query['NetType'] = request.net_type
        if not UtilClient.is_unset(request.option_soft_ware_list):
            query['OptionSoftWareList'] = request.option_soft_ware_list
        if not UtilClient.is_unset(request.period):
            query['Period'] = request.period
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_group_id):
            query['SecurityGroupId'] = request.security_group_id
        if not UtilClient.is_unset(request.security_group_name):
            query['SecurityGroupName'] = request.security_group_name
        if not UtilClient.is_unset(request.ssh_enable):
            query['SshEnable'] = request.ssh_enable
        if not UtilClient.is_unset(request.tag):
            query['Tag'] = request.tag
        if not UtilClient.is_unset(request.template_name):
            query['TemplateName'] = request.template_name
        if not UtilClient.is_unset(request.use_custom_hive_meta_db):
            query['UseCustomHiveMetaDb'] = request.use_custom_hive_meta_db
        if not UtilClient.is_unset(request.use_local_meta_db):
            query['UseLocalMetaDb'] = request.use_local_meta_db
        if not UtilClient.is_unset(request.user_defined_emr_ecs_role):
            query['UserDefinedEmrEcsRole'] = request.user_defined_emr_ecs_role
        if not UtilClient.is_unset(request.v_switch_id):
            query['VSwitchId'] = request.v_switch_id
        if not UtilClient.is_unset(request.vpc_id):
            query['VpcId'] = request.vpc_id
        if not UtilClient.is_unset(request.zone_id):
            query['ZoneId'] = request.zone_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateClusterTemplate',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.CreateClusterTemplateResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_cluster_template(
        self,
        request: emr_20160408_models.CreateClusterTemplateRequest,
    ) -> emr_20160408_models.CreateClusterTemplateResponse:
        runtime = util_models.RuntimeOptions()
        return self.create_cluster_template_with_options(request, runtime)

    async def create_cluster_template_async(
        self,
        request: emr_20160408_models.CreateClusterTemplateRequest,
    ) -> emr_20160408_models.CreateClusterTemplateResponse:
        runtime = util_models.RuntimeOptions()
        return await self.create_cluster_template_with_options_async(request, runtime)

    def create_cluster_v2with_options(
        self,
        request: emr_20160408_models.CreateClusterV2Request,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.CreateClusterV2Response:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.authorize_content):
            query['AuthorizeContent'] = request.authorize_content
        if not UtilClient.is_unset(request.auto_pay_order):
            query['AutoPayOrder'] = request.auto_pay_order
        if not UtilClient.is_unset(request.auto_renew):
            query['AutoRenew'] = request.auto_renew
        if not UtilClient.is_unset(request.bootstrap_action):
            query['BootstrapAction'] = request.bootstrap_action
        if not UtilClient.is_unset(request.charge_type):
            query['ChargeType'] = request.charge_type
        if not UtilClient.is_unset(request.click_house_conf):
            query['ClickHouseConf'] = request.click_house_conf
        if not UtilClient.is_unset(request.client_token):
            query['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.cluster_type):
            query['ClusterType'] = request.cluster_type
        if not UtilClient.is_unset(request.config):
            query['Config'] = request.config
        if not UtilClient.is_unset(request.configurations):
            query['Configurations'] = request.configurations
        if not UtilClient.is_unset(request.data_disk_encrypted):
            query['DataDiskEncrypted'] = request.data_disk_encrypted
        if not UtilClient.is_unset(request.data_disk_kmskey_id):
            query['DataDiskKMSKeyId'] = request.data_disk_kmskey_id
        if not UtilClient.is_unset(request.deposit_type):
            query['DepositType'] = request.deposit_type
        if not UtilClient.is_unset(request.eas_enable):
            query['EasEnable'] = request.eas_enable
        if not UtilClient.is_unset(request.emr_ver):
            query['EmrVer'] = request.emr_ver
        if not UtilClient.is_unset(request.extra_attributes):
            query['ExtraAttributes'] = request.extra_attributes
        if not UtilClient.is_unset(request.high_availability_enable):
            query['HighAvailabilityEnable'] = request.high_availability_enable
        if not UtilClient.is_unset(request.host_component_info):
            query['HostComponentInfo'] = request.host_component_info
        if not UtilClient.is_unset(request.host_group):
            query['HostGroup'] = request.host_group
        if not UtilClient.is_unset(request.init_custom_hive_meta_db):
            query['InitCustomHiveMetaDB'] = request.init_custom_hive_meta_db
        if not UtilClient.is_unset(request.instance_generation):
            query['InstanceGeneration'] = request.instance_generation
        if not UtilClient.is_unset(request.io_optimized):
            query['IoOptimized'] = request.io_optimized
        if not UtilClient.is_unset(request.is_open_public_ip):
            query['IsOpenPublicIp'] = request.is_open_public_ip
        if not UtilClient.is_unset(request.key_pair_name):
            query['KeyPairName'] = request.key_pair_name
        if not UtilClient.is_unset(request.log_path):
            query['LogPath'] = request.log_path
        if not UtilClient.is_unset(request.machine_type):
            query['MachineType'] = request.machine_type
        if not UtilClient.is_unset(request.master_pwd):
            query['MasterPwd'] = request.master_pwd
        if not UtilClient.is_unset(request.meta_store_conf):
            query['MetaStoreConf'] = request.meta_store_conf
        if not UtilClient.is_unset(request.meta_store_type):
            query['MetaStoreType'] = request.meta_store_type
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.net_type):
            query['NetType'] = request.net_type
        if not UtilClient.is_unset(request.option_soft_ware_list):
            query['OptionSoftWareList'] = request.option_soft_ware_list
        if not UtilClient.is_unset(request.period):
            query['Period'] = request.period
        if not UtilClient.is_unset(request.promotion_info):
            query['PromotionInfo'] = request.promotion_info
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.related_cluster_id):
            query['RelatedClusterId'] = request.related_cluster_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_group_id):
            query['SecurityGroupId'] = request.security_group_id
        if not UtilClient.is_unset(request.security_group_name):
            query['SecurityGroupName'] = request.security_group_name
        if not UtilClient.is_unset(request.service_info):
            query['ServiceInfo'] = request.service_info
        if not UtilClient.is_unset(request.ssh_enable):
            query['SshEnable'] = request.ssh_enable
        if not UtilClient.is_unset(request.tag):
            query['Tag'] = request.tag
        if not UtilClient.is_unset(request.use_custom_hive_meta_db):
            query['UseCustomHiveMetaDB'] = request.use_custom_hive_meta_db
        if not UtilClient.is_unset(request.use_local_meta_db):
            query['UseLocalMetaDb'] = request.use_local_meta_db
        if not UtilClient.is_unset(request.user_defined_emr_ecs_role):
            query['UserDefinedEmrEcsRole'] = request.user_defined_emr_ecs_role
        if not UtilClient.is_unset(request.user_info):
            query['UserInfo'] = request.user_info
        if not UtilClient.is_unset(request.v_switch_id):
            query['VSwitchId'] = request.v_switch_id
        if not UtilClient.is_unset(request.vpc_id):
            query['VpcId'] = request.vpc_id
        if not UtilClient.is_unset(request.white_list_type):
            query['WhiteListType'] = request.white_list_type
        if not UtilClient.is_unset(request.zone_id):
            query['ZoneId'] = request.zone_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateClusterV2',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.CreateClusterV2Response(),
            self.call_api(params, req, runtime)
        )

    async def create_cluster_v2with_options_async(
        self,
        request: emr_20160408_models.CreateClusterV2Request,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.CreateClusterV2Response:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.authorize_content):
            query['AuthorizeContent'] = request.authorize_content
        if not UtilClient.is_unset(request.auto_pay_order):
            query['AutoPayOrder'] = request.auto_pay_order
        if not UtilClient.is_unset(request.auto_renew):
            query['AutoRenew'] = request.auto_renew
        if not UtilClient.is_unset(request.bootstrap_action):
            query['BootstrapAction'] = request.bootstrap_action
        if not UtilClient.is_unset(request.charge_type):
            query['ChargeType'] = request.charge_type
        if not UtilClient.is_unset(request.click_house_conf):
            query['ClickHouseConf'] = request.click_house_conf
        if not UtilClient.is_unset(request.client_token):
            query['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.cluster_type):
            query['ClusterType'] = request.cluster_type
        if not UtilClient.is_unset(request.config):
            query['Config'] = request.config
        if not UtilClient.is_unset(request.configurations):
            query['Configurations'] = request.configurations
        if not UtilClient.is_unset(request.data_disk_encrypted):
            query['DataDiskEncrypted'] = request.data_disk_encrypted
        if not UtilClient.is_unset(request.data_disk_kmskey_id):
            query['DataDiskKMSKeyId'] = request.data_disk_kmskey_id
        if not UtilClient.is_unset(request.deposit_type):
            query['DepositType'] = request.deposit_type
        if not UtilClient.is_unset(request.eas_enable):
            query['EasEnable'] = request.eas_enable
        if not UtilClient.is_unset(request.emr_ver):
            query['EmrVer'] = request.emr_ver
        if not UtilClient.is_unset(request.extra_attributes):
            query['ExtraAttributes'] = request.extra_attributes
        if not UtilClient.is_unset(request.high_availability_enable):
            query['HighAvailabilityEnable'] = request.high_availability_enable
        if not UtilClient.is_unset(request.host_component_info):
            query['HostComponentInfo'] = request.host_component_info
        if not UtilClient.is_unset(request.host_group):
            query['HostGroup'] = request.host_group
        if not UtilClient.is_unset(request.init_custom_hive_meta_db):
            query['InitCustomHiveMetaDB'] = request.init_custom_hive_meta_db
        if not UtilClient.is_unset(request.instance_generation):
            query['InstanceGeneration'] = request.instance_generation
        if not UtilClient.is_unset(request.io_optimized):
            query['IoOptimized'] = request.io_optimized
        if not UtilClient.is_unset(request.is_open_public_ip):
            query['IsOpenPublicIp'] = request.is_open_public_ip
        if not UtilClient.is_unset(request.key_pair_name):
            query['KeyPairName'] = request.key_pair_name
        if not UtilClient.is_unset(request.log_path):
            query['LogPath'] = request.log_path
        if not UtilClient.is_unset(request.machine_type):
            query['MachineType'] = request.machine_type
        if not UtilClient.is_unset(request.master_pwd):
            query['MasterPwd'] = request.master_pwd
        if not UtilClient.is_unset(request.meta_store_conf):
            query['MetaStoreConf'] = request.meta_store_conf
        if not UtilClient.is_unset(request.meta_store_type):
            query['MetaStoreType'] = request.meta_store_type
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.net_type):
            query['NetType'] = request.net_type
        if not UtilClient.is_unset(request.option_soft_ware_list):
            query['OptionSoftWareList'] = request.option_soft_ware_list
        if not UtilClient.is_unset(request.period):
            query['Period'] = request.period
        if not UtilClient.is_unset(request.promotion_info):
            query['PromotionInfo'] = request.promotion_info
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.related_cluster_id):
            query['RelatedClusterId'] = request.related_cluster_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_group_id):
            query['SecurityGroupId'] = request.security_group_id
        if not UtilClient.is_unset(request.security_group_name):
            query['SecurityGroupName'] = request.security_group_name
        if not UtilClient.is_unset(request.service_info):
            query['ServiceInfo'] = request.service_info
        if not UtilClient.is_unset(request.ssh_enable):
            query['SshEnable'] = request.ssh_enable
        if not UtilClient.is_unset(request.tag):
            query['Tag'] = request.tag
        if not UtilClient.is_unset(request.use_custom_hive_meta_db):
            query['UseCustomHiveMetaDB'] = request.use_custom_hive_meta_db
        if not UtilClient.is_unset(request.use_local_meta_db):
            query['UseLocalMetaDb'] = request.use_local_meta_db
        if not UtilClient.is_unset(request.user_defined_emr_ecs_role):
            query['UserDefinedEmrEcsRole'] = request.user_defined_emr_ecs_role
        if not UtilClient.is_unset(request.user_info):
            query['UserInfo'] = request.user_info
        if not UtilClient.is_unset(request.v_switch_id):
            query['VSwitchId'] = request.v_switch_id
        if not UtilClient.is_unset(request.vpc_id):
            query['VpcId'] = request.vpc_id
        if not UtilClient.is_unset(request.white_list_type):
            query['WhiteListType'] = request.white_list_type
        if not UtilClient.is_unset(request.zone_id):
            query['ZoneId'] = request.zone_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateClusterV2',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.CreateClusterV2Response(),
            await self.call_api_async(params, req, runtime)
        )

    def create_cluster_v2(
        self,
        request: emr_20160408_models.CreateClusterV2Request,
    ) -> emr_20160408_models.CreateClusterV2Response:
        runtime = util_models.RuntimeOptions()
        return self.create_cluster_v2with_options(request, runtime)

    async def create_cluster_v2_async(
        self,
        request: emr_20160408_models.CreateClusterV2Request,
    ) -> emr_20160408_models.CreateClusterV2Response:
        runtime = util_models.RuntimeOptions()
        return await self.create_cluster_v2with_options_async(request, runtime)

    def create_cluster_with_template_with_options(
        self,
        request: emr_20160408_models.CreateClusterWithTemplateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.CreateClusterWithTemplateResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.client_token):
            query['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.cluster_name):
            query['ClusterName'] = request.cluster_name
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.template_biz_id):
            query['TemplateBizId'] = request.template_biz_id
        if not UtilClient.is_unset(request.unique_tag):
            query['UniqueTag'] = request.unique_tag
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateClusterWithTemplate',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.CreateClusterWithTemplateResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_cluster_with_template_with_options_async(
        self,
        request: emr_20160408_models.CreateClusterWithTemplateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.CreateClusterWithTemplateResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.client_token):
            query['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.cluster_name):
            query['ClusterName'] = request.cluster_name
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.template_biz_id):
            query['TemplateBizId'] = request.template_biz_id
        if not UtilClient.is_unset(request.unique_tag):
            query['UniqueTag'] = request.unique_tag
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateClusterWithTemplate',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.CreateClusterWithTemplateResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_cluster_with_template(
        self,
        request: emr_20160408_models.CreateClusterWithTemplateRequest,
    ) -> emr_20160408_models.CreateClusterWithTemplateResponse:
        runtime = util_models.RuntimeOptions()
        return self.create_cluster_with_template_with_options(request, runtime)

    async def create_cluster_with_template_async(
        self,
        request: emr_20160408_models.CreateClusterWithTemplateRequest,
    ) -> emr_20160408_models.CreateClusterWithTemplateResponse:
        runtime = util_models.RuntimeOptions()
        return await self.create_cluster_with_template_with_options_async(request, runtime)

    def create_flow_with_options(
        self,
        request: emr_20160408_models.CreateFlowRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.CreateFlowResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.alert_conf):
            query['AlertConf'] = request.alert_conf
        if not UtilClient.is_unset(request.alert_ding_ding_group_biz_id):
            query['AlertDingDingGroupBizId'] = request.alert_ding_ding_group_biz_id
        if not UtilClient.is_unset(request.alert_user_group_biz_id):
            query['AlertUserGroupBizId'] = request.alert_user_group_biz_id
        if not UtilClient.is_unset(request.application):
            query['Application'] = request.application
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.create_cluster):
            query['CreateCluster'] = request.create_cluster
        if not UtilClient.is_unset(request.cron_expr):
            query['CronExpr'] = request.cron_expr
        if not UtilClient.is_unset(request.description):
            query['Description'] = request.description
        if not UtilClient.is_unset(request.end_schedule):
            query['EndSchedule'] = request.end_schedule
        if not UtilClient.is_unset(request.host_name):
            query['HostName'] = request.host_name
        if not UtilClient.is_unset(request.lifecycle):
            query['Lifecycle'] = request.lifecycle
        if not UtilClient.is_unset(request.log_archive_location):
            query['LogArchiveLocation'] = request.log_archive_location
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.namespace):
            query['Namespace'] = request.namespace
        if not UtilClient.is_unset(request.parent_category):
            query['ParentCategory'] = request.parent_category
        if not UtilClient.is_unset(request.parent_flow_list):
            query['ParentFlowList'] = request.parent_flow_list
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.start_schedule):
            query['StartSchedule'] = request.start_schedule
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateFlow',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.CreateFlowResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_flow_with_options_async(
        self,
        request: emr_20160408_models.CreateFlowRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.CreateFlowResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.alert_conf):
            query['AlertConf'] = request.alert_conf
        if not UtilClient.is_unset(request.alert_ding_ding_group_biz_id):
            query['AlertDingDingGroupBizId'] = request.alert_ding_ding_group_biz_id
        if not UtilClient.is_unset(request.alert_user_group_biz_id):
            query['AlertUserGroupBizId'] = request.alert_user_group_biz_id
        if not UtilClient.is_unset(request.application):
            query['Application'] = request.application
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.create_cluster):
            query['CreateCluster'] = request.create_cluster
        if not UtilClient.is_unset(request.cron_expr):
            query['CronExpr'] = request.cron_expr
        if not UtilClient.is_unset(request.description):
            query['Description'] = request.description
        if not UtilClient.is_unset(request.end_schedule):
            query['EndSchedule'] = request.end_schedule
        if not UtilClient.is_unset(request.host_name):
            query['HostName'] = request.host_name
        if not UtilClient.is_unset(request.lifecycle):
            query['Lifecycle'] = request.lifecycle
        if not UtilClient.is_unset(request.log_archive_location):
            query['LogArchiveLocation'] = request.log_archive_location
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.namespace):
            query['Namespace'] = request.namespace
        if not UtilClient.is_unset(request.parent_category):
            query['ParentCategory'] = request.parent_category
        if not UtilClient.is_unset(request.parent_flow_list):
            query['ParentFlowList'] = request.parent_flow_list
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.start_schedule):
            query['StartSchedule'] = request.start_schedule
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateFlow',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.CreateFlowResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_flow(
        self,
        request: emr_20160408_models.CreateFlowRequest,
    ) -> emr_20160408_models.CreateFlowResponse:
        runtime = util_models.RuntimeOptions()
        return self.create_flow_with_options(request, runtime)

    async def create_flow_async(
        self,
        request: emr_20160408_models.CreateFlowRequest,
    ) -> emr_20160408_models.CreateFlowResponse:
        runtime = util_models.RuntimeOptions()
        return await self.create_flow_with_options_async(request, runtime)

    def create_flow_category_with_options(
        self,
        request: emr_20160408_models.CreateFlowCategoryRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.CreateFlowCategoryResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.parent_id):
            query['ParentId'] = request.parent_id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.type):
            query['Type'] = request.type
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateFlowCategory',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.CreateFlowCategoryResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_flow_category_with_options_async(
        self,
        request: emr_20160408_models.CreateFlowCategoryRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.CreateFlowCategoryResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.parent_id):
            query['ParentId'] = request.parent_id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.type):
            query['Type'] = request.type
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateFlowCategory',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.CreateFlowCategoryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_flow_category(
        self,
        request: emr_20160408_models.CreateFlowCategoryRequest,
    ) -> emr_20160408_models.CreateFlowCategoryResponse:
        runtime = util_models.RuntimeOptions()
        return self.create_flow_category_with_options(request, runtime)

    async def create_flow_category_async(
        self,
        request: emr_20160408_models.CreateFlowCategoryRequest,
    ) -> emr_20160408_models.CreateFlowCategoryResponse:
        runtime = util_models.RuntimeOptions()
        return await self.create_flow_category_with_options_async(request, runtime)

    def create_flow_for_web_with_options(
        self,
        request: emr_20160408_models.CreateFlowForWebRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.CreateFlowForWebResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.alert_conf):
            query['AlertConf'] = request.alert_conf
        if not UtilClient.is_unset(request.alert_ding_ding_group_biz_id):
            query['AlertDingDingGroupBizId'] = request.alert_ding_ding_group_biz_id
        if not UtilClient.is_unset(request.alert_user_group_biz_id):
            query['AlertUserGroupBizId'] = request.alert_user_group_biz_id
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.create_cluster):
            query['CreateCluster'] = request.create_cluster
        if not UtilClient.is_unset(request.cron_expr):
            query['CronExpr'] = request.cron_expr
        if not UtilClient.is_unset(request.description):
            query['Description'] = request.description
        if not UtilClient.is_unset(request.end_schedule):
            query['EndSchedule'] = request.end_schedule
        if not UtilClient.is_unset(request.graph):
            query['Graph'] = request.graph
        if not UtilClient.is_unset(request.host_name):
            query['HostName'] = request.host_name
        if not UtilClient.is_unset(request.lifecycle):
            query['Lifecycle'] = request.lifecycle
        if not UtilClient.is_unset(request.log_archive_location):
            query['LogArchiveLocation'] = request.log_archive_location
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.namespace):
            query['Namespace'] = request.namespace
        if not UtilClient.is_unset(request.parent_category):
            query['ParentCategory'] = request.parent_category
        if not UtilClient.is_unset(request.parent_flow_list):
            query['ParentFlowList'] = request.parent_flow_list
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.start_schedule):
            query['StartSchedule'] = request.start_schedule
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateFlowForWeb',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.CreateFlowForWebResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_flow_for_web_with_options_async(
        self,
        request: emr_20160408_models.CreateFlowForWebRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.CreateFlowForWebResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.alert_conf):
            query['AlertConf'] = request.alert_conf
        if not UtilClient.is_unset(request.alert_ding_ding_group_biz_id):
            query['AlertDingDingGroupBizId'] = request.alert_ding_ding_group_biz_id
        if not UtilClient.is_unset(request.alert_user_group_biz_id):
            query['AlertUserGroupBizId'] = request.alert_user_group_biz_id
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.create_cluster):
            query['CreateCluster'] = request.create_cluster
        if not UtilClient.is_unset(request.cron_expr):
            query['CronExpr'] = request.cron_expr
        if not UtilClient.is_unset(request.description):
            query['Description'] = request.description
        if not UtilClient.is_unset(request.end_schedule):
            query['EndSchedule'] = request.end_schedule
        if not UtilClient.is_unset(request.graph):
            query['Graph'] = request.graph
        if not UtilClient.is_unset(request.host_name):
            query['HostName'] = request.host_name
        if not UtilClient.is_unset(request.lifecycle):
            query['Lifecycle'] = request.lifecycle
        if not UtilClient.is_unset(request.log_archive_location):
            query['LogArchiveLocation'] = request.log_archive_location
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.namespace):
            query['Namespace'] = request.namespace
        if not UtilClient.is_unset(request.parent_category):
            query['ParentCategory'] = request.parent_category
        if not UtilClient.is_unset(request.parent_flow_list):
            query['ParentFlowList'] = request.parent_flow_list
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.start_schedule):
            query['StartSchedule'] = request.start_schedule
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateFlowForWeb',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.CreateFlowForWebResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_flow_for_web(
        self,
        request: emr_20160408_models.CreateFlowForWebRequest,
    ) -> emr_20160408_models.CreateFlowForWebResponse:
        runtime = util_models.RuntimeOptions()
        return self.create_flow_for_web_with_options(request, runtime)

    async def create_flow_for_web_async(
        self,
        request: emr_20160408_models.CreateFlowForWebRequest,
    ) -> emr_20160408_models.CreateFlowForWebResponse:
        runtime = util_models.RuntimeOptions()
        return await self.create_flow_for_web_with_options_async(request, runtime)

    def create_flow_job_with_options(
        self,
        request: emr_20160408_models.CreateFlowJobRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.CreateFlowJobResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.adhoc):
            query['Adhoc'] = request.adhoc
        if not UtilClient.is_unset(request.alert_conf):
            query['AlertConf'] = request.alert_conf
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.fail_act):
            query['FailAct'] = request.fail_act
        if not UtilClient.is_unset(request.max_retry):
            query['MaxRetry'] = request.max_retry
        if not UtilClient.is_unset(request.max_running_time_sec):
            query['MaxRunningTimeSec'] = request.max_running_time_sec
        if not UtilClient.is_unset(request.mode):
            query['Mode'] = request.mode
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.parent_category):
            query['ParentCategory'] = request.parent_category
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.retry_interval):
            query['RetryInterval'] = request.retry_interval
        if not UtilClient.is_unset(request.retry_policy):
            query['RetryPolicy'] = request.retry_policy
        if not UtilClient.is_unset(request.type):
            query['Type'] = request.type
        body = {}
        if not UtilClient.is_unset(request.custom_variables):
            body['CustomVariables'] = request.custom_variables
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.env_conf):
            body['EnvConf'] = request.env_conf
        if not UtilClient.is_unset(request.monitor_conf):
            body['MonitorConf'] = request.monitor_conf
        if not UtilClient.is_unset(request.param_conf):
            body['ParamConf'] = request.param_conf
        if not UtilClient.is_unset(request.params):
            body['Params'] = request.params
        if not UtilClient.is_unset(request.resource_list):
            body['ResourceList'] = request.resource_list
        if not UtilClient.is_unset(request.run_conf):
            body['RunConf'] = request.run_conf
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateFlowJob',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.CreateFlowJobResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_flow_job_with_options_async(
        self,
        request: emr_20160408_models.CreateFlowJobRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.CreateFlowJobResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.adhoc):
            query['Adhoc'] = request.adhoc
        if not UtilClient.is_unset(request.alert_conf):
            query['AlertConf'] = request.alert_conf
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.fail_act):
            query['FailAct'] = request.fail_act
        if not UtilClient.is_unset(request.max_retry):
            query['MaxRetry'] = request.max_retry
        if not UtilClient.is_unset(request.max_running_time_sec):
            query['MaxRunningTimeSec'] = request.max_running_time_sec
        if not UtilClient.is_unset(request.mode):
            query['Mode'] = request.mode
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.parent_category):
            query['ParentCategory'] = request.parent_category
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.retry_interval):
            query['RetryInterval'] = request.retry_interval
        if not UtilClient.is_unset(request.retry_policy):
            query['RetryPolicy'] = request.retry_policy
        if not UtilClient.is_unset(request.type):
            query['Type'] = request.type
        body = {}
        if not UtilClient.is_unset(request.custom_variables):
            body['CustomVariables'] = request.custom_variables
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.env_conf):
            body['EnvConf'] = request.env_conf
        if not UtilClient.is_unset(request.monitor_conf):
            body['MonitorConf'] = request.monitor_conf
        if not UtilClient.is_unset(request.param_conf):
            body['ParamConf'] = request.param_conf
        if not UtilClient.is_unset(request.params):
            body['Params'] = request.params
        if not UtilClient.is_unset(request.resource_list):
            body['ResourceList'] = request.resource_list
        if not UtilClient.is_unset(request.run_conf):
            body['RunConf'] = request.run_conf
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateFlowJob',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.CreateFlowJobResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_flow_job(
        self,
        request: emr_20160408_models.CreateFlowJobRequest,
    ) -> emr_20160408_models.CreateFlowJobResponse:
        runtime = util_models.RuntimeOptions()
        return self.create_flow_job_with_options(request, runtime)

    async def create_flow_job_async(
        self,
        request: emr_20160408_models.CreateFlowJobRequest,
    ) -> emr_20160408_models.CreateFlowJobResponse:
        runtime = util_models.RuntimeOptions()
        return await self.create_flow_job_with_options_async(request, runtime)

    def create_flow_project_with_options(
        self,
        request: emr_20160408_models.CreateFlowProjectRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.CreateFlowProjectResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.description):
            query['Description'] = request.description
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.product_type):
            query['ProductType'] = request.product_type
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateFlowProject',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.CreateFlowProjectResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_flow_project_with_options_async(
        self,
        request: emr_20160408_models.CreateFlowProjectRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.CreateFlowProjectResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.description):
            query['Description'] = request.description
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.product_type):
            query['ProductType'] = request.product_type
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateFlowProject',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.CreateFlowProjectResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_flow_project(
        self,
        request: emr_20160408_models.CreateFlowProjectRequest,
    ) -> emr_20160408_models.CreateFlowProjectResponse:
        runtime = util_models.RuntimeOptions()
        return self.create_flow_project_with_options(request, runtime)

    async def create_flow_project_async(
        self,
        request: emr_20160408_models.CreateFlowProjectRequest,
    ) -> emr_20160408_models.CreateFlowProjectResponse:
        runtime = util_models.RuntimeOptions()
        return await self.create_flow_project_with_options_async(request, runtime)

    def create_flow_project_cluster_setting_with_options(
        self,
        request: emr_20160408_models.CreateFlowProjectClusterSettingRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.CreateFlowProjectClusterSettingResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.default_queue):
            query['DefaultQueue'] = request.default_queue
        if not UtilClient.is_unset(request.default_user):
            query['DefaultUser'] = request.default_user
        if not UtilClient.is_unset(request.host_list):
            query['HostList'] = request.host_list
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.queue_list):
            query['QueueList'] = request.queue_list
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.user_list):
            query['UserList'] = request.user_list
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateFlowProjectClusterSetting',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.CreateFlowProjectClusterSettingResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_flow_project_cluster_setting_with_options_async(
        self,
        request: emr_20160408_models.CreateFlowProjectClusterSettingRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.CreateFlowProjectClusterSettingResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.default_queue):
            query['DefaultQueue'] = request.default_queue
        if not UtilClient.is_unset(request.default_user):
            query['DefaultUser'] = request.default_user
        if not UtilClient.is_unset(request.host_list):
            query['HostList'] = request.host_list
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.queue_list):
            query['QueueList'] = request.queue_list
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.user_list):
            query['UserList'] = request.user_list
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateFlowProjectClusterSetting',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.CreateFlowProjectClusterSettingResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_flow_project_cluster_setting(
        self,
        request: emr_20160408_models.CreateFlowProjectClusterSettingRequest,
    ) -> emr_20160408_models.CreateFlowProjectClusterSettingResponse:
        runtime = util_models.RuntimeOptions()
        return self.create_flow_project_cluster_setting_with_options(request, runtime)

    async def create_flow_project_cluster_setting_async(
        self,
        request: emr_20160408_models.CreateFlowProjectClusterSettingRequest,
    ) -> emr_20160408_models.CreateFlowProjectClusterSettingResponse:
        runtime = util_models.RuntimeOptions()
        return await self.create_flow_project_cluster_setting_with_options_async(request, runtime)

    def create_flow_project_user_with_options(
        self,
        request: emr_20160408_models.CreateFlowProjectUserRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.CreateFlowProjectUserResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.user):
            query['User'] = request.user
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateFlowProjectUser',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.CreateFlowProjectUserResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_flow_project_user_with_options_async(
        self,
        request: emr_20160408_models.CreateFlowProjectUserRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.CreateFlowProjectUserResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.user):
            query['User'] = request.user
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateFlowProjectUser',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.CreateFlowProjectUserResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_flow_project_user(
        self,
        request: emr_20160408_models.CreateFlowProjectUserRequest,
    ) -> emr_20160408_models.CreateFlowProjectUserResponse:
        runtime = util_models.RuntimeOptions()
        return self.create_flow_project_user_with_options(request, runtime)

    async def create_flow_project_user_async(
        self,
        request: emr_20160408_models.CreateFlowProjectUserRequest,
    ) -> emr_20160408_models.CreateFlowProjectUserResponse:
        runtime = util_models.RuntimeOptions()
        return await self.create_flow_project_user_with_options_async(request, runtime)

    def create_resource_pool_with_options(
        self,
        request: emr_20160408_models.CreateResourcePoolRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.CreateResourcePoolResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.active):
            query['Active'] = request.active
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.config):
            query['Config'] = request.config
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.note):
            query['Note'] = request.note
        if not UtilClient.is_unset(request.pool_type):
            query['PoolType'] = request.pool_type
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.yarn_site_config):
            query['YarnSiteConfig'] = request.yarn_site_config
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateResourcePool',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.CreateResourcePoolResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_resource_pool_with_options_async(
        self,
        request: emr_20160408_models.CreateResourcePoolRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.CreateResourcePoolResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.active):
            query['Active'] = request.active
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.config):
            query['Config'] = request.config
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.note):
            query['Note'] = request.note
        if not UtilClient.is_unset(request.pool_type):
            query['PoolType'] = request.pool_type
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.yarn_site_config):
            query['YarnSiteConfig'] = request.yarn_site_config
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateResourcePool',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.CreateResourcePoolResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_resource_pool(
        self,
        request: emr_20160408_models.CreateResourcePoolRequest,
    ) -> emr_20160408_models.CreateResourcePoolResponse:
        runtime = util_models.RuntimeOptions()
        return self.create_resource_pool_with_options(request, runtime)

    async def create_resource_pool_async(
        self,
        request: emr_20160408_models.CreateResourcePoolRequest,
    ) -> emr_20160408_models.CreateResourcePoolResponse:
        runtime = util_models.RuntimeOptions()
        return await self.create_resource_pool_with_options_async(request, runtime)

    def create_resource_queue_with_options(
        self,
        request: emr_20160408_models.CreateResourceQueueRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.CreateResourceQueueResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.config):
            query['Config'] = request.config
        if not UtilClient.is_unset(request.leaf):
            query['Leaf'] = request.leaf
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.parent_queue_id):
            query['ParentQueueId'] = request.parent_queue_id
        if not UtilClient.is_unset(request.qualified_name):
            query['QualifiedName'] = request.qualified_name
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.resource_pool_id):
            query['ResourcePoolId'] = request.resource_pool_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateResourceQueue',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.CreateResourceQueueResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_resource_queue_with_options_async(
        self,
        request: emr_20160408_models.CreateResourceQueueRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.CreateResourceQueueResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.config):
            query['Config'] = request.config
        if not UtilClient.is_unset(request.leaf):
            query['Leaf'] = request.leaf
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.parent_queue_id):
            query['ParentQueueId'] = request.parent_queue_id
        if not UtilClient.is_unset(request.qualified_name):
            query['QualifiedName'] = request.qualified_name
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.resource_pool_id):
            query['ResourcePoolId'] = request.resource_pool_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateResourceQueue',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.CreateResourceQueueResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_resource_queue(
        self,
        request: emr_20160408_models.CreateResourceQueueRequest,
    ) -> emr_20160408_models.CreateResourceQueueResponse:
        runtime = util_models.RuntimeOptions()
        return self.create_resource_queue_with_options(request, runtime)

    async def create_resource_queue_async(
        self,
        request: emr_20160408_models.CreateResourceQueueRequest,
    ) -> emr_20160408_models.CreateResourceQueueResponse:
        runtime = util_models.RuntimeOptions()
        return await self.create_resource_queue_with_options_async(request, runtime)

    def create_scaling_group_v2with_options(
        self,
        request: emr_20160408_models.CreateScalingGroupV2Request,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.CreateScalingGroupV2Response:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.description):
            query['Description'] = request.description
        if not UtilClient.is_unset(request.host_group_id):
            query['HostGroupId'] = request.host_group_id
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateScalingGroupV2',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.CreateScalingGroupV2Response(),
            self.call_api(params, req, runtime)
        )

    async def create_scaling_group_v2with_options_async(
        self,
        request: emr_20160408_models.CreateScalingGroupV2Request,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.CreateScalingGroupV2Response:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.description):
            query['Description'] = request.description
        if not UtilClient.is_unset(request.host_group_id):
            query['HostGroupId'] = request.host_group_id
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CreateScalingGroupV2',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.CreateScalingGroupV2Response(),
            await self.call_api_async(params, req, runtime)
        )

    def create_scaling_group_v2(
        self,
        request: emr_20160408_models.CreateScalingGroupV2Request,
    ) -> emr_20160408_models.CreateScalingGroupV2Response:
        runtime = util_models.RuntimeOptions()
        return self.create_scaling_group_v2with_options(request, runtime)

    async def create_scaling_group_v2_async(
        self,
        request: emr_20160408_models.CreateScalingGroupV2Request,
    ) -> emr_20160408_models.CreateScalingGroupV2Response:
        runtime = util_models.RuntimeOptions()
        return await self.create_scaling_group_v2with_options_async(request, runtime)

    def delete_cluster_template_with_options(
        self,
        request: emr_20160408_models.DeleteClusterTemplateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DeleteClusterTemplateResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_id):
            query['BizId'] = request.biz_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteClusterTemplate',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DeleteClusterTemplateResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_cluster_template_with_options_async(
        self,
        request: emr_20160408_models.DeleteClusterTemplateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DeleteClusterTemplateResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_id):
            query['BizId'] = request.biz_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteClusterTemplate',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DeleteClusterTemplateResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_cluster_template(
        self,
        request: emr_20160408_models.DeleteClusterTemplateRequest,
    ) -> emr_20160408_models.DeleteClusterTemplateResponse:
        runtime = util_models.RuntimeOptions()
        return self.delete_cluster_template_with_options(request, runtime)

    async def delete_cluster_template_async(
        self,
        request: emr_20160408_models.DeleteClusterTemplateRequest,
    ) -> emr_20160408_models.DeleteClusterTemplateResponse:
        runtime = util_models.RuntimeOptions()
        return await self.delete_cluster_template_with_options_async(request, runtime)

    def delete_flow_with_options(
        self,
        request: emr_20160408_models.DeleteFlowRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DeleteFlowResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteFlow',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DeleteFlowResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_flow_with_options_async(
        self,
        request: emr_20160408_models.DeleteFlowRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DeleteFlowResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteFlow',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DeleteFlowResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_flow(
        self,
        request: emr_20160408_models.DeleteFlowRequest,
    ) -> emr_20160408_models.DeleteFlowResponse:
        runtime = util_models.RuntimeOptions()
        return self.delete_flow_with_options(request, runtime)

    async def delete_flow_async(
        self,
        request: emr_20160408_models.DeleteFlowRequest,
    ) -> emr_20160408_models.DeleteFlowResponse:
        runtime = util_models.RuntimeOptions()
        return await self.delete_flow_with_options_async(request, runtime)

    def delete_flow_category_with_options(
        self,
        request: emr_20160408_models.DeleteFlowCategoryRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DeleteFlowCategoryResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteFlowCategory',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DeleteFlowCategoryResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_flow_category_with_options_async(
        self,
        request: emr_20160408_models.DeleteFlowCategoryRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DeleteFlowCategoryResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteFlowCategory',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DeleteFlowCategoryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_flow_category(
        self,
        request: emr_20160408_models.DeleteFlowCategoryRequest,
    ) -> emr_20160408_models.DeleteFlowCategoryResponse:
        runtime = util_models.RuntimeOptions()
        return self.delete_flow_category_with_options(request, runtime)

    async def delete_flow_category_async(
        self,
        request: emr_20160408_models.DeleteFlowCategoryRequest,
    ) -> emr_20160408_models.DeleteFlowCategoryResponse:
        runtime = util_models.RuntimeOptions()
        return await self.delete_flow_category_with_options_async(request, runtime)

    def delete_flow_job_with_options(
        self,
        request: emr_20160408_models.DeleteFlowJobRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DeleteFlowJobResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteFlowJob',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DeleteFlowJobResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_flow_job_with_options_async(
        self,
        request: emr_20160408_models.DeleteFlowJobRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DeleteFlowJobResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteFlowJob',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DeleteFlowJobResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_flow_job(
        self,
        request: emr_20160408_models.DeleteFlowJobRequest,
    ) -> emr_20160408_models.DeleteFlowJobResponse:
        runtime = util_models.RuntimeOptions()
        return self.delete_flow_job_with_options(request, runtime)

    async def delete_flow_job_async(
        self,
        request: emr_20160408_models.DeleteFlowJobRequest,
    ) -> emr_20160408_models.DeleteFlowJobResponse:
        runtime = util_models.RuntimeOptions()
        return await self.delete_flow_job_with_options_async(request, runtime)

    def delete_flow_project_with_options(
        self,
        request: emr_20160408_models.DeleteFlowProjectRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DeleteFlowProjectResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteFlowProject',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DeleteFlowProjectResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_flow_project_with_options_async(
        self,
        request: emr_20160408_models.DeleteFlowProjectRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DeleteFlowProjectResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteFlowProject',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DeleteFlowProjectResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_flow_project(
        self,
        request: emr_20160408_models.DeleteFlowProjectRequest,
    ) -> emr_20160408_models.DeleteFlowProjectResponse:
        runtime = util_models.RuntimeOptions()
        return self.delete_flow_project_with_options(request, runtime)

    async def delete_flow_project_async(
        self,
        request: emr_20160408_models.DeleteFlowProjectRequest,
    ) -> emr_20160408_models.DeleteFlowProjectResponse:
        runtime = util_models.RuntimeOptions()
        return await self.delete_flow_project_with_options_async(request, runtime)

    def delete_flow_project_cluster_setting_with_options(
        self,
        request: emr_20160408_models.DeleteFlowProjectClusterSettingRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DeleteFlowProjectClusterSettingResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteFlowProjectClusterSetting',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DeleteFlowProjectClusterSettingResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_flow_project_cluster_setting_with_options_async(
        self,
        request: emr_20160408_models.DeleteFlowProjectClusterSettingRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DeleteFlowProjectClusterSettingResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteFlowProjectClusterSetting',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DeleteFlowProjectClusterSettingResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_flow_project_cluster_setting(
        self,
        request: emr_20160408_models.DeleteFlowProjectClusterSettingRequest,
    ) -> emr_20160408_models.DeleteFlowProjectClusterSettingResponse:
        runtime = util_models.RuntimeOptions()
        return self.delete_flow_project_cluster_setting_with_options(request, runtime)

    async def delete_flow_project_cluster_setting_async(
        self,
        request: emr_20160408_models.DeleteFlowProjectClusterSettingRequest,
    ) -> emr_20160408_models.DeleteFlowProjectClusterSettingResponse:
        runtime = util_models.RuntimeOptions()
        return await self.delete_flow_project_cluster_setting_with_options_async(request, runtime)

    def delete_flow_project_user_with_options(
        self,
        request: emr_20160408_models.DeleteFlowProjectUserRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DeleteFlowProjectUserResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.user_name):
            query['UserName'] = request.user_name
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteFlowProjectUser',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DeleteFlowProjectUserResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_flow_project_user_with_options_async(
        self,
        request: emr_20160408_models.DeleteFlowProjectUserRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DeleteFlowProjectUserResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.user_name):
            query['UserName'] = request.user_name
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteFlowProjectUser',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DeleteFlowProjectUserResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_flow_project_user(
        self,
        request: emr_20160408_models.DeleteFlowProjectUserRequest,
    ) -> emr_20160408_models.DeleteFlowProjectUserResponse:
        runtime = util_models.RuntimeOptions()
        return self.delete_flow_project_user_with_options(request, runtime)

    async def delete_flow_project_user_async(
        self,
        request: emr_20160408_models.DeleteFlowProjectUserRequest,
    ) -> emr_20160408_models.DeleteFlowProjectUserResponse:
        runtime = util_models.RuntimeOptions()
        return await self.delete_flow_project_user_with_options_async(request, runtime)

    def delete_resource_pool_with_options(
        self,
        request: emr_20160408_models.DeleteResourcePoolRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DeleteResourcePoolResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.resource_pool_id):
            query['ResourcePoolId'] = request.resource_pool_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteResourcePool',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DeleteResourcePoolResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_resource_pool_with_options_async(
        self,
        request: emr_20160408_models.DeleteResourcePoolRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DeleteResourcePoolResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.resource_pool_id):
            query['ResourcePoolId'] = request.resource_pool_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteResourcePool',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DeleteResourcePoolResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_resource_pool(
        self,
        request: emr_20160408_models.DeleteResourcePoolRequest,
    ) -> emr_20160408_models.DeleteResourcePoolResponse:
        runtime = util_models.RuntimeOptions()
        return self.delete_resource_pool_with_options(request, runtime)

    async def delete_resource_pool_async(
        self,
        request: emr_20160408_models.DeleteResourcePoolRequest,
    ) -> emr_20160408_models.DeleteResourcePoolResponse:
        runtime = util_models.RuntimeOptions()
        return await self.delete_resource_pool_with_options_async(request, runtime)

    def delete_resource_queue_with_options(
        self,
        request: emr_20160408_models.DeleteResourceQueueRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DeleteResourceQueueResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.resource_queue_id):
            query['ResourceQueueId'] = request.resource_queue_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteResourceQueue',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DeleteResourceQueueResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_resource_queue_with_options_async(
        self,
        request: emr_20160408_models.DeleteResourceQueueRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DeleteResourceQueueResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.resource_queue_id):
            query['ResourceQueueId'] = request.resource_queue_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteResourceQueue',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DeleteResourceQueueResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_resource_queue(
        self,
        request: emr_20160408_models.DeleteResourceQueueRequest,
    ) -> emr_20160408_models.DeleteResourceQueueResponse:
        runtime = util_models.RuntimeOptions()
        return self.delete_resource_queue_with_options(request, runtime)

    async def delete_resource_queue_async(
        self,
        request: emr_20160408_models.DeleteResourceQueueRequest,
    ) -> emr_20160408_models.DeleteResourceQueueResponse:
        runtime = util_models.RuntimeOptions()
        return await self.delete_resource_queue_with_options_async(request, runtime)

    def describe_cluster_basic_info_with_options(
        self,
        request: emr_20160408_models.DescribeClusterBasicInfoRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DescribeClusterBasicInfoResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeClusterBasicInfo',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DescribeClusterBasicInfoResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_cluster_basic_info_with_options_async(
        self,
        request: emr_20160408_models.DescribeClusterBasicInfoRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DescribeClusterBasicInfoResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeClusterBasicInfo',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DescribeClusterBasicInfoResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_cluster_basic_info(
        self,
        request: emr_20160408_models.DescribeClusterBasicInfoRequest,
    ) -> emr_20160408_models.DescribeClusterBasicInfoResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_cluster_basic_info_with_options(request, runtime)

    async def describe_cluster_basic_info_async(
        self,
        request: emr_20160408_models.DescribeClusterBasicInfoRequest,
    ) -> emr_20160408_models.DescribeClusterBasicInfoResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_cluster_basic_info_with_options_async(request, runtime)

    def describe_cluster_operation_host_task_log_with_options(
        self,
        request: emr_20160408_models.DescribeClusterOperationHostTaskLogRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DescribeClusterOperationHostTaskLogResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.host_id):
            query['HostId'] = request.host_id
        if not UtilClient.is_unset(request.operation_id):
            query['OperationId'] = request.operation_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.status):
            query['Status'] = request.status
        if not UtilClient.is_unset(request.task_id):
            query['TaskId'] = request.task_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeClusterOperationHostTaskLog',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DescribeClusterOperationHostTaskLogResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_cluster_operation_host_task_log_with_options_async(
        self,
        request: emr_20160408_models.DescribeClusterOperationHostTaskLogRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DescribeClusterOperationHostTaskLogResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.host_id):
            query['HostId'] = request.host_id
        if not UtilClient.is_unset(request.operation_id):
            query['OperationId'] = request.operation_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.status):
            query['Status'] = request.status
        if not UtilClient.is_unset(request.task_id):
            query['TaskId'] = request.task_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeClusterOperationHostTaskLog',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DescribeClusterOperationHostTaskLogResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_cluster_operation_host_task_log(
        self,
        request: emr_20160408_models.DescribeClusterOperationHostTaskLogRequest,
    ) -> emr_20160408_models.DescribeClusterOperationHostTaskLogResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_cluster_operation_host_task_log_with_options(request, runtime)

    async def describe_cluster_operation_host_task_log_async(
        self,
        request: emr_20160408_models.DescribeClusterOperationHostTaskLogRequest,
    ) -> emr_20160408_models.DescribeClusterOperationHostTaskLogResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_cluster_operation_host_task_log_with_options_async(request, runtime)

    def describe_cluster_resource_pool_scheduler_type_with_options(
        self,
        request: emr_20160408_models.DescribeClusterResourcePoolSchedulerTypeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DescribeClusterResourcePoolSchedulerTypeResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeClusterResourcePoolSchedulerType',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DescribeClusterResourcePoolSchedulerTypeResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_cluster_resource_pool_scheduler_type_with_options_async(
        self,
        request: emr_20160408_models.DescribeClusterResourcePoolSchedulerTypeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DescribeClusterResourcePoolSchedulerTypeResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeClusterResourcePoolSchedulerType',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DescribeClusterResourcePoolSchedulerTypeResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_cluster_resource_pool_scheduler_type(
        self,
        request: emr_20160408_models.DescribeClusterResourcePoolSchedulerTypeRequest,
    ) -> emr_20160408_models.DescribeClusterResourcePoolSchedulerTypeResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_cluster_resource_pool_scheduler_type_with_options(request, runtime)

    async def describe_cluster_resource_pool_scheduler_type_async(
        self,
        request: emr_20160408_models.DescribeClusterResourcePoolSchedulerTypeRequest,
    ) -> emr_20160408_models.DescribeClusterResourcePoolSchedulerTypeResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_cluster_resource_pool_scheduler_type_with_options_async(request, runtime)

    def describe_cluster_service_with_options(
        self,
        request: emr_20160408_models.DescribeClusterServiceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DescribeClusterServiceResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.service_name):
            query['ServiceName'] = request.service_name
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeClusterService',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DescribeClusterServiceResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_cluster_service_with_options_async(
        self,
        request: emr_20160408_models.DescribeClusterServiceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DescribeClusterServiceResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.service_name):
            query['ServiceName'] = request.service_name
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeClusterService',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DescribeClusterServiceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_cluster_service(
        self,
        request: emr_20160408_models.DescribeClusterServiceRequest,
    ) -> emr_20160408_models.DescribeClusterServiceResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_cluster_service_with_options(request, runtime)

    async def describe_cluster_service_async(
        self,
        request: emr_20160408_models.DescribeClusterServiceRequest,
    ) -> emr_20160408_models.DescribeClusterServiceResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_cluster_service_with_options_async(request, runtime)

    def describe_cluster_service_config_with_options(
        self,
        request: emr_20160408_models.DescribeClusterServiceConfigRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DescribeClusterServiceConfigResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.config_version):
            query['ConfigVersion'] = request.config_version
        if not UtilClient.is_unset(request.group_id):
            query['GroupId'] = request.group_id
        if not UtilClient.is_unset(request.host_instance_id):
            query['HostInstanceId'] = request.host_instance_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.service_name):
            query['ServiceName'] = request.service_name
        if not UtilClient.is_unset(request.tag_value):
            query['TagValue'] = request.tag_value
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeClusterServiceConfig',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DescribeClusterServiceConfigResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_cluster_service_config_with_options_async(
        self,
        request: emr_20160408_models.DescribeClusterServiceConfigRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DescribeClusterServiceConfigResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.config_version):
            query['ConfigVersion'] = request.config_version
        if not UtilClient.is_unset(request.group_id):
            query['GroupId'] = request.group_id
        if not UtilClient.is_unset(request.host_instance_id):
            query['HostInstanceId'] = request.host_instance_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.service_name):
            query['ServiceName'] = request.service_name
        if not UtilClient.is_unset(request.tag_value):
            query['TagValue'] = request.tag_value
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeClusterServiceConfig',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DescribeClusterServiceConfigResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_cluster_service_config(
        self,
        request: emr_20160408_models.DescribeClusterServiceConfigRequest,
    ) -> emr_20160408_models.DescribeClusterServiceConfigResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_cluster_service_config_with_options(request, runtime)

    async def describe_cluster_service_config_async(
        self,
        request: emr_20160408_models.DescribeClusterServiceConfigRequest,
    ) -> emr_20160408_models.DescribeClusterServiceConfigResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_cluster_service_config_with_options_async(request, runtime)

    def describe_cluster_service_config_tag_with_options(
        self,
        request: emr_20160408_models.DescribeClusterServiceConfigTagRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DescribeClusterServiceConfigTagResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.config_tag):
            query['ConfigTag'] = request.config_tag
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.service_name):
            query['ServiceName'] = request.service_name
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeClusterServiceConfigTag',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DescribeClusterServiceConfigTagResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_cluster_service_config_tag_with_options_async(
        self,
        request: emr_20160408_models.DescribeClusterServiceConfigTagRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DescribeClusterServiceConfigTagResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.config_tag):
            query['ConfigTag'] = request.config_tag
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.service_name):
            query['ServiceName'] = request.service_name
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeClusterServiceConfigTag',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DescribeClusterServiceConfigTagResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_cluster_service_config_tag(
        self,
        request: emr_20160408_models.DescribeClusterServiceConfigTagRequest,
    ) -> emr_20160408_models.DescribeClusterServiceConfigTagResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_cluster_service_config_tag_with_options(request, runtime)

    async def describe_cluster_service_config_tag_async(
        self,
        request: emr_20160408_models.DescribeClusterServiceConfigTagRequest,
    ) -> emr_20160408_models.DescribeClusterServiceConfigTagResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_cluster_service_config_tag_with_options_async(request, runtime)

    def describe_cluster_template_with_options(
        self,
        request: emr_20160408_models.DescribeClusterTemplateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DescribeClusterTemplateResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_id):
            query['BizId'] = request.biz_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeClusterTemplate',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DescribeClusterTemplateResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_cluster_template_with_options_async(
        self,
        request: emr_20160408_models.DescribeClusterTemplateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DescribeClusterTemplateResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_id):
            query['BizId'] = request.biz_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeClusterTemplate',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DescribeClusterTemplateResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_cluster_template(
        self,
        request: emr_20160408_models.DescribeClusterTemplateRequest,
    ) -> emr_20160408_models.DescribeClusterTemplateResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_cluster_template_with_options(request, runtime)

    async def describe_cluster_template_async(
        self,
        request: emr_20160408_models.DescribeClusterTemplateRequest,
    ) -> emr_20160408_models.DescribeClusterTemplateResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_cluster_template_with_options_async(request, runtime)

    def describe_cluster_v2with_options(
        self,
        request: emr_20160408_models.DescribeClusterV2Request,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DescribeClusterV2Response:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeClusterV2',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DescribeClusterV2Response(),
            self.call_api(params, req, runtime)
        )

    async def describe_cluster_v2with_options_async(
        self,
        request: emr_20160408_models.DescribeClusterV2Request,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DescribeClusterV2Response:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeClusterV2',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DescribeClusterV2Response(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_cluster_v2(
        self,
        request: emr_20160408_models.DescribeClusterV2Request,
    ) -> emr_20160408_models.DescribeClusterV2Response:
        runtime = util_models.RuntimeOptions()
        return self.describe_cluster_v2with_options(request, runtime)

    async def describe_cluster_v2_async(
        self,
        request: emr_20160408_models.DescribeClusterV2Request,
    ) -> emr_20160408_models.DescribeClusterV2Response:
        runtime = util_models.RuntimeOptions()
        return await self.describe_cluster_v2with_options_async(request, runtime)

    def describe_flow_with_options(
        self,
        request: emr_20160408_models.DescribeFlowRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DescribeFlowResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeFlow',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DescribeFlowResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_flow_with_options_async(
        self,
        request: emr_20160408_models.DescribeFlowRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DescribeFlowResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeFlow',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DescribeFlowResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_flow(
        self,
        request: emr_20160408_models.DescribeFlowRequest,
    ) -> emr_20160408_models.DescribeFlowResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_flow_with_options(request, runtime)

    async def describe_flow_async(
        self,
        request: emr_20160408_models.DescribeFlowRequest,
    ) -> emr_20160408_models.DescribeFlowResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_flow_with_options_async(request, runtime)

    def describe_flow_category_with_options(
        self,
        request: emr_20160408_models.DescribeFlowCategoryRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DescribeFlowCategoryResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeFlowCategory',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DescribeFlowCategoryResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_flow_category_with_options_async(
        self,
        request: emr_20160408_models.DescribeFlowCategoryRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DescribeFlowCategoryResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeFlowCategory',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DescribeFlowCategoryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_flow_category(
        self,
        request: emr_20160408_models.DescribeFlowCategoryRequest,
    ) -> emr_20160408_models.DescribeFlowCategoryResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_flow_category_with_options(request, runtime)

    async def describe_flow_category_async(
        self,
        request: emr_20160408_models.DescribeFlowCategoryRequest,
    ) -> emr_20160408_models.DescribeFlowCategoryResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_flow_category_with_options_async(request, runtime)

    def describe_flow_category_tree_with_options(
        self,
        request: emr_20160408_models.DescribeFlowCategoryTreeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DescribeFlowCategoryTreeResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.category_id):
            query['CategoryId'] = request.category_id
        if not UtilClient.is_unset(request.keyword):
            query['Keyword'] = request.keyword
        if not UtilClient.is_unset(request.mode):
            query['Mode'] = request.mode
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.type):
            query['Type'] = request.type
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeFlowCategoryTree',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DescribeFlowCategoryTreeResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_flow_category_tree_with_options_async(
        self,
        request: emr_20160408_models.DescribeFlowCategoryTreeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DescribeFlowCategoryTreeResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.category_id):
            query['CategoryId'] = request.category_id
        if not UtilClient.is_unset(request.keyword):
            query['Keyword'] = request.keyword
        if not UtilClient.is_unset(request.mode):
            query['Mode'] = request.mode
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.type):
            query['Type'] = request.type
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeFlowCategoryTree',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DescribeFlowCategoryTreeResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_flow_category_tree(
        self,
        request: emr_20160408_models.DescribeFlowCategoryTreeRequest,
    ) -> emr_20160408_models.DescribeFlowCategoryTreeResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_flow_category_tree_with_options(request, runtime)

    async def describe_flow_category_tree_async(
        self,
        request: emr_20160408_models.DescribeFlowCategoryTreeRequest,
    ) -> emr_20160408_models.DescribeFlowCategoryTreeResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_flow_category_tree_with_options_async(request, runtime)

    def describe_flow_instance_with_options(
        self,
        request: emr_20160408_models.DescribeFlowInstanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DescribeFlowInstanceResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeFlowInstance',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DescribeFlowInstanceResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_flow_instance_with_options_async(
        self,
        request: emr_20160408_models.DescribeFlowInstanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DescribeFlowInstanceResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeFlowInstance',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DescribeFlowInstanceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_flow_instance(
        self,
        request: emr_20160408_models.DescribeFlowInstanceRequest,
    ) -> emr_20160408_models.DescribeFlowInstanceResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_flow_instance_with_options(request, runtime)

    async def describe_flow_instance_async(
        self,
        request: emr_20160408_models.DescribeFlowInstanceRequest,
    ) -> emr_20160408_models.DescribeFlowInstanceResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_flow_instance_with_options_async(request, runtime)

    def describe_flow_job_with_options(
        self,
        request: emr_20160408_models.DescribeFlowJobRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DescribeFlowJobResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeFlowJob',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DescribeFlowJobResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_flow_job_with_options_async(
        self,
        request: emr_20160408_models.DescribeFlowJobRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DescribeFlowJobResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeFlowJob',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DescribeFlowJobResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_flow_job(
        self,
        request: emr_20160408_models.DescribeFlowJobRequest,
    ) -> emr_20160408_models.DescribeFlowJobResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_flow_job_with_options(request, runtime)

    async def describe_flow_job_async(
        self,
        request: emr_20160408_models.DescribeFlowJobRequest,
    ) -> emr_20160408_models.DescribeFlowJobResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_flow_job_with_options_async(request, runtime)

    def describe_flow_node_instance_with_options(
        self,
        request: emr_20160408_models.DescribeFlowNodeInstanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DescribeFlowNodeInstanceResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeFlowNodeInstance',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DescribeFlowNodeInstanceResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_flow_node_instance_with_options_async(
        self,
        request: emr_20160408_models.DescribeFlowNodeInstanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DescribeFlowNodeInstanceResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeFlowNodeInstance',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DescribeFlowNodeInstanceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_flow_node_instance(
        self,
        request: emr_20160408_models.DescribeFlowNodeInstanceRequest,
    ) -> emr_20160408_models.DescribeFlowNodeInstanceResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_flow_node_instance_with_options(request, runtime)

    async def describe_flow_node_instance_async(
        self,
        request: emr_20160408_models.DescribeFlowNodeInstanceRequest,
    ) -> emr_20160408_models.DescribeFlowNodeInstanceResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_flow_node_instance_with_options_async(request, runtime)

    def describe_flow_node_instance_container_log_with_options(
        self,
        request: emr_20160408_models.DescribeFlowNodeInstanceContainerLogRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DescribeFlowNodeInstanceContainerLogResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_id):
            query['AppId'] = request.app_id
        if not UtilClient.is_unset(request.container_id):
            query['ContainerId'] = request.container_id
        if not UtilClient.is_unset(request.length):
            query['Length'] = request.length
        if not UtilClient.is_unset(request.log_name):
            query['LogName'] = request.log_name
        if not UtilClient.is_unset(request.node_instance_id):
            query['NodeInstanceId'] = request.node_instance_id
        if not UtilClient.is_unset(request.offset):
            query['Offset'] = request.offset
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeFlowNodeInstanceContainerLog',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DescribeFlowNodeInstanceContainerLogResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_flow_node_instance_container_log_with_options_async(
        self,
        request: emr_20160408_models.DescribeFlowNodeInstanceContainerLogRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DescribeFlowNodeInstanceContainerLogResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_id):
            query['AppId'] = request.app_id
        if not UtilClient.is_unset(request.container_id):
            query['ContainerId'] = request.container_id
        if not UtilClient.is_unset(request.length):
            query['Length'] = request.length
        if not UtilClient.is_unset(request.log_name):
            query['LogName'] = request.log_name
        if not UtilClient.is_unset(request.node_instance_id):
            query['NodeInstanceId'] = request.node_instance_id
        if not UtilClient.is_unset(request.offset):
            query['Offset'] = request.offset
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeFlowNodeInstanceContainerLog',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DescribeFlowNodeInstanceContainerLogResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_flow_node_instance_container_log(
        self,
        request: emr_20160408_models.DescribeFlowNodeInstanceContainerLogRequest,
    ) -> emr_20160408_models.DescribeFlowNodeInstanceContainerLogResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_flow_node_instance_container_log_with_options(request, runtime)

    async def describe_flow_node_instance_container_log_async(
        self,
        request: emr_20160408_models.DescribeFlowNodeInstanceContainerLogRequest,
    ) -> emr_20160408_models.DescribeFlowNodeInstanceContainerLogResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_flow_node_instance_container_log_with_options_async(request, runtime)

    def describe_flow_node_instance_launcher_log_with_options(
        self,
        request: emr_20160408_models.DescribeFlowNodeInstanceLauncherLogRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DescribeFlowNodeInstanceLauncherLogResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.length):
            query['Length'] = request.length
        if not UtilClient.is_unset(request.lines):
            query['Lines'] = request.lines
        if not UtilClient.is_unset(request.node_instance_id):
            query['NodeInstanceId'] = request.node_instance_id
        if not UtilClient.is_unset(request.offset):
            query['Offset'] = request.offset
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.reverse):
            query['Reverse'] = request.reverse
        if not UtilClient.is_unset(request.start):
            query['Start'] = request.start
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeFlowNodeInstanceLauncherLog',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DescribeFlowNodeInstanceLauncherLogResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_flow_node_instance_launcher_log_with_options_async(
        self,
        request: emr_20160408_models.DescribeFlowNodeInstanceLauncherLogRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DescribeFlowNodeInstanceLauncherLogResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.length):
            query['Length'] = request.length
        if not UtilClient.is_unset(request.lines):
            query['Lines'] = request.lines
        if not UtilClient.is_unset(request.node_instance_id):
            query['NodeInstanceId'] = request.node_instance_id
        if not UtilClient.is_unset(request.offset):
            query['Offset'] = request.offset
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.reverse):
            query['Reverse'] = request.reverse
        if not UtilClient.is_unset(request.start):
            query['Start'] = request.start
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeFlowNodeInstanceLauncherLog',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DescribeFlowNodeInstanceLauncherLogResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_flow_node_instance_launcher_log(
        self,
        request: emr_20160408_models.DescribeFlowNodeInstanceLauncherLogRequest,
    ) -> emr_20160408_models.DescribeFlowNodeInstanceLauncherLogResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_flow_node_instance_launcher_log_with_options(request, runtime)

    async def describe_flow_node_instance_launcher_log_async(
        self,
        request: emr_20160408_models.DescribeFlowNodeInstanceLauncherLogRequest,
    ) -> emr_20160408_models.DescribeFlowNodeInstanceLauncherLogResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_flow_node_instance_launcher_log_with_options_async(request, runtime)

    def describe_flow_project_with_options(
        self,
        request: emr_20160408_models.DescribeFlowProjectRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DescribeFlowProjectResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeFlowProject',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DescribeFlowProjectResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_flow_project_with_options_async(
        self,
        request: emr_20160408_models.DescribeFlowProjectRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DescribeFlowProjectResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeFlowProject',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DescribeFlowProjectResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_flow_project(
        self,
        request: emr_20160408_models.DescribeFlowProjectRequest,
    ) -> emr_20160408_models.DescribeFlowProjectResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_flow_project_with_options(request, runtime)

    async def describe_flow_project_async(
        self,
        request: emr_20160408_models.DescribeFlowProjectRequest,
    ) -> emr_20160408_models.DescribeFlowProjectResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_flow_project_with_options_async(request, runtime)

    def describe_flow_project_cluster_setting_with_options(
        self,
        request: emr_20160408_models.DescribeFlowProjectClusterSettingRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DescribeFlowProjectClusterSettingResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeFlowProjectClusterSetting',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DescribeFlowProjectClusterSettingResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_flow_project_cluster_setting_with_options_async(
        self,
        request: emr_20160408_models.DescribeFlowProjectClusterSettingRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DescribeFlowProjectClusterSettingResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeFlowProjectClusterSetting',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DescribeFlowProjectClusterSettingResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_flow_project_cluster_setting(
        self,
        request: emr_20160408_models.DescribeFlowProjectClusterSettingRequest,
    ) -> emr_20160408_models.DescribeFlowProjectClusterSettingResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_flow_project_cluster_setting_with_options(request, runtime)

    async def describe_flow_project_cluster_setting_async(
        self,
        request: emr_20160408_models.DescribeFlowProjectClusterSettingRequest,
    ) -> emr_20160408_models.DescribeFlowProjectClusterSettingResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_flow_project_cluster_setting_with_options_async(request, runtime)

    def describe_scaling_config_item_v2with_options(
        self,
        request: emr_20160408_models.DescribeScalingConfigItemV2Request,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DescribeScalingConfigItemV2Response:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.config_item_type):
            query['ConfigItemType'] = request.config_item_type
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.scaling_config_item_id):
            query['ScalingConfigItemId'] = request.scaling_config_item_id
        if not UtilClient.is_unset(request.scaling_group_biz_id):
            query['ScalingGroupBizId'] = request.scaling_group_biz_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeScalingConfigItemV2',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DescribeScalingConfigItemV2Response(),
            self.call_api(params, req, runtime)
        )

    async def describe_scaling_config_item_v2with_options_async(
        self,
        request: emr_20160408_models.DescribeScalingConfigItemV2Request,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DescribeScalingConfigItemV2Response:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.config_item_type):
            query['ConfigItemType'] = request.config_item_type
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.scaling_config_item_id):
            query['ScalingConfigItemId'] = request.scaling_config_item_id
        if not UtilClient.is_unset(request.scaling_group_biz_id):
            query['ScalingGroupBizId'] = request.scaling_group_biz_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeScalingConfigItemV2',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DescribeScalingConfigItemV2Response(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_scaling_config_item_v2(
        self,
        request: emr_20160408_models.DescribeScalingConfigItemV2Request,
    ) -> emr_20160408_models.DescribeScalingConfigItemV2Response:
        runtime = util_models.RuntimeOptions()
        return self.describe_scaling_config_item_v2with_options(request, runtime)

    async def describe_scaling_config_item_v2_async(
        self,
        request: emr_20160408_models.DescribeScalingConfigItemV2Request,
    ) -> emr_20160408_models.DescribeScalingConfigItemV2Response:
        runtime = util_models.RuntimeOptions()
        return await self.describe_scaling_config_item_v2with_options_async(request, runtime)

    def describe_scaling_group_instance_v2with_options(
        self,
        request: emr_20160408_models.DescribeScalingGroupInstanceV2Request,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DescribeScalingGroupInstanceV2Response:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.host_group_biz_id):
            query['HostGroupBizId'] = request.host_group_biz_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.scaling_group_biz_id):
            query['ScalingGroupBizId'] = request.scaling_group_biz_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeScalingGroupInstanceV2',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DescribeScalingGroupInstanceV2Response(),
            self.call_api(params, req, runtime)
        )

    async def describe_scaling_group_instance_v2with_options_async(
        self,
        request: emr_20160408_models.DescribeScalingGroupInstanceV2Request,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DescribeScalingGroupInstanceV2Response:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.host_group_biz_id):
            query['HostGroupBizId'] = request.host_group_biz_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.scaling_group_biz_id):
            query['ScalingGroupBizId'] = request.scaling_group_biz_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeScalingGroupInstanceV2',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DescribeScalingGroupInstanceV2Response(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_scaling_group_instance_v2(
        self,
        request: emr_20160408_models.DescribeScalingGroupInstanceV2Request,
    ) -> emr_20160408_models.DescribeScalingGroupInstanceV2Response:
        runtime = util_models.RuntimeOptions()
        return self.describe_scaling_group_instance_v2with_options(request, runtime)

    async def describe_scaling_group_instance_v2_async(
        self,
        request: emr_20160408_models.DescribeScalingGroupInstanceV2Request,
    ) -> emr_20160408_models.DescribeScalingGroupInstanceV2Response:
        runtime = util_models.RuntimeOptions()
        return await self.describe_scaling_group_instance_v2with_options_async(request, runtime)

    def describe_scaling_group_v2with_options(
        self,
        request: emr_20160408_models.DescribeScalingGroupV2Request,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DescribeScalingGroupV2Response:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.host_group_biz_id):
            query['HostGroupBizId'] = request.host_group_biz_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.scaling_group_biz_id):
            query['ScalingGroupBizId'] = request.scaling_group_biz_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeScalingGroupV2',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DescribeScalingGroupV2Response(),
            self.call_api(params, req, runtime)
        )

    async def describe_scaling_group_v2with_options_async(
        self,
        request: emr_20160408_models.DescribeScalingGroupV2Request,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.DescribeScalingGroupV2Response:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.host_group_biz_id):
            query['HostGroupBizId'] = request.host_group_biz_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.scaling_group_biz_id):
            query['ScalingGroupBizId'] = request.scaling_group_biz_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeScalingGroupV2',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.DescribeScalingGroupV2Response(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_scaling_group_v2(
        self,
        request: emr_20160408_models.DescribeScalingGroupV2Request,
    ) -> emr_20160408_models.DescribeScalingGroupV2Response:
        runtime = util_models.RuntimeOptions()
        return self.describe_scaling_group_v2with_options(request, runtime)

    async def describe_scaling_group_v2_async(
        self,
        request: emr_20160408_models.DescribeScalingGroupV2Request,
    ) -> emr_20160408_models.DescribeScalingGroupV2Response:
        runtime = util_models.RuntimeOptions()
        return await self.describe_scaling_group_v2with_options_async(request, runtime)

    def join_resource_group_with_options(
        self,
        request: emr_20160408_models.JoinResourceGroupRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.JoinResourceGroupResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_id):
            query['ResourceId'] = request.resource_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.resource_type):
            query['ResourceType'] = request.resource_type
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='JoinResourceGroup',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.JoinResourceGroupResponse(),
            self.call_api(params, req, runtime)
        )

    async def join_resource_group_with_options_async(
        self,
        request: emr_20160408_models.JoinResourceGroupRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.JoinResourceGroupResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_id):
            query['ResourceId'] = request.resource_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.resource_type):
            query['ResourceType'] = request.resource_type
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='JoinResourceGroup',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.JoinResourceGroupResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def join_resource_group(
        self,
        request: emr_20160408_models.JoinResourceGroupRequest,
    ) -> emr_20160408_models.JoinResourceGroupResponse:
        runtime = util_models.RuntimeOptions()
        return self.join_resource_group_with_options(request, runtime)

    async def join_resource_group_async(
        self,
        request: emr_20160408_models.JoinResourceGroupRequest,
    ) -> emr_20160408_models.JoinResourceGroupResponse:
        runtime = util_models.RuntimeOptions()
        return await self.join_resource_group_with_options_async(request, runtime)

    def kill_flow_job_with_options(
        self,
        request: emr_20160408_models.KillFlowJobRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.KillFlowJobResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.job_instance_id):
            query['JobInstanceId'] = request.job_instance_id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='KillFlowJob',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.KillFlowJobResponse(),
            self.call_api(params, req, runtime)
        )

    async def kill_flow_job_with_options_async(
        self,
        request: emr_20160408_models.KillFlowJobRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.KillFlowJobResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.job_instance_id):
            query['JobInstanceId'] = request.job_instance_id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='KillFlowJob',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.KillFlowJobResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def kill_flow_job(
        self,
        request: emr_20160408_models.KillFlowJobRequest,
    ) -> emr_20160408_models.KillFlowJobResponse:
        runtime = util_models.RuntimeOptions()
        return self.kill_flow_job_with_options(request, runtime)

    async def kill_flow_job_async(
        self,
        request: emr_20160408_models.KillFlowJobRequest,
    ) -> emr_20160408_models.KillFlowJobResponse:
        runtime = util_models.RuntimeOptions()
        return await self.kill_flow_job_with_options_async(request, runtime)

    def list_cluster_host_with_options(
        self,
        request: emr_20160408_models.ListClusterHostRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListClusterHostResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.component_name):
            query['ComponentName'] = request.component_name
        if not UtilClient.is_unset(request.group_type):
            query['GroupType'] = request.group_type
        if not UtilClient.is_unset(request.host_group_id):
            query['HostGroupId'] = request.host_group_id
        if not UtilClient.is_unset(request.host_instance_id):
            query['HostInstanceId'] = request.host_instance_id
        if not UtilClient.is_unset(request.host_name):
            query['HostName'] = request.host_name
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.private_ip):
            query['PrivateIp'] = request.private_ip
        if not UtilClient.is_unset(request.public_ip):
            query['PublicIp'] = request.public_ip
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.status_list):
            query['StatusList'] = request.status_list
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListClusterHost',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListClusterHostResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_cluster_host_with_options_async(
        self,
        request: emr_20160408_models.ListClusterHostRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListClusterHostResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.component_name):
            query['ComponentName'] = request.component_name
        if not UtilClient.is_unset(request.group_type):
            query['GroupType'] = request.group_type
        if not UtilClient.is_unset(request.host_group_id):
            query['HostGroupId'] = request.host_group_id
        if not UtilClient.is_unset(request.host_instance_id):
            query['HostInstanceId'] = request.host_instance_id
        if not UtilClient.is_unset(request.host_name):
            query['HostName'] = request.host_name
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.private_ip):
            query['PrivateIp'] = request.private_ip
        if not UtilClient.is_unset(request.public_ip):
            query['PublicIp'] = request.public_ip
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.status_list):
            query['StatusList'] = request.status_list
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListClusterHost',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListClusterHostResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_cluster_host(
        self,
        request: emr_20160408_models.ListClusterHostRequest,
    ) -> emr_20160408_models.ListClusterHostResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_cluster_host_with_options(request, runtime)

    async def list_cluster_host_async(
        self,
        request: emr_20160408_models.ListClusterHostRequest,
    ) -> emr_20160408_models.ListClusterHostResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_cluster_host_with_options_async(request, runtime)

    def list_cluster_host_component_with_options(
        self,
        request: emr_20160408_models.ListClusterHostComponentRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListClusterHostComponentResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.component_name):
            query['ComponentName'] = request.component_name
        if not UtilClient.is_unset(request.component_status):
            query['ComponentStatus'] = request.component_status
        if not UtilClient.is_unset(request.host_instance_id):
            query['HostInstanceId'] = request.host_instance_id
        if not UtilClient.is_unset(request.host_name):
            query['HostName'] = request.host_name
        if not UtilClient.is_unset(request.host_role):
            query['HostRole'] = request.host_role
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.service_name):
            query['ServiceName'] = request.service_name
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListClusterHostComponent',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListClusterHostComponentResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_cluster_host_component_with_options_async(
        self,
        request: emr_20160408_models.ListClusterHostComponentRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListClusterHostComponentResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.component_name):
            query['ComponentName'] = request.component_name
        if not UtilClient.is_unset(request.component_status):
            query['ComponentStatus'] = request.component_status
        if not UtilClient.is_unset(request.host_instance_id):
            query['HostInstanceId'] = request.host_instance_id
        if not UtilClient.is_unset(request.host_name):
            query['HostName'] = request.host_name
        if not UtilClient.is_unset(request.host_role):
            query['HostRole'] = request.host_role
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.service_name):
            query['ServiceName'] = request.service_name
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListClusterHostComponent',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListClusterHostComponentResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_cluster_host_component(
        self,
        request: emr_20160408_models.ListClusterHostComponentRequest,
    ) -> emr_20160408_models.ListClusterHostComponentResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_cluster_host_component_with_options(request, runtime)

    async def list_cluster_host_component_async(
        self,
        request: emr_20160408_models.ListClusterHostComponentRequest,
    ) -> emr_20160408_models.ListClusterHostComponentResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_cluster_host_component_with_options_async(request, runtime)

    def list_cluster_host_group_with_options(
        self,
        request: emr_20160408_models.ListClusterHostGroupRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListClusterHostGroupResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.host_group_id):
            query['HostGroupId'] = request.host_group_id
        if not UtilClient.is_unset(request.host_group_name):
            query['HostGroupName'] = request.host_group_name
        if not UtilClient.is_unset(request.host_group_type):
            query['HostGroupType'] = request.host_group_type
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.status_list):
            query['StatusList'] = request.status_list
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListClusterHostGroup',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListClusterHostGroupResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_cluster_host_group_with_options_async(
        self,
        request: emr_20160408_models.ListClusterHostGroupRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListClusterHostGroupResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.host_group_id):
            query['HostGroupId'] = request.host_group_id
        if not UtilClient.is_unset(request.host_group_name):
            query['HostGroupName'] = request.host_group_name
        if not UtilClient.is_unset(request.host_group_type):
            query['HostGroupType'] = request.host_group_type
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.status_list):
            query['StatusList'] = request.status_list
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListClusterHostGroup',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListClusterHostGroupResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_cluster_host_group(
        self,
        request: emr_20160408_models.ListClusterHostGroupRequest,
    ) -> emr_20160408_models.ListClusterHostGroupResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_cluster_host_group_with_options(request, runtime)

    async def list_cluster_host_group_async(
        self,
        request: emr_20160408_models.ListClusterHostGroupRequest,
    ) -> emr_20160408_models.ListClusterHostGroupResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_cluster_host_group_with_options_async(request, runtime)

    def list_cluster_installed_service_with_options(
        self,
        request: emr_20160408_models.ListClusterInstalledServiceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListClusterInstalledServiceResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListClusterInstalledService',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListClusterInstalledServiceResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_cluster_installed_service_with_options_async(
        self,
        request: emr_20160408_models.ListClusterInstalledServiceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListClusterInstalledServiceResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListClusterInstalledService',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListClusterInstalledServiceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_cluster_installed_service(
        self,
        request: emr_20160408_models.ListClusterInstalledServiceRequest,
    ) -> emr_20160408_models.ListClusterInstalledServiceResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_cluster_installed_service_with_options(request, runtime)

    async def list_cluster_installed_service_async(
        self,
        request: emr_20160408_models.ListClusterInstalledServiceRequest,
    ) -> emr_20160408_models.ListClusterInstalledServiceResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_cluster_installed_service_with_options_async(request, runtime)

    def list_cluster_operation_with_options(
        self,
        request: emr_20160408_models.ListClusterOperationRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListClusterOperationResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.operation_id):
            query['OperationId'] = request.operation_id
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.service_name):
            query['ServiceName'] = request.service_name
        if not UtilClient.is_unset(request.status):
            query['Status'] = request.status
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListClusterOperation',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListClusterOperationResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_cluster_operation_with_options_async(
        self,
        request: emr_20160408_models.ListClusterOperationRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListClusterOperationResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.operation_id):
            query['OperationId'] = request.operation_id
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.service_name):
            query['ServiceName'] = request.service_name
        if not UtilClient.is_unset(request.status):
            query['Status'] = request.status
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListClusterOperation',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListClusterOperationResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_cluster_operation(
        self,
        request: emr_20160408_models.ListClusterOperationRequest,
    ) -> emr_20160408_models.ListClusterOperationResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_cluster_operation_with_options(request, runtime)

    async def list_cluster_operation_async(
        self,
        request: emr_20160408_models.ListClusterOperationRequest,
    ) -> emr_20160408_models.ListClusterOperationResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_cluster_operation_with_options_async(request, runtime)

    def list_cluster_operation_host_with_options(
        self,
        request: emr_20160408_models.ListClusterOperationHostRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListClusterOperationHostResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.operation_id):
            query['OperationId'] = request.operation_id
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.status):
            query['Status'] = request.status
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListClusterOperationHost',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListClusterOperationHostResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_cluster_operation_host_with_options_async(
        self,
        request: emr_20160408_models.ListClusterOperationHostRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListClusterOperationHostResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.operation_id):
            query['OperationId'] = request.operation_id
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.status):
            query['Status'] = request.status
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListClusterOperationHost',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListClusterOperationHostResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_cluster_operation_host(
        self,
        request: emr_20160408_models.ListClusterOperationHostRequest,
    ) -> emr_20160408_models.ListClusterOperationHostResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_cluster_operation_host_with_options(request, runtime)

    async def list_cluster_operation_host_async(
        self,
        request: emr_20160408_models.ListClusterOperationHostRequest,
    ) -> emr_20160408_models.ListClusterOperationHostResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_cluster_operation_host_with_options_async(request, runtime)

    def list_cluster_operation_host_task_with_options(
        self,
        request: emr_20160408_models.ListClusterOperationHostTaskRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListClusterOperationHostTaskResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.host_id):
            query['HostId'] = request.host_id
        if not UtilClient.is_unset(request.operation_id):
            query['OperationId'] = request.operation_id
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.status):
            query['Status'] = request.status
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListClusterOperationHostTask',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListClusterOperationHostTaskResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_cluster_operation_host_task_with_options_async(
        self,
        request: emr_20160408_models.ListClusterOperationHostTaskRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListClusterOperationHostTaskResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.host_id):
            query['HostId'] = request.host_id
        if not UtilClient.is_unset(request.operation_id):
            query['OperationId'] = request.operation_id
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.status):
            query['Status'] = request.status
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListClusterOperationHostTask',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListClusterOperationHostTaskResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_cluster_operation_host_task(
        self,
        request: emr_20160408_models.ListClusterOperationHostTaskRequest,
    ) -> emr_20160408_models.ListClusterOperationHostTaskResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_cluster_operation_host_task_with_options(request, runtime)

    async def list_cluster_operation_host_task_async(
        self,
        request: emr_20160408_models.ListClusterOperationHostTaskRequest,
    ) -> emr_20160408_models.ListClusterOperationHostTaskResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_cluster_operation_host_task_with_options_async(request, runtime)

    def list_cluster_operation_task_with_options(
        self,
        request: emr_20160408_models.ListClusterOperationTaskRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListClusterOperationTaskResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.operation_id):
            query['OperationId'] = request.operation_id
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.status):
            query['Status'] = request.status
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListClusterOperationTask',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListClusterOperationTaskResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_cluster_operation_task_with_options_async(
        self,
        request: emr_20160408_models.ListClusterOperationTaskRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListClusterOperationTaskResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.operation_id):
            query['OperationId'] = request.operation_id
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.status):
            query['Status'] = request.status
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListClusterOperationTask',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListClusterOperationTaskResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_cluster_operation_task(
        self,
        request: emr_20160408_models.ListClusterOperationTaskRequest,
    ) -> emr_20160408_models.ListClusterOperationTaskResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_cluster_operation_task_with_options(request, runtime)

    async def list_cluster_operation_task_async(
        self,
        request: emr_20160408_models.ListClusterOperationTaskRequest,
    ) -> emr_20160408_models.ListClusterOperationTaskResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_cluster_operation_task_with_options_async(request, runtime)

    def list_cluster_service_with_options(
        self,
        request: emr_20160408_models.ListClusterServiceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListClusterServiceResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListClusterService',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListClusterServiceResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_cluster_service_with_options_async(
        self,
        request: emr_20160408_models.ListClusterServiceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListClusterServiceResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListClusterService',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListClusterServiceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_cluster_service(
        self,
        request: emr_20160408_models.ListClusterServiceRequest,
    ) -> emr_20160408_models.ListClusterServiceResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_cluster_service_with_options(request, runtime)

    async def list_cluster_service_async(
        self,
        request: emr_20160408_models.ListClusterServiceRequest,
    ) -> emr_20160408_models.ListClusterServiceResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_cluster_service_with_options_async(request, runtime)

    def list_cluster_service_component_health_info_with_options(
        self,
        request: emr_20160408_models.ListClusterServiceComponentHealthInfoRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListClusterServiceComponentHealthInfoResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.component_name):
            query['ComponentName'] = request.component_name
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.service_name):
            query['ServiceName'] = request.service_name
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListClusterServiceComponentHealthInfo',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListClusterServiceComponentHealthInfoResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_cluster_service_component_health_info_with_options_async(
        self,
        request: emr_20160408_models.ListClusterServiceComponentHealthInfoRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListClusterServiceComponentHealthInfoResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.component_name):
            query['ComponentName'] = request.component_name
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.service_name):
            query['ServiceName'] = request.service_name
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListClusterServiceComponentHealthInfo',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListClusterServiceComponentHealthInfoResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_cluster_service_component_health_info(
        self,
        request: emr_20160408_models.ListClusterServiceComponentHealthInfoRequest,
    ) -> emr_20160408_models.ListClusterServiceComponentHealthInfoResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_cluster_service_component_health_info_with_options(request, runtime)

    async def list_cluster_service_component_health_info_async(
        self,
        request: emr_20160408_models.ListClusterServiceComponentHealthInfoRequest,
    ) -> emr_20160408_models.ListClusterServiceComponentHealthInfoResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_cluster_service_component_health_info_with_options_async(request, runtime)

    def list_cluster_service_config_history_with_options(
        self,
        request: emr_20160408_models.ListClusterServiceConfigHistoryRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListClusterServiceConfigHistoryResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.author):
            query['Author'] = request.author
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.comment):
            query['Comment'] = request.comment
        if not UtilClient.is_unset(request.config_file_name):
            query['ConfigFileName'] = request.config_file_name
        if not UtilClient.is_unset(request.config_item_key):
            query['ConfigItemKey'] = request.config_item_key
        if not UtilClient.is_unset(request.config_version):
            query['ConfigVersion'] = request.config_version
        if not UtilClient.is_unset(request.host_group_id):
            query['HostGroupId'] = request.host_group_id
        if not UtilClient.is_unset(request.host_instance_id):
            query['HostInstanceId'] = request.host_instance_id
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.service_name):
            query['ServiceName'] = request.service_name
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListClusterServiceConfigHistory',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListClusterServiceConfigHistoryResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_cluster_service_config_history_with_options_async(
        self,
        request: emr_20160408_models.ListClusterServiceConfigHistoryRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListClusterServiceConfigHistoryResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.author):
            query['Author'] = request.author
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.comment):
            query['Comment'] = request.comment
        if not UtilClient.is_unset(request.config_file_name):
            query['ConfigFileName'] = request.config_file_name
        if not UtilClient.is_unset(request.config_item_key):
            query['ConfigItemKey'] = request.config_item_key
        if not UtilClient.is_unset(request.config_version):
            query['ConfigVersion'] = request.config_version
        if not UtilClient.is_unset(request.host_group_id):
            query['HostGroupId'] = request.host_group_id
        if not UtilClient.is_unset(request.host_instance_id):
            query['HostInstanceId'] = request.host_instance_id
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.service_name):
            query['ServiceName'] = request.service_name
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListClusterServiceConfigHistory',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListClusterServiceConfigHistoryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_cluster_service_config_history(
        self,
        request: emr_20160408_models.ListClusterServiceConfigHistoryRequest,
    ) -> emr_20160408_models.ListClusterServiceConfigHistoryResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_cluster_service_config_history_with_options(request, runtime)

    async def list_cluster_service_config_history_async(
        self,
        request: emr_20160408_models.ListClusterServiceConfigHistoryRequest,
    ) -> emr_20160408_models.ListClusterServiceConfigHistoryResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_cluster_service_config_history_with_options_async(request, runtime)

    def list_cluster_service_quick_link_with_options(
        self,
        request: emr_20160408_models.ListClusterServiceQuickLinkRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListClusterServiceQuickLinkResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.direct_type):
            query['DirectType'] = request.direct_type
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.service_name):
            query['ServiceName'] = request.service_name
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListClusterServiceQuickLink',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListClusterServiceQuickLinkResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_cluster_service_quick_link_with_options_async(
        self,
        request: emr_20160408_models.ListClusterServiceQuickLinkRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListClusterServiceQuickLinkResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.direct_type):
            query['DirectType'] = request.direct_type
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.service_name):
            query['ServiceName'] = request.service_name
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListClusterServiceQuickLink',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListClusterServiceQuickLinkResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_cluster_service_quick_link(
        self,
        request: emr_20160408_models.ListClusterServiceQuickLinkRequest,
    ) -> emr_20160408_models.ListClusterServiceQuickLinkResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_cluster_service_quick_link_with_options(request, runtime)

    async def list_cluster_service_quick_link_async(
        self,
        request: emr_20160408_models.ListClusterServiceQuickLinkRequest,
    ) -> emr_20160408_models.ListClusterServiceQuickLinkResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_cluster_service_quick_link_with_options_async(request, runtime)

    def list_cluster_templates_with_options(
        self,
        request: emr_20160408_models.ListClusterTemplatesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListClusterTemplatesResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_id):
            query['BizId'] = request.biz_id
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.product_type):
            query['ProductType'] = request.product_type
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListClusterTemplates',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListClusterTemplatesResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_cluster_templates_with_options_async(
        self,
        request: emr_20160408_models.ListClusterTemplatesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListClusterTemplatesResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.biz_id):
            query['BizId'] = request.biz_id
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.product_type):
            query['ProductType'] = request.product_type
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListClusterTemplates',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListClusterTemplatesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_cluster_templates(
        self,
        request: emr_20160408_models.ListClusterTemplatesRequest,
    ) -> emr_20160408_models.ListClusterTemplatesResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_cluster_templates_with_options(request, runtime)

    async def list_cluster_templates_async(
        self,
        request: emr_20160408_models.ListClusterTemplatesRequest,
    ) -> emr_20160408_models.ListClusterTemplatesResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_cluster_templates_with_options_async(request, runtime)

    def list_clusters_with_options(
        self,
        request: emr_20160408_models.ListClustersRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListClustersResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_type_list):
            query['ClusterTypeList'] = request.cluster_type_list
        if not UtilClient.is_unset(request.create_type):
            query['CreateType'] = request.create_type
        if not UtilClient.is_unset(request.default_status):
            query['DefaultStatus'] = request.default_status
        if not UtilClient.is_unset(request.deposit_type):
            query['DepositType'] = request.deposit_type
        if not UtilClient.is_unset(request.expired_tag_list):
            query['ExpiredTagList'] = request.expired_tag_list
        if not UtilClient.is_unset(request.is_desc):
            query['IsDesc'] = request.is_desc
        if not UtilClient.is_unset(request.machine_type):
            query['MachineType'] = request.machine_type
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.status_list):
            query['StatusList'] = request.status_list
        if not UtilClient.is_unset(request.tag):
            query['Tag'] = request.tag
        if not UtilClient.is_unset(request.vpc_id):
            query['VpcId'] = request.vpc_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListClusters',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListClustersResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_clusters_with_options_async(
        self,
        request: emr_20160408_models.ListClustersRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListClustersResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_type_list):
            query['ClusterTypeList'] = request.cluster_type_list
        if not UtilClient.is_unset(request.create_type):
            query['CreateType'] = request.create_type
        if not UtilClient.is_unset(request.default_status):
            query['DefaultStatus'] = request.default_status
        if not UtilClient.is_unset(request.deposit_type):
            query['DepositType'] = request.deposit_type
        if not UtilClient.is_unset(request.expired_tag_list):
            query['ExpiredTagList'] = request.expired_tag_list
        if not UtilClient.is_unset(request.is_desc):
            query['IsDesc'] = request.is_desc
        if not UtilClient.is_unset(request.machine_type):
            query['MachineType'] = request.machine_type
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.status_list):
            query['StatusList'] = request.status_list
        if not UtilClient.is_unset(request.tag):
            query['Tag'] = request.tag
        if not UtilClient.is_unset(request.vpc_id):
            query['VpcId'] = request.vpc_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListClusters',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListClustersResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_clusters(
        self,
        request: emr_20160408_models.ListClustersRequest,
    ) -> emr_20160408_models.ListClustersResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_clusters_with_options(request, runtime)

    async def list_clusters_async(
        self,
        request: emr_20160408_models.ListClustersRequest,
    ) -> emr_20160408_models.ListClustersResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_clusters_with_options_async(request, runtime)

    def list_emr_available_config_with_options(
        self,
        request: emr_20160408_models.ListEmrAvailableConfigRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListEmrAvailableConfigResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListEmrAvailableConfig',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListEmrAvailableConfigResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_emr_available_config_with_options_async(
        self,
        request: emr_20160408_models.ListEmrAvailableConfigRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListEmrAvailableConfigResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListEmrAvailableConfig',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListEmrAvailableConfigResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_emr_available_config(
        self,
        request: emr_20160408_models.ListEmrAvailableConfigRequest,
    ) -> emr_20160408_models.ListEmrAvailableConfigResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_emr_available_config_with_options(request, runtime)

    async def list_emr_available_config_async(
        self,
        request: emr_20160408_models.ListEmrAvailableConfigRequest,
    ) -> emr_20160408_models.ListEmrAvailableConfigResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_emr_available_config_with_options_async(request, runtime)

    def list_emr_available_resource_with_options(
        self,
        request: emr_20160408_models.ListEmrAvailableResourceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListEmrAvailableResourceResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.cluster_type):
            query['ClusterType'] = request.cluster_type
        if not UtilClient.is_unset(request.data_disk_type):
            query['DataDiskType'] = request.data_disk_type
        if not UtilClient.is_unset(request.deposit_type):
            query['DepositType'] = request.deposit_type
        if not UtilClient.is_unset(request.destination_resource):
            query['DestinationResource'] = request.destination_resource
        if not UtilClient.is_unset(request.emr_version):
            query['EmrVersion'] = request.emr_version
        if not UtilClient.is_unset(request.instance_charge_type):
            query['InstanceChargeType'] = request.instance_charge_type
        if not UtilClient.is_unset(request.instance_type):
            query['InstanceType'] = request.instance_type
        if not UtilClient.is_unset(request.net_type):
            query['NetType'] = request.net_type
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.spot_strategy):
            query['SpotStrategy'] = request.spot_strategy
        if not UtilClient.is_unset(request.system_disk_type):
            query['SystemDiskType'] = request.system_disk_type
        if not UtilClient.is_unset(request.zone_id):
            query['ZoneId'] = request.zone_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListEmrAvailableResource',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListEmrAvailableResourceResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_emr_available_resource_with_options_async(
        self,
        request: emr_20160408_models.ListEmrAvailableResourceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListEmrAvailableResourceResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.cluster_type):
            query['ClusterType'] = request.cluster_type
        if not UtilClient.is_unset(request.data_disk_type):
            query['DataDiskType'] = request.data_disk_type
        if not UtilClient.is_unset(request.deposit_type):
            query['DepositType'] = request.deposit_type
        if not UtilClient.is_unset(request.destination_resource):
            query['DestinationResource'] = request.destination_resource
        if not UtilClient.is_unset(request.emr_version):
            query['EmrVersion'] = request.emr_version
        if not UtilClient.is_unset(request.instance_charge_type):
            query['InstanceChargeType'] = request.instance_charge_type
        if not UtilClient.is_unset(request.instance_type):
            query['InstanceType'] = request.instance_type
        if not UtilClient.is_unset(request.net_type):
            query['NetType'] = request.net_type
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.spot_strategy):
            query['SpotStrategy'] = request.spot_strategy
        if not UtilClient.is_unset(request.system_disk_type):
            query['SystemDiskType'] = request.system_disk_type
        if not UtilClient.is_unset(request.zone_id):
            query['ZoneId'] = request.zone_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListEmrAvailableResource',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListEmrAvailableResourceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_emr_available_resource(
        self,
        request: emr_20160408_models.ListEmrAvailableResourceRequest,
    ) -> emr_20160408_models.ListEmrAvailableResourceResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_emr_available_resource_with_options(request, runtime)

    async def list_emr_available_resource_async(
        self,
        request: emr_20160408_models.ListEmrAvailableResourceRequest,
    ) -> emr_20160408_models.ListEmrAvailableResourceResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_emr_available_resource_with_options_async(request, runtime)

    def list_emr_main_version_with_options(
        self,
        request: emr_20160408_models.ListEmrMainVersionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListEmrMainVersionResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.emr_version):
            query['EmrVersion'] = request.emr_version
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.stack_name):
            query['StackName'] = request.stack_name
        if not UtilClient.is_unset(request.stack_version):
            query['StackVersion'] = request.stack_version
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListEmrMainVersion',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListEmrMainVersionResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_emr_main_version_with_options_async(
        self,
        request: emr_20160408_models.ListEmrMainVersionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListEmrMainVersionResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.emr_version):
            query['EmrVersion'] = request.emr_version
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.stack_name):
            query['StackName'] = request.stack_name
        if not UtilClient.is_unset(request.stack_version):
            query['StackVersion'] = request.stack_version
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListEmrMainVersion',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListEmrMainVersionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_emr_main_version(
        self,
        request: emr_20160408_models.ListEmrMainVersionRequest,
    ) -> emr_20160408_models.ListEmrMainVersionResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_emr_main_version_with_options(request, runtime)

    async def list_emr_main_version_async(
        self,
        request: emr_20160408_models.ListEmrMainVersionRequest,
    ) -> emr_20160408_models.ListEmrMainVersionResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_emr_main_version_with_options_async(request, runtime)

    def list_flow_with_options(
        self,
        request: emr_20160408_models.ListFlowRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListFlowResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.job_id):
            query['JobId'] = request.job_id
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.periodic):
            query['Periodic'] = request.periodic
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.status):
            query['Status'] = request.status
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListFlow',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListFlowResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_flow_with_options_async(
        self,
        request: emr_20160408_models.ListFlowRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListFlowResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.job_id):
            query['JobId'] = request.job_id
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.periodic):
            query['Periodic'] = request.periodic
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.status):
            query['Status'] = request.status
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListFlow',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListFlowResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_flow(
        self,
        request: emr_20160408_models.ListFlowRequest,
    ) -> emr_20160408_models.ListFlowResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_flow_with_options(request, runtime)

    async def list_flow_async(
        self,
        request: emr_20160408_models.ListFlowRequest,
    ) -> emr_20160408_models.ListFlowResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_flow_with_options_async(request, runtime)

    def list_flow_category_with_options(
        self,
        request: emr_20160408_models.ListFlowCategoryRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListFlowCategoryResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.parent_id):
            query['ParentId'] = request.parent_id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.root):
            query['Root'] = request.root
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListFlowCategory',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListFlowCategoryResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_flow_category_with_options_async(
        self,
        request: emr_20160408_models.ListFlowCategoryRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListFlowCategoryResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.parent_id):
            query['ParentId'] = request.parent_id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.root):
            query['Root'] = request.root
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListFlowCategory',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListFlowCategoryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_flow_category(
        self,
        request: emr_20160408_models.ListFlowCategoryRequest,
    ) -> emr_20160408_models.ListFlowCategoryResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_flow_category_with_options(request, runtime)

    async def list_flow_category_async(
        self,
        request: emr_20160408_models.ListFlowCategoryRequest,
    ) -> emr_20160408_models.ListFlowCategoryResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_flow_category_with_options_async(request, runtime)

    def list_flow_cluster_with_options(
        self,
        request: emr_20160408_models.ListFlowClusterRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListFlowClusterResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListFlowCluster',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListFlowClusterResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_flow_cluster_with_options_async(
        self,
        request: emr_20160408_models.ListFlowClusterRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListFlowClusterResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListFlowCluster',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListFlowClusterResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_flow_cluster(
        self,
        request: emr_20160408_models.ListFlowClusterRequest,
    ) -> emr_20160408_models.ListFlowClusterResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_flow_cluster_with_options(request, runtime)

    async def list_flow_cluster_async(
        self,
        request: emr_20160408_models.ListFlowClusterRequest,
    ) -> emr_20160408_models.ListFlowClusterResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_flow_cluster_with_options_async(request, runtime)

    def list_flow_cluster_all_with_options(
        self,
        request: emr_20160408_models.ListFlowClusterAllRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListFlowClusterAllResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.product_type):
            query['ProductType'] = request.product_type
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListFlowClusterAll',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListFlowClusterAllResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_flow_cluster_all_with_options_async(
        self,
        request: emr_20160408_models.ListFlowClusterAllRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListFlowClusterAllResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.product_type):
            query['ProductType'] = request.product_type
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListFlowClusterAll',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListFlowClusterAllResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_flow_cluster_all(
        self,
        request: emr_20160408_models.ListFlowClusterAllRequest,
    ) -> emr_20160408_models.ListFlowClusterAllResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_flow_cluster_all_with_options(request, runtime)

    async def list_flow_cluster_all_async(
        self,
        request: emr_20160408_models.ListFlowClusterAllRequest,
    ) -> emr_20160408_models.ListFlowClusterAllResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_flow_cluster_all_with_options_async(request, runtime)

    def list_flow_cluster_all_hosts_with_options(
        self,
        request: emr_20160408_models.ListFlowClusterAllHostsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListFlowClusterAllHostsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListFlowClusterAllHosts',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListFlowClusterAllHostsResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_flow_cluster_all_hosts_with_options_async(
        self,
        request: emr_20160408_models.ListFlowClusterAllHostsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListFlowClusterAllHostsResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListFlowClusterAllHosts',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListFlowClusterAllHostsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_flow_cluster_all_hosts(
        self,
        request: emr_20160408_models.ListFlowClusterAllHostsRequest,
    ) -> emr_20160408_models.ListFlowClusterAllHostsResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_flow_cluster_all_hosts_with_options(request, runtime)

    async def list_flow_cluster_all_hosts_async(
        self,
        request: emr_20160408_models.ListFlowClusterAllHostsRequest,
    ) -> emr_20160408_models.ListFlowClusterAllHostsResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_flow_cluster_all_hosts_with_options_async(request, runtime)

    def list_flow_cluster_host_with_options(
        self,
        request: emr_20160408_models.ListFlowClusterHostRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListFlowClusterHostResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListFlowClusterHost',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListFlowClusterHostResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_flow_cluster_host_with_options_async(
        self,
        request: emr_20160408_models.ListFlowClusterHostRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListFlowClusterHostResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListFlowClusterHost',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListFlowClusterHostResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_flow_cluster_host(
        self,
        request: emr_20160408_models.ListFlowClusterHostRequest,
    ) -> emr_20160408_models.ListFlowClusterHostResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_flow_cluster_host_with_options(request, runtime)

    async def list_flow_cluster_host_async(
        self,
        request: emr_20160408_models.ListFlowClusterHostRequest,
    ) -> emr_20160408_models.ListFlowClusterHostResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_flow_cluster_host_with_options_async(request, runtime)

    def list_flow_instance_with_options(
        self,
        request: emr_20160408_models.ListFlowInstanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListFlowInstanceResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.flow_id):
            query['FlowId'] = request.flow_id
        if not UtilClient.is_unset(request.flow_name):
            query['FlowName'] = request.flow_name
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.node_instance_id):
            query['NodeInstanceId'] = request.node_instance_id
        if not UtilClient.is_unset(request.order_by):
            query['OrderBy'] = request.order_by
        if not UtilClient.is_unset(request.order_type):
            query['OrderType'] = request.order_type
        if not UtilClient.is_unset(request.owner):
            query['Owner'] = request.owner
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.status_list):
            query['StatusList'] = request.status_list
        if not UtilClient.is_unset(request.time_range):
            query['TimeRange'] = request.time_range
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListFlowInstance',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListFlowInstanceResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_flow_instance_with_options_async(
        self,
        request: emr_20160408_models.ListFlowInstanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListFlowInstanceResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.flow_id):
            query['FlowId'] = request.flow_id
        if not UtilClient.is_unset(request.flow_name):
            query['FlowName'] = request.flow_name
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.node_instance_id):
            query['NodeInstanceId'] = request.node_instance_id
        if not UtilClient.is_unset(request.order_by):
            query['OrderBy'] = request.order_by
        if not UtilClient.is_unset(request.order_type):
            query['OrderType'] = request.order_type
        if not UtilClient.is_unset(request.owner):
            query['Owner'] = request.owner
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.status_list):
            query['StatusList'] = request.status_list
        if not UtilClient.is_unset(request.time_range):
            query['TimeRange'] = request.time_range
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListFlowInstance',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListFlowInstanceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_flow_instance(
        self,
        request: emr_20160408_models.ListFlowInstanceRequest,
    ) -> emr_20160408_models.ListFlowInstanceResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_flow_instance_with_options(request, runtime)

    async def list_flow_instance_async(
        self,
        request: emr_20160408_models.ListFlowInstanceRequest,
    ) -> emr_20160408_models.ListFlowInstanceResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_flow_instance_with_options_async(request, runtime)

    def list_flow_job_with_options(
        self,
        request: emr_20160408_models.ListFlowJobRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListFlowJobResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.adhoc):
            query['Adhoc'] = request.adhoc
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.type):
            query['Type'] = request.type
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListFlowJob',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListFlowJobResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_flow_job_with_options_async(
        self,
        request: emr_20160408_models.ListFlowJobRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListFlowJobResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.adhoc):
            query['Adhoc'] = request.adhoc
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.type):
            query['Type'] = request.type
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListFlowJob',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListFlowJobResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_flow_job(
        self,
        request: emr_20160408_models.ListFlowJobRequest,
    ) -> emr_20160408_models.ListFlowJobResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_flow_job_with_options(request, runtime)

    async def list_flow_job_async(
        self,
        request: emr_20160408_models.ListFlowJobRequest,
    ) -> emr_20160408_models.ListFlowJobResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_flow_job_with_options_async(request, runtime)

    def list_flow_job_history_with_options(
        self,
        request: emr_20160408_models.ListFlowJobHistoryRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListFlowJobHistoryResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.job_type):
            query['JobType'] = request.job_type
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.status_list):
            query['StatusList'] = request.status_list
        if not UtilClient.is_unset(request.time_range):
            query['TimeRange'] = request.time_range
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListFlowJobHistory',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListFlowJobHistoryResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_flow_job_history_with_options_async(
        self,
        request: emr_20160408_models.ListFlowJobHistoryRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListFlowJobHistoryResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.instance_id):
            query['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.job_type):
            query['JobType'] = request.job_type
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.status_list):
            query['StatusList'] = request.status_list
        if not UtilClient.is_unset(request.time_range):
            query['TimeRange'] = request.time_range
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListFlowJobHistory',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListFlowJobHistoryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_flow_job_history(
        self,
        request: emr_20160408_models.ListFlowJobHistoryRequest,
    ) -> emr_20160408_models.ListFlowJobHistoryResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_flow_job_history_with_options(request, runtime)

    async def list_flow_job_history_async(
        self,
        request: emr_20160408_models.ListFlowJobHistoryRequest,
    ) -> emr_20160408_models.ListFlowJobHistoryResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_flow_job_history_with_options_async(request, runtime)

    def list_flow_node_instance_with_options(
        self,
        request: emr_20160408_models.ListFlowNodeInstanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListFlowNodeInstanceResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.order_by):
            query['OrderBy'] = request.order_by
        if not UtilClient.is_unset(request.order_type):
            query['OrderType'] = request.order_type
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.status_list):
            query['StatusList'] = request.status_list
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListFlowNodeInstance',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListFlowNodeInstanceResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_flow_node_instance_with_options_async(
        self,
        request: emr_20160408_models.ListFlowNodeInstanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListFlowNodeInstanceResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.order_by):
            query['OrderBy'] = request.order_by
        if not UtilClient.is_unset(request.order_type):
            query['OrderType'] = request.order_type
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        if not UtilClient.is_unset(request.status_list):
            query['StatusList'] = request.status_list
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListFlowNodeInstance',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListFlowNodeInstanceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_flow_node_instance(
        self,
        request: emr_20160408_models.ListFlowNodeInstanceRequest,
    ) -> emr_20160408_models.ListFlowNodeInstanceResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_flow_node_instance_with_options(request, runtime)

    async def list_flow_node_instance_async(
        self,
        request: emr_20160408_models.ListFlowNodeInstanceRequest,
    ) -> emr_20160408_models.ListFlowNodeInstanceResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_flow_node_instance_with_options_async(request, runtime)

    def list_flow_node_instance_container_status_with_options(
        self,
        request: emr_20160408_models.ListFlowNodeInstanceContainerStatusRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListFlowNodeInstanceContainerStatusResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.node_instance_id):
            query['NodeInstanceId'] = request.node_instance_id
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListFlowNodeInstanceContainerStatus',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListFlowNodeInstanceContainerStatusResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_flow_node_instance_container_status_with_options_async(
        self,
        request: emr_20160408_models.ListFlowNodeInstanceContainerStatusRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListFlowNodeInstanceContainerStatusResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.node_instance_id):
            query['NodeInstanceId'] = request.node_instance_id
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListFlowNodeInstanceContainerStatus',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListFlowNodeInstanceContainerStatusResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_flow_node_instance_container_status(
        self,
        request: emr_20160408_models.ListFlowNodeInstanceContainerStatusRequest,
    ) -> emr_20160408_models.ListFlowNodeInstanceContainerStatusResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_flow_node_instance_container_status_with_options(request, runtime)

    async def list_flow_node_instance_container_status_async(
        self,
        request: emr_20160408_models.ListFlowNodeInstanceContainerStatusRequest,
    ) -> emr_20160408_models.ListFlowNodeInstanceContainerStatusResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_flow_node_instance_container_status_with_options_async(request, runtime)

    def list_flow_node_sql_result_with_options(
        self,
        request: emr_20160408_models.ListFlowNodeSqlResultRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListFlowNodeSqlResultResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.length):
            query['Length'] = request.length
        if not UtilClient.is_unset(request.node_instance_id):
            query['NodeInstanceId'] = request.node_instance_id
        if not UtilClient.is_unset(request.offset):
            query['Offset'] = request.offset
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.sql_index):
            query['SqlIndex'] = request.sql_index
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListFlowNodeSqlResult',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListFlowNodeSqlResultResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_flow_node_sql_result_with_options_async(
        self,
        request: emr_20160408_models.ListFlowNodeSqlResultRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListFlowNodeSqlResultResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.length):
            query['Length'] = request.length
        if not UtilClient.is_unset(request.node_instance_id):
            query['NodeInstanceId'] = request.node_instance_id
        if not UtilClient.is_unset(request.offset):
            query['Offset'] = request.offset
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.sql_index):
            query['SqlIndex'] = request.sql_index
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListFlowNodeSqlResult',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListFlowNodeSqlResultResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_flow_node_sql_result(
        self,
        request: emr_20160408_models.ListFlowNodeSqlResultRequest,
    ) -> emr_20160408_models.ListFlowNodeSqlResultResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_flow_node_sql_result_with_options(request, runtime)

    async def list_flow_node_sql_result_async(
        self,
        request: emr_20160408_models.ListFlowNodeSqlResultRequest,
    ) -> emr_20160408_models.ListFlowNodeSqlResultResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_flow_node_sql_result_with_options_async(request, runtime)

    def list_flow_project_with_options(
        self,
        request: emr_20160408_models.ListFlowProjectRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListFlowProjectResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.product_type):
            query['ProductType'] = request.product_type
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListFlowProject',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListFlowProjectResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_flow_project_with_options_async(
        self,
        request: emr_20160408_models.ListFlowProjectRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListFlowProjectResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.product_type):
            query['ProductType'] = request.product_type
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListFlowProject',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListFlowProjectResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_flow_project(
        self,
        request: emr_20160408_models.ListFlowProjectRequest,
    ) -> emr_20160408_models.ListFlowProjectResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_flow_project_with_options(request, runtime)

    async def list_flow_project_async(
        self,
        request: emr_20160408_models.ListFlowProjectRequest,
    ) -> emr_20160408_models.ListFlowProjectResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_flow_project_with_options_async(request, runtime)

    def list_flow_project_cluster_setting_with_options(
        self,
        request: emr_20160408_models.ListFlowProjectClusterSettingRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListFlowProjectClusterSettingResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListFlowProjectClusterSetting',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListFlowProjectClusterSettingResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_flow_project_cluster_setting_with_options_async(
        self,
        request: emr_20160408_models.ListFlowProjectClusterSettingRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListFlowProjectClusterSettingResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListFlowProjectClusterSetting',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListFlowProjectClusterSettingResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_flow_project_cluster_setting(
        self,
        request: emr_20160408_models.ListFlowProjectClusterSettingRequest,
    ) -> emr_20160408_models.ListFlowProjectClusterSettingResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_flow_project_cluster_setting_with_options(request, runtime)

    async def list_flow_project_cluster_setting_async(
        self,
        request: emr_20160408_models.ListFlowProjectClusterSettingRequest,
    ) -> emr_20160408_models.ListFlowProjectClusterSettingResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_flow_project_cluster_setting_with_options_async(request, runtime)

    def list_flow_project_user_with_options(
        self,
        request: emr_20160408_models.ListFlowProjectUserRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListFlowProjectUserResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListFlowProjectUser',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListFlowProjectUserResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_flow_project_user_with_options_async(
        self,
        request: emr_20160408_models.ListFlowProjectUserRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListFlowProjectUserResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListFlowProjectUser',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListFlowProjectUserResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_flow_project_user(
        self,
        request: emr_20160408_models.ListFlowProjectUserRequest,
    ) -> emr_20160408_models.ListFlowProjectUserResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_flow_project_user_with_options(request, runtime)

    async def list_flow_project_user_async(
        self,
        request: emr_20160408_models.ListFlowProjectUserRequest,
    ) -> emr_20160408_models.ListFlowProjectUserResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_flow_project_user_with_options_async(request, runtime)

    def list_resource_pool_with_options(
        self,
        request: emr_20160408_models.ListResourcePoolRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListResourcePoolResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.pool_type):
            query['PoolType'] = request.pool_type
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListResourcePool',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListResourcePoolResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_resource_pool_with_options_async(
        self,
        request: emr_20160408_models.ListResourcePoolRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListResourcePoolResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.pool_type):
            query['PoolType'] = request.pool_type
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListResourcePool',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListResourcePoolResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_resource_pool(
        self,
        request: emr_20160408_models.ListResourcePoolRequest,
    ) -> emr_20160408_models.ListResourcePoolResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_resource_pool_with_options(request, runtime)

    async def list_resource_pool_async(
        self,
        request: emr_20160408_models.ListResourcePoolRequest,
    ) -> emr_20160408_models.ListResourcePoolResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_resource_pool_with_options_async(request, runtime)

    def list_scaling_activity_v2with_options(
        self,
        request: emr_20160408_models.ListScalingActivityV2Request,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListScalingActivityV2Response:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_biz_id):
            query['ClusterBizId'] = request.cluster_biz_id
        if not UtilClient.is_unset(request.current_size):
            query['CurrentSize'] = request.current_size
        if not UtilClient.is_unset(request.host_group_id):
            query['HostGroupId'] = request.host_group_id
        if not UtilClient.is_unset(request.host_group_name):
            query['HostGroupName'] = request.host_group_name
        if not UtilClient.is_unset(request.limit):
            query['Limit'] = request.limit
        if not UtilClient.is_unset(request.order_field):
            query['OrderField'] = request.order_field
        if not UtilClient.is_unset(request.order_mode):
            query['OrderMode'] = request.order_mode
        if not UtilClient.is_unset(request.page_count):
            query['PageCount'] = request.page_count
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.scaling_group_biz_id):
            query['ScalingGroupBizId'] = request.scaling_group_biz_id
        if not UtilClient.is_unset(request.scaling_rule_name):
            query['ScalingRuleName'] = request.scaling_rule_name
        if not UtilClient.is_unset(request.status):
            query['Status'] = request.status
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListScalingActivityV2',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListScalingActivityV2Response(),
            self.call_api(params, req, runtime)
        )

    async def list_scaling_activity_v2with_options_async(
        self,
        request: emr_20160408_models.ListScalingActivityV2Request,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListScalingActivityV2Response:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_biz_id):
            query['ClusterBizId'] = request.cluster_biz_id
        if not UtilClient.is_unset(request.current_size):
            query['CurrentSize'] = request.current_size
        if not UtilClient.is_unset(request.host_group_id):
            query['HostGroupId'] = request.host_group_id
        if not UtilClient.is_unset(request.host_group_name):
            query['HostGroupName'] = request.host_group_name
        if not UtilClient.is_unset(request.limit):
            query['Limit'] = request.limit
        if not UtilClient.is_unset(request.order_field):
            query['OrderField'] = request.order_field
        if not UtilClient.is_unset(request.order_mode):
            query['OrderMode'] = request.order_mode
        if not UtilClient.is_unset(request.page_count):
            query['PageCount'] = request.page_count
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.scaling_group_biz_id):
            query['ScalingGroupBizId'] = request.scaling_group_biz_id
        if not UtilClient.is_unset(request.scaling_rule_name):
            query['ScalingRuleName'] = request.scaling_rule_name
        if not UtilClient.is_unset(request.status):
            query['Status'] = request.status
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListScalingActivityV2',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListScalingActivityV2Response(),
            await self.call_api_async(params, req, runtime)
        )

    def list_scaling_activity_v2(
        self,
        request: emr_20160408_models.ListScalingActivityV2Request,
    ) -> emr_20160408_models.ListScalingActivityV2Response:
        runtime = util_models.RuntimeOptions()
        return self.list_scaling_activity_v2with_options(request, runtime)

    async def list_scaling_activity_v2_async(
        self,
        request: emr_20160408_models.ListScalingActivityV2Request,
    ) -> emr_20160408_models.ListScalingActivityV2Response:
        runtime = util_models.RuntimeOptions()
        return await self.list_scaling_activity_v2with_options_async(request, runtime)

    def list_scaling_config_item_v2with_options(
        self,
        request: emr_20160408_models.ListScalingConfigItemV2Request,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListScalingConfigItemV2Response:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.config_item_type):
            query['ConfigItemType'] = request.config_item_type
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.scaling_group_biz_id):
            query['ScalingGroupBizId'] = request.scaling_group_biz_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListScalingConfigItemV2',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListScalingConfigItemV2Response(),
            self.call_api(params, req, runtime)
        )

    async def list_scaling_config_item_v2with_options_async(
        self,
        request: emr_20160408_models.ListScalingConfigItemV2Request,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListScalingConfigItemV2Response:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.config_item_type):
            query['ConfigItemType'] = request.config_item_type
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.scaling_group_biz_id):
            query['ScalingGroupBizId'] = request.scaling_group_biz_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListScalingConfigItemV2',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListScalingConfigItemV2Response(),
            await self.call_api_async(params, req, runtime)
        )

    def list_scaling_config_item_v2(
        self,
        request: emr_20160408_models.ListScalingConfigItemV2Request,
    ) -> emr_20160408_models.ListScalingConfigItemV2Response:
        runtime = util_models.RuntimeOptions()
        return self.list_scaling_config_item_v2with_options(request, runtime)

    async def list_scaling_config_item_v2_async(
        self,
        request: emr_20160408_models.ListScalingConfigItemV2Request,
    ) -> emr_20160408_models.ListScalingConfigItemV2Response:
        runtime = util_models.RuntimeOptions()
        return await self.list_scaling_config_item_v2with_options_async(request, runtime)

    def list_scaling_group_v2with_options(
        self,
        request: emr_20160408_models.ListScalingGroupV2Request,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListScalingGroupV2Response:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_biz_id):
            query['ClusterBizId'] = request.cluster_biz_id
        if not UtilClient.is_unset(request.current_size):
            query['CurrentSize'] = request.current_size
        if not UtilClient.is_unset(request.limit):
            query['Limit'] = request.limit
        if not UtilClient.is_unset(request.order_field):
            query['OrderField'] = request.order_field
        if not UtilClient.is_unset(request.order_mode):
            query['OrderMode'] = request.order_mode
        if not UtilClient.is_unset(request.page_count):
            query['PageCount'] = request.page_count
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListScalingGroupV2',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListScalingGroupV2Response(),
            self.call_api(params, req, runtime)
        )

    async def list_scaling_group_v2with_options_async(
        self,
        request: emr_20160408_models.ListScalingGroupV2Request,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListScalingGroupV2Response:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_biz_id):
            query['ClusterBizId'] = request.cluster_biz_id
        if not UtilClient.is_unset(request.current_size):
            query['CurrentSize'] = request.current_size
        if not UtilClient.is_unset(request.limit):
            query['Limit'] = request.limit
        if not UtilClient.is_unset(request.order_field):
            query['OrderField'] = request.order_field
        if not UtilClient.is_unset(request.order_mode):
            query['OrderMode'] = request.order_mode
        if not UtilClient.is_unset(request.page_count):
            query['PageCount'] = request.page_count
        if not UtilClient.is_unset(request.page_number):
            query['PageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListScalingGroupV2',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListScalingGroupV2Response(),
            await self.call_api_async(params, req, runtime)
        )

    def list_scaling_group_v2(
        self,
        request: emr_20160408_models.ListScalingGroupV2Request,
    ) -> emr_20160408_models.ListScalingGroupV2Response:
        runtime = util_models.RuntimeOptions()
        return self.list_scaling_group_v2with_options(request, runtime)

    async def list_scaling_group_v2_async(
        self,
        request: emr_20160408_models.ListScalingGroupV2Request,
    ) -> emr_20160408_models.ListScalingGroupV2Response:
        runtime = util_models.RuntimeOptions()
        return await self.list_scaling_group_v2with_options_async(request, runtime)

    def list_tag_resources_with_options(
        self,
        request: emr_20160408_models.ListTagResourcesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListTagResourcesResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.next_token):
            query['NextToken'] = request.next_token
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_id):
            query['ResourceId'] = request.resource_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.resource_type):
            query['ResourceType'] = request.resource_type
        if not UtilClient.is_unset(request.tag):
            query['Tag'] = request.tag
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListTagResources',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListTagResourcesResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_tag_resources_with_options_async(
        self,
        request: emr_20160408_models.ListTagResourcesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ListTagResourcesResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.next_token):
            query['NextToken'] = request.next_token
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_id):
            query['ResourceId'] = request.resource_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.resource_type):
            query['ResourceType'] = request.resource_type
        if not UtilClient.is_unset(request.tag):
            query['Tag'] = request.tag
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ListTagResources',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ListTagResourcesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_tag_resources(
        self,
        request: emr_20160408_models.ListTagResourcesRequest,
    ) -> emr_20160408_models.ListTagResourcesResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_tag_resources_with_options(request, runtime)

    async def list_tag_resources_async(
        self,
        request: emr_20160408_models.ListTagResourcesRequest,
    ) -> emr_20160408_models.ListTagResourcesResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_tag_resources_with_options_async(request, runtime)

    def modify_cluster_name_with_options(
        self,
        request: emr_20160408_models.ModifyClusterNameRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ModifyClusterNameResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ModifyClusterName',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ModifyClusterNameResponse(),
            self.call_api(params, req, runtime)
        )

    async def modify_cluster_name_with_options_async(
        self,
        request: emr_20160408_models.ModifyClusterNameRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ModifyClusterNameResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ModifyClusterName',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ModifyClusterNameResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def modify_cluster_name(
        self,
        request: emr_20160408_models.ModifyClusterNameRequest,
    ) -> emr_20160408_models.ModifyClusterNameResponse:
        runtime = util_models.RuntimeOptions()
        return self.modify_cluster_name_with_options(request, runtime)

    async def modify_cluster_name_async(
        self,
        request: emr_20160408_models.ModifyClusterNameRequest,
    ) -> emr_20160408_models.ModifyClusterNameResponse:
        runtime = util_models.RuntimeOptions()
        return await self.modify_cluster_name_with_options_async(request, runtime)

    def modify_cluster_service_config_with_options(
        self,
        request: emr_20160408_models.ModifyClusterServiceConfigRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ModifyClusterServiceConfigResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.comment):
            query['Comment'] = request.comment
        if not UtilClient.is_unset(request.config_params):
            query['ConfigParams'] = request.config_params
        if not UtilClient.is_unset(request.config_type):
            query['ConfigType'] = request.config_type
        if not UtilClient.is_unset(request.custom_config_params):
            query['CustomConfigParams'] = request.custom_config_params
        if not UtilClient.is_unset(request.gateway_cluster_id_list):
            query['GatewayClusterIdList'] = request.gateway_cluster_id_list
        if not UtilClient.is_unset(request.group_id):
            query['GroupId'] = request.group_id
        if not UtilClient.is_unset(request.host_instance_id):
            query['HostInstanceId'] = request.host_instance_id
        if not UtilClient.is_unset(request.refresh_host_config):
            query['RefreshHostConfig'] = request.refresh_host_config
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.service_name):
            query['ServiceName'] = request.service_name
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ModifyClusterServiceConfig',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ModifyClusterServiceConfigResponse(),
            self.call_api(params, req, runtime)
        )

    async def modify_cluster_service_config_with_options_async(
        self,
        request: emr_20160408_models.ModifyClusterServiceConfigRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ModifyClusterServiceConfigResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.comment):
            query['Comment'] = request.comment
        if not UtilClient.is_unset(request.config_params):
            query['ConfigParams'] = request.config_params
        if not UtilClient.is_unset(request.config_type):
            query['ConfigType'] = request.config_type
        if not UtilClient.is_unset(request.custom_config_params):
            query['CustomConfigParams'] = request.custom_config_params
        if not UtilClient.is_unset(request.gateway_cluster_id_list):
            query['GatewayClusterIdList'] = request.gateway_cluster_id_list
        if not UtilClient.is_unset(request.group_id):
            query['GroupId'] = request.group_id
        if not UtilClient.is_unset(request.host_instance_id):
            query['HostInstanceId'] = request.host_instance_id
        if not UtilClient.is_unset(request.refresh_host_config):
            query['RefreshHostConfig'] = request.refresh_host_config
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.service_name):
            query['ServiceName'] = request.service_name
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ModifyClusterServiceConfig',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ModifyClusterServiceConfigResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def modify_cluster_service_config(
        self,
        request: emr_20160408_models.ModifyClusterServiceConfigRequest,
    ) -> emr_20160408_models.ModifyClusterServiceConfigResponse:
        runtime = util_models.RuntimeOptions()
        return self.modify_cluster_service_config_with_options(request, runtime)

    async def modify_cluster_service_config_async(
        self,
        request: emr_20160408_models.ModifyClusterServiceConfigRequest,
    ) -> emr_20160408_models.ModifyClusterServiceConfigResponse:
        runtime = util_models.RuntimeOptions()
        return await self.modify_cluster_service_config_with_options_async(request, runtime)

    def modify_cluster_template_with_options(
        self,
        request: emr_20160408_models.ModifyClusterTemplateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ModifyClusterTemplateResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auto_renew):
            query['AutoRenew'] = request.auto_renew
        if not UtilClient.is_unset(request.biz_id):
            query['BizId'] = request.biz_id
        if not UtilClient.is_unset(request.bootstrap_action):
            query['BootstrapAction'] = request.bootstrap_action
        if not UtilClient.is_unset(request.charge_type):
            query['ChargeType'] = request.charge_type
        if not UtilClient.is_unset(request.cluster_type):
            query['ClusterType'] = request.cluster_type
        if not UtilClient.is_unset(request.config):
            query['Config'] = request.config
        if not UtilClient.is_unset(request.configurations):
            query['Configurations'] = request.configurations
        if not UtilClient.is_unset(request.data_disk_encrypted):
            query['DataDiskEncrypted'] = request.data_disk_encrypted
        if not UtilClient.is_unset(request.data_disk_kmskey_id):
            query['DataDiskKMSKeyId'] = request.data_disk_kmskey_id
        if not UtilClient.is_unset(request.deposit_type):
            query['DepositType'] = request.deposit_type
        if not UtilClient.is_unset(request.eas_enable):
            query['EasEnable'] = request.eas_enable
        if not UtilClient.is_unset(request.emr_ver):
            query['EmrVer'] = request.emr_ver
        if not UtilClient.is_unset(request.high_availability_enable):
            query['HighAvailabilityEnable'] = request.high_availability_enable
        if not UtilClient.is_unset(request.host_group):
            query['HostGroup'] = request.host_group
        if not UtilClient.is_unset(request.init_custom_hive_meta_db):
            query['InitCustomHiveMetaDb'] = request.init_custom_hive_meta_db
        if not UtilClient.is_unset(request.instance_generation):
            query['InstanceGeneration'] = request.instance_generation
        if not UtilClient.is_unset(request.io_optimized):
            query['IoOptimized'] = request.io_optimized
        if not UtilClient.is_unset(request.is_open_public_ip):
            query['IsOpenPublicIp'] = request.is_open_public_ip
        if not UtilClient.is_unset(request.key_pair_name):
            query['KeyPairName'] = request.key_pair_name
        if not UtilClient.is_unset(request.log_path):
            query['LogPath'] = request.log_path
        if not UtilClient.is_unset(request.machine_type):
            query['MachineType'] = request.machine_type
        if not UtilClient.is_unset(request.master_pwd):
            query['MasterPwd'] = request.master_pwd
        if not UtilClient.is_unset(request.meta_store_conf):
            query['MetaStoreConf'] = request.meta_store_conf
        if not UtilClient.is_unset(request.meta_store_type):
            query['MetaStoreType'] = request.meta_store_type
        if not UtilClient.is_unset(request.net_type):
            query['NetType'] = request.net_type
        if not UtilClient.is_unset(request.option_soft_ware_list):
            query['OptionSoftWareList'] = request.option_soft_ware_list
        if not UtilClient.is_unset(request.period):
            query['Period'] = request.period
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_group_id):
            query['SecurityGroupId'] = request.security_group_id
        if not UtilClient.is_unset(request.security_group_name):
            query['SecurityGroupName'] = request.security_group_name
        if not UtilClient.is_unset(request.ssh_enable):
            query['SshEnable'] = request.ssh_enable
        if not UtilClient.is_unset(request.tag):
            query['Tag'] = request.tag
        if not UtilClient.is_unset(request.template_name):
            query['TemplateName'] = request.template_name
        if not UtilClient.is_unset(request.use_custom_hive_meta_db):
            query['UseCustomHiveMetaDb'] = request.use_custom_hive_meta_db
        if not UtilClient.is_unset(request.use_local_meta_db):
            query['UseLocalMetaDb'] = request.use_local_meta_db
        if not UtilClient.is_unset(request.user_defined_emr_ecs_role):
            query['UserDefinedEmrEcsRole'] = request.user_defined_emr_ecs_role
        if not UtilClient.is_unset(request.v_switch_id):
            query['VSwitchId'] = request.v_switch_id
        if not UtilClient.is_unset(request.vpc_id):
            query['VpcId'] = request.vpc_id
        if not UtilClient.is_unset(request.zone_id):
            query['ZoneId'] = request.zone_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ModifyClusterTemplate',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ModifyClusterTemplateResponse(),
            self.call_api(params, req, runtime)
        )

    async def modify_cluster_template_with_options_async(
        self,
        request: emr_20160408_models.ModifyClusterTemplateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ModifyClusterTemplateResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auto_renew):
            query['AutoRenew'] = request.auto_renew
        if not UtilClient.is_unset(request.biz_id):
            query['BizId'] = request.biz_id
        if not UtilClient.is_unset(request.bootstrap_action):
            query['BootstrapAction'] = request.bootstrap_action
        if not UtilClient.is_unset(request.charge_type):
            query['ChargeType'] = request.charge_type
        if not UtilClient.is_unset(request.cluster_type):
            query['ClusterType'] = request.cluster_type
        if not UtilClient.is_unset(request.config):
            query['Config'] = request.config
        if not UtilClient.is_unset(request.configurations):
            query['Configurations'] = request.configurations
        if not UtilClient.is_unset(request.data_disk_encrypted):
            query['DataDiskEncrypted'] = request.data_disk_encrypted
        if not UtilClient.is_unset(request.data_disk_kmskey_id):
            query['DataDiskKMSKeyId'] = request.data_disk_kmskey_id
        if not UtilClient.is_unset(request.deposit_type):
            query['DepositType'] = request.deposit_type
        if not UtilClient.is_unset(request.eas_enable):
            query['EasEnable'] = request.eas_enable
        if not UtilClient.is_unset(request.emr_ver):
            query['EmrVer'] = request.emr_ver
        if not UtilClient.is_unset(request.high_availability_enable):
            query['HighAvailabilityEnable'] = request.high_availability_enable
        if not UtilClient.is_unset(request.host_group):
            query['HostGroup'] = request.host_group
        if not UtilClient.is_unset(request.init_custom_hive_meta_db):
            query['InitCustomHiveMetaDb'] = request.init_custom_hive_meta_db
        if not UtilClient.is_unset(request.instance_generation):
            query['InstanceGeneration'] = request.instance_generation
        if not UtilClient.is_unset(request.io_optimized):
            query['IoOptimized'] = request.io_optimized
        if not UtilClient.is_unset(request.is_open_public_ip):
            query['IsOpenPublicIp'] = request.is_open_public_ip
        if not UtilClient.is_unset(request.key_pair_name):
            query['KeyPairName'] = request.key_pair_name
        if not UtilClient.is_unset(request.log_path):
            query['LogPath'] = request.log_path
        if not UtilClient.is_unset(request.machine_type):
            query['MachineType'] = request.machine_type
        if not UtilClient.is_unset(request.master_pwd):
            query['MasterPwd'] = request.master_pwd
        if not UtilClient.is_unset(request.meta_store_conf):
            query['MetaStoreConf'] = request.meta_store_conf
        if not UtilClient.is_unset(request.meta_store_type):
            query['MetaStoreType'] = request.meta_store_type
        if not UtilClient.is_unset(request.net_type):
            query['NetType'] = request.net_type
        if not UtilClient.is_unset(request.option_soft_ware_list):
            query['OptionSoftWareList'] = request.option_soft_ware_list
        if not UtilClient.is_unset(request.period):
            query['Period'] = request.period
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.security_group_id):
            query['SecurityGroupId'] = request.security_group_id
        if not UtilClient.is_unset(request.security_group_name):
            query['SecurityGroupName'] = request.security_group_name
        if not UtilClient.is_unset(request.ssh_enable):
            query['SshEnable'] = request.ssh_enable
        if not UtilClient.is_unset(request.tag):
            query['Tag'] = request.tag
        if not UtilClient.is_unset(request.template_name):
            query['TemplateName'] = request.template_name
        if not UtilClient.is_unset(request.use_custom_hive_meta_db):
            query['UseCustomHiveMetaDb'] = request.use_custom_hive_meta_db
        if not UtilClient.is_unset(request.use_local_meta_db):
            query['UseLocalMetaDb'] = request.use_local_meta_db
        if not UtilClient.is_unset(request.user_defined_emr_ecs_role):
            query['UserDefinedEmrEcsRole'] = request.user_defined_emr_ecs_role
        if not UtilClient.is_unset(request.v_switch_id):
            query['VSwitchId'] = request.v_switch_id
        if not UtilClient.is_unset(request.vpc_id):
            query['VpcId'] = request.vpc_id
        if not UtilClient.is_unset(request.zone_id):
            query['ZoneId'] = request.zone_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ModifyClusterTemplate',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ModifyClusterTemplateResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def modify_cluster_template(
        self,
        request: emr_20160408_models.ModifyClusterTemplateRequest,
    ) -> emr_20160408_models.ModifyClusterTemplateResponse:
        runtime = util_models.RuntimeOptions()
        return self.modify_cluster_template_with_options(request, runtime)

    async def modify_cluster_template_async(
        self,
        request: emr_20160408_models.ModifyClusterTemplateRequest,
    ) -> emr_20160408_models.ModifyClusterTemplateResponse:
        runtime = util_models.RuntimeOptions()
        return await self.modify_cluster_template_with_options_async(request, runtime)

    def modify_flow_category_with_options(
        self,
        request: emr_20160408_models.ModifyFlowCategoryRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ModifyFlowCategoryResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.parent_id):
            query['ParentId'] = request.parent_id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ModifyFlowCategory',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ModifyFlowCategoryResponse(),
            self.call_api(params, req, runtime)
        )

    async def modify_flow_category_with_options_async(
        self,
        request: emr_20160408_models.ModifyFlowCategoryRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ModifyFlowCategoryResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.parent_id):
            query['ParentId'] = request.parent_id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ModifyFlowCategory',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ModifyFlowCategoryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def modify_flow_category(
        self,
        request: emr_20160408_models.ModifyFlowCategoryRequest,
    ) -> emr_20160408_models.ModifyFlowCategoryResponse:
        runtime = util_models.RuntimeOptions()
        return self.modify_flow_category_with_options(request, runtime)

    async def modify_flow_category_async(
        self,
        request: emr_20160408_models.ModifyFlowCategoryRequest,
    ) -> emr_20160408_models.ModifyFlowCategoryResponse:
        runtime = util_models.RuntimeOptions()
        return await self.modify_flow_category_with_options_async(request, runtime)

    def modify_flow_for_web_with_options(
        self,
        request: emr_20160408_models.ModifyFlowForWebRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ModifyFlowForWebResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.alert_conf):
            query['AlertConf'] = request.alert_conf
        if not UtilClient.is_unset(request.alert_ding_ding_group_biz_id):
            query['AlertDingDingGroupBizId'] = request.alert_ding_ding_group_biz_id
        if not UtilClient.is_unset(request.alert_user_group_biz_id):
            query['AlertUserGroupBizId'] = request.alert_user_group_biz_id
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.create_cluster):
            query['CreateCluster'] = request.create_cluster
        if not UtilClient.is_unset(request.cron_expr):
            query['CronExpr'] = request.cron_expr
        if not UtilClient.is_unset(request.description):
            query['Description'] = request.description
        if not UtilClient.is_unset(request.end_schedule):
            query['EndSchedule'] = request.end_schedule
        if not UtilClient.is_unset(request.graph):
            query['Graph'] = request.graph
        if not UtilClient.is_unset(request.host_name):
            query['HostName'] = request.host_name
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.lifecycle):
            query['Lifecycle'] = request.lifecycle
        if not UtilClient.is_unset(request.log_archive_location):
            query['LogArchiveLocation'] = request.log_archive_location
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.namespace):
            query['Namespace'] = request.namespace
        if not UtilClient.is_unset(request.parent_category):
            query['ParentCategory'] = request.parent_category
        if not UtilClient.is_unset(request.parent_flow_list):
            query['ParentFlowList'] = request.parent_flow_list
        if not UtilClient.is_unset(request.periodic):
            query['Periodic'] = request.periodic
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.start_schedule):
            query['StartSchedule'] = request.start_schedule
        if not UtilClient.is_unset(request.status):
            query['Status'] = request.status
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ModifyFlowForWeb',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ModifyFlowForWebResponse(),
            self.call_api(params, req, runtime)
        )

    async def modify_flow_for_web_with_options_async(
        self,
        request: emr_20160408_models.ModifyFlowForWebRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ModifyFlowForWebResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.alert_conf):
            query['AlertConf'] = request.alert_conf
        if not UtilClient.is_unset(request.alert_ding_ding_group_biz_id):
            query['AlertDingDingGroupBizId'] = request.alert_ding_ding_group_biz_id
        if not UtilClient.is_unset(request.alert_user_group_biz_id):
            query['AlertUserGroupBizId'] = request.alert_user_group_biz_id
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.create_cluster):
            query['CreateCluster'] = request.create_cluster
        if not UtilClient.is_unset(request.cron_expr):
            query['CronExpr'] = request.cron_expr
        if not UtilClient.is_unset(request.description):
            query['Description'] = request.description
        if not UtilClient.is_unset(request.end_schedule):
            query['EndSchedule'] = request.end_schedule
        if not UtilClient.is_unset(request.graph):
            query['Graph'] = request.graph
        if not UtilClient.is_unset(request.host_name):
            query['HostName'] = request.host_name
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.lifecycle):
            query['Lifecycle'] = request.lifecycle
        if not UtilClient.is_unset(request.log_archive_location):
            query['LogArchiveLocation'] = request.log_archive_location
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.namespace):
            query['Namespace'] = request.namespace
        if not UtilClient.is_unset(request.parent_category):
            query['ParentCategory'] = request.parent_category
        if not UtilClient.is_unset(request.parent_flow_list):
            query['ParentFlowList'] = request.parent_flow_list
        if not UtilClient.is_unset(request.periodic):
            query['Periodic'] = request.periodic
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.start_schedule):
            query['StartSchedule'] = request.start_schedule
        if not UtilClient.is_unset(request.status):
            query['Status'] = request.status
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ModifyFlowForWeb',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ModifyFlowForWebResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def modify_flow_for_web(
        self,
        request: emr_20160408_models.ModifyFlowForWebRequest,
    ) -> emr_20160408_models.ModifyFlowForWebResponse:
        runtime = util_models.RuntimeOptions()
        return self.modify_flow_for_web_with_options(request, runtime)

    async def modify_flow_for_web_async(
        self,
        request: emr_20160408_models.ModifyFlowForWebRequest,
    ) -> emr_20160408_models.ModifyFlowForWebResponse:
        runtime = util_models.RuntimeOptions()
        return await self.modify_flow_for_web_with_options_async(request, runtime)

    def modify_flow_project_with_options(
        self,
        request: emr_20160408_models.ModifyFlowProjectRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ModifyFlowProjectResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.description):
            query['Description'] = request.description
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ModifyFlowProject',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ModifyFlowProjectResponse(),
            self.call_api(params, req, runtime)
        )

    async def modify_flow_project_with_options_async(
        self,
        request: emr_20160408_models.ModifyFlowProjectRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ModifyFlowProjectResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.description):
            query['Description'] = request.description
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ModifyFlowProject',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ModifyFlowProjectResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def modify_flow_project(
        self,
        request: emr_20160408_models.ModifyFlowProjectRequest,
    ) -> emr_20160408_models.ModifyFlowProjectResponse:
        runtime = util_models.RuntimeOptions()
        return self.modify_flow_project_with_options(request, runtime)

    async def modify_flow_project_async(
        self,
        request: emr_20160408_models.ModifyFlowProjectRequest,
    ) -> emr_20160408_models.ModifyFlowProjectResponse:
        runtime = util_models.RuntimeOptions()
        return await self.modify_flow_project_with_options_async(request, runtime)

    def modify_flow_project_cluster_setting_with_options(
        self,
        request: emr_20160408_models.ModifyFlowProjectClusterSettingRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ModifyFlowProjectClusterSettingResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.default_queue):
            query['DefaultQueue'] = request.default_queue
        if not UtilClient.is_unset(request.default_user):
            query['DefaultUser'] = request.default_user
        if not UtilClient.is_unset(request.host_list):
            query['HostList'] = request.host_list
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.queue_list):
            query['QueueList'] = request.queue_list
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.user_list):
            query['UserList'] = request.user_list
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ModifyFlowProjectClusterSetting',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ModifyFlowProjectClusterSettingResponse(),
            self.call_api(params, req, runtime)
        )

    async def modify_flow_project_cluster_setting_with_options_async(
        self,
        request: emr_20160408_models.ModifyFlowProjectClusterSettingRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ModifyFlowProjectClusterSettingResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.default_queue):
            query['DefaultQueue'] = request.default_queue
        if not UtilClient.is_unset(request.default_user):
            query['DefaultUser'] = request.default_user
        if not UtilClient.is_unset(request.host_list):
            query['HostList'] = request.host_list
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.queue_list):
            query['QueueList'] = request.queue_list
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.user_list):
            query['UserList'] = request.user_list
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ModifyFlowProjectClusterSetting',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ModifyFlowProjectClusterSettingResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def modify_flow_project_cluster_setting(
        self,
        request: emr_20160408_models.ModifyFlowProjectClusterSettingRequest,
    ) -> emr_20160408_models.ModifyFlowProjectClusterSettingResponse:
        runtime = util_models.RuntimeOptions()
        return self.modify_flow_project_cluster_setting_with_options(request, runtime)

    async def modify_flow_project_cluster_setting_async(
        self,
        request: emr_20160408_models.ModifyFlowProjectClusterSettingRequest,
    ) -> emr_20160408_models.ModifyFlowProjectClusterSettingResponse:
        runtime = util_models.RuntimeOptions()
        return await self.modify_flow_project_cluster_setting_with_options_async(request, runtime)

    def modify_resource_pool_with_options(
        self,
        request: emr_20160408_models.ModifyResourcePoolRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ModifyResourcePoolResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.active):
            query['Active'] = request.active
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.config):
            query['Config'] = request.config
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.yarnsiteconfig):
            query['Yarnsiteconfig'] = request.yarnsiteconfig
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ModifyResourcePool',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ModifyResourcePoolResponse(),
            self.call_api(params, req, runtime)
        )

    async def modify_resource_pool_with_options_async(
        self,
        request: emr_20160408_models.ModifyResourcePoolRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ModifyResourcePoolResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.active):
            query['Active'] = request.active
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.config):
            query['Config'] = request.config
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.yarnsiteconfig):
            query['Yarnsiteconfig'] = request.yarnsiteconfig
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ModifyResourcePool',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ModifyResourcePoolResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def modify_resource_pool(
        self,
        request: emr_20160408_models.ModifyResourcePoolRequest,
    ) -> emr_20160408_models.ModifyResourcePoolResponse:
        runtime = util_models.RuntimeOptions()
        return self.modify_resource_pool_with_options(request, runtime)

    async def modify_resource_pool_async(
        self,
        request: emr_20160408_models.ModifyResourcePoolRequest,
    ) -> emr_20160408_models.ModifyResourcePoolResponse:
        runtime = util_models.RuntimeOptions()
        return await self.modify_resource_pool_with_options_async(request, runtime)

    def modify_resource_pool_scheduler_type_with_options(
        self,
        request: emr_20160408_models.ModifyResourcePoolSchedulerTypeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ModifyResourcePoolSchedulerTypeResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.scheduler_type):
            query['SchedulerType'] = request.scheduler_type
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ModifyResourcePoolSchedulerType',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ModifyResourcePoolSchedulerTypeResponse(),
            self.call_api(params, req, runtime)
        )

    async def modify_resource_pool_scheduler_type_with_options_async(
        self,
        request: emr_20160408_models.ModifyResourcePoolSchedulerTypeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ModifyResourcePoolSchedulerTypeResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.scheduler_type):
            query['SchedulerType'] = request.scheduler_type
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ModifyResourcePoolSchedulerType',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ModifyResourcePoolSchedulerTypeResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def modify_resource_pool_scheduler_type(
        self,
        request: emr_20160408_models.ModifyResourcePoolSchedulerTypeRequest,
    ) -> emr_20160408_models.ModifyResourcePoolSchedulerTypeResponse:
        runtime = util_models.RuntimeOptions()
        return self.modify_resource_pool_scheduler_type_with_options(request, runtime)

    async def modify_resource_pool_scheduler_type_async(
        self,
        request: emr_20160408_models.ModifyResourcePoolSchedulerTypeRequest,
    ) -> emr_20160408_models.ModifyResourcePoolSchedulerTypeResponse:
        runtime = util_models.RuntimeOptions()
        return await self.modify_resource_pool_scheduler_type_with_options_async(request, runtime)

    def modify_resource_queue_with_options(
        self,
        request: emr_20160408_models.ModifyResourceQueueRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ModifyResourceQueueResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.config):
            query['Config'] = request.config
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.leaf):
            query['Leaf'] = request.leaf
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.parent_queue_id):
            query['ParentQueueId'] = request.parent_queue_id
        if not UtilClient.is_unset(request.qualified_name):
            query['QualifiedName'] = request.qualified_name
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.resource_pool_id):
            query['ResourcePoolId'] = request.resource_pool_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ModifyResourceQueue',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ModifyResourceQueueResponse(),
            self.call_api(params, req, runtime)
        )

    async def modify_resource_queue_with_options_async(
        self,
        request: emr_20160408_models.ModifyResourceQueueRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ModifyResourceQueueResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.config):
            query['Config'] = request.config
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.leaf):
            query['Leaf'] = request.leaf
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.parent_queue_id):
            query['ParentQueueId'] = request.parent_queue_id
        if not UtilClient.is_unset(request.qualified_name):
            query['QualifiedName'] = request.qualified_name
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.resource_pool_id):
            query['ResourcePoolId'] = request.resource_pool_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ModifyResourceQueue',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ModifyResourceQueueResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def modify_resource_queue(
        self,
        request: emr_20160408_models.ModifyResourceQueueRequest,
    ) -> emr_20160408_models.ModifyResourceQueueResponse:
        runtime = util_models.RuntimeOptions()
        return self.modify_resource_queue_with_options(request, runtime)

    async def modify_resource_queue_async(
        self,
        request: emr_20160408_models.ModifyResourceQueueRequest,
    ) -> emr_20160408_models.ModifyResourceQueueResponse:
        runtime = util_models.RuntimeOptions()
        return await self.modify_resource_queue_with_options_async(request, runtime)

    def modify_scaling_config_item_v2with_options(
        self,
        request: emr_20160408_models.ModifyScalingConfigItemV2Request,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ModifyScalingConfigItemV2Response:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.config_item_biz_id):
            query['ConfigItemBizId'] = request.config_item_biz_id
        if not UtilClient.is_unset(request.config_item_information):
            query['ConfigItemInformation'] = request.config_item_information
        if not UtilClient.is_unset(request.config_item_type):
            query['ConfigItemType'] = request.config_item_type
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.scaling_group_biz_id):
            query['ScalingGroupBizId'] = request.scaling_group_biz_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ModifyScalingConfigItemV2',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ModifyScalingConfigItemV2Response(),
            self.call_api(params, req, runtime)
        )

    async def modify_scaling_config_item_v2with_options_async(
        self,
        request: emr_20160408_models.ModifyScalingConfigItemV2Request,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ModifyScalingConfigItemV2Response:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.config_item_biz_id):
            query['ConfigItemBizId'] = request.config_item_biz_id
        if not UtilClient.is_unset(request.config_item_information):
            query['ConfigItemInformation'] = request.config_item_information
        if not UtilClient.is_unset(request.config_item_type):
            query['ConfigItemType'] = request.config_item_type
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.scaling_group_biz_id):
            query['ScalingGroupBizId'] = request.scaling_group_biz_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ModifyScalingConfigItemV2',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ModifyScalingConfigItemV2Response(),
            await self.call_api_async(params, req, runtime)
        )

    def modify_scaling_config_item_v2(
        self,
        request: emr_20160408_models.ModifyScalingConfigItemV2Request,
    ) -> emr_20160408_models.ModifyScalingConfigItemV2Response:
        runtime = util_models.RuntimeOptions()
        return self.modify_scaling_config_item_v2with_options(request, runtime)

    async def modify_scaling_config_item_v2_async(
        self,
        request: emr_20160408_models.ModifyScalingConfigItemV2Request,
    ) -> emr_20160408_models.ModifyScalingConfigItemV2Response:
        runtime = util_models.RuntimeOptions()
        return await self.modify_scaling_config_item_v2with_options_async(request, runtime)

    def modify_scaling_group_v2with_options(
        self,
        request: emr_20160408_models.ModifyScalingGroupV2Request,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ModifyScalingGroupV2Response:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.description):
            query['Description'] = request.description
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.scaling_group_biz_id):
            query['ScalingGroupBizId'] = request.scaling_group_biz_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ModifyScalingGroupV2',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ModifyScalingGroupV2Response(),
            self.call_api(params, req, runtime)
        )

    async def modify_scaling_group_v2with_options_async(
        self,
        request: emr_20160408_models.ModifyScalingGroupV2Request,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ModifyScalingGroupV2Response:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.description):
            query['Description'] = request.description
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.scaling_group_biz_id):
            query['ScalingGroupBizId'] = request.scaling_group_biz_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ModifyScalingGroupV2',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ModifyScalingGroupV2Response(),
            await self.call_api_async(params, req, runtime)
        )

    def modify_scaling_group_v2(
        self,
        request: emr_20160408_models.ModifyScalingGroupV2Request,
    ) -> emr_20160408_models.ModifyScalingGroupV2Response:
        runtime = util_models.RuntimeOptions()
        return self.modify_scaling_group_v2with_options(request, runtime)

    async def modify_scaling_group_v2_async(
        self,
        request: emr_20160408_models.ModifyScalingGroupV2Request,
    ) -> emr_20160408_models.ModifyScalingGroupV2Response:
        runtime = util_models.RuntimeOptions()
        return await self.modify_scaling_group_v2with_options_async(request, runtime)

    def refresh_cluster_resource_pool_with_options(
        self,
        request: emr_20160408_models.RefreshClusterResourcePoolRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.RefreshClusterResourcePoolResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.resource_pool_id):
            query['ResourcePoolId'] = request.resource_pool_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='RefreshClusterResourcePool',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.RefreshClusterResourcePoolResponse(),
            self.call_api(params, req, runtime)
        )

    async def refresh_cluster_resource_pool_with_options_async(
        self,
        request: emr_20160408_models.RefreshClusterResourcePoolRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.RefreshClusterResourcePoolResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.resource_pool_id):
            query['ResourcePoolId'] = request.resource_pool_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='RefreshClusterResourcePool',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.RefreshClusterResourcePoolResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def refresh_cluster_resource_pool(
        self,
        request: emr_20160408_models.RefreshClusterResourcePoolRequest,
    ) -> emr_20160408_models.RefreshClusterResourcePoolResponse:
        runtime = util_models.RuntimeOptions()
        return self.refresh_cluster_resource_pool_with_options(request, runtime)

    async def refresh_cluster_resource_pool_async(
        self,
        request: emr_20160408_models.RefreshClusterResourcePoolRequest,
    ) -> emr_20160408_models.RefreshClusterResourcePoolResponse:
        runtime = util_models.RuntimeOptions()
        return await self.refresh_cluster_resource_pool_with_options_async(request, runtime)

    def release_cluster_with_options(
        self,
        request: emr_20160408_models.ReleaseClusterRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ReleaseClusterResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.force_release):
            query['ForceRelease'] = request.force_release
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ReleaseCluster',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ReleaseClusterResponse(),
            self.call_api(params, req, runtime)
        )

    async def release_cluster_with_options_async(
        self,
        request: emr_20160408_models.ReleaseClusterRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ReleaseClusterResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.force_release):
            query['ForceRelease'] = request.force_release
        if not UtilClient.is_unset(request.id):
            query['Id'] = request.id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ReleaseCluster',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ReleaseClusterResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def release_cluster(
        self,
        request: emr_20160408_models.ReleaseClusterRequest,
    ) -> emr_20160408_models.ReleaseClusterResponse:
        runtime = util_models.RuntimeOptions()
        return self.release_cluster_with_options(request, runtime)

    async def release_cluster_async(
        self,
        request: emr_20160408_models.ReleaseClusterRequest,
    ) -> emr_20160408_models.ReleaseClusterResponse:
        runtime = util_models.RuntimeOptions()
        return await self.release_cluster_with_options_async(request, runtime)

    def release_cluster_host_group_with_options(
        self,
        request: emr_20160408_models.ReleaseClusterHostGroupRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ReleaseClusterHostGroupResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.decommission_timeout):
            query['DecommissionTimeout'] = request.decommission_timeout
        if not UtilClient.is_unset(request.enable_graceful_decommission):
            query['EnableGracefulDecommission'] = request.enable_graceful_decommission
        if not UtilClient.is_unset(request.host_group_id):
            query['HostGroupId'] = request.host_group_id
        if not UtilClient.is_unset(request.instance_id_list):
            query['InstanceIdList'] = request.instance_id_list
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.release_number):
            query['ReleaseNumber'] = request.release_number
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ReleaseClusterHostGroup',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ReleaseClusterHostGroupResponse(),
            self.call_api(params, req, runtime)
        )

    async def release_cluster_host_group_with_options_async(
        self,
        request: emr_20160408_models.ReleaseClusterHostGroupRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ReleaseClusterHostGroupResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.decommission_timeout):
            query['DecommissionTimeout'] = request.decommission_timeout
        if not UtilClient.is_unset(request.enable_graceful_decommission):
            query['EnableGracefulDecommission'] = request.enable_graceful_decommission
        if not UtilClient.is_unset(request.host_group_id):
            query['HostGroupId'] = request.host_group_id
        if not UtilClient.is_unset(request.instance_id_list):
            query['InstanceIdList'] = request.instance_id_list
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.release_number):
            query['ReleaseNumber'] = request.release_number
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ReleaseClusterHostGroup',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ReleaseClusterHostGroupResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def release_cluster_host_group(
        self,
        request: emr_20160408_models.ReleaseClusterHostGroupRequest,
    ) -> emr_20160408_models.ReleaseClusterHostGroupResponse:
        runtime = util_models.RuntimeOptions()
        return self.release_cluster_host_group_with_options(request, runtime)

    async def release_cluster_host_group_async(
        self,
        request: emr_20160408_models.ReleaseClusterHostGroupRequest,
    ) -> emr_20160408_models.ReleaseClusterHostGroupResponse:
        runtime = util_models.RuntimeOptions()
        return await self.release_cluster_host_group_with_options_async(request, runtime)

    def remove_scaling_config_item_v2with_options(
        self,
        request: emr_20160408_models.RemoveScalingConfigItemV2Request,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.RemoveScalingConfigItemV2Response:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.config_item_biz_id):
            query['ConfigItemBizId'] = request.config_item_biz_id
        if not UtilClient.is_unset(request.config_item_type):
            query['ConfigItemType'] = request.config_item_type
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.scaling_group_biz_id):
            query['ScalingGroupBizId'] = request.scaling_group_biz_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='RemoveScalingConfigItemV2',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.RemoveScalingConfigItemV2Response(),
            self.call_api(params, req, runtime)
        )

    async def remove_scaling_config_item_v2with_options_async(
        self,
        request: emr_20160408_models.RemoveScalingConfigItemV2Request,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.RemoveScalingConfigItemV2Response:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.config_item_biz_id):
            query['ConfigItemBizId'] = request.config_item_biz_id
        if not UtilClient.is_unset(request.config_item_type):
            query['ConfigItemType'] = request.config_item_type
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.scaling_group_biz_id):
            query['ScalingGroupBizId'] = request.scaling_group_biz_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='RemoveScalingConfigItemV2',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.RemoveScalingConfigItemV2Response(),
            await self.call_api_async(params, req, runtime)
        )

    def remove_scaling_config_item_v2(
        self,
        request: emr_20160408_models.RemoveScalingConfigItemV2Request,
    ) -> emr_20160408_models.RemoveScalingConfigItemV2Response:
        runtime = util_models.RuntimeOptions()
        return self.remove_scaling_config_item_v2with_options(request, runtime)

    async def remove_scaling_config_item_v2_async(
        self,
        request: emr_20160408_models.RemoveScalingConfigItemV2Request,
    ) -> emr_20160408_models.RemoveScalingConfigItemV2Response:
        runtime = util_models.RuntimeOptions()
        return await self.remove_scaling_config_item_v2with_options_async(request, runtime)

    def rerun_flow_with_options(
        self,
        request: emr_20160408_models.RerunFlowRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.RerunFlowResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.flow_instance_id):
            query['FlowInstanceId'] = request.flow_instance_id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.re_run_fail):
            query['ReRunFail'] = request.re_run_fail
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='RerunFlow',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.RerunFlowResponse(),
            self.call_api(params, req, runtime)
        )

    async def rerun_flow_with_options_async(
        self,
        request: emr_20160408_models.RerunFlowRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.RerunFlowResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.flow_instance_id):
            query['FlowInstanceId'] = request.flow_instance_id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.re_run_fail):
            query['ReRunFail'] = request.re_run_fail
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='RerunFlow',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.RerunFlowResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def rerun_flow(
        self,
        request: emr_20160408_models.RerunFlowRequest,
    ) -> emr_20160408_models.RerunFlowResponse:
        runtime = util_models.RuntimeOptions()
        return self.rerun_flow_with_options(request, runtime)

    async def rerun_flow_async(
        self,
        request: emr_20160408_models.RerunFlowRequest,
    ) -> emr_20160408_models.RerunFlowResponse:
        runtime = util_models.RuntimeOptions()
        return await self.rerun_flow_with_options_async(request, runtime)

    def resize_cluster_v2with_options(
        self,
        request: emr_20160408_models.ResizeClusterV2Request,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ResizeClusterV2Response:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auto_pay_order):
            query['AutoPayOrder'] = request.auto_pay_order
        if not UtilClient.is_unset(request.clickhouse_conf):
            query['ClickhouseConf'] = request.clickhouse_conf
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.host_component_info):
            query['HostComponentInfo'] = request.host_component_info
        if not UtilClient.is_unset(request.host_group):
            query['HostGroup'] = request.host_group
        if not UtilClient.is_unset(request.is_open_public_ip):
            query['IsOpenPublicIp'] = request.is_open_public_ip
        if not UtilClient.is_unset(request.promotion_info):
            query['PromotionInfo'] = request.promotion_info
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.vswitch_id):
            query['VswitchId'] = request.vswitch_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ResizeClusterV2',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ResizeClusterV2Response(),
            self.call_api(params, req, runtime)
        )

    async def resize_cluster_v2with_options_async(
        self,
        request: emr_20160408_models.ResizeClusterV2Request,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ResizeClusterV2Response:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auto_pay_order):
            query['AutoPayOrder'] = request.auto_pay_order
        if not UtilClient.is_unset(request.clickhouse_conf):
            query['ClickhouseConf'] = request.clickhouse_conf
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.host_component_info):
            query['HostComponentInfo'] = request.host_component_info
        if not UtilClient.is_unset(request.host_group):
            query['HostGroup'] = request.host_group
        if not UtilClient.is_unset(request.is_open_public_ip):
            query['IsOpenPublicIp'] = request.is_open_public_ip
        if not UtilClient.is_unset(request.promotion_info):
            query['PromotionInfo'] = request.promotion_info
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.vswitch_id):
            query['VswitchId'] = request.vswitch_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ResizeClusterV2',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ResizeClusterV2Response(),
            await self.call_api_async(params, req, runtime)
        )

    def resize_cluster_v2(
        self,
        request: emr_20160408_models.ResizeClusterV2Request,
    ) -> emr_20160408_models.ResizeClusterV2Response:
        runtime = util_models.RuntimeOptions()
        return self.resize_cluster_v2with_options(request, runtime)

    async def resize_cluster_v2_async(
        self,
        request: emr_20160408_models.ResizeClusterV2Request,
    ) -> emr_20160408_models.ResizeClusterV2Response:
        runtime = util_models.RuntimeOptions()
        return await self.resize_cluster_v2with_options_async(request, runtime)

    def resume_flow_with_options(
        self,
        request: emr_20160408_models.ResumeFlowRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ResumeFlowResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.flow_instance_id):
            query['FlowInstanceId'] = request.flow_instance_id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ResumeFlow',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ResumeFlowResponse(),
            self.call_api(params, req, runtime)
        )

    async def resume_flow_with_options_async(
        self,
        request: emr_20160408_models.ResumeFlowRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.ResumeFlowResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.flow_instance_id):
            query['FlowInstanceId'] = request.flow_instance_id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ResumeFlow',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.ResumeFlowResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def resume_flow(
        self,
        request: emr_20160408_models.ResumeFlowRequest,
    ) -> emr_20160408_models.ResumeFlowResponse:
        runtime = util_models.RuntimeOptions()
        return self.resume_flow_with_options(request, runtime)

    async def resume_flow_async(
        self,
        request: emr_20160408_models.ResumeFlowRequest,
    ) -> emr_20160408_models.ResumeFlowResponse:
        runtime = util_models.RuntimeOptions()
        return await self.resume_flow_with_options_async(request, runtime)

    def run_cluster_service_action_with_options(
        self,
        request: emr_20160408_models.RunClusterServiceActionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.RunClusterServiceActionResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.comment):
            query['Comment'] = request.comment
        if not UtilClient.is_unset(request.component_name_list):
            query['ComponentNameList'] = request.component_name_list
        if not UtilClient.is_unset(request.custom_command):
            query['CustomCommand'] = request.custom_command
        if not UtilClient.is_unset(request.custom_params):
            query['CustomParams'] = request.custom_params
        if not UtilClient.is_unset(request.execute_strategy):
            query['ExecuteStrategy'] = request.execute_strategy
        if not UtilClient.is_unset(request.host_group_id_list):
            query['HostGroupIdList'] = request.host_group_id_list
        if not UtilClient.is_unset(request.host_id_list):
            query['HostIdList'] = request.host_id_list
        if not UtilClient.is_unset(request.interval):
            query['Interval'] = request.interval
        if not UtilClient.is_unset(request.is_rolling):
            query['IsRolling'] = request.is_rolling
        if not UtilClient.is_unset(request.node_count_per_batch):
            query['NodeCountPerBatch'] = request.node_count_per_batch
        if not UtilClient.is_unset(request.only_restart_stale_config_nodes):
            query['OnlyRestartStaleConfigNodes'] = request.only_restart_stale_config_nodes
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.service_action_name):
            query['ServiceActionName'] = request.service_action_name
        if not UtilClient.is_unset(request.service_name):
            query['ServiceName'] = request.service_name
        if not UtilClient.is_unset(request.totlerate_fail_count):
            query['TotlerateFailCount'] = request.totlerate_fail_count
        if not UtilClient.is_unset(request.turn_on_maintenance_mode):
            query['TurnOnMaintenanceMode'] = request.turn_on_maintenance_mode
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='RunClusterServiceAction',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.RunClusterServiceActionResponse(),
            self.call_api(params, req, runtime)
        )

    async def run_cluster_service_action_with_options_async(
        self,
        request: emr_20160408_models.RunClusterServiceActionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.RunClusterServiceActionResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.comment):
            query['Comment'] = request.comment
        if not UtilClient.is_unset(request.component_name_list):
            query['ComponentNameList'] = request.component_name_list
        if not UtilClient.is_unset(request.custom_command):
            query['CustomCommand'] = request.custom_command
        if not UtilClient.is_unset(request.custom_params):
            query['CustomParams'] = request.custom_params
        if not UtilClient.is_unset(request.execute_strategy):
            query['ExecuteStrategy'] = request.execute_strategy
        if not UtilClient.is_unset(request.host_group_id_list):
            query['HostGroupIdList'] = request.host_group_id_list
        if not UtilClient.is_unset(request.host_id_list):
            query['HostIdList'] = request.host_id_list
        if not UtilClient.is_unset(request.interval):
            query['Interval'] = request.interval
        if not UtilClient.is_unset(request.is_rolling):
            query['IsRolling'] = request.is_rolling
        if not UtilClient.is_unset(request.node_count_per_batch):
            query['NodeCountPerBatch'] = request.node_count_per_batch
        if not UtilClient.is_unset(request.only_restart_stale_config_nodes):
            query['OnlyRestartStaleConfigNodes'] = request.only_restart_stale_config_nodes
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.service_action_name):
            query['ServiceActionName'] = request.service_action_name
        if not UtilClient.is_unset(request.service_name):
            query['ServiceName'] = request.service_name
        if not UtilClient.is_unset(request.totlerate_fail_count):
            query['TotlerateFailCount'] = request.totlerate_fail_count
        if not UtilClient.is_unset(request.turn_on_maintenance_mode):
            query['TurnOnMaintenanceMode'] = request.turn_on_maintenance_mode
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='RunClusterServiceAction',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.RunClusterServiceActionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def run_cluster_service_action(
        self,
        request: emr_20160408_models.RunClusterServiceActionRequest,
    ) -> emr_20160408_models.RunClusterServiceActionResponse:
        runtime = util_models.RuntimeOptions()
        return self.run_cluster_service_action_with_options(request, runtime)

    async def run_cluster_service_action_async(
        self,
        request: emr_20160408_models.RunClusterServiceActionRequest,
    ) -> emr_20160408_models.RunClusterServiceActionResponse:
        runtime = util_models.RuntimeOptions()
        return await self.run_cluster_service_action_with_options_async(request, runtime)

    def run_scaling_action_v2with_options(
        self,
        request: emr_20160408_models.RunScalingActionV2Request,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.RunScalingActionV2Response:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.action_param):
            query['ActionParam'] = request.action_param
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.scaling_action_type):
            query['ScalingActionType'] = request.scaling_action_type
        if not UtilClient.is_unset(request.scaling_group_biz_id):
            query['ScalingGroupBizId'] = request.scaling_group_biz_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='RunScalingActionV2',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.RunScalingActionV2Response(),
            self.call_api(params, req, runtime)
        )

    async def run_scaling_action_v2with_options_async(
        self,
        request: emr_20160408_models.RunScalingActionV2Request,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.RunScalingActionV2Response:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.action_param):
            query['ActionParam'] = request.action_param
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_group_id):
            query['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.scaling_action_type):
            query['ScalingActionType'] = request.scaling_action_type
        if not UtilClient.is_unset(request.scaling_group_biz_id):
            query['ScalingGroupBizId'] = request.scaling_group_biz_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='RunScalingActionV2',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.RunScalingActionV2Response(),
            await self.call_api_async(params, req, runtime)
        )

    def run_scaling_action_v2(
        self,
        request: emr_20160408_models.RunScalingActionV2Request,
    ) -> emr_20160408_models.RunScalingActionV2Response:
        runtime = util_models.RuntimeOptions()
        return self.run_scaling_action_v2with_options(request, runtime)

    async def run_scaling_action_v2_async(
        self,
        request: emr_20160408_models.RunScalingActionV2Request,
    ) -> emr_20160408_models.RunScalingActionV2Response:
        runtime = util_models.RuntimeOptions()
        return await self.run_scaling_action_v2with_options_async(request, runtime)

    def start_flow_with_options(
        self,
        request: emr_20160408_models.StartFlowRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.StartFlowResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.flow_instance_id):
            query['FlowInstanceId'] = request.flow_instance_id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='StartFlow',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.StartFlowResponse(),
            self.call_api(params, req, runtime)
        )

    async def start_flow_with_options_async(
        self,
        request: emr_20160408_models.StartFlowRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.StartFlowResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.flow_instance_id):
            query['FlowInstanceId'] = request.flow_instance_id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='StartFlow',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.StartFlowResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def start_flow(
        self,
        request: emr_20160408_models.StartFlowRequest,
    ) -> emr_20160408_models.StartFlowResponse:
        runtime = util_models.RuntimeOptions()
        return self.start_flow_with_options(request, runtime)

    async def start_flow_async(
        self,
        request: emr_20160408_models.StartFlowRequest,
    ) -> emr_20160408_models.StartFlowResponse:
        runtime = util_models.RuntimeOptions()
        return await self.start_flow_with_options_async(request, runtime)

    def submit_flow_with_options(
        self,
        request: emr_20160408_models.SubmitFlowRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.SubmitFlowResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.conf):
            query['Conf'] = request.conf
        if not UtilClient.is_unset(request.flow_id):
            query['FlowId'] = request.flow_id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='SubmitFlow',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.SubmitFlowResponse(),
            self.call_api(params, req, runtime)
        )

    async def submit_flow_with_options_async(
        self,
        request: emr_20160408_models.SubmitFlowRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.SubmitFlowResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.conf):
            query['Conf'] = request.conf
        if not UtilClient.is_unset(request.flow_id):
            query['FlowId'] = request.flow_id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='SubmitFlow',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.SubmitFlowResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def submit_flow(
        self,
        request: emr_20160408_models.SubmitFlowRequest,
    ) -> emr_20160408_models.SubmitFlowResponse:
        runtime = util_models.RuntimeOptions()
        return self.submit_flow_with_options(request, runtime)

    async def submit_flow_async(
        self,
        request: emr_20160408_models.SubmitFlowRequest,
    ) -> emr_20160408_models.SubmitFlowResponse:
        runtime = util_models.RuntimeOptions()
        return await self.submit_flow_with_options_async(request, runtime)

    def submit_flow_job_with_options(
        self,
        request: emr_20160408_models.SubmitFlowJobRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.SubmitFlowJobResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.conf):
            query['Conf'] = request.conf
        if not UtilClient.is_unset(request.host_name):
            query['HostName'] = request.host_name
        if not UtilClient.is_unset(request.job_id):
            query['JobId'] = request.job_id
        if not UtilClient.is_unset(request.job_instance_id):
            query['JobInstanceId'] = request.job_instance_id
        if not UtilClient.is_unset(request.namespace):
            query['Namespace'] = request.namespace
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='SubmitFlowJob',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.SubmitFlowJobResponse(),
            self.call_api(params, req, runtime)
        )

    async def submit_flow_job_with_options_async(
        self,
        request: emr_20160408_models.SubmitFlowJobRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.SubmitFlowJobResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cluster_id):
            query['ClusterId'] = request.cluster_id
        if not UtilClient.is_unset(request.conf):
            query['Conf'] = request.conf
        if not UtilClient.is_unset(request.host_name):
            query['HostName'] = request.host_name
        if not UtilClient.is_unset(request.job_id):
            query['JobId'] = request.job_id
        if not UtilClient.is_unset(request.job_instance_id):
            query['JobInstanceId'] = request.job_instance_id
        if not UtilClient.is_unset(request.namespace):
            query['Namespace'] = request.namespace
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='SubmitFlowJob',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.SubmitFlowJobResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def submit_flow_job(
        self,
        request: emr_20160408_models.SubmitFlowJobRequest,
    ) -> emr_20160408_models.SubmitFlowJobResponse:
        runtime = util_models.RuntimeOptions()
        return self.submit_flow_job_with_options(request, runtime)

    async def submit_flow_job_async(
        self,
        request: emr_20160408_models.SubmitFlowJobRequest,
    ) -> emr_20160408_models.SubmitFlowJobResponse:
        runtime = util_models.RuntimeOptions()
        return await self.submit_flow_job_with_options_async(request, runtime)

    def suspend_flow_with_options(
        self,
        request: emr_20160408_models.SuspendFlowRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.SuspendFlowResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.flow_instance_id):
            query['FlowInstanceId'] = request.flow_instance_id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='SuspendFlow',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.SuspendFlowResponse(),
            self.call_api(params, req, runtime)
        )

    async def suspend_flow_with_options_async(
        self,
        request: emr_20160408_models.SuspendFlowRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.SuspendFlowResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.flow_instance_id):
            query['FlowInstanceId'] = request.flow_instance_id
        if not UtilClient.is_unset(request.project_id):
            query['ProjectId'] = request.project_id
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='SuspendFlow',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.SuspendFlowResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def suspend_flow(
        self,
        request: emr_20160408_models.SuspendFlowRequest,
    ) -> emr_20160408_models.SuspendFlowResponse:
        runtime = util_models.RuntimeOptions()
        return self.suspend_flow_with_options(request, runtime)

    async def suspend_flow_async(
        self,
        request: emr_20160408_models.SuspendFlowRequest,
    ) -> emr_20160408_models.SuspendFlowResponse:
        runtime = util_models.RuntimeOptions()
        return await self.suspend_flow_with_options_async(request, runtime)

    def tag_resources_with_options(
        self,
        request: emr_20160408_models.TagResourcesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.TagResourcesResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_id):
            query['ResourceId'] = request.resource_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.resource_type):
            query['ResourceType'] = request.resource_type
        if not UtilClient.is_unset(request.tag):
            query['Tag'] = request.tag
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='TagResources',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.TagResourcesResponse(),
            self.call_api(params, req, runtime)
        )

    async def tag_resources_with_options_async(
        self,
        request: emr_20160408_models.TagResourcesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.TagResourcesResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_id):
            query['ResourceId'] = request.resource_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.resource_type):
            query['ResourceType'] = request.resource_type
        if not UtilClient.is_unset(request.tag):
            query['Tag'] = request.tag
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='TagResources',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.TagResourcesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def tag_resources(
        self,
        request: emr_20160408_models.TagResourcesRequest,
    ) -> emr_20160408_models.TagResourcesResponse:
        runtime = util_models.RuntimeOptions()
        return self.tag_resources_with_options(request, runtime)

    async def tag_resources_async(
        self,
        request: emr_20160408_models.TagResourcesRequest,
    ) -> emr_20160408_models.TagResourcesResponse:
        runtime = util_models.RuntimeOptions()
        return await self.tag_resources_with_options_async(request, runtime)

    def untag_resources_with_options(
        self,
        request: emr_20160408_models.UntagResourcesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.UntagResourcesResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.all):
            query['All'] = request.all
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_id):
            query['ResourceId'] = request.resource_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.resource_type):
            query['ResourceType'] = request.resource_type
        if not UtilClient.is_unset(request.tag_key):
            query['TagKey'] = request.tag_key
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UntagResources',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.UntagResourcesResponse(),
            self.call_api(params, req, runtime)
        )

    async def untag_resources_with_options_async(
        self,
        request: emr_20160408_models.UntagResourcesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> emr_20160408_models.UntagResourcesResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.all):
            query['All'] = request.all
        if not UtilClient.is_unset(request.region_id):
            query['RegionId'] = request.region_id
        if not UtilClient.is_unset(request.resource_id):
            query['ResourceId'] = request.resource_id
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.resource_type):
            query['ResourceType'] = request.resource_type
        if not UtilClient.is_unset(request.tag_key):
            query['TagKey'] = request.tag_key
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UntagResources',
            version='2016-04-08',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            emr_20160408_models.UntagResourcesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def untag_resources(
        self,
        request: emr_20160408_models.UntagResourcesRequest,
    ) -> emr_20160408_models.UntagResourcesResponse:
        runtime = util_models.RuntimeOptions()
        return self.untag_resources_with_options(request, runtime)

    async def untag_resources_async(
        self,
        request: emr_20160408_models.UntagResourcesRequest,
    ) -> emr_20160408_models.UntagResourcesResponse:
        runtime = util_models.RuntimeOptions()
        return await self.untag_resources_with_options_async(request, runtime)
