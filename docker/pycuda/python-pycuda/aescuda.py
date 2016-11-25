import os, sys, unittest, binascii
import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule
import numpy
import array, time, math, numpy


class AES:

	sbox = (99,124,119,123,242,107,111,197,48,1,103,43,254,215,171,
			   118,202,130,201,125,250,89,71,240,173,212,162,175,156,164,114,192,183,253,
			   147,38,54,63,247,204,52,165,229,241,113,216,49,21,4,199,35,195,24,150,5,154,
			   7,18,128,226,235,39,178,117,9,131,44,26,27,110,90,160,82,59,214,179,41,227,
			   47,132,83,209,0,237,32,252,177,91,106,203,190,57,74,76,88,207,208,239,170,
			   251,67,77,51,133,69,249,2,127,80,60,159,168,81,163,64,143,146,157,56,245,
			   188,182,218,33,16,255,243,210,205,12,19,236,95,151,68,23,196,167,126,61,
			   100,93,25,115,96,129,79,220,34,42,144,136,70,238,184,20,222,94,11,219,224,
			   50,58,10,73,6,36,92,194,211,172,98,145,149,228,121,231,200,55,109,141,213,
			   78,169,108,86,244,234,101,122,174,8,186,120,37,46,28,166,180,198,232,221,
			   116,31,75,189,139,138,112,62,181,102,72,3,246,14,97,53,87,185,134,193,29,
			   158,225,248,152,17,105,217,142,148,155,30,135,233,206,85,40,223,140,161,
			   137,13,191,230,66,104,65,153,45,15,176,84,187,22)

	cuda_inited = False

	
	threadMax = 1024
	blockMax = 1024
	cuda_buf_size = 16 * blockMax * threadMax

	def __init__(self, key, threadMax = 1024, blockMax = 1024):
		self.key = key
		self.threadMax = threadMax
		self.blockMax = blockMax

		self.expandKey()
		self.gen_tbox()

	def gen_tbox(self):
		self.Te = [numpy.zeros(256, numpy.uint32) for i in xrange(4)]
		d = bytearray(256)

		for i in xrange(128):
			d[i] = i << 1;
			d[128 + i] = (i << 1) ^ 0x1b;
		for i in xrange(256):
			self.Te[0][i] = self.tuple2word((d[self.sbox[i]], self.sbox[i], self.sbox[i], d[self.sbox[i]] ^ self.sbox[i]))
			self.Te[1][i] = self.tuple2word((d[self.sbox[i]] ^ self.sbox[i], d[self.sbox[i]], self.sbox[i], self.sbox[i]))
			self.Te[2][i] = self.tuple2word((self.sbox[i], d[self.sbox[i]] ^ self.sbox[i], d[self.sbox[i]], self.sbox[i]))
			self.Te[3][i] = self.tuple2word((self.sbox[i], self.sbox[i], d[self.sbox[i]] ^ self.sbox[i], d[self.sbox[i]]))

	def tuple2word(self, x):
		return (x[0] << 24) | (x[1] << 16) | (x[2] << 8) | x[3]

	def byte2word(self, bArr):
		return (bArr[0] << 24) | (bArr[1] << 16) | (bArr[2] << 8) | bArr[3]

	def word2byte(self, w):
		b = bytearray(4)
		b[0] = w >> 24
		b[1] = (w >> 16) & 0xff
		b[2] = (w >> 8) & 0xff
		b[3] = w & 0xff
		return b

	def expandKey(self):
		if not self.key or len(self.key) not in (16, 16):
			raise Exception("invalid key")
		ks = bytearray((len(self.key) / 4 + 7) * 16)
		ks[0 : 16] = self.key

		self.keySchedule = numpy.zeros(4 * (len(self.key) / 4 + 7), numpy.uint32)

		rcon = 1

		for i in xrange(len(self.key), len(ks), 4):
			temp = ks[i - 4 : i]
			if i % len(self.key) == 0:
				temp = (self.sbox[temp[1]] ^ rcon, self.sbox[temp[2]], self.sbox[temp[3]], self.sbox[temp[0]])
				rcon = rcon << 1
				if rcon >= 256:
					rcon ^= 0x11b;
			for j in xrange(0, 4):
				ks[i + j] = ks[i + j - len(self.key)] ^ temp[j]
		for i in xrange(len(ks) / 16):
			self.keySchedule[i * 4 : (i + 1) * 4] = (self.byte2word(ks[i * 16 : i * 16 + 4]), self.byte2word(ks[i * 16 + 4 : i * 16 + 8]), self.byte2word(ks[i * 16 + 8 : i * 16 + 12]), self.byte2word(ks[i * 16 + 12 : i * 16 + 16]))

	def printKeySchedule(self):
		for i in xrange(0, len(self.keySchedule)):
			line = "(%08x, %08x, %08x, %08x)" % (self.keySchedule[i][0], self.keySchedule[i][1], self.keySchedule[i][2], self.keySchedule[i][3])
			print line

	def printDebugInfo(self):
		print self.Te

	def __addRoundKey(self, dst, src):
		for i in xrange(len(dst)):
			dst[i] ^= src[i]

	def __block_encrypt(self, pt):
		s = [0] * 4
		rk = self.keySchedule[0 : 4]
		for i in xrange(4):
			s[i] = self.byte2word(pt[i * 4 : (i + 1) * 4])
			# add round key
			s[i] ^= rk[i]

		t = [0] * 4

		for i in xrange(1, 10):
			rk = self.keySchedule[i * 4 : (i + 1) * 4]
			t[0] = self.Te[0][s[0] >> 24] ^ self.Te[1][(s[1] >> 16) & 0xff] ^ self.Te[2][(s[2] >> 8 ) & 0xff] ^ self.Te[3][(s[3]) & 0xff] ^ rk[0]
			t[1] = self.Te[0][s[1] >> 24] ^ self.Te[1][(s[2] >> 16) & 0xff] ^ self.Te[2][(s[3] >> 8 ) & 0xff] ^ self.Te[3][(s[0]) & 0xff] ^ rk[1]
			t[2] = self.Te[0][s[2] >> 24] ^ self.Te[1][(s[3] >> 16) & 0xff] ^ self.Te[2][(s[0] >> 8 ) & 0xff] ^ self.Te[3][(s[1]) & 0xff] ^ rk[2]
			t[3] = self.Te[0][s[3] >> 24] ^ self.Te[1][(s[0] >> 16) & 0xff] ^ self.Te[2][(s[1] >> 8 ) & 0xff] ^ self.Te[3][(s[2]) & 0xff] ^ rk[3]

			for j in xrange(4):
				s[j] = t[j]

		rk = self.keySchedule[40 : 44]
		s[0] = (self.Te[2][(t[0] >> 24)] & 0xff000000) ^ (self.Te[3][(t[1] >> 16) & 0xff] & 0x00ff0000) ^ (self.Te[0][(t[2] >> 8) & 0xff] & 0x0000ff00) ^ (self.Te[1][t[3] & 0xff] & 0x000000ff) ^ rk[0]
		s[1] = (self.Te[2][(t[1] >> 24)] & 0xff000000) ^ (self.Te[3][(t[2] >> 16) & 0xff] & 0x00ff0000) ^ (self.Te[0][(t[3] >> 8) & 0xff] & 0x0000ff00) ^ (self.Te[1][t[0] & 0xff] & 0x000000ff) ^ rk[1]
		s[2] = (self.Te[2][(t[2] >> 24)] & 0xff000000) ^ (self.Te[3][(t[3] >> 16) & 0xff] & 0x00ff0000) ^ (self.Te[0][(t[0] >> 8) & 0xff] & 0x0000ff00) ^ (self.Te[1][t[1] & 0xff] & 0x000000ff) ^ rk[2]
		s[3] = (self.Te[2][(t[3] >> 24)] & 0xff000000) ^ (self.Te[3][(t[0] >> 16) & 0xff] & 0x00ff0000) ^ (self.Te[0][(t[1] >> 8) & 0xff] & 0x0000ff00) ^ (self.Te[1][t[2] & 0xff] & 0x000000ff) ^ rk[3]

		ct = bytearray(len(pt))
		for i in range(4):
			ct[i * 4 : (i + 1) * 4] = self.word2byte(s[i])
		return ct

	def basic_encrypt(self, pt):
		if len(pt) % 16 != 0:
			raise Exception("invalid block size: " + str(len(pt)))

		if not isinstance(pt, bytearray):
			if isinstance(pt, str):
				pt = bytearray(pt)

		ct = bytearray(len(pt))

		for i in xrange(0, len(pt), 16):
			ct[i : i + 16] = self.__block_encrypt(pt[i : i + 16])

		return ct

	def init_cuda(self):
		if self.cuda_inited:
			return
		cuda_kernel = """
#include <stdio.h>

__device__ __constant__ unsigned int keySchedule[44];
__device__ __constant__ unsigned int Te0[256];
__device__ __constant__ unsigned int Te1[256];
__device__ __constant__ unsigned int Te2[256];
__device__ __constant__ unsigned int Te3[256];
__device__ __constant__ unsigned int length;
__device__ __constant__ unsigned int threadMax;


__global__ void printKeySchedule(){
	for(int i = 0; i < 11; i++){
		for(int j = 0; j < 4; j++){
			printf("%08x", keySchedule[i * 4 + j]);
		}
		printf("\\n");
	}
}

__device__ unsigned int bytestoword(unsigned char* b){
	return (b[0] << 24) | (b[1] << 16) | (b[2] << 8) | b[3];
}

__device__ void wordtobytes(unsigned char* b, unsigned int w){
	b[0] = (w >> 24);
	b[1] = (w >> 16) & 0xff;
	b[2] = (w >> 8) & 0xff;
	b[3] = w & 0xff;
}

__device__ void addRoundKey(unsigned int *s, unsigned int *k){
	s[0] ^= k[0];
	s[1] ^= k[1];
	s[2] ^= k[2];
	s[3] ^= k[3];
}

__global__ void encrypt(unsigned char* in){
	int p = blockIdx.x * 1024 + threadIdx.x;
	if(p * 16 >= length)
		return;
	unsigned char* block = in + p * 16;
	unsigned int s[4], t[4];
	unsigned int *rk;
	s[0] = bytestoword(block);
	s[1] = bytestoword(block + 4);
	s[2] = bytestoword(block + 8);
	s[3] = bytestoword(block + 12);

	addRoundKey(s, keySchedule);

	for(int i = 1; i < 10; i++){
		rk = keySchedule + i * 4;
		t[0] = Te0[s[0] >> 24] ^ Te1[(s[1] >> 16) & 0xff] ^ Te2[(s[2] >> 8 ) & 0xff] ^ Te3[(s[3]) & 0xff] ^ rk[0];
		t[1] = Te0[s[1] >> 24] ^ Te1[(s[2] >> 16) & 0xff] ^ Te2[(s[3] >> 8 ) & 0xff] ^ Te3[(s[0]) & 0xff] ^ rk[1];
		t[2] = Te0[s[2] >> 24] ^ Te1[(s[3] >> 16) & 0xff] ^ Te2[(s[0] >> 8 ) & 0xff] ^ Te3[(s[1]) & 0xff] ^ rk[2];
		t[3] = Te0[s[3] >> 24] ^ Te1[(s[0] >> 16) & 0xff] ^ Te2[(s[1] >> 8 ) & 0xff] ^ Te3[(s[2]) & 0xff] ^ rk[3];

		for(int j = 0; j < 4; j++)
			s[j] = t[j];
	}

	rk = keySchedule + 4 * 10;
	s[0] = (Te2[(t[0] >> 24)] & 0xff000000) ^ (Te3[(t[1] >> 16) & 0xff] & 0x00ff0000) ^ (Te0[(t[2] >> 8) & 0xff] & 0x0000ff00) ^ (Te1[t[3] & 0xff] & 0x000000ff) ^ rk[0];
	s[1] = (Te2[(t[1] >> 24)] & 0xff000000) ^ (Te3[(t[2] >> 16) & 0xff] & 0x00ff0000) ^ (Te0[(t[3] >> 8) & 0xff] & 0x0000ff00) ^ (Te1[t[0] & 0xff] & 0x000000ff) ^ rk[1];
	s[2] = (Te2[(t[2] >> 24)] & 0xff000000) ^ (Te3[(t[3] >> 16) & 0xff] & 0x00ff0000) ^ (Te0[(t[0] >> 8) & 0xff] & 0x0000ff00) ^ (Te1[t[1] & 0xff] & 0x000000ff) ^ rk[2];
	s[3] = (Te2[(t[3] >> 24)] & 0xff000000) ^ (Te3[(t[0] >> 16) & 0xff] & 0x00ff0000) ^ (Te0[(t[1] >> 8) & 0xff] & 0x0000ff00) ^ (Te1[t[2] & 0xff] & 0x000000ff) ^ rk[3];

	wordtobytes(block, s[0]);
	wordtobytes(block + 4, s[1]);
	wordtobytes(block + 8, s[2]);
	wordtobytes(block + 12, s[3]);
}

	"""
		
		mod = SourceModule(cuda_kernel)
		dKeySchedule = mod.get_global("keySchedule")[0]
		cuda.memcpy_htod(dKeySchedule, self.keySchedule)
		dThreadMax = mod.get_global("threadMax")[0]
		cuda.memcpy_htod(dThreadMax, numpy.array([self.threadMax], numpy.uint32))
		self.dLength = mod.get_global('length')[0]

		dTe0 = mod.get_global("Te0")[0]
		cuda.memcpy_htod(dTe0, self.Te[0])
		dTe1 = mod.get_global("Te1")[0]
		cuda.memcpy_htod(dTe1, self.Te[1])
		dTe2 = mod.get_global("Te2")[0]
		cuda.memcpy_htod(dTe2, self.Te[2])
		dTe3 = mod.get_global("Te3")[0]
		cuda.memcpy_htod(dTe3, self.Te[3])

		self.mod = mod

		self.cuda_buf = cuda.mem_alloc(self.cuda_buf_size)

		self.batchMax = self.threadMax * self.blockMax * 16

		self.cuda_inited = True

	def cuda_encrypt(self, pt):
		if len(pt) <= 0 or len(pt) % 16 != 0:
			raise Exception("invalid block size: " + str(len(pt)))

		if isinstance(pt, str):
			pass
		elif isinstance(pt, bytearray):
			pass
		else:
			raise Exception("invalid input type: " + type(pt))	
		self.init_cuda()

		# printKS = self.mod.get_function("printKeySchedule")
		# printKS(block = (1, 1, 1))



		enc = self.mod.get_function("encrypt");
		ct = numpy.empty(len(pt), dtype = numpy.ubyte)

		start = 0
		remain = len(pt)

		while remain > 0:
			threadNum = self.blockMax
			blockNum = 1
			if remain >= self.batchMax:
				dispose = self.batchMax
				blockNum = self.blockMax
				threadNum = self.threadMax
			elif remain > self.blockMax * 16:
				blockNum = int(math.ceil(float(remain / 16) / self.threadMax))
				threadm = self.threadMax
				dispose = remain
			else:
				threadNum = remain / 16
				dispose = remain
			remain -= dispose

			cuda.memcpy_htod(self.cuda_buf, pt[start : start + dispose])
			cuda.memcpy_htod(self.dLength, numpy.array([dispose], numpy.uint32))

			enc(self.cuda_buf, block = (threadNum, 1, 1), grid = (blockNum, 1))

			cuda.memcpy_dtoh(ct[start : start + dispose], self.cuda_buf)
			
			start += dispose

			
		return ct



