from probables import BloomFilter as BaseBloomFilter
from typing import Callable, List, Union
import numpy as np
from functools import lru_cache
import xxhash

def default_xxhash(key: Union[str, bytes], depth: int = 1) -> List[int]:
    """The default xxhash hashing routine

    Args:
        key (str): The element to be hashed
        depth (int): The number of hash permutations to compute
    Returns:
        list(int): List of 64-bit hashed representation of key hashes
    Note:
        Returns the upper-most 64 bits"""
    res = []
    for idx in range(depth):
        res.append(xxhash.xxh32(key, idx).intdigest())
    return res

class BloomFilter(object):
    
    def __init__(self,
                 epsilon: float,
                 false_positive_rate: float = 0.001,
                 size_modifier: float = 1.0):
        self._epsilon = epsilon
        self._fpr = false_positive_rate
        self._size_modifier = size_modifier
        self._capacity = int(8*size_modifier*(1024**2) * ((np.log(2)**2) / np.abs(np.log(false_positive_rate))))
        self._bloom = BaseBloomFilter(est_elements=self._capacity,
                                      false_positive_rate=self._fpr,
                                      hash_function=default_xxhash)
        
    def status(self) -> str:
        """Return an information string detailing the size of the BloomFilter
           object.

        Returns:
            A string containing detailed info for the BloomFilter object.

        """
        status_str = "Bloom filter for distance threshold %f, " \
                   "storing %d pairs, " \
                   "with capacity for %d before false positive rate higher than %f. " \
                   "Using %.2f MB of memory for bloom bit vector." % (self._epsilon,
                                                  self._bloom.elements_added,
                                                  self._capacity,
                                                  self._fpr,
                                                  self._bloom.export_size()/(1024**2))
        return status_str
    
    def add_pair(self, x, y):
        self._bloom.add(str(min(x,y))+"__"+str(max(x,y)))
        
    def check_pair(self, x, y):
        if self._bloom.elements_added == 0: #Speed shortcircuit, does this work after a file load? TODO: check elements_added after load
            return False
        return str(min(x,y))+"__"+str(max(x,y)) in self._bloom

