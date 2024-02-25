module.exports = {
  apps: [
    {
      name: 'validator',
      script: 'python3',
      args: './neurons/validator.py --wallet.name <WALLET_NAME> --wallet.hotkey <HOTKEY_NAME> --netuid 93 --logging.debug --logging.trace --subtensor.network finney'
    },
  ],
};
