terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0.0"
    }
  }
  required_version = ">= 0.14.9"
}
resource "azurerm_resource_group" "example" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_service_plan" "example" {
  name                = var.app_service_plan_name
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  os_type              = "Linux"
  sku_name            = var.app_service_plan_sku
}


resource "azurerm_linux_web_app" "example" {
  name                = var.app_service_name
  resource_group_name = azurerm_resource_group.example.name
  location            = azurerm_resource_group.example.location
  service_plan_id = azurerm_service_plan.example.id

  site_config {
  }

  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_app_service_source_control" "name" {
  app_id = azurerm_linux_web_app.example.id
}


# resource "azurerm_role_assignment" "example" {
#   principal_id            = azurerm_web_app.example.identity[0].principal_id
#   scope                   = azurerm_resource_group.example.id
#   role_definition_name    = "AcrPull"
# }

# resource "azurerm_web_app" "example" {
#   name                = "dicesaralapply"
#   location            = azurerm_resource_group.example.location
#   resource_group_name = azurerm_resource_group.example.name
#   app_service_plan_id = azurerm_app_service_plan.example.id

#   identity {
#     type = "SystemAssigned"
#   }

#   site_config {
#     linux_fx_version = "DOCKER|thisacr.azurecr.io/imagename:latest"
#   }
# }
