import yaml
from functools import lru_cache

def scalar_constructor(loader, node):
    value = loader.construct_scalar(node)
    return value

yaml.add_constructor('!ref', scalar_constructor)
yaml.add_constructor('!no-provenance', scalar_constructor)
yaml.add_constructor('!color', scalar_constructor)
yaml.add_constructor('!cite', scalar_constructor)
yaml.add_constructor('!metadata', scalar_constructor)

def update_params(yaml_obj):
    params = {}
    for d in yaml_obj['action']['parameters']:
        params.update(d)
    return params

def distance_measure_from_artifact(artifact):
    yaml_action = yaml.load(open(str(artifact._archiver.provenance_dir)+
                            "/action/action.yaml"), Loader=yaml.Loader)
    params = update_params(yaml_action)
    if 'metric' in params:
        return params['metric']
    else:
        alias_uuid = yaml_action['action']['alias-of']
        yaml_alias = yaml.load(open(str(artifact._archiver.provenance_dir)+
                              "/artifacts/"+alias_uuid+"/action/action.yaml"), Loader=yaml.Loader)
        params = update_params(yaml_alias)
        if 'metric' in params:
            return params['metric']
        else:
            alias_uuid = yaml_alias['action']['alias-of']
            yaml_alias = yaml.load(open(str(artifact._archiver.provenance_dir)+"/artifacts/"+
                                   alias_uuid+"/action/action.yaml"), Loader=yaml.Loader)
            params = update_params(yaml_alias)
            if 'metric' in params:
                return params['metric']
            else:
                return 'unknown' #Should we scrape further up? This is typical of pipeline distance matrices

def dtw_wrapper(u,v):
    from dtw import dtw
    #Fast-compute the dynamic time warping distance with a catch
    #to fall back to nan
    #try:
    dist = dtw(u.values,v.values,distance_only=True).distance
    #except:
    #    dist = np.nan
    return dist

def cc_wrapper(u,v):
    import numpy as np
    import scipy as sp
    #Compute the maximum cross correlation between two time series and then convert it into a distance
    # by subtracting the result from 1
    return 1 - np.max(sp.signal.correlate(u.values,v.values, mode='same', method='auto'))

