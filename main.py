from typing import Dict, Any, List
from datetime import datetime
from collections import defaultdict

from vali_objects.scoring.scoring import Scoring
from vali_objects.vali_dataclasses.perf_ledger import PerfLedger, PerfCheckpoint
from vali_objects.position import Position
from vali_objects.vali_config import TradePair

cps = [
    {
        "accum_ms": 43200000,
        "carry_fee_loss": 0.0,
        "gain": 0.0010381421508632723,
        "last_update_ms": 1743508800000,
        "loss": -0.0011435489169096232,
        "mdd": 0.999608592434854,
        "mpv": 1.000199229466044,
        "n_updates": 264,
        "open_ms": 3103441,
        "prev_portfolio_carry_fee": 1.0,
        "prev_portfolio_ret": 0.9998945987890513,
        "prev_portfolio_spread_fee": 1.0,
        "spread_fee_loss": 0.0,
    },
    {
        "accum_ms": 43200000,
        "carry_fee_loss": -5.0069930111959875e-05,
        "gain": 0.01876445070085235,
        "last_update_ms": 1743552000000,
        "loss": -0.019810286182807838,
        "mdd": 0.9977584035892277,
        "mpv": 1.000296302553891,
        "n_updates": 681,
        "open_ms": 43200000,
        "prev_portfolio_carry_fee": 0.9999499313233661,
        "prev_portfolio_ret": 0.9988494201771262,
        "prev_portfolio_spread_fee": 1.0,
        "spread_fee_loss": 0.0,
    },
    {
        "accum_ms": 43200000,
        "carry_fee_loss": 0.0,
        "gain": 0.03327569374938068,
        "last_update_ms": 1743595200000,
        "loss": -0.03222989487055651,
        "mdd": 0.997040189166983,
        "mpv": 1.0008900164922954,
        "n_updates": 718,
        "open_ms": 43200000,
        "prev_portfolio_carry_fee": 0.9999499313233661,
        "prev_portfolio_ret": 0.9998945621897779,
        "prev_portfolio_spread_fee": 1.0,
        "spread_fee_loss": 0.0,
    },
    {
        "accum_ms": 43200000,
        "carry_fee_loss": 0.0,
        "gain": 0.03899483131406683,
        "last_update_ms": 1743638400000,
        "loss": -0.04567012645998837,
        "mdd": 0.9854739027230959,
        "mpv": 1.006679034567331,
        "n_updates": 497,
        "open_ms": 21534701,
        "prev_portfolio_carry_fee": 0.9999499313233661,
        "prev_portfolio_ret": 0.9932421988189996,
        "prev_portfolio_spread_fee": 1.0,
        "spread_fee_loss": 0.0,
    },
]

cps1 = [
    {
        "accum_ms": 43200000,
        "carry_fee_loss": -2.3300345913780215e-05,
        "gain": 0.07227838363091864,
        "last_update_ms": 1744027200000,
        "loss": -0.07616114104996953,
        "mdd": 0.9767722306917356,
        "mpv": 0.9967652143078651,
        "n_updates": 704,
        "open_ms": 40883646,
        "prev_portfolio_carry_fee": 0.9999266324155072,
        "prev_portfolio_ret": 0.989393157584942,
        "prev_portfolio_spread_fee": 1.0,
        "spread_fee_loss": 0.0,
    },
    {
        "accum_ms": 43200000,
        "carry_fee_loss": -0.0002135004588671789,
        "gain": 0.1465514005245302,
        "last_update_ms": 1744070400000,
        "loss": -0.13022543595769845,
        "mdd": 0.9803805748134627,
        "mpv": 1.0089628479133728,
        "n_updates": 779,
        "open_ms": 43200000,
        "prev_portfolio_carry_fee": 0.999713170408582,
        "prev_portfolio_ret": 1.0056785307108806,
        "prev_portfolio_spread_fee": 1.0,
        "spread_fee_loss": 0.0,
    },
    {
        "accum_ms": 43200000,
        "carry_fee_loss": 0.0,
        "gain": 0.24898575060890746,
        "last_update_ms": 1744113600000,
        "loss": -0.2636574901932099,
        "mdd": 0.9742257636009942,
        "mpv": 1.0056785307108806,
        "n_updates": 1236,
        "open_ms": 43200000,
        "prev_portfolio_carry_fee": 0.999713170408582,
        "prev_portfolio_ret": 0.991031190928065,
        "prev_portfolio_spread_fee": 1.0,
        "spread_fee_loss": 0.0,
    },
    {
        "accum_ms": 43200000,
        "carry_fee_loss": -0.0012517482527969286,
        "gain": 0.2990499804399198,
        "last_update_ms": 1744156800000,
        "loss": -0.3654046746381711,
        "mdd": 0.9116240144599299,
        "mpv": 1.0039007535371414,
        "n_updates": 773,
        "open_ms": 43200000,
        "prev_portfolio_carry_fee": 0.9984625640796637,
        "prev_portfolio_ret": 0.927405881473434,
        "prev_portfolio_spread_fee": 1.0,
        "spread_fee_loss": 0.0,
    },
]


