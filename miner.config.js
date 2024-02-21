module.exports = {
  apps: [
    {
      name: 'test-miner',
      script: 'python3',
      args: './neurons/miner.py --wallet.name testMiner --wallet.hotkey default --netuid 1 --logging.debug --logging.trace --subtensor.network local --subtensor.chain_endpoint 127.0.0.1:9946'
    },
  ],
};
