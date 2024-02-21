# py-teamdynamix
Python client for interacting with the TeamDynamix (TDX) ITSM APIs. The TDX API documentation is viewable via `{yourorg}.teamdynamix.com/TDWebAPI`.

# Authentication 
A [TeamDynamix service account](https://solutions.teamdynamix.com/TDClient/1965/Portal/KB/ArticleDet?ID=132442) is required to use this client.  

A standard or admin service account can be used.

## Standard Service Account

```python
from pytdx.tdx import Tdx

tdx_client = Tdx(
    username="svc_account_username",
    password="svc_account_password",
    hostname="yourorg.teamdynamix.com",
    environment="sandbox",
    asset_app_id=1111,
    client_portal_app_id=2222,
    ticketing_app_id=3333,
    is_admin=False,
)
```


## Admin Service Account
When using an Admin account, instantiate the `Tdx` class with `is_admin=True`.

`username` = Your organization's Web Services BEID  
`password` = The service account Web Services Key


# Usage
The `Tdx` class contains methods for interacting with Tickets, Assets, Knowledge Base Articles, etc. 

```python 
tdx_client.get_ticket(ticket_id=123456)
```