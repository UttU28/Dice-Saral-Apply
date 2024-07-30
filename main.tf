terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=3.0.0"
    }
  }
  backend "azurerm" {
    resource_group_name  = "thisstoragerg"
    storage_account_name = "dicestorage02"
    container_name       = "13form"
    key                  = "tfstatedice"
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "backend-app" {
  name     = "${var.resource_group_name_prefix}-backend"
  location = var.resource_group_location
}
resource "azurerm_service_plan" "backend" {
  name                = "${var.project_name}-appserviceplan"
  resource_group_name = azurerm_resource_group.backend-app.name
  location            = azurerm_resource_group.backend-app.location
  os_type             = "Linux"
  sku_name            = "B1"
}

resource "azurerm_linux_web_app" "backend" {
  name                = "${var.project_name}-webapp"
  resource_group_name = azurerm_resource_group.backend-app.name
  location            = azurerm_service_plan.backend.location
  service_plan_id     = azurerm_service_plan.backend.id

  site_config {
    always_on = "true"
    application_stack {
      docker_image = "thisacr.azurecr.io/imagename:latest"
      #   docker_image     = "${azurerm_container_registry.acr.login_server}/${var.image_name}:latest"
      docker_image_tag = "latest"
      python_version   = "3.9"
    }
  }

  app_settings = {
    "DOCKER_REGISTRY_SERVER_URL"      = "https://thisacr.azurecr.io"
    "DOCKER_REGISTRY_SERVER_USERNAME" = "thisacr"
    "DOCKER_REGISTRY_SERVER_PASSWORD" = "U9+ivfherZPq3+UWDnj1fxftpOqWUgXqspIc90YYFI+ACRBkerUy"
    # "DOCKER_REGISTRY_SERVER_USERNAME" = azurerm_container_registry.acr.admin_username
    # "DOCKER_REGISTRY_SERVER_PASSWORD" = azurerm_container_registry.acr.admin_password
  }
}
