# terraform {
#   required_providers {
#     azurerm = {
#       source  = "hashicorp/azurerm"
#       version = "=3.0.0"
#     }
#   }
#   backend "azurerm" {
#     resource_group_name  = "thisstoragerg"
#     storage_account_name = "dicestorage02"
#     container_name       = "13form"
#     key                  = "tfstatedice"
#   }
# }

# provider "azurerm" {
#   features {}
# }

# resource "azurerm_resource_group" "hub" {
#   name     = "${var.resource_group_name_prefix}-hub"
#   location = var.resource_group_location
# }

# resource "azurerm_container_registry" "acr" {
#   name                = "${var.project_name}acr"
#   resource_group_name = azurerm_resource_group.hub.name
#   location            = azurerm_resource_group.hub.location
#   sku                 = "Standard"
#   admin_enabled       = true
# }
