module.exports = {
  apps: [
    {
      name: 'miner',
      script: 'python3',
      args: './neurons/miner.py --netuid 93 --logging.debug --logging.trace --subtensor.network finney'
    },
  ],
};
