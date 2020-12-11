#  Release Notes

## v3.0 - New options: block GETs also, allow private IPs, and support for domain names

* New feature (setting `ADMINRESTRICT_BLOCK_GET = True`) to enable this middleware to filter access for ALL accesses to admin page URLs (GET or POST).
* New feature (setting `ADMINRESTRICT_DENIED_MSG = "custom msg"`) to allow custom body for 403 denied responses.
* New feature (setting `ADMINRESTRICT_ALLOW_PRIVATE_IP = True`) to allow all RFC1918 addresses to access admin pages regardless of entries in AllowedIP table
* New feature to support allowing access in the AllowedIP table via CIDR ranges.
* New feature to support allowing access in the AllowedIP table via domain names. Use case: dynamic DNS domain names.

Release date 2020-12-11
