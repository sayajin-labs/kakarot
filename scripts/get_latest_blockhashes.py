import asyncio
import logging
import json
from pathlib import Path

from starkware.starknet.services.api.feeder_gateway.feeder_gateway_client import FeederGatewayClient
from services.external_api.client import RetryConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FEEDER_GATEWAY_URL = "https://alpha4.starknet.io/feeder_gateway" # alpha-goerli


async def main():
    # Instantiate a FeederGatewayClient object
    # -1 means unlimited retries
    retry_config = RetryConfig(n_retries=-1)
    feeder_gateway_client = FeederGatewayClient(url=FEEDER_GATEWAY_URL, retry_config=retry_config)

    # Get the latest block
    # Sometimes get_block returns "null" as value
    # Walrus operator for assignment expression
    while (latest_block := await feeder_gateway_client.get_block()) == "null":
        continue
    logger.info(f"Latest block number: {latest_block.block_number}")

    # Get the last 256 blocks excluding the current block
    # Convert the list of blockhashes in to dictionary { block_number: block_hash }
    last_256_blocks = [
        await feeder_gateway_client.get_block(block_number=latest_block.block_number - i)
        for i in range(1, 257)
    ]
    last_256_blockhashes = {
        block.block_number: block.block_hash
        for block in last_256_blocks
    }
    
    # Dump JSON to file
    with open(Path("sequencer") / "blockhashes.json", "w") as file:
        context = {
            "current_block": {
                "block_number": latest_block.block_number,
                "timestamp": latest_block.timestamp
            },
            "last_256_blocks": last_256_blockhashes
        }
        json.dump(context, file)
    logger.info(f"Blockhashes retrieved from block number {min(last_256_blockhashes.keys())} to {max(last_256_blockhashes.keys())}")

if __name__== "__main__":
    asyncio.run(main())
