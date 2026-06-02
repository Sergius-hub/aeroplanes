from abc import ABC, abstractmethod

class BaseAPI(ABC):

	def __init__(self, url: str, headers: dict | None = None, params: dict | None = None):
		self.url = url
		self.headers = headers
		self.params = params


	@abstractmethod
	def get_response( self, *args, **kwargs ):
		pass