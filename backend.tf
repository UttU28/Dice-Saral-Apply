terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=3.0.0"
    }
  }
  backend "azurerm" {
    resource_group_name  = "infra-rg"
    storage_account_name = "clinicainfra"
    container_name       = "tfstate"
    key                  = "tfstatealter"
  }
}

provider "azurerm" {
  features {}
}