from datetime import datetime, timezone
import pandas as pd
import numpy as np

class Tweet:
    def __init__(self, path):
        self.path = path
        self._df = pd.DataFrame()

    def utc_to_local(self, utc_dt):
        return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz='US/Eastern')

    @property
    def df(self):
        if self._df.empty:
            self._df = pd.read_csv(self.path)
            self._df.date = pd.to_datetime(self._df.date.values, utc=True)
            self._df.date = self._df.date.apply(self.utc_to_local)

        return self._df

    @property
    def rem(self):
        df = self.df[self.df.line == 'REM_infoservice'].reset_index(drop=True)
        remove = 'the|with|issue|planifiée'    
        stop = 'interruption|arrêt de service'    
        slow = 'ralentissement de service|reprise'
        restart = 'rétabli|Service normal sur la ligne A1'
        return self.df_encoding(df, remove, stop, slow, restart)

    @property
    def stm(self):
        df = self.df[self.df.line != 'REM_infoservice'].reset_index(drop=True)
        remove = [
            'the',
            'with',
            'issue',
            'ongoing',
            'holiday',
            'between',
            'Normal métro service',
            'disruption',
            'Seuls les interruptions de service',
            'Planfication sensée',
            'smart',
            'limite temporairement la diffusion automatisée',
            'peuvent causer',
            '@.*',
            'stopping',
            'What',
            'We'
        ]
        stop = 'interruption|Arrêt ligne|Arrêt prolongé ligne'  
        slow = 'reprise|Perturbation du service'
        restart = [
            'rétabli',
            'fin de la perturbation',
            'Service normal du métro',
            '"interruption de service .* terminée"'
        ]
        
        return self.df_encoding(df, '|'.join(remove), stop, slow, '|'.join(restart))

    def df_encoding(self, df, remove, stop, slow, restart):
        df_ = df.copy()
        df_ = df_[~df_.tweet.str.contains(remove, case=False)].reset_index(drop=True)
        df_['stop'] = df_.tweet.str.contains(stop, case=False).astype(int)
        df_['slow'] = df_.tweet.str.contains(slow, case=False).astype(int)
        df_['restart'] = df_.tweet.str.contains(restart, case=False).astype(int)
        df_['duration'] = np.nan
        return df_      

if __name__ == '__main__':
    path = '../data/twitter_stm_rem.csv'
    t = Tweet(path)
    x = t.stm
    print(x)




