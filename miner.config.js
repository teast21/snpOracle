module.exports = {
  apps: [
    {
      name: 'miner',
      script: 'python3',
      args: './neurons/miner.py --axon.port <PORT> --wallet.name <WALLET_NAME> --wallet.hotkey <HOTKEY_NAME> --netuid 93 --logging.debug --logging.trace --subtensor.network finney'
    },
  ],
};
