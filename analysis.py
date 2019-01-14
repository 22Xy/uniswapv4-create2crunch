import time

interval_seconds = 10

checkpoint = time.time()
d_checkpoint = None
r_checkpoint = None
count_checkpoint = None
total_checkpoint = None
iterations = 0

while True:
	print(f'\n\n\nruntime: {round((time.time() - checkpoint) / 60, 2)} minutes')

	iterations += 1
	with open('./efficient_addresses.txt') as f:
	    content = f.readlines()

	d = [int(i[116:]) for i in content]

	if d_checkpoint is None:
		d_checkpoint = len(d)

	d_change = len(d) - d_checkpoint
	d_iterations = round(d_change/(iterations * interval_seconds), 4)
	print(
		f'valuable submissions found this run: {d_change} or {d_iterations}',
		'per second'
	)

	r = {}
	count = {}

	for i in d:
	  if i not in r:
	    r[i] = i
	    count[i] = 1
	  else:
	    r[i] += i
	    count[i] += 1

	total = 0
	for i in range(max(d) + 1):
	  if i in r:
	  	total += r[i]

	longest = max(len(str(k)) for k in count.keys())

	if total_checkpoint is None:
		total_checkpoint = total

	change = total - total_checkpoint
	iterations = round(change/(iterations * interval_seconds), 4)
	print('sum of rewards this run:', change, 'or', iterations ,'per second')

	if d_change > 0:
		print('reward ratio this run:', round(change / d_change, 4))

	print('\ntotal valuable submissions found:', len(d))

	print('total rewards:', total)
	if len(d) > 0:
		print('total reward ratio:', round(total / len(d), 4))

	print('total submissions by amount:')
	for k, v in sorted(count.items()):
		print(f' * {str(k).rjust(longest)}: {v}')

	print('total submission rewards by %:')
	for i in range(max(d) + 1):
	  if i in r:
	  	ratio = r[i] / total
	  	print(f' * {str(i).rjust(longest)}: {round(ratio * 10000) / 100}%')

	most_valuable_index = d.index(max(d))
	print('\nmost valuable submission found:', d[most_valuable_index])
	print('found at line:', most_valuable_index + 1)
	print(' * salt:', content[most_valuable_index][:66])
	print(' * contract address:', content[most_valuable_index][70:112])

	leading_zero_bytes = 0
	for i, char in enumerate(content[most_valuable_index][72:111]):
		if i % 2 == 0:
			if (
			  char == '0' and
			  content[most_valuable_index][72:112][i + 1] == '0'
			):
				leading_zero_bytes += 1
			else:
				break

	print(' * leading zero bytes:', leading_zero_bytes)

	zero_bytes = 0
	for i, char in enumerate(content[most_valuable_index][72:111]):
		if (
		  i % 2 == 0 and
		  char == '0' and
		  content[most_valuable_index][72:112][i + 1] == '0'
		):
			zero_bytes += 1

	print(' * total zero bytes:', zero_bytes)

	time.sleep(interval_seconds)