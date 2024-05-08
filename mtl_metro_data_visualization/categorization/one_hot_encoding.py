from mtl_metro_data_visualization.categorization.tweets import Tweets

class OneHotEncoding(Tweets):
	def __init__(self):
		super().__init__()
		pass


	def stop_slow_restart(self):
		pass


if __name__ == '__main__':
    oh = OneHotEncoding()
    print(oh.df)