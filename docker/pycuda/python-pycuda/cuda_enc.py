import aescuda, time, numpy


bs = 16 * 1024 * 1024
print "\n\nblock size: %d bytes" % bs

aes = aescuda.AES("1234567890123456")
for i in range(0, 64):
	pt = numpy.random.bytes(bs)
	s = time.clock()
	aes.cuda_encrypt(pt)
	e = time.clock()
	print "[CUDA ENC] time: %fs, speed: %.2fMiB/s" % ((e - s), (bs / (e - s) / 1024 / 1024))

