<div align="center">

# **Foundry PredictionNet** <!-- omit in toc -->
---
---
---
## Foundry Accelerate <!-- omit in toc -->

[Website](https://foundrydigital.com/accelerate/) • [Validator](https://taostats.io/validators/foundry/) • [Twitter](https://x.com/FoundryServices?s=20)
</div>

---
- [Introduction](#introduction)
- [Design Decisions](#design-decisions)
- [Installation](#installation)
  - [Install PM2](#install-pm2)
  - [Install PredictionNet](#install-predictionnet)
- [About the Rewards Mechanism](#about-the-rewards-mechanism)
- [License](#license)

---
## Introduction

Foundry is launching Foundry PredictionNet to incentivize miners to make predictions on the S&P 500 price frequently throughout trading hours. Validators send miners a timestamp (a future time) for which the miners need to make an S&P 500 price prediction for. Miners need to respond with their prediction for the price of the S&P 500 at the given time. Validators store the miner predictions, and then calculate the scores of the miners after the predictions mature. Miners are ranked against eachother, naturally incentivizing competition between the miners. 

---
## Design Decisions

A Bittensor integration into financial markets will expose Bittensor to the largest system in the world; the global economy. The S&P 500 serves as a perfect starting place for financial predictions given its utility and name recognition. Financial market predictions were chosen for three main reasons:
1) __Utility:__ financial markets provide a massive userbase of professional traders, wealth managers, and individuals alike
2) __Objective Rewards Mechanism:__ by tying the rewards mechanism to an external source of truth (yahoo finance's S&P Price), the defensibility of the subnet regarding gamification is quite strong.
3) __Adversarial Environment:__ the adversarial environment, especially given the rewards mechanism, will allow for significant diversity of models. Miners will be driven to acquire different datasets, implement different training methods, and utilize different model architectures in order to develop the most performant models. 
---
## Installation
### Install PM2
First, install PM2:
```
sudo apt update
sudo apt install nodejs npm
sudo npm install pm2@latest -g
```
Verify installation:
```
pm2 --version
```
### Compute Requirements

| Validator |   Miner   |
|---------- |-----------|
|  8gb RAM  |  8gb RAM  | 
|  2 vCPUs  |  2 vCPUs  | 

### Install-PredictionNet

Begin by creating and sourcing a python virtual environment:
```
python3 -m venv .snX
source .snX/bin/activate
```
Clone the Foundry PredictionNet repo:
```
git clone https://github.com/teast21/predictionnet.git
```
Install Requirements:
```
pip3 -e install predictionnet
```

### Running a Miner
ecosystem.config.js files have been created to make deployment of miners and validators easier for the node operator. These files are the default configuration files for PM2, and allow the user to define the environment & application in a cleaner way. IMPORTANT: Make sure your have activated your virtual environment before running your validator/miner. 
To run your miner:
```
pm2 start miner.config.js
```
The miner.config.js has few flags added. Any standard flags can be passed, for example, wallet name and hotkey name will default to "default"; if you have a different configuration, edit your "args" in miner.config.js. Below shows a miner.config.js with extra configuration flags. 
```
module.exports = {
  apps: [
    {
      name: 'miner',
      script: 'python3',
      args: './neurons/miner.py --netuid X --logging.debug --logging.trace --subtensor.network local --wallet.name walletName --wallet.hotkey hotkeyName --axon.port 8000'
    },
  ],
};
```
### Running a Validator
ecosystem.config.js files have been created to make deployment of miners and validators easier for the node operator. These files are the default configuration files for PM2, and allow the user to define the environment & application in a cleaner way. IMPORTANT: Make sure your have activated your virtual environment before running your validator/miner. 

To run your validator:
```
pm2 start validator.config.js
```

The validator.config.js has few flags added. Any standard flags can be passed, for example, wallet name and hotkey name will default to "default"; if you have a different configuration, edit your "args" in miner.config.js. Below shows a miner.config.js with extra configuration flags. 
```
module.exports = {
  apps: [
    {
      name: 'validator',
      script: 'python3',
      args: './neurons/validator.py --netuid X --logging.debug --logging.trace --subtensor.network local --wallet.name walletName --wallet.hotkey hotkeyName'
    },
  ],
};
```

## About the Rewards Mechanism

The simplicity of the rewards mechanism is quite intentional. There are no methods to require a machine learning model be run by the miners. This is because the nature of the problem is such that machine learning models will inherently perform better than any method of gamification. By effectively performing a commit-reveal on a future S&P Price Prediction, PredictionNet ensures that only well-tuned models will survive. 

Root Mean Squared Error(RMSE) is calculated as such:
![image](https://github.com/teast21/predictionnet/assets/109384972/214b9b12-2563-498c-8f06-956c9f9ee7b0)

The RMSE is then normalized to enforce scores between 0 and 1, and those scores are used to update the existing scores in the metagraph. The weighting function applied to how scores are added to the metagraph creates a pseudo-rolling average score for predictions. Thus, a miner will have perfect trust after a perfect prediction, and will also not have 0 trust after having the worst prediction of an epoch. Consistent high-quality performance will result in high trust, and consistent low-quality performance will result in low trust and eventual de-registration. 

---

## License
This repository is licensed under the MIT License.
```text
# The MIT License (MIT)
# Copyright © 2024 Foundry Digital

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
```