class TestCUDAAES(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def _test_debuginfo(self):
		aes = AES('passward')
		aes.printKeySchedule()

	def test_basic_encrypt(self):
		key = bytearray(16)
		for i in xrange(16):
			key[i] = i
		rslt = (210,83,99,252,114,19,55,100,138,104,243,74,190,243,180,5)
		
		aes = AES(key)
		# aes.printKeySchedule()
		# print binascii.hexlify(key)

		pt = 'abcdefghijklmnop'
		# print binascii.hexlify(pt)
		ct = aes.basic_encrypt(pt)
		# print binascii.hexlify(ct)

		for i in xrange(len(rslt)):
			self.assertEqual(rslt[i], ct[i])

	def test_cuda_encrypt(self):
		key = bytearray(16)
		for i in xrange(16):
			key[i] = i
		rslt = (210,83,99,252,114,19,55,100,138,104,243,74,190,243,180,5)
		aes = AES(key)
		pt = 'abcdefghijklmnop'
		# print binascii.hexlify(pt)
		ct = aes.cuda_encrypt(pt)
		# print binascii.hexlify(ct)

		for i in xrange(len(rslt)):
			self.assertEqual(rslt[i], ct[i])

	def test_compare(self):
		key = bytearray(16)
		for i in xrange(16):
			key[i] = i
		aes = AES(key, 4)

		bs = 1024
		pt = numpy.random.bytes(bs)

		ct1 = aes.basic_encrypt(pt)
		ct2 = aes.cuda_encrypt(pt)

		for i in xrange(len(pt)):
		 	self.assertEqual(ct1[i], ct2[i])

	def test_benchmark(self):
		key = numpy.random.bytes(16)
		aes = AES(key)

		for i in xrange(17):
			bs = 16 * pow(2, i)
			print "\nBlock size: %d bytes" % bs
			# pt = 'abcdefghijklmnop' * (bs / 16)
			pt = numpy.random.bytes(bs)

			s = time.clock()
			aes.basic_encrypt(pt)
			e = time.clock()
			print "CPU: %fs, speed: %.2fMiB/s" % ((e - s), (bs / (e - s) / 1024 / 1024))

			s = time.clock()
			aes.cuda_encrypt(pt)
			e = time.clock()
			print "CUDA: %fs, speed: %.2fMiB/s" % ((e - s), (bs / (e - s) / 1024 / 1024))


if __name__ == "__main__":
	unittest.main()
