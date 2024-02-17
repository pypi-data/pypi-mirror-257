from datetime import datetime
from typing import Any, Dict, List
import json
from .models import Performance, RuntimeConfig, RuntimeMode 
from .runtime import Runtime

class BacktestPerformance:
    def __init__(self, config: RuntimeConfig):
        self.candle_topics = config.candle_topics

        if config.initial_capital == None:
            self.initial_capital = 10_000
        else:
            self.initial_capital = config.initial_capital 

        self.trades = {}

        if config.start_time != None:
            self.start_time = config.start_time.timestamp()

        if config.end_time != None:
            self.end_time = config.end_time.timestamp()

        self.version = "1.2.0"


    def set_trade_result(self, id: str, perf: Performance):
        self.trades[id] = perf

    def generate_json(self):
        x = json.dumps(self.__dict__, default=str)
        date = datetime.now().date();
        date = ''.join(str(date).split('-'));
        time = datetime.now().time();
        time = ''.join(str(time).split('.')[0].split(':'));
        file = open(f"performance-{date}{time}.json", "w")
        file.write(x);

class Permutation:
    results = []

    def __init__(self, config: RuntimeConfig):
        if config.mode != RuntimeMode.Backtest:
            raise Exception("Permutation is only allowed in Backtest mode!")
        self.config = config
    
    async def run(self, strategy_params: Dict[str, List[Any]], runtime: Runtime):
        length = -1;
        result = BacktestPerformance(self.config)
        for key in strategy_params.keys():
            if length == -1:
                length = len(strategy_params[key])
                break;

        for i in range(length):
            for key in strategy_params.keys():
                await runtime.set_param(key, str(strategy_params[key][i]))

            id = ""
            for key in strategy_params.keys():
                id += f"{key}={strategy_params[key][i]},"

            self.results.append([id, await runtime.start()])

        for id, perf in self.results:
            result.set_trade_result(id, perf)

        result.generate_json()
