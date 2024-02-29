module.exports = {
  apps: [
    {
      name: 'miner',
      script: 'python3',
      args: './neurons/miner.py --netuid 28 --logging.debug --logging.trace --subtensor.network local --wallet.name walletName --wallet.hotkey hotkeyName --axon.port 8091 --model base_lstm.h5'
    },
  ],
};
