from msgraph import GraphServiceClient
from e5renewer.processor.msapis._caller import api


@api("AgreementAcceptances.Get")
async def get_agreement_acceptances(client: GraphServiceClient):
    return await client.agreement_acceptances.get()


@api("Admin.Get")
async def get_admin(client: GraphServiceClient):
    return await client.admin.get()


@api("Agreements.Get")
async def get_agreements(client: GraphServiceClient):
    return await client.agreements.get()


@api("AppCatalogs.Get")
async def get_app_catalogs(client: GraphServiceClient):
    return await client.app_catalogs.get()


@api("ApplicationTemplates.Get")
async def get_application_templates(client: GraphServiceClient):
    return await client.application_templates.get()


@api("Applications.Get")
async def get_applications(client: GraphServiceClient):
    return await client.applications.get()


@api("AuditLogs.Get")
async def get_audit_logs(client: GraphServiceClient):
    return await client.audit_logs.get()


@api("AuthenticationMethodConfigurations.Get")
async def get_authentication_method_configurations(client: GraphServiceClient):
    return await client.authentication_method_configurations.get()


@api("AuthenticationMethodsPolicy.Get")
async def get_authentication_methods_policy(client: GraphServiceClient):
    return await client.authentication_methods_policy.get()


@api("CertificateBasedAuthConfiguration.Get")
async def get_certificate_based_auth_configuration(client: GraphServiceClient):
    return await client.certificate_based_auth_configuration.get()


@api("Chats.Get")
async def get_chats(client: GraphServiceClient):
    return await client.chats.get()


@api("Communications.Get")
async def get_communications(client: GraphServiceClient):
    return await client.communications.get()


@api("Compliance.Get")
async def get_compliance(client: GraphServiceClient):
    return await client.compliance.get()


@api("Connections.Get")
async def get_connections(client: GraphServiceClient):
    return await client.connections.get()


@api("Contacts.Get")
async def get_contacts(client: GraphServiceClient):
    return await client.contacts.get()


@api("DataPolicyOperations.Get")
async def get_data_policy_operations(client: GraphServiceClient):
    return await client.data_policy_operations.get()


@api("DeviceAppManagement.Get")
async def get_device_app_management(client: GraphServiceClient):
    return await client.device_app_management.get()


@api("DeviceManagement.Get")
async def get_device_management(client: GraphServiceClient):
    return await client.device_management.get()


@api("Devices.Get")
async def get_devices(client: GraphServiceClient):
    return await client.devices.get()


@api("Direcory.Get")
async def get_directory(client: GraphServiceClient):
    return await client.directory.get()


@api("DirectoryObjects.Get")
async def get_directory_objects(client: GraphServiceClient):
    return await client.directory_objects.get()


@api("DirectoryRoleTemplates.Get")
async def get_directory_role_temlates(client: GraphServiceClient):
    return await client.directory_role_templates.get()


@api("DirectoryRoles.Get")
async def get_directory_roles(client: GraphServiceClient):
    return await client.directory_roles.get()


@api("DomainDnsRecords.Get")
async def get_domain_dns_records(client: GraphServiceClient):
    return await client.domain_dns_records.get()


@api("Domains.Get")
async def get_domains(client: GraphServiceClient):
    return await client.domains.get()


@api("Drives.Get")
async def get_drives(client: GraphServiceClient):
    return await client.drives.get()


@api("Education.Get")
async def get_education(client: GraphServiceClient):
    return await client.education.get()


@api("EmployeeExperience.Get")
async def get_employee_experience(client: GraphServiceClient):
    return await client.employee_experience.get()


@api("External.Get")
async def get_external(client: GraphServiceClient):
    return await client.external.get()


@api("FilterOperators.Get")
async def get_filter_operators(client: GraphServiceClient):
    return await client.filter_operators.get()


@api("Functions.Get")
async def get_functions(client: GraphServiceClient):
    return await client.functions.get()


@api("GroupLifecyclePolicies.Get")
async def get_group_lifecycle_policies(client: GraphServiceClient):
    return await client.group_lifecycle_policies.get()


@api("GroupSettingTemplates.Get")
async def get_group_setting_templates(client: GraphServiceClient):
    return await client.group_setting_templates.get()


@api("GroupSetings.Get")
async def get_group_settings(client: GraphServiceClient):
    return await client.group_settings.get()


@api("Groups.Get")
async def get_groups(client: GraphServiceClient):
    return await client.groups.get()


@api("Identity.Get")
async def get_identity(client: GraphServiceClient):
    return await client.identity.get()


@api("IdentityGovernance.Get")
async def get_identity_governance(client: GraphServiceClient):
    return await client.identity_governance.get()


@api("IdentityProtection.Get")
async def get_identity_protection(client: GraphServiceClient):
    return await client.identity_protection.get()


@api("IdentityProviders.Get")
async def get_identity_providers(client: GraphServiceClient):
    return await client.identity_providers.get()


