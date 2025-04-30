# The MIT License (MIT)
# Copyright © 2024 Yuma Rao
# developer: Taoshidev
# Copyright © 2024 Taoshi Inc
import json
import os
import argparse
import threading
import traceback
import time
import bittensor as bt
import subprocess

class Miner:
    def __init__(self):
        self.config = self.get_config()
        assert self.config.netuid in (89, 351), "InfiniteQuant runs on netuid 89 (mainnet) and - (testnet)"
        self.is_testnet = self.config.netuid == 351
        self.setup_logging_directory()
        self.initialize_bittensor_objects()
        #self.check_miner_registration()
        self.my_subnet_uid = self.metagraph.hotkeys.index(self.wallet.hotkey.ss58_address)
        bt.logging.info(f"Running miner on netuid {self.config.netuid} with uid: {self.my_subnet_uid}")

        
    def setup_logging_directory(self):
        if not os.path.exists(self.config.full_path):
            os.makedirs(self.config.full_path, exist_ok=True)

    def initialize_bittensor_objects(self):
        self.wallet = bt.wallet(config=self.config)
        self.subtensor = bt.subtensor(config=self.config)
        self.metagraph = self.subtensor.metagraph(self.config.netuid)

    def check_miner_registration(self):
        if self.wallet.hotkey.ss58_address not in self.metagraph.hotkeys:
            bt.logging.error("Your miner is not registered. Please register and try again.")
            exit()

    @staticmethod
    def get_config():
        parser = argparse.ArgumentParser()
        # Adds override arguments for network and netuid.
        parser.add_argument("--netuid", type=int, default=1, help="The chain subnet uid.")
        # Adds subtensor specific arguments i.e. --subtensor.chain_endpoint ... --subtensor.network ...
        bt.subtensor.add_args(parser)
        # Adds logging specific arguments i.e. --logging.debug ..., --logging.trace .. or --logging.logging_dir ...
        bt.logging.add_args(parser)
        # Adds wallet specific arguments i.e. --wallet.name ..., --wallet.hotkey ./. or --wallet.path ...
        bt.wallet.add_args(parser)
        
        # Parse the config (will take command-line arguments if provided)
        # To print help message, run python3 template/miner.py --help
        config = bt.config(parser)
        bt.logging.enable_info()
        if config.logging.debug:
            bt.logging.enable_debug()
        if config.logging.trace:
            bt.logging.enable_trace()

        # Step 3: Set up logging directory
        # Logging is crucial for monitoring and debugging purposes.
        config.full_path = os.path.expanduser(
            "{}/{}/{}/netuid{}/{}".format(
                config.logging.logging_dir,
                config.wallet.name,
                config.wallet.hotkey,
                config.netuid,
                "miner",
            )
        )
        return config

    
    def run(self):
        bt.logging(config=self.config, logging_dir=self.config.full_path)
        bt.logging.info("Starting miner loop.")

        bt.logging.info("Waiting for signals...")
        while True:
            try:
                time.sleep(1)
            # If someone intentionally stops the miner, it'll safely terminate operations.
            except KeyboardInterrupt:
                bt.logging.success("Miner killed by keyboard interrupt.")
                break
            # In case of unforeseen errors, the miner will log the error and continue operations.
            except Exception:
                bt.logging.error(traceback.format_exc())
                time.sleep(10)


if __name__ == "__main__":
    miner = Miner()
    miner.run()
