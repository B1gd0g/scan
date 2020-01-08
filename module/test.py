
def test():
	for i in range(100):
		print(i)
		for j in sys.stdout: 
			print(j)
			break
			print("结束")

sys.stdin.readlines() 