@api("InfomationProtecion.Get")
async def get_infomation_protection(client: GraphServiceClient):
    return await client.information_protection.get()


@api("Invitations.Get")
async def get_invitations(client: GraphServiceClient):
    return await client.invitations.get()


@api("OAuth2PermissionGrants.Get")
async def get_oauth2_permission_grants(client: GraphServiceClient):
    return await client.oauth2_permission_grants.get()


@api("Organization.Get")
async def get_organization(client: GraphServiceClient):
    return await client.organization.get()


@api("PermissionGrants.Get")
async def get_permission_grants(client: GraphServiceClient):
    return await client.permission_grants.get()


@api("Places.Count.Get")
async def get_places_count(client: GraphServiceClient):
    return await client.places.count.get()


@api("Places.GraphRoom.Get")
async def get_places_graph_room(client: GraphServiceClient):
    return await client.places.graph_room.get()


@api("Planner.Get")
async def get_planner(client: GraphServiceClient):
    return await client.planner.get()


@api("Policies.Get")
async def get_policies(client: GraphServiceClient):
    return await client.policies.get()


@api("Print.Get")
async def get_print(client: GraphServiceClient):
    return await client.print.get()


@api("Privacy.Get")
async def get_privacy(client: GraphServiceClient):
    return await client.privacy.get()


@api("Reports.Get")
async def get_reports(client: GraphServiceClient):
    return await client.reports.get()


@api("RoleManagement.Get")
async def get_role_management(client: GraphServiceClient):
    return await client.role_management.get()


@api("SchemaExtensions.Get")
async def get_schema_extensions(client: GraphServiceClient):
    return await client.schema_extensions.get()


@api("ScopedRoleMemberships.Get")
async def get_scoped_role_memberships(client: GraphServiceClient):
    return await client.scoped_role_memberships.get()


@api("Search.Get")
async def get_search(client: GraphServiceClient):
    return await client.search.get()


@api("Security.Get")
async def get_security(client: GraphServiceClient):
    return await client.security.get()


@api("ServicePrincipals.Get")
async def get_service_principals(client: GraphServiceClient):
    return await client.service_principals.get()


@api("Shares.Get")
async def get_shares(client: GraphServiceClient):
    return await client.shares.get()


@api("Sites.Get")
async def get_sites(client: GraphServiceClient):
    return await client.sites.get()


@api("Solutions.Get")
async def get_solutions(client: GraphServiceClient):
    return await client.solutions.get()


@api("SubscribedSkus.Get")
async def get_subscribed_skus(client: GraphServiceClient):
    return await client.subscribed_skus.get()


@api("Subscriptions.Get")
async def get_subscriptions(client: GraphServiceClient):
    return await client.subscriptions.get()


@api("Teams.Get")
async def get_teams(client: GraphServiceClient):
    return await client.teams.get()


@api("TeamsTemplates.Get")
async def get_teams_templates(client: GraphServiceClient):
    return await client.teams_templates.get()


@api("Teamwork.Get")
async def get_teamwork(client: GraphServiceClient):
    return await client.teamwork.get()


@api("TenantRelationships.Get")
async def get_tenant_relationships(client: GraphServiceClient):
    return await client.tenant_relationships.get()


@api("Users.Get")
async def get_users(client: GraphServiceClient):
    return await client.users.get()


__all__ = [
    "get_admin",
    "get_agreement_acceptances",
    "get_agreements",
    "get_app_catalogs",
    "get_application_templates",
    "get_applications",
    "get_audit_logs",
    "get_authentication_method_configurations",
    "get_authentication_methods_policy",
    "get_certificate_based_auth_configuration",
    "get_chats",
    "get_communications",
    "get_compliance",
    "get_connections",
    "get_contacts",
    "get_data_policy_operations",
    "get_device_app_management",
    "get_device_management",
    "get_devices",
    "get_directory",
    "get_directory_objects",
    "get_directory_role_temlates",
    "get_directory_roles",
    "get_domain_dns_records",
    "get_domains",
    "get_drives",
    "get_education",
    "get_employee_experience",
    "get_external",
    "get_filter_operators",
    "get_functions",
    "get_group_lifecycle_policies",
    "get_group_setting_templates",
    "get_group_settings",
    "get_groups",
    "get_identity",
    "get_identity_governance",
    "get_identity_protection",
    "get_identity_providers",
    "get_infomation_protection",
    "get_invitations",
    "get_oauth2_permission_grants",
    "get_organization",
    "get_permission_grants",
    "get_places_count",
    "get_places_graph_room",
    "get_planner",
    "get_policies",
    "get_privacy",
    "get_reports",
    "get_role_management",
    "get_schema_extensions",
    "get_scoped_role_memberships",
    "get_search",
    "get_security",
    "get_service_principals",
    "get_shares",
    "get_sites",
    "get_solutions",
    "get_subscribed_skus",
    "get_subscriptions",
    "get_teams",
    "get_teams_templates",
    "get_teamwork",
    "get_tenant_relationships",
    "get_users",
]
