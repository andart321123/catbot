def binAndBase2(num: str, from_: int, to: int) -> str:
	'''
	Converts from any number system to another one

	num: number to convert
	from_: from which number system convert
	to: to which number system convert
	returns converted number
	'''
	HEX1 = {'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15}
	HEX2 = {v: k for k, v in HEX1.items()}

	# to decimal
	if to in (10,):
		if from_ in(2, 8, 16):
			result = 0
			num = list(num)
			num.reverse()

			for i in range(len(num)):
				if not num[i].isdigit():
					num[i] = HEX1[num[i].upper()]
				else:
					num[i] = int(num[i])
				if num[i] != 0:
					result += num[i] * from_ ** i
	elif to in (2, 8, 16):
		# from decimal
		if from_ == 10:

			result = ''

			num = int(num)
			while num > 0:
				# Если буква
				if num % to > 9:
					result += HEX2[num % to]
					num = num // to
				else:
					result += str(num % to)
					num = num // to
				
			result = list(result)
			result.reverse()
			result = ''.join(result)
		else:
			# рекурсивно вызовем функцию
			return binAndBase2(binAndBase2(num, from_, 10), 10, to)

	return str(result)

binAndBase2

if __name__ == '__main__':
	while True:
		print(type(binAndBase2(input('число '), from_=int(input('из ')), to=int(input('в ')))))

	# 3AF -> 943
	# 103 -> 147(8)
	# 71 -> 1000111
