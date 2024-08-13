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

resource "azurerm_container_app_environment" "app_environment" {
  name                = local.dicesaralapply-app-environment
  location            = azurerm_resource_group.resource_group.location
  resource_group_name = azurerm_resource_group.resource_group.name
}