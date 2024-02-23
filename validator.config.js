module.exports = {
  apps: [
    {
      name: 'test-validator',
      script: 'python3',
      args: './neurons/validator.py --wallet.name testValidator --wallet.hotkey default --netuid 93 --logging.debug --logging.trace --subtensor.network test'
    },
  ],
};
