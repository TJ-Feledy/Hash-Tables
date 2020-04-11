# '''
# Linked List hash table key/value pair
# '''
class LinkedPair:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class HashTable:
    '''
    A hash table that with `capacity` buckets
    that accepts string keys
    '''
    def __init__(self, capacity):
        self.initCap = capacity
        self.capacity = int(capacity)  # Number of buckets in the hash table
        self.storage = [None] * capacity
        self.size = 0


    def _hash(self, key):
        '''
        Hash an arbitrary key and return an integer.

        You may replace the Python hash with DJB2 as a stretch goal.
        '''
        return hash(key)


    def _hash_djb2(self, key):
        '''
        Hash an arbitrary key using DJB2 hash

        OPTIONAL STRETCH: Research and implement DJB2
        '''
        hash = 5381
        byte_array = key.encode('utf-8')

        for byte in byte_array:
            hash = ((hash * 33) ^ byte) % 0x100000000

        return hash


    def _hash_mod(self, key):
        '''
        Take an arbitrary key and return a valid integer index
        within the storage capacity of the hash table.
        '''
        return int(self._hash_djb2(key) % self.capacity)


    def insert(self, key, value):
        '''
        Store the value with the given key.

        # Part 1: Hash collisions should be handled with an error warning. (Think about and
        # investigate the impact this will have on the tests)


        # Part 2: Change this so that hash collisions are handled with Linked List Chaining.

        Fill this in.
        '''
        # hash the key to create an index
        # create a new node, to be inserted
        index = self._hash_mod(key)
        node = LinkedPair(key, value)
        # ********Part 1********
        # if self.storage[index] is not None:
        #     print('Error:  The space at this index is already occupied!')

        # ********Part 2********
        # if the hashed index is occupied, add the node to the end of the Linked List
        # else add the node at the hashed index
        curr_node = self.storage[index]

        while curr_node is not None and curr_node.key != key:
            curr_node = curr_node.next
        # set the previous node's next node to point to the newly created node
        if curr_node is not None:
            curr_node.value = value

        else:
            node.next = self.storage[index]
            self.storage[index] = node

        self.size += 1

        if (self.load_factor(self.capacity) >= 0.7) and (int(self.initCap) != int(self.capacity)):
            print(self.load_factor(self.capacity))
            self.resize()

    def remove(self, key):
        '''
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Fill this in.
        '''
        # hash the key to create an index
        # create a current node at hashed index
        # create a previous node equal to None to start
        index = self._hash_mod(key)
        curr_node = self.storage[index]
        prev_node = None

        # iterate through linked list
        # while the current node is not None and its key is not equal to given key
        # previous node equals current node
        # current node equals next node
        while curr_node is not None and curr_node.key != key:
            prev_node = curr_node
            curr_node = curr_node.next

        # If current node is equal to None, print a warning
        # else: if the previous node is equal to None, current node equals None
        #       else, overwrite pointer to current node from previous node to point at next node.
        if curr_node is None:
            print('The given Key does not exist!')
        else:
            if prev_node is None:
                self.storage[index] = curr_node.next
            else:
                prev_node.next = curr_node.next

            self.size -= 1

            if (self.load_factor(self.capacity) <= 0.2) and (int(self.initCap) != int(self.capacity)):
                print(self.load_factor(self.capacity))
                self.resize()


    def retrieve(self, key):
        '''
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Fill this in.
        '''
        # Hash the key to create an index
        # create a current node
        index = self._hash_mod(key)
        curr_node = self.storage[index]

        # iterate through linked list to find the given key
        # while current node is not None and current node's key is not equal to given key
        # current node = the next node
        while curr_node is not None and curr_node.key != key:
            curr_node = curr_node.next

        # if current node is None, return None
        # else return current node's value
        if curr_node is None:
            return None
        else:
            return curr_node.value


    def resize(self):
        '''
        Doubles the capacity of the hash table and
        rehash all key/value pairs.

        Fill this in.
        '''
        # double the capacity
        # create new storage
        temp_storage = self.storage
        if self.load_factor(self.capacity) >= 0.7:
            self.capacity = int(self.capacity * 2)
        elif self.load_factor(self.capacity) <= 0.2 and self.load_factor(self.capacity/2) < 0.7:
            self.capacity = int(self.capacity / 2)
        print(self.capacity)
        self.storage = [None] * self.capacity
        self.size = 0

        # iterate through storage to copy it to new storage
        # for each index in storage
        # at that index insert the current item
        for item in temp_storage:
            curr_item = item
            while curr_item is not None:
                self.insert(curr_item.key, curr_item.value)
                curr_item = curr_item.next

    def load_factor(self, capacity):
        return self.size/capacity

if __name__ == "__main__":
    ht = HashTable(2)

    ht.insert("line_1", "Tiny hash table")
    ht.insert("line_2", "Filled beyond capacity")
    ht.insert("line_3", "Linked list saves the day!")

    print("")

    # Test storing beyond capacity
    print(ht.retrieve("line_1"))
    print(ht.retrieve("line_2"))
    print(ht.retrieve("line_3"))

    # Test resizing
    old_capacity = len(ht.storage)
    old_load = ht.load_factor(ht.capacity)
    ht.resize()
    new_capacity = len(ht.storage)
    new_load = ht.load_factor(ht.capacity)

    print(f"\nResized from {old_capacity}, load factor {old_load} to {new_capacity}, load factor {new_load}.\n")

    # Test if data intact after resizing
    print(ht.retrieve("line_1"))
    print(ht.retrieve("line_2"))
    print(ht.retrieve("line_3"))

    print("")
