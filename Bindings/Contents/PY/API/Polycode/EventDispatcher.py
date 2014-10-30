
class EventDispatcher(object):

	def EventDispatcher(self):
		self.listenerEntries = {}

	def addEventListener(self, listener, callback, eventCode):
		if self.listenerEntries == None :
			self.listenerEntries = {}
		newEntry = {}
		if self.__ptr != None :
			newEntry.handler = Polycore.EventHandler(newEntry)
			Polycore.EventDispatcher_addEventListener(self.__ptr, newEntry.handler, eventCode)
		newEntry.listener = listener
		newEntry.callback = callback
		newEntry.eventCode = eventCode
		self.listenerEntries[self.listenerEntries+1] = newEntry

	def removeAllHandlers(self):
		if self.listenerEntries == None :
			self.listenerEntries = {}
		if self.__ptr != None :
			Polycore.EventDispatcher_removeAllHandlers(self.__ptr)
		self.listenerEntries = {}

	def removeAllHandlersForListener(self, listener):
		if self.listenerEntries == None :
			self.listenerEntries = {}
		i=1
		while i <= self.listenerEntries:
			if self.listenerEntries[i].listener == listener :
				if self.__ptr != None and self.listenerEntries[i].handler != None :
					Polycore.EventDispatcher_removeAllHandlersForListener(self.__ptr, self.listenerEntries[i].handler)
					Polycore.delete_EventHandler(self.listenerEntries[i].handler)
				table.remove(self.listenerEntries, i)
			else:
				i = i + 1

	def removeEventListener(self, listener, eventCode):
		if self.listenerEntries == None :
			self.listenerEntries = {}
		i=1
		while i <= self.listenerEntries:
			if self.listenerEntries[i].listener == listener and self.listenerEntries[i].eventCode == eventCode :
				if self.__ptr != None and self.listenerEntries[i].handler != None :
					Polycore.EventDispatcher_removeAllHandlersForListener(self.__ptr, self.listenerEntries[i].handler)
					Polycore.delete_EventHandler(self.listenerEntries[i].handler)
				table.remove(self.listenerEntries, i)
			else:
				i = i + 1

	def dispatchEvent(self, event, eventCode):
		if self.listenerEntries == None :
			self.listenerEntries = {}
		for i in self.listenerEntries.keys():
			if self.listenerEntries[i].eventCode == eventCode :
				self.listenerEntries[i].callback(self.listenerEntries[i].listener, event)