def convert_trade_to_perf_checkpoint(trade: Dict[str, Any]) -> PerfCheckpoint:
    # Parse entry/exit datetime strings
    entry_dt = datetime.strptime(trade["entryOn"], "%m/%d/%Y %I:%M %p")
    exit_dt = datetime.strptime(trade["exitOn"], "%m/%d/%Y %I:%M %p")

    # Calculate values
    delta_value = trade["result"] / trade["accountValue"] * 100
    gain = delta_value if delta_value > 0 else 0.0
    loss = delta_value if delta_value < 0 else 0.0

    open_ms = (entry_dt.hour * 3600 + entry_dt.minute * 60 + entry_dt.second) * 1000
    accum_ms = int((exit_dt - entry_dt).total_seconds() * 1000)
    last_update_ms = int(exit_dt.timestamp() * 1000)

    return PerfCheckpoint(
        last_update_ms=last_update_ms,
        prev_portfolio_ret=1.0,  # default, you can adjust if needed
        accum_ms=accum_ms,
        open_ms=open_ms,
        gain=gain,
        loss=loss,
        mpv=1.0 + (gain + loss) / trade["accountValue"],  # example calc
    )


def group_trades_by_symbol(trades: List[Dict[str, Any]]) -> Dict[str, PerfLedger]:
    result = defaultdict(list)
    
    for trade in trades:
        symbol = trade["symbol"]
        checkpoint = convert_trade_to_perf_checkpoint(trade)
        result[symbol].append(checkpoint)
    
    ledgers: Dict[str, PerfLedger] = {}
    for symbol, cps in result.items():
        # Use the last update time of the first checkpoint as initialization time (optional logic)
        init_time = cps[0].last_update_ms if cps else 0
        ledgers[symbol] = PerfLedger(initialization_time_ms=init_time, cps=cps)

    return ledgers


ledger_dict = group_trades_by_symbol(
    [
    {
      "trade": 0,
      "symbol": "QCOM (Index_NASDAQ 100)",
      "entryOn": "1/6/2010 4:00 PM",
      "exitOn": "1/7/2010 4:00 PM",
      "entryValue": 32.82,
      "exitValue": 32.48,
      "accountValue": 100000,
      "positionSize": 304,
      "positionExposure": "9.977%",
      "result": -103.36
    },
    {
      "trade": 1,
      "symbol": "EXPE (Index_NASDAQ 100)",
      "entryOn": "1/6/2010 4:00 PM",
      "exitOn": "1/7/2010 4:00 PM",
      "entryValue": 23.15,
      "exitValue": 22.3,
      "accountValue": 99863.2,
      "positionSize": 431,
      "positionExposure": "9.991%",
      "result": -366.35
    },
    {
      "trade": 2,
      "symbol": "MSFT (Index_NASDAQ 100)",
      "entryOn": "1/6/2010 4:00 PM",
      "exitOn": "1/7/2010 4:00 PM",
      "entryValue": 23.2,
      "exitValue": 23.01,
      "accountValue": 99427.89,
      "positionSize": 428,
      "positionExposure": "9.987%",
      "result": -81.32
    },
    {
      "trade": 3,
      "symbol": "QGEN (Index_NASDAQ 100)",
      "entryOn": "1/6/2010 4:00 PM",
      "exitOn": "1/7/2010 4:00 PM",
      "entryValue": 23.44,
      "exitValue": 23.39,
      "accountValue": 99393.65,
      "positionSize": 424,
      "positionExposure": "9.999%",
      "result": -21.20
    }
  ]
)


def main():
    # Dummy data for positions
    positions = {
        "miner1": [
            Position(
                trade_pair=TradePair.BTCUSD,
                miner_hotkey="miner1",
                position_uuid="uid1",
                open_ms=123,
                return_at_close=1.05,
            )
        ],
        # "miner2": [Position(trade_pair=TradePair.BTCUSD, miner_hotkey='miner2', position_uuid='uid2', open_ms=233, return_at_close=0.95)],
        # "miner3": [Position(trade_pair=TradePair.BTCUSD, miner_hotkey='miner3', position_uuid='uid3', open_ms=456, return_at_close=1.10)]
    }

    # Call the score_miners method
    evaluation_time_ms = None  # or set to a specific timestamp
    weighting = False  # or True if weighting is needed

    scores = Scoring.score_miners(ledger_dict, positions, evaluation_time_ms, weighting)

    # Print the scores
    print(scores)


if __name__ == "__main__":
    main()
