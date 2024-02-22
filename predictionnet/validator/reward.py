# The MIT License (MIT)
# Copyright © 2023 Yuma Rao
# TODO(developer): Set your name
# Copyright © 2023 <your name>

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

import torch
from typing import List
import bittensor as bt
from predictionnet.protocol import Challenge
import time
from datetime import datetime, timedelta
import yfinance as yf
from pytz import timezone
import numpy as np
from sklearn.metrics import mean_squared_error

def get_rmse(challenge: List[Challenge], close_price: float) -> float:
    if challenge.prediction is None:
        raise ValueError("Where is my prediction bro.?")
    prediction_arr = np.array([c.prediction for c in challenge])
    squared_error = (prediction_arr - close_price) ** 2
    rmse = squared_error ** 0.5
    return rmse
    
def reward(response: Challenge, close_price: float) -> float:
    """
    Reward the miner response to the dummy request. This method returns a reward
    value for the miner, which is used to update the miner's score.

    Returns:
    - float: The reward value for the miner.
    """
    mse = mean_squared_error(response.prediction, close_price)
    
    return mse #1.0 if response == close_price * 2 else 0

# Query prob editied to query: Protocol defined synapse
# For this method mostly should defer to Rahul/Tommy
def get_rewards(
    self,
    query: Challenge,
    responses: List[Challenge],
) -> torch.FloatTensor:
    """
    Returns a tensor of rewards for the given query and responses.

    Args:
    - query (int): The query sent to the miner.
    - responses (List[Challenge]): A list of responses from the miner.
    
    Returns:
    - torch.FloatTensor: A tensor of rewards for the given query and responses.
    """

    if len(responses) == 0:
        bt.logging.info("Got no responses. Returning reward tensor of zeros.")
        return [], torch.zeros_like(0).to(self.device)  # Fallback strategy: Log and return 0.
    
    # Prepare to extract close price for this timestamp
    ticker_symbol = '^GSPC'
    ticker = yf.Ticker(ticker_symbol)

    timestamp = query.timestamp
    timestamp = datetime.fromisoformat(timestamp)

    # Round up current timestamp and then wait until that time has been hit
    rounded_up_time = timestamp - timedelta(minutes=timestamp.minute % 5,
                                    seconds=timestamp.second,
                                    microseconds=timestamp.microsecond) + timedelta(minutes=5)
    
    ny_timezone = timezone('America/New_York')

    while (datetime.now(ny_timezone) < rounded_up_time):
        bt.logging.info("Waiting for next 5m interval...")
        time.sleep(15)

    current_time_adjusted = rounded_up_time - timedelta(minutes=10)

    data = ticker.history(start=current_time_adjusted, end=timestamp, interval='5m')
    close_price = data['Close'].iloc[-1]
    
    # Get all the reward results by iteratively calling your reward() function.
    return torch.FloatTensor(
        [reward(close_price, response) for response in responses]
    ).to(self.device)
