from probables import BloomFilter as BaseBloomFilter
from zipfile import Path, ZipFile
from .input import InputManager
from .bloom import BloomIndex, default_xxhash
import tempfile
from tqdm.notebook import tqdm
import numpy as np

class Pairiscope(object):
    def __init__(self, **kwargs):
        #Set up DataManager
        self.input = InputManager(**kwargs)
        self.index = BloomIndex(**kwargs)
         
    def status(self, list_filters=False, abundance_summary=False, count_threshold=1):
        #Return information about the blooms, what has been computed
        status_str = self.input.status()
        if abundance_summary and self.input._source_type == 'table':
            sorted_features = self.input._source.sum(axis=1).sort_values(ascending=False)
            above_threshold = set(sorted_features[sorted_features > count_threshold].index)
            fully_indexed = set(self.index.fully_indexed)
            above_threshold_fully_indexed = above_threshold.intersection(fully_indexed)
            indexed_percent = float(len(above_threshold_fully_indexed))/len(above_threshold)*100
            status_str += "\n%2.2f%% of objects > %d counts have been fully indexed\n" % (indexed_percent, count_threshold)
        status_str += self.index.status(list_filters)
        
        return status_str
    
    def simulation(self):
        # Fill the index with simulated pairs
        pass
    
    def is_fully_indexed(self, object_name):
        # Check if an object is fully indexed in the current BloomIndex
        # This means that all distances between this and all other in-cache items have been computed
        return object_name in self.index.fully_indexed
    
    def fully_indexed(self, object_name):
        self.index.fully_indexed.add(object_name)
        
    def all_neighbours(self, obj, max_distance=None, combine_bitvectors=False):
        #Returns all the neighbours up to a max distance provided
        if max_distance is None:
            max_distance = self.index._sorted_epsilon[-1]
        neighbours = set()
        for object_2 in self.index.fully_indexed: #Only useful to check objects that are in the index
            if self.index.are_neighbours(obj, object_2, max_distance=max_distance, combine_bitvectors=combine_bitvectors):
                neighbours.add(object_2)
        return neighbours
    
    def all_neighbors(self, *args):
        return self.all_neighbours(*args)
    
    def index_all(self):
        #TODO: Allow checkpointing by canceling?
        #This index just pulls the objects in one at a time, in no particular order
        if not self.input.loaded:
            raise RuntimeError("Data source not loaded, cannot fill fingerprint. Load through InputManager() accessed with .input")
        try:
            total = (len(self.input._object_names) * (len(self.input._object_names) - 1))/2
            with tqdm(total=total) as pbar:
                for object_1 in self.input._object_names:
                    if self.is_fully_indexed(object_1):
                        pbar.update(len(self.index.fully_indexed)-1)
                        continue #Already fully indexed
                    for object_2 in self.index.fully_indexed:
                        #Go through all others in index and add that pair information
                        dist = self.input.pair_distance(object_1, object_2)
                        #print(dist)
                        self.index.add_pair(object_1, object_2, 
                                            dist)
                        pbar.update(1)
                    self.fully_indexed(object_1)
                    
        except KeyboardInterrupt:
            print("Interrupted with %d objects fully indexed. Run again to continue where indexing left off." % (len(self.index.fully_indexed),))
            return
            
    
    def index_by_search(self, object_name):
        if not self.input.loaded:
            raise RuntimeError("Data source not loaded, cannot fill fingerprint. Load through InputManager() accessed with .input")
        if self.fully_indexed(object_name):
            print("%s already in index; no further action required" % (object_name,))
        else:
            total = len(self.index.fully_indexed)
            with tqdm(total=total) as pbar:
                for object_2 in self.index.fully_indexed:
                    self.index.add_pair(object_name, object_2,
                                       self.input.pair_distance(object_name, object_2))
                    pbar.update(1)
                self.fully_indexed(object_name)
            print("%s successfully added to existing index" % (object_name,))
    
    def index_by_abundance(self, count_threshold=1):
        if not self.input.loaded:
            raise RuntimeError("Data source not loaded, cannot fill fingerprint. Load through InputManager() accessed with .input")
        if self.input._source_type != 'table':
            raise RuntimeError("Source type not a table, cannot fill by abundance without abundance data.")
        #Sort by abundance
        if self.input._sparse_source:
            flat_sums = np.array(self.input._object_sums.flatten().tolist()[0])
            above_threshold = np.where(flat_sums>=count_threshold)[0]
            object_names = np.array(self.input._object_names)[above_threshold]
            object_sums = self.input._object_sums[above_threshold]
            sorted_index = np.argsort(object_sums,axis=0).tolist()[::-1]
            sorted_sums = self.input._object_sums[sorted_index]
            sorted_features = np.array(self.input._object_names)[sorted_index]
            sorted_features = sorted_features.flatten()
        else:
            sorted_features = self.input._source.sum(axis=1).sort_values(ascending=False)
            #Cut off any objects less than the min abundance, make just a list of names
            sorted_features = sorted_features[sorted_features>=count_threshold].index
        #Fully index the remaining set, starting with the most abundant vs. all that are fully indexed already
        print("Indexing in order of abundance")
        try:
            total = len(sorted_features)
            with tqdm(total=total) as pbar:
                for object_1 in sorted_features:
                    if self.is_fully_indexed(object_1):
                        pbar.update(1)
                        continue #Already fully indexed
                    for object_2 in self.index.fully_indexed:
                        #Go through all others in index and add that pair information
                        dist = self.input.pair_distance(object_1, object_2)
                        self.index.add_pair(object_1, object_2, 
                                            dist)
                    self.fully_indexed(object_1)
                    pbar.update(1)
        except KeyboardInterrupt:
            print("Interrupted with %d objects fully indexed. Run again to continue where indexing left off." % (len(self.index.fully_indexed),))
            return
    
    def index_by_taxonomy(self, query_taxonomy):
        if not self.input.loaded:
            raise RuntimeError("Data source not loaded, cannot fill fingerprint. Load through InputManager() accessed with .input")
        if not self.input.taxonomy_loaded:
            raise RuntimeError("Taxonomy not yet loaded. Load taxonomy artifiact with input.load_taxonomy()")
        #Remove any features that do not hit the query_taxonomy string
        filtered_features = self.input._taxonomy_source[ \
                            self.input._taxonomy_source['Taxon'].str.contains(query_taxonomy)].index
        try:
            total = (len(filtered_features) * (len(filtered_features) - 1))/2
            with tqdm(total=total) as pbar:
                for object_1 in filtered_features:
                    if self.is_fully_indexed(object_1):
                        pbar.update(len(self.index.fully_indexed)-1)
                        continue #Already fully indexed
                    for object_2 in self.index.fully_indexed:
                        #Go through all others in index and add that pair information
                        dist = self.input.pair_distance(object_1, object_2)
                        self.index.add_pair(object_1, object_2, 
                                            dist)
                        pbar.update(1)
                    self.fully_indexed(object_1)
        except KeyboardInterrupt:
            print("Interrupted with %d objects fully indexed. Run again to continue where indexing left off." % (len(self.index.fully_indexed),))
            return

    def cluster(self, initial_obj, epsilon, min_pts=3, max_output=100, combine_bitvectors=False):
        #Use a simple DBSCAN-inspired algorithm on input data to identify new nodes to include in the index
        #Start with initial obj
        #Get all neighbours within epsilon
        cluster_set = set([initial_obj])
        cluster_size = 1
        search_queue = [initial_obj]
        cleared = set()
        while True:
            if len(search_queue) == 0:
                break
            obj = search_queue.pop()
            if obj in cleared:
                continue
            neighbours = self.all_neighbours(obj, max_distance=epsilon, combine_bitvectors=combine_bitvectors)
            if len(neighbours) + 1 >= min_pts:
                 #obj is a core point, so all its neighbours belong in the cluster
                for neighbour in neighbours:
                    cluster_set.add(neighbour)
                    if len(cluster_set) >= max_output:
                        break
                    if neighbour not in cleared:
                        search_queue.append(neighbour)
            elif len(cluster_set) == 1: #Only to check neighbours to bump out of a edge point starter
                for neighbour in neighbours:
                    if len(self.all_neighbours(neighbour, max_distance=epsilon, combine_bitvectors=combine_bitvectors)) + 1 >= min_pts:
                        if neighbour not in cluster_set:
                            search_queue.append(neighbour)
            cleared.add(obj)
            
        return cluster_set
    
    def index_by_cluster(self, initial_obj, max_distance=None):
        # General algo: start with initial_obj and search the entire unindexed data set for neighbours
        # and add them iteratively
        if not self.input.loaded:
            raise RuntimeError("Data source not loaded, cannot fill fingerprint. Load through InputManager() accessed with .input")
        #TODO: Finish this mode
        pass
    
    def save(self, output_filename):
        #This is, for now, a basic save function
        #In the future, a proper QIIME2 artifact IO is planned
        #Open a zip file
        with ZipFile(output_filename, 'w') as output_archive:
            #Open a text file params.txt
            with output_archive.open('params.txt','w') as parameter_file:
                #Save the parameters
                #Epsilons
                parameter_file.write(" ".join([ str(x) for x in self.index._sorted_epsilon ]).encode()+b"\n")
                #Bloom filter parameters
                parameter_file.write(str(self.index.blooms[0]._fpr).encode()+b"\n")
                parameter_file.write(str(self.index.blooms[0]._capacity).encode()+b"\n")
                parameter_file.write(str(self.index.blooms[0]._size_modifier).encode()+b"\n")
                #Distance measure
                parameter_file.write(self.input._distance_measure.encode()+b"\n")
                #Loaded input information
                #parameter_file.write(ananke_obj.input._source.encode()+b"\n")
                parameter_file.write(self.input._source_file.encode()+b"\n")
                parameter_file.write(self.input._source_type.encode()+b"\n")
            #Fully indexed set as fully_index.txt and use names that were inserted
            with output_archive.open("fully_indexed.txt",'w') as full_index_file:
                for obj in self.index.fully_indexed:
                    full_index_file.write(obj.encode()+b"\n")
            #Save each of the bloom filters
            for bloom in self.index.blooms:
                with output_archive.open(str(bloom._epsilon)+".bloom",'w') as bloom_file:
                    bloom._bloom._bloom.tofile(bloom_file)  # type: ignore
                    bloom_file.write(
                        bloom._bloom._FOOTER_STRUCT.pack(
                        bloom._bloom.estimated_elements,
                        bloom._bloom.elements_added,
                        bloom._bloom.false_positive_rate))
    
    @classmethod
    def load(cls, pair_archive, load_original_file=True, load_taxonomy=True):
        with ZipFile(pair_archive,'r') as load_file:
            with load_file.open('params.txt') as parameter_file:
                blooms = parameter_file.readline().strip().decode().split(" ")
                epsilon_range = [float(x) for x in blooms]
                fpr = float(parameter_file.readline().strip())
                capacity = int(parameter_file.readline().strip())
                size_modifier = float(parameter_file.readline().strip())
                distance_measure = parameter_file.readline().strip().decode()
                input_file = parameter_file.readline().strip().decode()
                input_type = parameter_file.readline().strip().decode()
            with load_file.open('fully_indexed.txt','r') as full_index_file:
                full_index = set()
                for line in full_index_file.readlines():
                    full_index.add(line.strip().decode())
            #Introduce new loaded Pairiscope object
            p = Pairiscope(epsilon_values=epsilon_range)
            p.input._object_names = list(full_index)
            p.input._distance_measure = distance_measure
            p.index.fully_indexed = full_index
            #Apparently we have to decompress these to pass the work off to pyprobable's
            #BloomFilter class's filepath directive, without writing my own load
            temp_dir = tempfile.TemporaryDirectory()
            for idx, bloom in enumerate(blooms):
                bloom = bloom + ".bloom"
                load_file.extract(bloom,path=temp_dir.name)
                bf = BaseBloomFilter(filepath=temp_dir.name+"/"+bloom, hash_function=default_xxhash)
                p.index.blooms[idx]._bloom = bf
            if load_original_file:
                #TODO: Finish this properly
                if input_type == 'table':
                    p.input.load_table(input_file, distance_measure, sparse=True)
            return p
