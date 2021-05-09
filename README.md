# prometheus-chia-exporter
Prometheus exporter for several chia node statistics
It's assumed that the full node, the harvester and the wallet run on the same system.
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
```

# Requirements
The exporter is meant to be run from your chia-blockchain venv. Additionally you need `prometheus-client` as specified in `requirements.txt`

```
cd chia-blockchain
. ./activate
cd ../prometheus-chia-exporter
pip install -r requirements.txt
```

# Installation
copy the systemd unit files to `/etc/systemd/system/

```
sudo cp systemd/chia_exporter.service /etc/systemd/system
# Edit the file to have correct chia blockchain path and username
sudo systemctl daemon-reload
sudo systemctl enable chia_exporter
sudo systemctl start chia_exporter
```


Edit `self_hostname` in `prometheus-chia-exporter/chia-exporter.py` 

# Usage
Start the systemd service
Import `grafana/dashboard.json` to your grafana
Add prometheus config

```
scrape_configs:
  - job_name: 'chia'
    static_configs:
      - targets: ['nodeip:8000']
```
