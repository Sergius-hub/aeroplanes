from abc import ABC, abstractmethod

class BaseAPI(ABC):

	def __init__(self, url: str, headers: dict, params: dict):
		self.url = url
		self.headers = headers
		self.params = params

	@abstractmethod
	def set_request( self, *args, **kwargs ):
		pass

	@abstractmethod
	def get_response( self, *args, **kwargs ):
		pass