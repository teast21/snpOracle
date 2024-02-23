module.exports = {
  apps: [
    {
      name: 'test-miner',
      script: 'python3',
      args: './neurons/miner.py --axon.port 8092 --wallet.name testMiner --wallet.hotkey default --netuid 93 --logging.debug --logging.trace --subtensor.network test'
    },
  ],
};
