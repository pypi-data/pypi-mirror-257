import io, os, sys, types
from IPython import get_ipython
from nbformat import read
from IPython.core.interactiveshell import InteractiveShell
import pyntload.helper
import re
import logging


#detect environment (local or databricks)
running_on_databricks = None
databricks_workspace_URL = None

try:
    os.environ["DATABRICKS_RUNTIME_VERSION"]
    running_on_databricks=1

    #just a test
    databricks_workspace_URL = spark.conf.get("spark.databricks.workspaceUrl")
    print("Databricks workspace URL = ", databricks_workspace_URL)

except:
    running_on_databricks=0

#methods as adapted from jupyter notebook help website
def find_notebook(fullname, path=None):

    print("----- find_notebook -----")

    if running_on_databricks:

        print("--- databricks ---")

        #path is extracted via sys.path (if it contains Workspace, ignore. For some reason, Databricks REST API cannot handle if /Workspace is first part of path)
        pattern = re.compile('/databricks|/local_disk0|/usr')
        path = [path for path in sys.path if ( (not pattern.match(path)) and len(path)!=0 )]
        print("path = ", path)

        #extract filename (and possible subdirectories)
        fullname = fullname.split('/')[-1]
        print("fullname = ", fullname)

        #if subdirectories are present in the filename, add them to the path list (in first place, so it considers that first)
        name=fullname

        if len(fullname.split('.')) >1:
            name = fullname.split('.')[-1] 
            subdirs = fullname.split('.')[:-1]      
            path.insert(0, os.getcwd() + '/' + '/'.join(subdirs))
            print("path after adding child directories = ", path)

    else:
        print("--- local ---")

        #extract filename
        name = fullname.rsplit('.', 1)[-1]
        print("name = ", name)
        print("path = ", path)

        #if no path supplied, try the current directory
        if not path:
            print("!NO PATH SUPPLIED")
            path = sys.path

    #for each path supplied (NOTE: pathis a list of possible paths)
    for d in path:
        print("!PATH SUPPLIED")

        #create notebook path ( = location of notebook)
        nb_path = os.path.join(d, name + ".ipynb")
        print("nb_path = ", nb_path)

        #if the notebook exists, return the path
        if os.path.exists(nb_path):
            return nb_path
            
        #try again, but look for other filename of notebook
        nb_path = nb_path.replace("_", " ")
        print("nb_path (bezcause not found first time)= ", nb_path)

        if os.path.exists(nb_path):
            return nb_path

class NotebookLoader(object):
    """Module Loader for Jupyter Notebooks"""
    def __init__(self, path=None):
        self.shell = InteractiveShell.instance()
        self.path = path

    def load_module(self, fullname):
        
        print("----- load_module -----")

        #init the module
        #create the module and add it to sys.modules if name in sys.modules:
        #return sys.modules[name]
        mod = types.ModuleType(fullname)
        mod.__file__ = self.path
        mod.__loader__ = self
        mod.__dict__['get_ipython'] = get_ipython
        sys.modules[fullname] = mod

        #extra work to ensure that magics that would affect the user_ns
        #actually affect the notebook module's ns
        save_user_ns = self.shell.user_ns
        self.shell.user_ns = mod.__dict__

        print('MODULE INIT COMPLETE')

        #load the notebook contents
        if running_on_databricks:
            print("--- databricks ---")

            print("self.path = ", self.path)
            list_of_cells = pyntload.helper.read_databricks_notebook(self.path)

            try:
                for cell in list_of_cells:
                    
                    if cell["cell_type"] == 'code':
                        # transform the input to executable Python
                        code = self.shell.input_transformer_manager.transform_cell(''.join(cell['source']))
                        # run the code in themodule
                        exec(code, mod.__dict__)
            finally:
                self.shell.user_ns = save_user_ns

            print("!CODE IMPORTED")

        else:
            print("--- local ---")

            print("self.path = ", self.path)
            #self.path is nb_path. Following reads the notebook
            with io.open(self.path, 'r', encoding='utf-8') as f:
                nb = read(f, 4)

            #list of all cells in the notebook
            list_of_cells = nb.cells
        
            #try finally: always reset self.shell.user_ns after completing for loop (whether or not for loop succeeeded)
            try:
                for cell in list_of_cells:
                    
                    if cell.cell_type == 'code':
                        #transform the input to executable Python
                        code = self.shell.input_transformer_manager.transform_cell(cell.source)

                        #run the code in the module
                        exec(code, mod.__dict__)
            finally:
                self.shell.user_ns = save_user_ns

            print("!CODE IMPORTED")

        return mod


class NotebookFinder(object):

    def __init__(self):
        self.loaders = {}

    def find_module(self, fullname, path=None):
        #based on the name of the notebook and the path, find the notebook path
        nb_path = find_notebook(fullname, path)

        #return if no notebook path is found
        if not nb_path:
            return
        
        #if a notebook path is found, import the notebook
        else:
        
            key = nb_path

            print("key = ", key)
            print("nb_path = ", nb_path)
            #register with self.loaders, return
            if key not in self.loaders:
                self.loaders[key] = NotebookLoader(nb_path)

            return self.loaders[key]

sys.meta_path.append(NotebookFinder())
