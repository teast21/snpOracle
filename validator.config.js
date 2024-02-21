module.exports = {
  apps: [
    {
      name: 'test-validator',
      script: 'python3',
      args: './neurons/validator.py --wallet.name testValidator --wallet.hotkey default --netuid 1 --logging.debug --logging.trace --subtensor.network local --subtensor.chain_endpoint 127.0.0.1:9946'
    },
  ],
};
