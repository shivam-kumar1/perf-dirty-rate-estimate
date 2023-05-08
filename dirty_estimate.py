def parse_addresses(addresses, debug=False):
	failed = []
	for i in range(len(addresses)):
	    try:
	    	addresses[i] = int(addresses[i], 16)
	    except:
			failed.append(addresses[i])
			addresses[i] = ''
	addresses = list(filter(lambda x: x != '', addresses))
	if debug:
		print("Couldn't parse these into hex int: ", failed)
	return addresses


def find_matches(pages, dirtied):

	i, j = 0, 0
	n, m = len(dirtied), len(pages)

	results = []

	for i in range(n):
		dirty_addr = dirtied[i]
		while j < m:
			page_addr = pages[j]
			if dirty_addr >= page_addr and dirty_addr < (page_addr + 4096):
				results.append((hex(page_addr), hex(dirty_addr), hex(page_addr + 4096)))
				break
			elif dirty_addr >= (page_addr + 4096):
				# Move to the next page in the sorted list
				j += 1
			else:
				# Dirty address cannot be mapped to any page
				break

	return results


# Get the mappings of VM's memory (virtual to physical)

mappings = open('mappings.txt').read().split('\n')
mappings = mappings[:-1] # Ignoring the last blank line
mappings = list(map(lambda x : x.split(' ')[1], mappings)) # mapping: vaddr paddr
mappings = parse_addresses(mappings)
mappings = sorted(mappings)
print("Printing first 100 VM's pages' physical addresses: ", mappings[:100])


# Get the physical addresses of dirtied pages

dirtied = open('mem_report').read()
dirtied = dirtied.split('\n')
dirtied = list(map(lambda x : x.split(' ')[-1], dirtied)) # Ignoring the last blank line
dirtied = parse_addresses(dirtied)
dirtied = sorted(dirtied)
print("Printing first 100 dirtied pages' physical addresses: ", dirtied[:100])


# Iterate over the sorted arrays to find the matches

results = find_matches(mappings, dirtied)


# Open output file to save matches

output = open('matches.txt', 'w')
for match in results:
	output.write(match[0] + " " + match[1] + " " + match[2] + "\n")
output.close()

# Print the results on the console

print("Printing first 10 matches: ", results[:10])
print("Matches found: ", len(results))
