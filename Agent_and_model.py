from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import logging
import heapq

class OrderBook:
    def __init__(self):
        self.buy_orders = []  # Min heap for buy orders (price asc)
        self.sell_orders = []  # Max heap for sell orders (price desc)

    def add_buy_order(self, price, volume):
        heapq.heappush(self.buy_orders, (price, volume))

    def add_sell_order(self, price, volume):
        heapq.heappush(self.sell_orders, (-price, volume))

    def match_orders(self):
        while self.buy_orders and self.sell_orders and self.buy_orders[0][0] >= -self.sell_orders[0][0]:
            buy_price, buy_volume = heapq.heappop(self.buy_orders)
            sell_price, sell_volume = heapq.heappop(self.sell_orders)
            sell_price = -sell_price  

            # Determine transaction price and volume
            transaction_price = (buy_price + sell_price) / 2
            transaction_volume = min(buy_volume, sell_volume)

            # Update volumes if not fully matched
            if buy_volume > sell_volume:
                heapq.heappush(self.buy_orders, (buy_price, buy_volume - sell_volume))
            elif sell_volume > buy_volume:
                heapq.heappush(self.sell_orders, (-sell_price, sell_volume - buy_volume))

            return transaction_price, transaction_volume
        return None, None

class CryptoMarketModel(Model):
    def __init__(self, N):
        super().__init__()
        self.num_agents = N
        self.schedule = RandomActivation(self)
        self.market_info = {"current_price": curr, "trend": "bullish", "mar-ket_volume": volume}
        self.order_book = OrderBook()

        # Setting up logging
        logging.basicConfig(filename='crypto_market_model.log', lev-el=logging.INFO)

        # Initialize agents
        for i in range(self.num_agents):
            a = TraderAgent(i, self, random.choice(["conservative", "aggres-sive"]))
            self.schedule.add(a)

        self.datacollector = DataCollector(
            model_reporters={"Price": lambda m: m.market_info["current_price"],
                             "Total USD": lambda m: sum([agent.wallet["USD"] for agent in m.schedule.agents]),
                             "Total ": lambda m: sum([agent.wallet[crypto_name] for agent in m.schedule.agents]),
                             "Market Volatility": lambda m: abs(m.economic_factor - 1)}
        )

    def step(self):
        try:
            self.update_market_conditions()
            self.schedule.step()
            self.execute_orders()
            self.datacollector.collect(self)
        except Exception as e:
            logging.error(f"Error during model step execution: {e}")

    def update_market_conditions(self):
        self.market_info["trend"] 

    def execute_orders(self):
        transaction_price, transaction_volume = self.order_book.match_orders()
        if transaction_price and transaction_volume:
            self.market_info["current_price"] = transaction_price
            self.market_info["market_volume"] += transaction_volume

    def add_order(self, order_type, price, volume):
        if order_type == 'buy':
            self.order_book.add_buy_order(price, volume)
        elif order_type == 'sell':
            self.order_book.add_sell_order(price, volume)

    def get_market_info(self):
        return self.market_info



class TraderAgent(Agent):
    def __init__(self, unique_id, model, strategy):
        super().__init__(unique_id, model)
        self.strategy = strategy
        self.wallet = {"USD": 1000, crypto_name: 0}
        self.liquidity_constraints = {"max_trade_volume": 100}
        self.risk_appetite = 0.5  
        self.market_sentiment = "neutral"
        self.learning_component = None
        self.initial_investment = 1000  
        logging.basicConfig(filename='trader_agent.log', level=logging.INFO)

    def step(self):
        try:
            market_info = self.model.get_market_info()
            self.adjust_strategy()
            self.update_learning_component(market_info)
            self.manage_risk(market_info['current_price'])
            self.make_decision(market_info)
        except Exception as e:
            logging.error(f"Error during step execution: {e}")

  

    def manage_risk(self, current_price):
        if self.wallet[crypto_name] * current_price < self.initial_investment * (1 - self.risk_appetite):
            self.sell_all_crypto(current_price)

    def make_decision(self, market_info):
        current_price = market_info['current_price']
        if market_info['trend'] == "bullish":
            self.buy_crypto(current_price)
        elif market_info['trend'] == "bearish":
            self.sell_crypto(current_price)

    def buy_crypto(self, current_price):
        try:
            buy_proportion = 0.5 if self.strategy == "aggressive" else 0.2
            max_amount_to_buy = self.calculate_buy_amount(buy_proportion, current_price)
            amount_to_buy = min(max_amount_to_buy, self.liquidity_constraints["max_trade_volume"])
            if amount_to_buy > 0:
                self.model.add_order('buy', current_price, amount_to_buy, self.unique_id)
                logging.info(f"{self.unique_id} placed order to buy {amount_to_buy} BTC at {current_price}.")
            else:
                logging.warning(f"{self.unique_id} attempted to place buy order but had insufficient USD.")
        except Exception as e:
            logging.error(f"Error in buy_crypto: {e}")

    def sell_crypto(self, current_price):
        try:
            sell_proportion = 0.5 if self.strategy == "aggressive" else 0.2
            amount_to_sell = self.calculate_sell_amount(sell_proportion)
            if amount_to_sell > 0:
                self.model.add_order('sell', current_price, amount_to_sell, self.unique_id)
                logging.info(f"{self.unique_id} placed order to sell {amount_to_sell} BTC at {current_price}.")
            else:
                logging.warning(f"{self.unique_id} attempted to place sell order but had insufficient amount.")
        except Exception as e:
            logging.error(f"Error in sell_crypto: {e}")

    def sell_all_crypto(self, current_price):
        try:
            if self.wallet[crypto_name] > 0:
                self.wallet["USD"] += self.wallet[crypto_name] * current_price
                self.wallet[crypto_name] = 0
                logging.info(f"{self.unique_id} sold all BTC.")
            else:
                logging.warning(f"{self.unique_id} had no BTC to sell.")
        except Exception as e:
            logging.error(f"Error in sell_all_crypto: {e}")

    def calculate_buy_amount(self, proportion, current_price):
        return min(self.wallet["USD"] * proportion / current_price, self.wallet["USD"] / current_price)

    def calculate_sell_amount(self, proportion):
        return self.wallet[crypto_name] * proportion

    def calculate_roi(self):
        current_value = self.wallet["USD"] + self.wallet[crypto_name] * self.model.get_current_btc_price()
        return (current_value - self.initial_investment) / self.initial_investment

    def process_transaction(self, transaction_type, price, volume):
        """
        Update the agent's wallet based on the transaction details.
        """
        if transaction_type == 'buy':
            actual_cost = price * volume
            self.wallet[crypto_name] += volume
            self.wallet["USD"] -= actual_cost
        elif transaction_type == 'sell':
            self.wallet[crypto_name] -= volume
            self.wallet["USD"] += price * volume
        logging.info(f"{self.unique_id} completed a {transaction_type} trans-action of {volume} {crypto_name} at {price}.")
