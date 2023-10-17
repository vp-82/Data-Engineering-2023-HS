# Function to display hashtable
def display_hash(hashTable):
	
	for i in range(len(hashTable)):
		print(i, end = " ")
		
		for j in hashTable[i]:
			print("-->", end = " ")
			print(j, end = " ")
			
		print()

# Creating Hashtable as a nested list
HashTable = [[] for _ in range(10)]

# Hashing Function to return key for every value
def Hashing(keyvalue):
	return keyvalue % len(HashTable)

# Insert Function to add values to the hash table
def insert(Hashtable, keyvalue, value):
	
	hash_key = Hashing(keyvalue)
	Hashtable[hash_key].append(value)

# Apply hash function
insert(HashTable, 10, 'Berlin')
insert(HashTable, 25, 'Zürich')
insert(HashTable, 20, 'Paris')
insert(HashTable, 9,  'London')
insert(HashTable, 21, 'Rom')
insert(HashTable, 21, 'Lissabon')

display_hash (HashTable)



