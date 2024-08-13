terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
    }
  }
  backend "azurerm" {
    resource_group_name  = "thisstoragerg"
    storage_account_name = "dicestorage02"
    container_name       = "13form"
    key                  = "dicesaralapplyState"
  }
}

resource "azurerm_resource_group" "resource_group" {
  name     = local.dicesaralapply-rg
  location = local.general-location
}

resource "azurerm_log_analytics_workspace" "log_analytics_workspace" {
  name                = local.dicesaralapply-log-analytics-workspace
  location            = azurerm_resource_group.resource_group.location
  resource_group_name = azurerm_resource_group.resource_group.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_container_app_environment" "app_environment" {
  name                = local.dicesaralapply-app-environment
  location            = azurerm_resource_group.resource_group.location
  resource_group_name = azurerm_resource_group.resource_group.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.log_analytics_workspace.id
}