class InputManager(object):
    def __init__(self, **kwargs):
        self.loaded = False
        self.metadata_loaded = False
        self.taxonomy_loaded = False
        self._distance_measure = "none"
        self._sparse_source = False
        
    def status(self) -> str:
        """Return an information string detailing the size of the BloomIndex
           object.

        Returns:
            A string containing detailed info for the BloomIndex object.

        """
        status_str = "***** Input Source *****\n"
        status_str += "Source is %sloaded\n" % ("not " if not self.loaded else "",)
        if self.loaded:
            status_str += "Type: %s\n" % (self._source_type,)
            status_str += "Source file: %s\n" % (self._source_file,)
            if self._source_type == 'distance_matrix':
                status_str += "Using %.2fMB of memory for distance structure\n" % (self._source.memory_usage(deep=True).sum()/(1024*1024),)
            elif self._source_type == 'tree':
                status_str += "Using %.2f MB on tree distance matrix floats\n" % (self._source.data.nbytes/(1024*1024))
            elif self._source_type == 'table':
                status_str += "Using %.2fMB of memory for original count table\n" % (self._source.memory_usage(deep=True).sum()/(1024*1024),)
        return status_str
    
    def load_tree(self, tree_artifact):
        self._source_type = 'tree'
        from qiime2 import Artifact
        import skbio
        tree = Artifact.load(tree_artifact).view(skbio.TreeNode)
        self._source = tree.tip_tip_distances()
        self._source_file = tree_artifact
        self._object_names = [x.name for x in tree.tips()]
        self._pair_dist_fn = lambda x,y: self._source[x,y]
        self._distance_measure = "pre-computed tree"
        self.loaded = True
    
    def load_distance_matrix(self, distance_matrix_artifact):
        self._source_type = 'distance_matrix'
        from qiime2 import Artifact
        artifact = Artifact.load(distance_matrix_artifact)
        measure = distance_measure_from_artifact(artifact)
        import skbio
        self._source = artifact.view(skbio.DistanceMatrix).to_data_frame()
        self._source_file = distance_matrix_artifact
        self._object_names = self._source.index.tolist()
        self._pair_dist_fn = lambda x,y: self._source[x][y]
        self._distance_measure = "pre-computed matrix"
        self.loaded = True
        
    def load_table(self, table_artifact, distance_measure, scaled=False, sparse=False, order_func=None, verbose=False):
        supported_measures = ["euclidean","sts","dtw","cc"]
        if distance_measure not in supported_measures:
            raise ValueError("Distance computation on count tables is only configured for the following distance measures: %s" % (", ".join(supported_measures)))
        self._source_type = 'table'
        if verbose: print("Loading qiime2")
        from qiime2 import Artifact
        if verbose: print("Loading table artifact")
        artifact = Artifact.load(table_artifact)
        if verbose: print("Loading pandas")
        import pandas as pd
        if verbose: print("Converting to pandas DataFrame")
        if sparse:
            self._sparse_source = True
            from qiime2.core.archive import Archiver
            import h5py
            from scipy.sparse import csr_matrix
            #Extract to temp file using QIIME2's library methods
            archive = Archiver.get_archive(table_artifact)
            path, cache = Archiver._make_temp_path(archive.uuid)
            archive.mount(path)
            process_alias, data_path = \
                cache._rename_to_data(archive.uuid, path)
            h5t=h5py.File(str(data_path)+"/data/feature-table.biom")
            object_names = h5t["observation/ids"]
            sample_names = h5t["sample/ids"]
            matrix = csr_matrix((h5t["observation/matrix/data"],
                                 h5t["observation/matrix/indices"],
                                 h5t["observation/matrix/indptr"]))
            self._object_sums = matrix.sum(axis=1)
            #We want to target a pandas matrix because of its solid indexing capabilities
            pandas_matrix = pd.DataFrame.sparse.from_spmatrix(matrix)
            del matrix
            pandas_matrix.index = object_names
            pandas_matrix.index = pandas_matrix.index.str.decode("utf-8")
            pandas_matrix.columns = [x.decode() for x in sample_names]
            self._source = pandas_matrix
        else:
            self._source = artifact.view(pd.DataFrame).T

        @lru_cache(maxsize=None)
        def cached_loc_fetch(x):
            return self._source.loc[x]
        if scaled:
            @lru_cache(maxsize=None)
            def cached_loc_fetch(x):
                a=self._source.loc[x]
                return a/a.sum()
        self._source_file = table_artifact
        if verbose: print("Getting feature names")
        self._object_names = self._source.index.to_list()
        self._sample_names = self._source.columns.to_list()

        if order_func is not None:
            if verbose: print("Putting samples in specified order")
            self._source = self._source[order_func(self._sample_names)]

        if verbose: print("Loading numpy, scipy & setting up distance function")
        import scipy as sp
        import numpy as np
        if distance_measure == 'euclidean':
            distance_func = sp.spatial.distance.euclidean
        elif distance_measure == 'sts':
            distance_func = sts_wrapper
        elif distance_measure == 'dtw':
            distance_func = dtw_wrapper
        elif distance_measure == 'cc':
            distance_func = cc_wrapper
        self._distance_measure = distance_measure
        def distance_wrapper(x,y):
            x_array = cached_loc_fetch(x)
            y_array = cached_loc_fetch(y)
            return distance_func(x_array, y_array)
        self._pair_dist_fn = distance_wrapper
        self.loaded = True
    
    def load_taxonomy(self, taxonomy_artifact):
        from qiime2 import Artifact
        artifact = Artifact.load(taxonomy_artifact)
        import pandas as pd
        self._taxonomy_source = artifact.view(pd.DataFrame)
        self._taxonomy_source_file = taxonomy_artifact
        self._taxonomy_source = self._taxonomy_source.loc[self._object_names]
        self.taxonomy_loaded = True
    
    def load_metadata(self, time_point_col='time'):
        #Here we load time points for use with STS and to make time series plots
        pass
    
    def feature_names(self):
        return self._object_names

    def sample_names(self):
        return self._sample_names
    
    def pair_distance(self, x, y):
        # Extracts the pair distance
        return self._pair_dist_fn(x,y)
