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

import typing
import bittensor as bt
import pydantic

# TODO(developer): Rewrite with your protocol definition.

# This is the protocol for the dummy miner and validator.
# It is a simple request-response protocol where the validator sends a request
# to the miner, and the miner responds with a dummy response.

# ---- miner ----
# Example usage:
#   def dummy( synapse: Dummy ) -> Dummy:
#       synapse.dummy_output = synapse.dummy_input + 1
#       return synapse
#   axon = bt.axon().attach( dummy ).serve(netuid=...).start()

# ---- validator ---
# Example usage:
#   dendrite = bt.dendrite()
#   dummy_output = dendrite.query( Dummy( dummy_input = 1 ) )
#   assert dummy_output == 2


class Challenge(bt.Synapse):
    """
    A simple dummy protocol representation which uses bt.Synapse as its base.
    This protocol helps in handling dummy request and response communication between
    the miner and the validator.

    Attributes:
    - dummy_input: An integer value representing the input request sent by the validator.
    - dummy_output: An optional integer value which, when filled, represents the response from the miner.
    """

    # Required request input, filled by sending dendrite caller.
    timestamp: int = pydantic.Field(
        ...,
        title="Timestamp",
        description="The time stamp at which the validation is taking place for",
        allow_mutation=False,
    )

    open_price : float = pydantic.Field(
        ...,
        title="High price",
        description="The open price of S&P 500 for the day",
        allow_mutation=False,
    )

    high_price : float = pydantic.Field(
        ...,
        title="High price",
        description="The high price of S&P 500 for the day",
        allow_mutation=False,
    )

    low_price : float = pydantic.Field(
        ...,
        title="High price",
        description="The low price of S&P 500 for the day",
        allow_mutation=False,
    )

    volume : float = pydantic.Field(
        ...,
        title="Volume",
        description="S&P 500 trading volume",
        allow_mutation=False,
    )

    # Optional request output, filled by recieving axon.
    close_price: typing.Optional[float] = pydantic.Field(
        ...,
        title="Closing price",
        description="Closing price of S&P 500 closing price"
    )

    def deserialize(self) -> int:
        """
        Deserialize the dummy output. This method retrieves the response from
        the miner in the form of dummy_output, deserializes it and returns it
        as the output of the dendrite.query() call.

        Returns:
        - int: The deserialized response, which in this case is the value of dummy_output.

        Example:
        Assuming a Dummy instance has a dummy_output value of 5:
        >>> dummy_instance = Dummy(dummy_input=4)
        >>> dummy_instance.dummy_output = 5
        >>> dummy_instance.deserialize()
        5
        """
        return self.close_price