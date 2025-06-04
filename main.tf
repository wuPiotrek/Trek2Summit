terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=4.1.0"
    }
  }
}
provider "azurerm" {
  features {}
  resource_provider_registrations = "none"
}

terraform {
  backend "azurerm" {
    resource_group_name  = "rg-PiotrW"
    storage_account_name = "sapiotrw"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
  }
}

resource "azurerm_service_plan" "example" {
  name                = "piotrw-app-service-plan"
  location            = "westeurope"
  resource_group_name = "rg-PiotrW"
  os_type             = "Linux"
  sku_name            = "P0v3"
}


resource "azurerm_linux_web_app" "example" {
  name                = "piotrw-webapp-t2s-workshop-1"
  location            = "westeurope"
  resource_group_name = "rg-PiotrW"
  service_plan_id     = azurerm_service_plan.example.id
  site_config {}
}

resource "azurerm_mssql_server" "example" {
  name                         = "piotrw-webapp-t2s-workshop-db"
  resource_group_name          = "rg-PiotrW"
  location                     = "westeurope"
  version                      = "12.0"
  administrator_login          = "4dm1n157r470r"
  administrator_login_password = "4-v3ry-53cr37-p455w0rd"
}

resource "azurerm_mssql_database" "example" {
  name         = "piotrw-db"
  server_id    = azurerm_mssql_server.example.id
  collation    = "Polish_CI_AS" 
  license_type = "LicenseIncluded"
  max_size_gb  = 2
  sku_name     = "S0"
  enclave_type = "VBS"

  tags = {
    foo = "bar"
  }

  # prevent the possibility of accidental data loss
  lifecycle {
    prevent_destroy = true
  }
}