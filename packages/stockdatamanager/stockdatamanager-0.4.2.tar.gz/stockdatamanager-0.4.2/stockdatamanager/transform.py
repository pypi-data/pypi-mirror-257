"""
This module contains the Transform class which is designed to do multiple manipulation with financial data
"""
import pandas as pd
import numpy as np
import pandas_datareader.data as web
import Fetcher
class Transform:
    """
    A utility class for performing various technical analysis calculations on stock market data.
    
    This class supports operations such as calculating moving averages, exponential moving averages,
    Bollinger Bands, Relative Strength Index (RSI), Moving Average Convergence Divergence (MACD),
    and many other technical indicators. It can work with data either fetched directly using a ticker symbol
    or with an externally supplied pandas DataFrame.

    Attributes:
        ticker (str, optional): The ticker symbol of the stock to fetch data for. If specified, data
                                will be fetched using the Fetcher class.
        dataframe (pd.DataFrame, optional): An externally supplied pandas DataFrame containing stock
                                            market data. Expected to have columns like 'Close', 'High',
                                            'Low', and 'Volume'.
        df (pd.DataFrame): The primary DataFrame used for calculations, derived either from the fetched
                           data using the ticker symbol or directly supplied as an argument.
        yf_stock (yf.Ticker, optional): The yfinance Ticker object for the specified ticker symbol,
                                        available if a ticker symbol was provided.

    Methods:
        This class provides a variety of methods for technical analysis calculations, including:
        - exponential_weights: Applies exponential weights to the 'Close' column.
        - adjust_inflation: Adjusts the 'Close' column for inflation using CPI data.
        - calculate_returns: Calculates the simple returns of the 'Close' column.
        - calculate_RSI: Calculates the Relative Strength Index.
        - calculate_MACD: Calculates the Moving Average Convergence Divergence.
        - calculate_bollinger_bands: Calculates Bollinger Bands.
        - calculate_EMA: Calculates the Exponential Moving Average.
        - calculate_SMA: Calculates the Simple Moving Average.
        - calculate_KAMA: Calculates Kaufman's Adaptive Moving Average.
        - calculate_on_balance_volume: Calculates On-Balance Volume.
        - calculate_ATR: Calculates the Average True Range.
        - calculate_ADI: Calculates the Accumulation/Distribution Index.
        - (and many more methods for various technical indicators...)

    Usage:
        To use this class, either provide a ticker symbol to fetch data or supply a pandas DataFrame directly.
        Once instantiated, call the desired method(s) to perform technical analysis calculations.

    Example:
        transform = Transform(ticker='AAPL')
        df_with_rsi = transform.calculate_RSI()
        df_with_macd = transform.calculate_MACD()

        # Or with an external DataFrame
        external_df = pd.DataFrame(...)  # Some DataFrame with market data
        transform = Transform(dataframe=external_df)
        df_with_bollinger = transform.calculate_bollinger_bands()
    """

    def __init__(self, 
                 ticker:str = None, 
                 dataframe:pd.DataFrame = None):
        if ticker:
            self.fetch = Fetcher(ticker)
            self.df, self.yf_stock = self.fetch.df, self.fetch.yf_stock
        elif dataframe:
            self.df = dataframe
    
    def exponential_weights(self, 
                            span:int, 
                            df:pd.DataFrame = None) -> pd.DataFrame:
        """Modifies the 'Close' column of the dataframe by applying exponential weights to it
        Inputs:
        - span: int: The span of the exponential weights
        - df: pd.DataFrame: The dataframe to be used - needs a 'Close' column - if None, the class dataframe is used
        """
        if df is None:
            df = self.df
        weights = np.exp(-np.log(2)*np.arange(len(df))/span)[::-1]
        weighted_close = df['Close'] * weights / weights.max()
        df['Close'] = weighted_close
        return df
    
    def adjust_inflation(self, 
                         df:pd.DataFrame = None) -> pd.DataFrame:
        """Adjusts the 'Close' column of the dataframe for inflation
        Inputs:
        - df: pd.DataFrame: The dataframe to be used - needs a 'Close' column - if None, the class dataframe is used
        """
        if df is None:
            df = self.df.copy()
        df.index = df.index.tz_localize(None)
        first_date = df.index.min()
        last_date = df.index.max()
        cpi_series_id = 'CPIAUCSL'
        cpi_data = web.DataReader(cpi_series_id, 'fred', first_date, last_date)
        cpi_data.rename(columns = {'CPIAUCSL':'CPI'}, inplace = True)
        base_cpi = cpi_data['CPI'].iloc[-1] 
        cpi_all_data = cpi_data.reindex(df.index, method = 'ffill')
        cpi_all_data = cpi_all_data.fillna(method = 'bfill')
        refactor = base_cpi / cpi_all_data['CPI']
        df['Refactored'] = df['Close'] * refactor
        return df

    def calculate_returns(self, 
                          df:pd.DataFrame = None) -> pd.DataFrame:
        """Calculates the returns of the 'Close' column of the dataframe
        Inputs:
        - df: pd.DataFrame: The dataframe to be used - needs a 'Close' column - if None, the class dataframe is used
        """
        if df is None:
            df = self.df
        df['Return'] = df['Close'].pct_change()
        return df
    
    def calculate_RSI(self, 
                      df:pd.DataFrame = None, 
                      period:int = 14) -> pd.DataFrame:
        """Calculates the Relative Strength Index of the 'Close' column of the dataframe
        Inputs:
        - df: pd.DataFrame: The dataframe to be used - needs a 'Close' column - if None, the class dataframe is used
        - period: int: The period to be used for the RSI calculation - default is 14"""
        if df is None:
            df = self.df
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
        RS = gain / loss
        RSI = 100 - (100 / (1 + RS))
        df['RSI'] = RSI
        return df
    
    def calculate_MACD(self, 
                       df:pd.DataFrame = None, 
                       short_window:int = 12, 
                       long_window:int = 26) -> pd.DataFrame:
        """Calculates the Moving Average Convergence Divergence of the 'Close' column of the dataframe
        Inputs:
        - df: pd.DataFrame: The dataframe to be used - needs a 'Close' column - if None, the class dataframe is used
        - short_window: int: The period to be used for the short EMA - default is 12
        - long_window: int: The period to be used for the long EMA - default is 26
        """
        if df is None:
            df = self.df
        short_ema = df['Close'].ewm(span = short_window, adjust = False).mean()
        long_ema = df['Close'].ewm(span = long_window, adjust = False).mean()
        df['MACD'] = short_ema - long_ema
        df['Signal'] = df['MACD'].ewm(span = 9, adjust = False).mean()
        return df
    
    def calculate_bollinger_bands(self, 
                                  df:pd.DataFrame = None, 
                                  window:int = 20) -> pd.DataFrame:
        """Calculates the Bollinger Bands of the 'Close' column of the dataframe
        Inputs:
        - df: pd.DataFrame: The dataframe to be used - needs a 'Close' column - if None, the class dataframe is used
        - window: int: The period to be used for the Bollinger Bands calculation - default is 20"""
        if df is None:
            df = self.df
        rolling_mean = df['Close'].rolling(window).mean()
        rolling_std = df['Close'].rolling(window).std()
        df['Upper'] = rolling_mean + (rolling_std * 2)
        df['Lower'] = rolling_mean - (rolling_std * 2)
        return df

    def calculate_EMA(self, 
                      df:pd.DataFrame = None, 
                      window:int = 20) -> pd.DataFrame:
        """Calculates the Exponential Moving Average of the 'Close' column of the dataframe
        Inputs:
        - df: pd.DataFrame: The dataframe to be used - needs a 'Close' column - if None, the class dataframe is used
        - window: int: The period to be used for the EMA calculation - default is 20"""
        if df is None:
            df = self.df
        df['EMA'] = df['Close'].ewm(span = window, adjust = False).mean()
        return df
    
    def calculate_SMA(self, 
                      df:pd.DataFrame = None, 
                      window:int = 20) -> pd.DataFrame:
        """Calculates the Simple Moving Average of the 'Close' column of the dataframe
        Inputs:
        - df: pd.DataFrame: The dataframe to be used - needs a 'Close' column - if None, the class dataframe is used
        - window: int: The period to be used for the SMA calculation - default is 20"""
        if df is None:
            df = self.df
        df['SMA'] = df['Close'].rolling(window).mean()
        return df
    
    def calculate_KAMA(self, 
                       df:pd.DataFrame = None, 
                       window:int = 20, 
                       fast:int=2, 
                       slow: int =30) -> pd.DataFrame:
        """Calculates the Kaufman's Adaptive Moving Average of the 'Close' column of the dataframe
        Inputs:
        - df: pd.DataFrame: The dataframe to be used - needs a 'Close' column - if None, the class dataframe is used
        - window: int: The period to be used for the KAMA calculation - default is 20
        - fast: int: The period to be used for the fast smoothing constant - default is 2
        - slow: int: The period to be used for the slow smoothing constant - default is 30"""
        if df is None:
            df = self.df
        change = df['Close'].diff(window).abs()
        volatility = df['Close'].diff().abs().rolling(window=window).sum()
        ER = change / volatility
        fastSC = 2 / (fast + 1)
        slowSC = 2 / (slow + 1)
        SC = (ER * (fastSC - slowSC) + slowSC) ** 2
        KAMA = pd.Series(index=df.index, data=np.NaN)
        KAMA.iloc[window] = df['Close'].iloc[window]
        for i in range(window + 1, len(df)):
            KAMA.iloc[i] = KAMA.iloc[i - 1] + SC.iloc[i] * (df['Close'].iloc[i] - KAMA.iloc[i - 1])
        df['KAMA'] = KAMA
        return df
    
    def calculate_on_balance_volume(self, 
                                    df:pd.DataFrame = None) -> pd.DataFrame:
        """Calculates the On Balance Volume of the 'Close' column of the dataframe
        Inputs:
        - df: pd.DataFrame: The dataframe to be used - needs a 'Close' and 'Volume' column - if None, the class dataframe is used"""
        if df is None:
            df = self.df
        df['OBV'] = np.where(df['Close'] > df['Close'].shift(1), df['Volume'], np.where(df['Close'] < df['Close'].shift(1), -df['Volume'], 0)).cumsum()
        return df

    def calculate_ATR(self, 
                      df:pd.DataFrame = None, 
                      window:int = 14) -> pd.DataFrame:
        """Calculates the Average True Range of the 'Close' column of the dataframe
        Inputs:
        - df: pd.DataFrame: The dataframe to be used - needs a 'Close', 'High' and 'Low' column - if None, the class dataframe is used
        - window: int: The period to be used for the ATR calculation - default is 14"""
        if df is None:
            df = self.df
        df['H-L'] = abs(df['High'] - df['Low'])
        df['H-PC'] = abs(df['High'] - df['Close'].shift(1))
        df['L-PC'] = abs(df['Low'] - df['Close'].shift(1))
        df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis = 1, skipna = False)
        df['ATR'] = df['TR'].rolling(window).mean()
        return df
    
    def calculate_ADI(self, 
                      df: pd.DataFrame = None) -> pd.DataFrame:
        """Calculates the Accumulation/Distribution Index of the 'Close' column of the dataframe
        Inputs:
        - df: pd.DataFrame: The dataframe to be used - needs a 'Close', 'High', 'Low' and 'Volume' column - if None, the class dataframe is used"""
        if df is None:
            df = self.df
        clv = ((df['Close'] - df['Low']) - (df['High'] - df['Close'])) 
        range_span = (df['High'] - df['Low'])
        df['MFM'] = np.where(range_span == 0, 0, clv / range_span)  
        df['MFMV'] = df['MFM'] * df['Volume']
        df['ADI'] = df['MFMV'].cumsum()
        
        return df


    def calculate_parabolic_sar(self, 
                                df, 
                                acceleration: float =0.02, 
                                maximum: float = 0.2) -> pd.DataFrame:
        """Calculates the Parabolic SAR of the 'Close' column of the dataframe
        Inputs:
        - df: pd.DataFrame: The dataframe to be used - needs a 'Close', 'High' and 'Low' column - if None, the class dataframe is used
        - acceleration: float: The acceleration factor to be used for the Parabolic SAR calculation - default is 0.02
        - maximum: float: The maximum acceleration factor to be used for the Parabolic SAR calculation - default is 0.2"""
        if df is None:
            df = self.df
        df['SAR'] = 0.0
        df['EP'] = 0.0
        df['AF'] = acceleration
        rising_trend = df['Close'].iloc[1] > df['Close'].iloc[0]
        if rising_trend:
            df['SAR'].iloc[0] = df['Low'].iloc[0]
            df['EP'].iloc[0] = df['High'].iloc[0]
        else:
            df['SAR'].iloc[0] = df['High'].iloc[0]
            df['EP'].iloc[0] = df['Low'].iloc[0]

        for i in range(1, len(df)):
            if (rising_trend and df['High'].iloc[i] > df['EP'].iloc[i-1]) or (not rising_trend and df['Low'].iloc[i] < df['EP'].iloc[i-1]):
                df['AF'].iloc[i] = min(df['AF'].iloc[i-1] + acceleration, maximum)
            else:
                df['AF'].iloc[i] = df['AF'].iloc[i-1]

            df['SAR'].iloc[i] = df['SAR'].iloc[i-1] + df['AF'].iloc[i-1] * (df['EP'].iloc[i-1] - df['SAR'].iloc[i-1])

            if rising_trend:
                if df['Low'].iloc[i] < df['SAR'].iloc[i]:
                    rising_trend = False
                    df['SAR'].iloc[i] = df['EP'].iloc[i-1]
                    df['EP'].iloc[i] = df['Low'].iloc[i]
                    df['AF'].iloc[i] = acceleration
                else:
                    if df['High'].iloc[i] > df['EP'].iloc[i-1]:
                        df['EP'].iloc[i] = df['High'].iloc[i]
            else:
                if df['High'].iloc[i] > df['SAR'].iloc[i]:
                    rising_trend = True
                    df['SAR'].iloc[i] = df['EP'].iloc[i-1]
                    df['EP'].iloc[i] = df['High'].iloc[i]
                    df['AF'].iloc[i] = acceleration
                else:
                    if df['Low'].iloc[i] < df['EP'].iloc[i-1]:
                        df['EP'].iloc[i] = df['Low'].iloc[i]

            if rising_trend:
                df['SAR'].iloc[i] = min(df['SAR'].iloc[i], df['Low'].iloc[i-1], df['Low'].iloc[i-2] if i >= 2 else df['SAR'].iloc[i])
            else:
                df['SAR'].iloc[i] = max(df['SAR'].iloc[i], df['High'].iloc[i-1], df['High'].iloc[i-2] if i >= 2 else df['SAR'].iloc[i])

        return df
    
    def calculate_stochastic_oscillator(self, 
                                        df:pd.DataFrame = None, 
                                        window:int = 14) -> pd.DataFrame:
        """Calculates the Stochastic Oscillator of the 'Close' column of the dataframe
        Inputs:
        - df: pd.DataFrame: The dataframe to be used - needs a 'Close', 'High' and 'Low' column - if None, the class dataframe is used
        - window: int: The period to be used for the Stochastic Oscillator calculation - default is 14"""
        if df is None:
            df = self.df
        low_str = 'L'+str(window)
        high_str = 'H'+str(window)
        df[low_str] = df['Low'].rolling(window).min()
        df[high_str] = df['High'].rolling(window).max()
        df['%K'] = 100 * ((df['Close'] - df[low_str]) / (df[high_str] - df[low_str]))
        df['%D'] = df['%K'].rolling(window).mean()
        return df
    
    def calculate_momentum(self, 
                           df:pd.DataFrame = None, 
                           window:int = 10) -> pd.DataFrame:
        """Calculates the Momentum of the 'Close' column of the dataframe
        Inputs:
        - df: pd.DataFrame: The dataframe to be used - needs a 'Close' column - if None, the class dataframe is used
        - window: int: The period to be used for the Momentum calculation - default is 10
        """
        if df is None:
            df = self.df
        df['Momentum'] = df['Close'] - df['Close'].shift(window)
        return df
    
    def calculate_williams_R(self, 
                             df:pd.DataFrame = None, 
                             window:int = 14) -> pd.DataFrame:
        """Calculates the Williams %R of the 'Close' column of the dataframe
        Inputs:
        - df: pd.DataFrame: The dataframe to be used - needs a 'Close', 'High' and 'Low' column - if None, the class dataframe is used
        - window: int: The period to be used for the Williams %R calculation - default is 14"""
        if df is None:
            df = self.df
        df['H'+ str(window)] = df['High'].rolling(window).max()
        df['L' + str(window)] = df['Low'].rolling(window).min()
        df['Williams %R'] = -100 * ((df['H'+ str(window)] - df['Close']) / (df['H'+ str(window)] - df['L' + str(window)]))
        return df
    
    def calculate_fibonacci_retracement(self,
                                        df:pd.DataFrame = None, 
                                        start_and_end_idxs:tuple=None, 
                                        fib_1: float = 0.236, 
                                        fib_2: float = 0.382, 
                                        fib_3: float = 0.618, 
                                        fib_4: float = 0.786) -> pd.DataFrame:
        """Calculates the Fibonacci Retracement of the 'Close' column of the dataframe
        Inputs:
        - df: pd.DataFrame: The dataframe to be used - needs a 'Close', 'High' and 'Low' column - if None, the class dataframe is used
        - start_and_end_idxs: tuple: The start and end indexes to be used for the calculation - if None, the whole dataframe is used
        - fib_1: float: The first fibonacci level - default is 0.236
        - fib_2: float: The second fibonacci level - default is 0.382
        - fib_3: float: The third fibonacci level - default is 0.618
        - fib_4: float: The fourth fibonacci level - default is 0.786"""
        if df is None:
            df = self.df
        if start_and_end_idxs is None:
            period_high = df['High'].max()
            period_low = df['Low'].min()
        else:
            start_index, end_index = start_and_end_idxs
            period_high = df['High'][start_index:end_index].max()
            period_low = df['Low'][start_index:end_index].min()
        diff = period_high - period_low

        df['Fib_' + str(fib_1 * 100) + '%'] = period_high - diff * fib_1
        df['Fib_' + str(fib_2 * 100) + '%'] = period_high - diff * fib_2
        df['Fib_' + str(fib_3 * 100) + '%'] = period_high - diff * fib_3
        df['Fib_' + str(fib_4 * 100) + '%'] = period_high - diff * fib_4

        return df
    
    def calculate_aroon_oscillator(self, 
                                   df:pd.DataFrame = None, 
                                   window:int = 25) -> pd.DataFrame:
        """Calculates the Aroon Oscillator of the 'Close' column of the dataframe
        Inputs:
        - df: pd.DataFrame: The dataframe to be used - needs a 'Close', 'High' and 'Low' column - if None, the class dataframe is used
        - window: int: The period to be used for the Aroon Oscillator calculation - default is 25"""
        if df is None:
            df = self.df
        df['Up'] = df['High'].rolling(window).apply(lambda x: x.argmax(), raw = True) / window * 100
        df['Down'] = df['Low'].rolling(window).apply(lambda x: x.argmin(), raw = True) / window * 100
        df['Aroon Oscillator'] = df['Up'] - df['Down']
        return df
    
    def calculate_ADX(self, 
                      df:pd.DataFrame = None, 
                      window:int = 14) -> pd.DataFrame:
        """Calculates the Average Directional Index of the 'Close' column of the dataframe
        Inputs:
        - df: pd.DataFrame: The dataframe to be used - needs a 'Close', 'High' and 'Low' column - if None, the class dataframe is used
        - window: int: The period to be used for the ADX calculation - default is 14"""
        if df is None:
            df = self.df
        df['TR'] = np.max([
            df['High'] - df['Low'], 
            abs(df['High'] - df['Close'].shift(1)), 
            abs(df['Low'] - df['Close'].shift(1))
        ], axis=0)
        df['+DM'] = np.where((df['High'] - df['High'].shift(1)) > (df['Low'].shift(1) - df['Low']), df['High'] - df['High'].shift(1), 0)
        df['+DM'] = df['+DM'].where(df['+DM'] > 0, 0)
        df['-DM'] = np.where((df['Low'].shift(1) - df['Low']) > (df['High'] - df['High'].shift(1)), df['Low'].shift(1) - df['Low'], 0)
        df['-DM'] = df['-DM'].where(df['-DM'] > 0, 0)
        df['TR14'] = df['TR'].rolling(window=window).sum()
        df['+DM14'] = df['+DM'].rolling(window=window).sum()
        df['-DM14'] = df['-DM'].rolling(window=window).sum()
        df['+DI14'] = 100 * (df['+DM14'] / df['TR14'])
        df['-DI14'] = 100 * (df['-DM14'] / df['TR14'])
        df['DX'] = 100 * abs((df['+DI14'] - df['-DI14']) / (df['+DI14'] + df['-DI14']))
        df['ADX'] = df['DX'].rolling(window=window).mean()
        df.drop(['TR', '+DM', '-DM', 'TR14', '+DM14', '-DM14', '+DI14', '-DI14', 'DX'], axis=1, inplace=True)

        return df

    def calculate_VWAP(self, 
                       df:pd.DataFrame = None) -> pd.DataFrame:
        """Calculates the Volume Weighted Average Price of the 'Close' column of the dataframe
        Inputs:
        - df: pd.DataFrame: The dataframe to be used - needs a 'Close', 'High', 'Low' and 'Volume' column - if None, the class dataframe is used
        """
        if df is None:
            df = self.df
        df['TP'] = (df['High'] + df['Low'] + df['Close']) / 3
        df['Traded'] = df['TP'] * df['Volume']
        df['Cumulative Traded'] = df['Traded'].cumsum()
        df['Cumulative Volume'] = df['Volume'].cumsum()
        df['VWAP'] = df['Cumulative Traded'] / df['Cumulative Volume']
        return df        
    
    def calculate_standard_pivot_points(self, 
                                        df:pd.DataFrame = None) -> pd.DataFrame:
        """Calculates the Standard Pivot Points of the 'Close' column of the dataframe
        Inputs:
        - df: pd.DataFrame: The dataframe to be used - needs 'High', 'Low' and 'Close' columns - if None, the class dataframe is used"""
        if df is None:
            df = self.df
        df['Pivot'] = (df['High'] + df['Low'] + df['Close']) / 3
        df['R1'] = 2 * df['Pivot'] - df['Low']
        df['S1'] = 2 * df['Pivot'] - df['High']
        df['R2'] = df['Pivot'] + df['High'] - df['Low']
        df['S2'] = df['Pivot'] - df['High'] + df['Low']
        df['R3'] = df['Pivot'] + 2 * (df['High'] - df['Low'])
        df['S3'] = df['Pivot'] - 2 * (df['High'] - df['Low'])
        return df
    
    def calculate_fibonacci_pivot_points(self, 
                                         df:pd.DataFrame = None, 
                                         fib1:float = 0.382, 
                                         fib2:float = 0.618, 
                                         fib3: float = 1.382) -> pd.DataFrame:
        """Calculates the Fibonacci Pivot Points of the 'Close' column of the dataframe
        Inputs:
        - df: pd.DataFrame: The dataframe to be used - needs to have 'High', 'Low' and 'Close' columns - if None, the class dataframe is used
        - fib1: float: The first fibonacci level - default is 0.382
        - fib2: float: The second fibonacci level - default is 0.618
        - fib3: float: The third fibonacci level - default is 1.382
        """
        if df is None:
            df = self.df
        df['Pivot'] = (df['High'] + df['Low'] + df['Close']) / 3
        df['R1'] = df['Pivot'] + fib1 * (df['High'] - df['Low'])
        df['S1'] = df['Pivot'] - fib1 * (df['High'] - df['Low'])
        df['R2'] = df['Pivot'] + fib2 * (df['High'] - df['Low'])
        df['S2'] = df['Pivot'] - fib2 * (df['High'] - df['Low'])
        df['R3'] = df['Pivot'] + fib3 * (df['High'] - df['Low'])
        df['S3'] = df['Pivot'] - fib3 * (df['High'] - df['Low'])
        return df
    
    def calculate_woodie_pivot_points(self, 
                                      df:pd.DataFrame = None) -> pd.DataFrame:
        """Calculates the Woodie Pivot Points of the 'Close' column of the dataframe
        Inputs:
        - df: pd.DataFrame: The dataframe to be used - needs to have 'High', 'Low' and 'Close' columns - if None, the class dataframe is used
        """
        if df is None:
            df = self.df
        df['Pivot'] = (2 * df['Close'] + df['High'] + df['Low']) / 4        
        df['R1'] = 2 * df['Pivot'] - df['Low']
        df['R2'] = df['Pivot'] + (df['High'] - df['Low'])  
        df['R3'] = df['R1'] + (df['High'] - df['Low']) 
        df['S1'] = 2 * df['Pivot'] - df['High']
        df['S2'] = df['Pivot'] - (df['High'] - df['Low'])  
        df['S3'] = df['S1'] - (df['High'] - df['Low'])  
        return df
    
    def calculate_ichimoku_cloud(self, 
                                 df:pd.DataFrame = None, 
                                 conversion_line_window:int = 9, 
                                 base_line_window:int = 26, 
                                 lagging_span_window:int = 52, 
                                 displacement:int = 26) -> pd.DataFrame:
        """Calculates the Ichimoku Cloud of the 'Close' column of the dataframe
        Inputs:
        - df: pd.DataFrame: The dataframe to be used - needs to have 'High', 'Low' and 'Close' columns - if None, the class dataframe is used
        - conversion_line_window: int: The period to be used for the conversion line calculation - default is 9
        - base_line_window: int: The period to be used for the base line calculation - default is 26
        - lagging_span_window: int: The period to be used for the lagging span calculation - default is 52
        - displacement: int: The displacement to be used for the lagging span calculation - default is 26
        """
        if df is None:
            df = self.df
        period_high = df['High'].rolling(conversion_line_window).max()
        period_low = df['Low'].rolling(conversion_line_window).min()
        df['Tenkan-sen'] = (period_high + period_low) / 2
        period_high = df['High'].rolling(base_line_window).max()
        period_low = df['Low'].rolling(base_line_window).min()
        df['Kijun-sen'] = (period_high + period_low) / 2
        df['Senkou Span A'] = ((df['Tenkan-sen'] + df['Kijun-sen']) / 2).shift(displacement)
        period_high = df['High'].rolling(lagging_span_window).max()
        period_low = df['Low'].rolling(lagging_span_window).min()
        df['Senkou Span B'] = ((period_high + period_low) / 2).shift(displacement)
        df['Chikou Span'] = df['Close'].shift(-displacement)
        return df
    
    def calculate_chaikin_money_flow(self, 
                                     df:pd.DataFrame = None, 
                                     window:int = 20) -> pd.DataFrame:
        """Calculates the Chaikin Money Flow of the 'Close' column of the dataframe
        Inputs:
        - df: pd.DataFrame: The dataframe to be used - needs to have 'High', 'Low', 'Close' and 'Volume' columns - if None, the class dataframe is used
        - window: int: The period to be used for the Chaikin Money Flow calculation - default is 20
        """
        if df is None:
            df = self.df
        df['MF Multiplier'] = (2 * df['Close'] - df['Low'] - df['High']) / (df['High'] - df['Low'])
        df['MF Volume'] = df['MF Multiplier'] * df['Volume']
        df['CMF'] = df['MF Volume'].rolling(window).sum() / df['Volume'].rolling(window).sum()
        return df
    
    def calculate_force_index(self, 
                              df:pd.DataFrame = None) -> pd.DataFrame:
        """Calculates the Force Index of the 'Close' column of the dataframe
        Inputs:
        - df: pd.DataFrame: The dataframe to be used - needs to have 'Close' and 'Volume' columns - if None, the class dataframe is used
        """
        if df is None:
            df = self.df
        df['Force Index'] = df['Close'].diff(1) * df['Volume']
        return df
    
    def calculate_zigzag(self, 
                         df:pd.DataFrame = None, 
                         threshold:float = 0.1) -> pd.DataFrame:
        """Calculates the ZigZag of the 'Close' column of the dataframe
        Inputs:
        - df: pd.DataFrame: The dataframe to be used - needs to have 'Close', 'High' and 'Low' column - if None, the class dataframe is used
        - threshold: float: The threshold to be used for the ZigZag calculation - default is 0.1
        """
        if df is None:
            df = self.df
        df['ZigZag'] = None
        last_pivot_price = df.iloc[0]['Close']
        df.loc[0, 'ZigZag'] = last_pivot_price
        last_pivot_index = 0
        trend = None 
        for i in range(1, len(df)):
            high_change = (df.iloc[i]['High'] - last_pivot_price) / last_pivot_price
            low_change = (df.iloc[i]['Low'] - last_pivot_price) / last_pivot_price
            if trend is None or (trend and low_change <= -threshold) or (not trend and high_change >= threshold):
                if trend is None:
                    trend = high_change >= threshold
                elif trend and low_change <= -threshold:
                    trend = False  
                elif not trend and high_change >= threshold:
                    trend = True  
                pivot_price = df.iloc[i]['High'] if trend else df.iloc[i]['Low']
                df.loc[last_pivot_index: i, 'ZigZag'] = [last_pivot_price] * (i - last_pivot_index)
                last_pivot_price = pivot_price
                last_pivot_index = i
        df.loc[last_pivot_index:, 'ZigZag'] = [last_pivot_price] * (len(df) - last_pivot_index)
        return df
    
    def calculate_stochastic_momentum_index(self, 
                                            df:pd.DataFrame = None, 
                                            n:int = 14, 
                                            m:int = 3, 
                                            x:int = 9) -> pd.DataFrame:
        """Calculates the Stochastic Momentum Index of the 'Close' column of the dataframe
        Inputs:
        - df: pd.DataFrame: The dataframe to be used - needs to have 'Close', 'High' and 'Low' columns - if None, the class dataframe is used
        - n: int: The period to be used for the first EMA calculation - default is 14
        - m: int: The period to be used for the second EMA calculation - default is 3
        - x: int: The period to be used for the Signal Line calculation - default is 9
        """
        if df is None:
            df = self.df
        midpoint = (df['High'] + df['Low']) / 2
        D = df['Close'] - midpoint
        D_SMA = D.rolling(window=n).mean()
        HL = df['High'] - df['Low']
        HL_SMA = HL.rolling(window=n).mean()
        D_SMA2 = D_SMA.rolling(window=m).mean()
        HL_SMA2 = HL_SMA.rolling(window=m).mean()
        df['SMI'] = (D_SMA2 / (HL_SMA2 / 2)) * 100
        df['SMI Signal Line'] = df['SMI'].rolling(window=x).mean()
        return df

    def calculate_keltner_channel(self, 
                                  df:pd.DataFrame = None, 
                                  window:int = 20, 
                                  atr_window:int = 10,
                                  multiplier:int = 1) -> pd.DataFrame:
        """Calculates the Keltner Channel of the 'Close' column of the dataframe
        Inputs:
        - df: pd.DataFrame: The dataframe to be used - needs to have 'Close', 'High' and 'Low' columns - if None, the class dataframe is used
        - window: int: The period to be used for the EMA calculation - default is 20
        - atr_window: int: The period to be used for the ATR calculation - default is 10
        - multiplier: int: The multiplier to be used for the Keltner Channel calculation - default is 1
        """
        if df is None:
            df = self.df
        df['TR'] = np.max([
            df['High'] - df['Low'], 
            abs(df['High'] - df['Close'].shift(1)), 
            abs(df['Low'] - df['Close'].shift(1))
        ], axis=0)
        df['ATR'] = df['TR'].rolling(window=atr_window).mean()
        df['Upper'] = df['EMA'] + (multiplier * df['ATR'])
        df['Lower'] = df['EMA'] - (multiplier * df['ATR'])
        return df
    
    def calculate_elder_force_index(self, 
                                    df:pd.DataFrame = None, 
                                    window:int = 13) -> pd.DataFrame:
        """Calculates the Elder Force Index of the 'Close' column of the dataframe
        Inputs:
        - df: pd.DataFrame: The dataframe to be used - needs to have 'Close' and 'Volume' columns - if None, the class dataframe is used
        - window: int: The period to be used for the Elder Force Index calculation - default is 13
        """

        if df is None:
            df = self.df
        df['Force Index'] = df['Close'].diff(window) * df['Volume']
        df['EMA'] = df['Force Index'].ewm(span=window, adjust=False).mean()
        return df
    
    def calculate_sd(self, 
                     df:pd.DataFrame = None, 
                     window:int = 20) -> pd.DataFrame:
        """Calculates the Standard Deviation of the 'Close' column of the dataframe
        Inputs:
        - df: pd.DataFrame: The dataframe to be used - needs to have 'Close' column - if None, the class dataframe is used
        - window: int: The period to be used for the Standard Deviation calculation - default is 20
        """
        if df is None:
            df = self.df
        df['SD'] = df['Close'].rolling(window).std()
        return df
    
    def calculate_detrended_price_oscillator(self, 
                                             df:pd.DataFrame = None, 
                                             window:int = 20) -> pd.DataFrame:
        """Calculates the Detrended Price Oscillator of the 'Close' column of the dataframe
        Inputs:
        - df: pd.DataFrame: The dataframe to be used - needs to have 'Close' column - if None, the class dataframe is used
        - window: int: The period to be used for the Detrended Price Oscillator calculation - default is 20
        """
        if df is None:
            df = self.df
        df['DPO'] = df['Close'] - df['Close'].rolling(window).mean().shift(int(window / 2) + 1)
        return df
    
    def calculate_commodity_channel_index(self, 
                                          df:pd.DataFrame = None, 
                                          window:int = 20) -> pd.DataFrame:
        """Calculates the Commodity Channel Index of the 'Close' column of the dataframe
        Inputs:
        - df: pd.DataFrame: The dataframe to be used - needs to have 'Close', 'High' and 'Low' columns - if None, the class dataframe is used
        - window: int: The period to be used for the Commodity Channel Index calculation - default is 20
        """

        if df is None:
            df = self.df
        TP = (df['High'] + df['Low'] + df['Close']) / 3
        df['CCI'] = (TP - TP.rolling(window).mean()) / (0.015 * TP.rolling(window).std())
        return df
    
    def calculate_CMO(self, 
                      df:pd.DataFrame = None, 
                      window:int = 9) -> pd.DataFrame:
        """Calculates the Chande Momentum Oscillator of the 'Close' column of the dataframe
        Inputs:
        - df: pd.DataFrame: The dataframe to be used - needs to have 'Close' column - if None, the class dataframe is used
        - window: int: The period to be used for the Chande Momentum Oscillator calculation - default is 9
        """

        if df is None:
            df = self.df
        up = df['Close'].diff().apply(lambda x: x if x > 0 else 0).rolling(window=window).sum()
        down = df['Close'].diff().apply(lambda x: -x if x < 0 else 0).rolling(window=window).sum()
        df['CMO'] = 100 * ((up - down) / (up + down))
        return df

    
    def calculate_market_facilitation_index(self, 
                                            df:pd.DataFrame = None) -> pd.DataFrame:
        """Calculates the Market Facilitation Index of the dataframe
        Inputs:
        - df: pd.DataFrame: The dataframe to be used - needs to have 'High' and 'Low' columns - if None, the class dataframe is used
        """

        if df is None:
            df = self.df
        df['MFI'] = (df['High'] - df['Low']) / df['Volume']
        return df

    def calculate_volume_oscillator(self, 
                                    df: pd.DataFrame, 
                                    short_window:int = 12, 
                                    long_window:int = 26) -> pd.DataFrame:
        """Calculates the Volume Oscillator of the 'Volume' column of the dataframe
        Inputs:
        - df: pd.DataFrame: The dataframe to be used - needs to have 'Volume' column - if None, the class dataframe is used
        - short_window: int: The period to be used for the short EMA calculation - default is 12
        - long_window: int: The period to be used for the long EMA calculation - default is 26
        """
        if df is None:
            df = self.df
        fast_vol_ema = df['Volume'].ewm(span=short_window, adjust=False).mean()
        slow_vol_ema = df['Volume'].ewm(span=long_window, adjust=False).mean()
        df['Volume Oscillator'] = ((fast_vol_ema - slow_vol_ema) / slow_vol_ema) * 100
        return df

    
    def calculate_trix(self, 
                       df:pd.DataFrame = None, 
                       window:int = 15) -> pd.DataFrame:
        """Calculates the TRIX of the 'Close' column of the dataframe
        Inputs:
        - df: pd.DataFrame: The dataframe to be used - needs to have 'Close' column - if None, the class dataframe is used
        - window: int: The period to be used for the TRIX calculation - default is 15
        """
        if df is None:
            df = self.df
        single_ema = df['Close'].ewm(span=window, adjust=False).mean()
        double_ema = single_ema.ewm(span=window, adjust=False).mean()
        triple_ema = double_ema.ewm(span=window, adjust=False).mean()
        df['TRIX'] = triple_ema.pct_change() * 100
        return df
    


    def calculate_know_sure_thing(self, 
                                  df:pd.DataFrame = None, 
                                  roc_short:int = 10, 
                                  roc_long: int = 15, 
                                  signal_period: int = 9) -> pd.DataFrame:
        """Calculates the Know Sure Thing of the 'Close' column of the dataframe
        Inputs:
        - df: pd.DataFrame: The dataframe to be used - needs to have 'Close' column - if None, the class dataframe is used
        - roc_short: int: The period to be used for the short Rate of Change calculation - default is 10
        - roc_long: int: The period to be used for the long Rate of Change calculation - default is 15
        - signal_period: int: The period to be used for the Signal Line calculation - default is 9
        """
        if df is None:
            df = self.df
        roc1 = df['Close'].diff(roc_short).rolling(roc_short).mean()
        roc2 = df['Close'].diff(roc_long).rolling(roc_long).mean()
        roc3 = df['Close'].diff(roc_long * 2).rolling(roc_long * 2).mean()
        roc4 = df['Close'].diff(roc_long * 3).rolling(roc_long * 3).mean()
        df['KST'] = roc1 + 2 * roc2 + 3 * roc3 + 4 * roc4
        df['KST Signal'] = df['KST'].rolling(signal_period).mean()
        return df
    
    def calculate_mass_index(self, 
                             df:pd.DataFrame = None, 
                             ema_period:int = 9,
                             sum_window:int = 25) -> pd.DataFrame:
        """Calculates the Mass Index of the dataframe
        Inputs:
        - df: pd.DataFrame: The dataframe to be used - needs to have 'High' and 'Low' columns - if None, the class dataframe is used
        - ema_period: int: The period to be used for the EMA calculation - default is 9
        - sum_window: int: The period to be used for the Sum calculation - default is 25
        """
        if df is None:
            df = self.df
        high_low_range = df['High'] - df['Low']
        single_ema = high_low_range.ewm(span=ema_period, adjust=False).mean()
        double_ema = single_ema.ewm(span=ema_period, adjust=False).mean()
        ema_ratio = single_ema / double_ema
        df['Mass Index'] = ema_ratio.rolling(window=sum_window).sum()
        return df

    def calculate_coppock_curve(self,
                                df:pd.DataFrame = None,
                                short_window:int = 11,
                                long_window:int = 14,
                                signal_period:int = 10) -> pd.DataFrame:
        """Calculates the Coppock Curve of the 'Close' column of the dataframe
        Inputs:
        - df: pd.DataFrame: The dataframe to be used - needs to have 'Close' column - if None, the class dataframe is used
        - short_window: int: The period to be used for the short Rate of Change calculation - default is 11
        - long_window: int: The period to be used for the long Rate of Change calculation - default is 14
        - signal_period: int: The period to be used for the Signal Line calculation - default is 10
        """
        
        def calculate_wma(df, period):
            weights = np.arange(1, period + 1)
            return df.rolling(window=period).apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True)

        if df is None:
            df = self.df
        roc1 = df['Close'].pct_change(short_window) * 100
        roc2 = df['Close'].pct_change(long_window) * 100
        roc_sum = roc1 + roc2
        df['Coppock Curve'] = calculate_wma(roc_sum, signal_period)
        return df
    
    def calculate_gann_angle_1x1(self,
                               df:pd.DataFrame = None,
                               projection_days:int = 30) -> pd.DataFrame:
        """Calculates the Gann 1x1 of the dataframe
        Inputs:
        - df: pd.DataFrame: The dataframe to be used - needs to have 'Close', 'High' and 'Low' column - if None, the class dataframe is used
        - projection_days: int: The number of days to be used for the projection - default is 30
        """
        def find_last_pivot(df, lookback=60):
            max_high = df['High'].iloc[-lookback:].idxmax()
            min_low = df['Low'].iloc[-lookback:].idxmin()
            if max_high > min_low:
                return 'high', max_high, df['High'].loc[max_high]
            else:
                return 'low', min_low, df['Low'].loc[min_low]
        if df is None:
            df = self.df
        pivot_type, pivot_index, pivot_value = find_last_pivot(df)
        df['Gann 1x1'] = np.nan  
        
        if pivot_type == 'high':
            df['Gann 1x1'].iloc[pivot_index:pivot_index+projection_days] = [pivot_value - i for i in range(projection_days)]
        elif pivot_type == 'low':
            df['Gann 1x1'].iloc[pivot_index:pivot_index+projection_days] = [pivot_value + i for i in range(projection_days)]    
        return df
        
    def calculate_capm(self, horizon: str = 'month') -> pd.DataFrame:
        """Calculates the Capital Asset Pricing Model of the stock using the risk free rate and the expected market return
        Inputs:
        - horizon: str: The horizon to be used for the calculation - default is 'month'
        """
        risk_free_rate = self.fetch.get_risk_free_rate(horizon).tail(1)['Close']
        expected_market_return = self.fetch.get_expected_market_return()['Close']
        if horizon == 'month':
            expected_market_return_val = expected_market_return.tail(13 * 7).mean()
        elif horizon == '5 year':
            expected_market_return_val = expected_market_return.tail(5 * 252).mean()
        elif horizon == '10 year':
            expected_market_return_val = expected_market_return.tail(10 * 252).mean()
        elif horizon == '30 year':
            expected_market_return_val = expected_market_return.tail(30 * 252).mean()
        beta = self.fetch.get_beta_value()
        capm = risk_free_rate + beta * (expected_market_return_val - risk_free_rate)
        return capm
