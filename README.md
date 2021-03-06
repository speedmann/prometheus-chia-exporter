# prometheus-chia-exporter
Prometheus exporter for several chia node statistics
It's assumed that the full node, the harvester and the wallet run on the same system.

![dashboard](https://github.com/speedmann/prometheus-chia-exporter/blob/main/screenshots/dashboard.png?raw=true)

```
# HELP chia_netspace_total Current total netspace
# TYPE chia_netspace_total gauge
chia_netspace_total 3.555581383124895e+18
# HELP chia_average_block_time Average time between blocks
# TYPE chia_average_block_time gauge
chia_average_block_time 31.812749003984063
# HELP chia_block_height Current highest block
# TYPE chia_block_height gauge
chia_block_height 255143.0
# HELP chia_sync_state Current sync state
# TYPE chia_sync_state gauge
chia_sync_state{chia_sync_state="synced"} 1.0
chia_sync_state{chia_sync_state="syncing"} 0.0
# HELP chia_wallet_balance Balance of wallets
# TYPE chia_wallet_balance gauge
chia_wallet_balance{id="1",name="Chia Wallet"} 1.899905e+012
# HELP chia_node_connections Currently open connections to node
# TYPE chia_node_connections gauge
chia_node_connections{type="3"} 1.0
chia_node_connections{type="1"} 22.0
chia_node_connections{type="6"} 1.0
# HELP chia_plots_count Total plots farmed by harvester
# TYPE chia_plots_count gauge
chia_plots_count 130.0
# HELP chia_plots_size Total plot size farmed by harvester
# TYPE chia_plots_size gauge
chia_plots_size 1.4148014850864e+013
# HELP chia_farmed_amount Total XCH farmed by harvester
# TYPE chia_farmed_amount gauge
chia_farmed_amount 2e+012
# HELP chia_farmed_last_block Last height a farm reward was farmed
# TYPE chia_farmed_last_block gauge
chia_farmed_last_block 206883.0
# HELP chia_time_to_win Expected time to win 
# TYPE chia_time_to_win gauge
chia_time_to_win 7.99496e+06
# HELP chia_reward_address_info Farming rewards go to this address 
# TYPE chia_reward_address_info gauge
chia_reward_address_info{farmer_target="farmer_address",pool_target="pool_address"} 1.0
# HELP chia_difficulty Current blockchain difficulty 
# TYPE chia_difficulty gauge
chia_difficulty 3.044624155857344e+18
```

# Requirements
The exporter is meant to be run from your chia-blockchain venv. Additionally you need `prometheus-client` as specified in `requirements.txt`

```
cd chia-blockchain
. ./activate
cd ../prometheus-chia-exporter
pip install -r requirements.txt
```

## Grafana
The provided dashboard does use features which are only available in the latest (7.5.5) version of grafana.
Please make sure you are using this or a newer version.

You can still decide to use an older version but then the `farmer_address` and `pool_address` display does not work correct.

# Installation
Copy the needed files to their locations as described below

```
# Copy the systemd unit file
sudo cp systemd/chia_exporter.service /etc/systemd/system
# Edit the unit file to have correct chia blockchain path and username
# Copy the environment file
sudo cp systemd/chia_exporter.env /etc/default/
# If the node you want to monitor does not run on the same host as the exporter, edit the env file
# copy the exporter to /usr/local/bin/
sudo cp prometheus-chia-exporter/chia-exporter.py /usr/local/bin/
# Reload systemd to have access to the new service
sudo systemctl daemon-reload
# Make sure the service is started on system boot
sudo systemctl enable chia_exporter
# Start the service
sudo systemctl start chia_exporter
```

## Custom config

You can monitor remote nodes by editing `/etc/default/chia_exporter.env` and changing the settings there 

# Usage
Start the systemd service
Import `grafana/dashboard.json` to your grafana
The exporter will listen on port 9824
Add prometheus config

```
scrape_configs:
  - job_name: 'chia'
    static_configs:
      - targets: ['nodeip:9824']
```

# Overriding hostnames

If you are running the full node on a different host or container, you can override the hostnames used for connecting to the daemons by setting one or all of the following environment variables: `FULL_NODE_HOST`, `WALLET_HOST`, `HARVESTER_HOST`, `FARMER_HOST`. All hostnames default to localhost.

# Updating

To update just copy the chia-exporter.py file to `/usr/local/bin/chia-exporter.py` again and restart the service `sodo systemctl restart chia_exporter`

# Donation
If you like this work and it helps you to monitor your farm please consider donating XCH to `xch1z026zx5a7xask0srznwnv9ktllc96flvcsk9ly7k06dhnje0asfsym8xuc`
It will be really appreciated and help me keeping this exporter working
