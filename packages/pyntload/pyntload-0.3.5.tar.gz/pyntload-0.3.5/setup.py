from distutils.core import setup
setup(
  name = 'pyntload',         
  packages = ['pyntload'],   
  version = '0.0.8',      
  license='MIT',        
  description = 'pyntload - a simple package for importing functions from notebooks in jupyter notebook, azure databricks, ...',   # Give a short description about your library
  author = 'Simon De Smul',                  
  author_email = 'simon.de.smul@hotmail.com',      #
  url = 'https://github.com/alinso-sdsmul/pyntload',   
  download_url = 'https://github.com/alinso-sdsmul/pyntload/archive/refs/tags/0.0.1.tar.gz',  
  keywords = ['Databricks', 'Notebooks', 'Import'],  
  install_requires=[            
          'requests'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)