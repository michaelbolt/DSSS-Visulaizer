import numpy as np
import matplotlib.pyplot as plt


class User :
	"""
	A user on the small-scale DSSS network.
	"""
	modulation = 'BPSK'
	symbolPeriod = 2
	symbolSamples = 300

	def __init__(self, code='', msg = ''):
		#initialize code and message
		self._code = code
		self._codeLength = len(code)
		self._msg = msg
		self._msgLength = len(msg)
		self.calculatePacket()

	def setCode(self, code):
		"""
		Change the DSSS code for this User and recalculate packet
		"""
		self._code = code
		self._codeFlip = ''
		for c in code:
			if c is '1':
				self._codeFlip += '0'
			else:
				self._codeFlip += '1'
		self._codeLength = len(code)
		self.calculatePacket()

	def setMsg(self, msg):
		"""
		Change the message for this User to transmit and recalculate packet
		"""
		self._msg = msg
		self._msgLength = len(msg)
		self.calculatePacket()

	def calculatePacket(self):
		"""
		Recalculate the packet to be transmitted.
		"""
		packet = ''
		for m in self._msg:
			#each message bit must be multiplied by each code bit
			if m is '1':
				packet += self._code
			else:
				packet += self._codeFlip
		self._packetLength = len(packet)
		self._packet = packet

	def calculateTransmission(self):
		"""
		Calculate the the waveform to be transmitted.
		"""
		# precalculate constants for efficiency
		numSamples = self._msgLength * self.symbolSamples
		bpskConstant = 2 * np.pi / self.symbolSamples * self._codeLength * 1.0
		packetIndexConstant = self._codeLength / self.symbolSamples
		# calcualte waveform to be transmitted
		self.txTime = np.linspace(0, self._msgLength * self.symbolPeriod, numSamples)	
		self.txSamples = np.zeros(numSamples)	
		for t in range(numSamples):
			if self._packet[ int(t * packetIndexConstant) ] is '1':
				self.txSamples[t] = 1 * np.cos(bpskConstant * t + np.pi)
			else:
				self.txSamples[t] = 1 * np.cos(bpskConstant * t + 0)
		
		# array of message bits to be plotted
		self.msgTime = np.linspace(0, self._msgLength*self.symbolPeriod, self._msgLength+1)
		self.msgSamples = np.zeros(self._msgLength+1)
		for t in range(self._msgLength):
			if self._msg[t] is '1':
				self.msgSamples[t] = 1.2
			else:
				self.msgSamples[t] = -1.2
		# first sample must be duplicated for step plotting
		self.msgSamples[1:] = self.msgSamples[0:-1]

		# array of packet bits to be plotted
		self.packetTime = np.linspace(0, self._msgLength*self.symbolPeriod, self._packetLength+1)
		self.packetSamples = np.zeros(self._packetLength+1)
		for t in range(self._packetLength):
			if self._packet[t] is '1':
				self.packetSamples[t] = 0.25
			else:
				self.packetSamples[t] = -0.25
		# first sample must be duplicated for step plotting
		self.packetSamples[1:] = self.packetSamples[0:-1]

	def plotTransmission(self):
		plt.plot(self.txTime, self.txSamples, '--k', linewidth=1)
		plt.step(self.msgTime, self.msgSamples, 'b')
		plt.step(self.packetTime, self.packetSamples, 'r')
		plt.show()


	def printMessage(self):
		"""
		Print currently stored User message.
		"""
		print(self._msg)

	def printCode(self):
		"""
		Print currently stored User code.
		"""
		print(self._code)

	def printPacket(self):
		"""
		Print currently stored User packet.
		"""
		print(self._packet)









if __name__ == "__main__":
    user = User()
    user.setCode('1011')
    user.setMsg('101')
    user.calculateTransmission()
    user.plotTransmission()









