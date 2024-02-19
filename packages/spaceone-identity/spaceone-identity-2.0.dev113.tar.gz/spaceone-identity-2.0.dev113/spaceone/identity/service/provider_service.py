import logging
from typing import Union

from spaceone.core.service import *
from spaceone.core.service.utils import *
from spaceone.core.error import *

from spaceone.identity.model.provider.request import *
from spaceone.identity.model.provider.response import *
from spaceone.identity.manager.provider_manager import ProviderManager

_LOGGER = logging.getLogger(__name__)


@authentication_handler
@authorization_handler
@mutation_handler
@event_handler
class ProviderService(BaseService):
    resource = "Provider"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.provider_mgr = ProviderManager()

    @transaction(permission="identity:Provider.write", role_types=["DOMAIN_ADMIN"])
    @convert_model
    def create(self, params: ProviderCreateRequest) -> Union[ProviderResponse, dict]:
        """create provider

        Args:
            params (ProviderCreateRequest): {
                'provider': 'str',      # required
                'name': 'str',          # required
                'alias': 'str',
                'color': 'str',
                'icon': 'str',
                'order': 'int',
                'options': 'dict',
                'tags': 'dict',
                'domain_id': 'str'      # injected from auth (required)
            }

        Returns:
            ProviderResponse:
        """

        provider_vo = self.provider_mgr.create_provider(params.dict())
        return ProviderResponse(**provider_vo.to_dict())

    @transaction(permission="identity:Provider.write", role_types=["DOMAIN_ADMIN"])
    @convert_model
    def update(self, params: ProviderUpdateRequest) -> Union[ProviderResponse, dict]:
        """update provider

        Args:
            params (ProviderUpdateRequest): {
                'provider': 'str',      # required
                'name': 'str',
                'alias': 'str',
                'color': 'str',
                'icon': 'str',
                'order': 'int',
                'options': 'dict',
                'tags': 'dict',
                'domain_id': 'str'      # injected from auth (required)
            }

        Returns:
            ProviderResponse:
        """

        provider_vo = self.provider_mgr.get_provider(params.provider, params.domain_id)
        if provider_vo.is_managed:
            raise ERROR_PERMISSION_DENIED()

        provider_vo = self.provider_mgr.update_provider_by_vo(
            params.dict(exclude_unset=True), provider_vo
        )

        return ProviderResponse(**provider_vo.to_dict())

    @transaction(permission="identity:Provider.write", role_types=["DOMAIN_ADMIN"])
    @convert_model
    def delete(self, params: ProviderDeleteRequest) -> None:
        """delete provider

        Args:
            params (ProviderDeleteRequest): {
                'provider': 'str',      # required
                'domain_id': 'str'      # injected from auth (required)
            }

        Returns:
            None
        """

        provider_vo = self.provider_mgr.get_provider(params.provider, params.domain_id)
        if provider_vo.is_managed:
            raise ERROR_PERMISSION_DENIED()

        self.provider_mgr.delete_provider_by_vo(provider_vo)

    @transaction(
        permission="identity:Provider.read",
        role_types=["DOMAIN_ADMIN", "WORKSPACE_OWNER", "WORKSPACE_MEMBER"],
    )
    @convert_model
    def get(self, params: ProviderGetRequest) -> Union[ProviderResponse, dict]:
        """delete provider

        Args:
            params (ProviderGetRequest): {
                'provider': 'str',      # required
                'domain_id': 'str'      # injected from auth (required)
            }

        Returns:
            ProviderResponse:
        """

        provider_vo = self.provider_mgr.get_provider(params.provider, params.domain_id)
        return ProviderResponse(**provider_vo.to_dict())

    @transaction(
        permission="identity:Provider.read",
        role_types=["DOMAIN_ADMIN", "WORKSPACE_OWNER", "WORKSPACE_MEMBER"],
    )
    @append_query_filter(["provider", "name", "alias", "is_managed", "domain_id"])
    @append_keyword_filter(["provider", "name"])
    @convert_model
    def list(
        self, params: ProviderSearchQueryRequest
    ) -> Union[ProvidersResponse, dict]:
        """list providers

        Args:
            params (ProviderSearchQueryRequest): {
                'query': 'dict (spaceone.api.core.v1.Query)',
                'provider': 'str',
                'name': 'str',
                'alias': 'str',
                'is_managed': 'bool',
                'domain_id': 'str'      # injected from auth (required)
            }

        Returns:
            ProvidersResponse:
        """

        query = params.query or {}
        provider_vos, total_count = self.provider_mgr.list_providers(
            query, params.domain_id
        )

        providers_info = [provider_vo.to_dict() for provider_vo in provider_vos]
        return ProvidersResponse(results=providers_info, total_count=total_count)

    @transaction(
        permission="identity:Provider.read",
        role_types=["DOMAIN_ADMIN", "WORKSPACE_OWNER", "WORKSPACE_MEMBER"],
    )
    @append_query_filter(["domain_id"])
    @append_keyword_filter(["provider", "name"])
    @convert_model
    def stat(self, params: ProviderStatQueryRequest) -> dict:
        """stat providers

        Args:
            params (ProviderStatQueryRequest): {
                'query': 'dict (spaceone.api.core.v1.StatisticsQuery)', # required
                'domain_id': 'str'    # injected from auth (required)
            }

        Returns:
            dict: {
                'results': 'list',
                'total_count': 'int'
            }

        """

        query = params.query or {}
        return self.provider_mgr.stat_providers(query)
