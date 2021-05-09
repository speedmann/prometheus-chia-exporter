from prometheus_client import start_http_server, Gauge, Enum, Info
import asyncio
import time
from chia.rpc.wallet_rpc_api import WalletRpcApi
from chia.rpc.wallet_rpc_client import WalletRpcClient
from chia.rpc.full_node_rpc_client import FullNodeRpcClient
from chia.rpc.harvester_rpc_client import HarvesterRpcClient
from chia.rpc.farmer_rpc_client import FarmerRpcClient
from chia.util.config import load_config
from chia.util.default_root import DEFAULT_ROOT_PATH
from chia.cmds.netspace_funcs import netstorge_async as w
from chia.cmds.farm_funcs import get_average_block_time

self_hostname="localhost"

net_config={"daemon_ssl":{"private_crt":"","private_key":""}}


NETSPACE = Gauge('chia_netspace_total', 'Current total netspace')
BLOCK_TIME = Gauge('chia_average_block_time', 'Average time between blocks')
HEIGHT = Gauge('chia_block_height', 'Current highest block')
SYNC_STATE = Enum('chia_sync_state', 'Current sync state', states=['synced','syncing'])
BALANCE = Gauge('chia_wallet_balance', 'Balance of wallets', ["name","id"])
PLOTS_TOTAL = Gauge('chia_plots_count', 'Total plots farmed by harvester')
PLOTS_SIZE = Gauge('chia_plots_size', 'Total plot size farmed by harvester')
FARMED_AMOUNT = Gauge('chia_farmed_amount', 'Total XCH farmed by harvester')
FARMED_LAST = Gauge('chia_farmed_last_block', 'Last height a farm reward was farmed')
TIME_TO_WIN = Gauge('chia_time_to_win', 'Expected time to win ')
REWARD_ADDRESS = Info('chia_reward_address', 'Farming rewards go to this address ')

async def main():
    try:
        config = load_config(DEFAULT_ROOT_PATH, "config.yaml")
        rpc_port = config["full_node"]["rpc_port"]
        wallet_rpc_port = config["wallet"]["rpc_port"]
        harvester_rpc_port = config["harvester"]["rpc_port"]
        farmer_rpc_port = config["farmer"]["rpc_port"]
        client = await WalletRpcClient.create(self_hostname, wallet_rpc_port,DEFAULT_ROOT_PATH,config)
        client_node = await FullNodeRpcClient.create(self_hostname, rpc_port,DEFAULT_ROOT_PATH,config)
        client_harvester = await HarvesterRpcClient.create(self_hostname, harvester_rpc_port,DEFAULT_ROOT_PATH,config)
        client_farmer = await FarmerRpcClient.create(self_hostname, farmer_rpc_port,DEFAULT_ROOT_PATH,config)

        # blockchain stuff
        blockchain = await client_node.get_blockchain_state()
        netspace = blockchain['space']
        NETSPACE.set(netspace)
        average_block_time = await get_average_block_time(rpc_port)
        BLOCK_TIME.set(average_block_time)
        status =blockchain['sync']['synced']
        if not status:
            SYNC_STATE.state('syncing')
        else:
            SYNC_STATE.state('synced')
        height = await client.get_height_info()
        HEIGHT.set(height)

        # wallet stuff
        wallets = await client.get_wallets()
        wallet_amounts = {}
        for wallet in wallets:
            balance = await client.get_wallet_balance(wallet['id'])
            #wallet_amounts[wallet['name']] = balance['confirmed_wallet_balance']
            BALANCE.labels(name=wallet['name'], id=wallet['id']).set(balance['confirmed_wallet_balance'])



        # harvester stats
        plots = await client_harvester.get_plots()
        plot_count = len(plots['plots'])
        PLOTS_TOTAL.set(plot_count)
        plot_size_total = 0
        for plot in plots['plots']:
            plot_size_total += plot['file_size']
        PLOTS_SIZE.set(plot_size_total)
        farmed_stat = await client.get_farmed_amount()
        farmed_amount = farmed_stat['farmed_amount']
        FARMED_AMOUNT.set(farmed_amount)
        farmed_last_height = farmed_stat['last_height_farmed']
        FARMED_LAST.set(farmed_last_height)

        seconds = 0
        if blockchain is not None and plots is not None:
            proportion = plot_size_total / blockchain["space"] if blockchain["space"] else -1
            seconds = int((average_block_time) / proportion) if proportion else -1
        TIME_TO_WIN.set(seconds)

        #Farmer stuff

        reward_address = await client_farmer.get_reward_targets(False)
        REWARD_ADDRESS.info({"farmer_target":reward_address["farmer_target"],"pool_target":reward_address["pool_target"]})



    except Exception as e:
        print('error connecting to something')
        print(e)

    finally:
        client.close()
        client_node.close()
        client_harvester.close()
        client_farmer.close()







if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    while True:
        asyncio.run(main())
        time.sleep(15)
