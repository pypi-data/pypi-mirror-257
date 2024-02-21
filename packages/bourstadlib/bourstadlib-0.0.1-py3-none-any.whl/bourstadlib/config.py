"""
Config module for BourstadLib
"""

from decouple import config  #type: ignore


def _get_keys_from_env() -> dict:
    dict =  {
        "FMP_API_KEY": config("FMP_API_KEY", None),
        "NASDAQ_API_KEY": config("NASDAQ_API_KEY", None),
        "ALPHA_VANTAGE_API_KEY": config("ALPHA_VANTAGE_API_KEY", None),
        }
    return {key: value for key, value in dict.items() if value is not None}



class Config:
    def __init__(self,
                 api_keys: dict|None = None,
                 ):
        if api_keys:
            self._keys: dict = api_keys
        else:
            self._keys:dict = _get_keys_from_env() #type: ignore[no-redef]
            
        self._apis = list(self._keys)