class BloomIndex(object):
    def __init__(self,
                 eps_start=0,
                 eps_stop=1,
                 num_bloom_filters=20,
                 eps_log=False,
                 epsilon_values=None,
                 **kwargs): #Max size in megabytes for a single filter, total size is len(epsilon_range)*max_size
        if epsilon_values != None:
            self._sorted_epsilon = np.sort(epsilon_values)
        else:
            if eps_log:
                range_fn = np.logspace
            else:
                range_fn = np.linspace
            epsilon_range = range_fn(eps_start, eps_stop, num_bloom_filters, endpoint=False)
            self._sorted_epsilon = np.sort(list(epsilon_range))
        if eps_log or (eps_start>0):
            print("No 0 bloom filter in specified range. Forcing an extra bloom filter at 0 to capture identical objects")
            self._sorted_epsilon = np.insert(self._sorted_epsilon, 0, 0., axis=0)
        self.blooms = [None]*len(self._sorted_epsilon)
        for idx, epsilon in enumerate(self._sorted_epsilon):
            self.blooms[idx] = BloomFilter(epsilon, **kwargs)
        #This tracks fully-cached names
        self.fully_indexed = set()
            
    def status(self, list_filters=True) -> str:
        """Return an information string detailing the size of the BloomIndex
           object.

        Returns:
            A string containing detailed info for the BloomIndex object.

        """
        single_bloom_size = self.blooms[0]._bloom.export_size()/(1024**2)
        nblooms = len(self.blooms)
        status_str = "%d bloom filters (%.2fMB each; %.2fMB total)\n" \
                     "%d pair capacity in each filter\n" \
                     "" % (nblooms,
                           single_bloom_size,
                           nblooms*single_bloom_size,
                           self.blooms[0]._capacity,)
        if list_filters:
            status_str += "***** Bloom Filters *****\n"
            status_str += "Epsilon       Stored Pairs\n"
            for idx, epsilon in enumerate(self._sorted_epsilon):
                capacity = 100*self.blooms[idx]._bloom.elements_added/ \
                           self.blooms[idx]._capacity
                capacity_str = "%.2f%% capacity" % (capacity,)
                if capacity >= 100:
                    capacity_str = "\x1b[1;31m" + capacity_str + "\x1b[0m"
                status_str += "%.6f      %d (%s, FPR %.4f%%)\n" % (epsilon, 
                                                                    self.blooms[idx]._bloom.elements_added,
                                                                    capacity_str,
                                                                    100*self.blooms[idx]._bloom.current_false_positive_rate())
        return status_str
   
    @lru_cache(maxsize=None)
    def _combine_bitvectors(self, distance):
        #Join the bit vectors up to distance, returning a smaller list of indexes to reduce searches required
        #for searching in bulk
        if distance == None:
            bloom_indexes = list(range(len(self._sorted_epsilon)))
        else:
            bloom_indexes = np.where(self._sorted_epsilon <= distance)[0]
        union_bfs = []
        epsilon_values = []
        union_bf = BaseBloomFilter(est_elements=self.blooms[bloom_indexes[-1]]._bloom.estimated_elements,
                                       false_positive_rate=self.blooms[bloom_indexes[-1]]._bloom.false_positive_rate,
                                       hash_function=default_xxhash)
        for idx in bloom_indexes:
            new_union_bf = union_bf.union(self.blooms[idx]._bloom)
            union_fpr = new_union_bf.current_false_positive_rate()
            if union_fpr >= self.blooms[idx]._fpr:
                union_bfs.append(union_bf)
                epsilon_values.append(self._sorted_epsilon[idx])
                union_bf = BaseBloomFilter(est_elements=self.blooms[bloom_indexes[-1]]._bloom.estimated_elements,
                                       false_positive_rate=self.blooms[bloom_indexes[-1]]._bloom.false_positive_rate,
                                       hash_function=default_xxhash)
            else:
                union_bf = new_union_bf
        if (len(epsilon_values) == 0) or (self._sorted_epsilon[idx] != epsilon_values[-1]):
            union_bfs.append(union_bf)
            epsilon_values.append(self._sorted_epsilon[idx])
        bi = BloomIndex(epsilon_values = epsilon_values)
        #Update the fully indexed set for bi to match self
        bi.fully_indexed = self.fully_indexed
        for idx, eps in enumerate(bi._sorted_epsilon):
            bi.blooms[idx] = BloomFilter(bi._sorted_epsilon[idx], 
                                          self.blooms[0]._fpr, 
                                          self.blooms[0]._size_modifier)
            #Replace bi's blooms with the union_bfs blooms
            bi.blooms[idx]._bloom = union_bfs[idx]
        print(bi.status(list_filters=True))
        return bi

    def add_pair(self, x, y, distance):
        if distance is np.nan:
            return
        if distance > self._sorted_epsilon[-1]:
            return #Exit and don't register if the distance is larger than we're tracking
        #If we don't check that and exit, argmax will return 0 and distant objects appear identical
        bf = self.blooms[np.argmax(self._sorted_epsilon >= distance)]
        #print("Registered distance at %f, inserted into bloom filter with epsilon %f" %(distance, bf._epsilon))
        bf.add_pair(x,y)
        
    def check_pair(self, x, y, distance):
        if distance > self._sorted_epsilon[-1]:
            raise ValueError("Cannot check at a distance larger than indexed")
        bloom_indexes = np.where(self._sorted_epsilon <= distance)[0]
        for idx in bloom_indexes:
            if self.blooms[idx].check_pair(x,y):
                return True
        return False
            
    def are_neighbours(self, x, y, max_distance=None, return_epsilon=False, combine_bitvectors=False):
        #Checks if x and y are a pair, with a possible cap 
        if combine_bitvectors:
            search_index = self._combine_bitvectors(max_distance)
            max_distance = search_index._sorted_epsilon[-1]
        else:
            search_index = self
            #TODO: test if collapsing all epsilon below max_distance and checking is faster
        if search_index.check_pair(x,y, max_distance):
            if return_epsilon:
                return self._sorted_epsilon[idx]
            else:
                return True
        return False

    def are_neighbors(self, *args): #For the Yanks
        return self.are_neighbours(*args)
