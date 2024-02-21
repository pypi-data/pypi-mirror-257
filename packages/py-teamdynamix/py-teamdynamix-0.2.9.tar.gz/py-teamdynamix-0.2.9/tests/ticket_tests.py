from pytdx.tdx import Tdx
from pytdx.models.ticket import Ticket

# from pytdx.models.ticket import TicketModel
import os
from dotenv import load_dotenv
import json

load_dotenv()

conn_info = json.loads(os.getenv("TDX_SB_CONN"))


tdx_client = Tdx(
    username=conn_info[0],
    password=conn_info[1],
    hostname=conn_info[2],
    environment=conn_info[3],
    asset_app_id=conn_info[4],
    client_portal_app_id=conn_info[5],
    ticketing_app_id=conn_info[6],
    is_admin=conn_info[7],
)


# ticket = tdx_client.get_ticket(id=20896004)

update_ticket = Ticket(Title="New Methods 2 - Test")

request = tdx_client.update_ticket(data=update_ticket)
print(request.ID)
