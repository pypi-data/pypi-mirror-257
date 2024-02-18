from setuptools import setup, find_packages
from pathlib import Path

this_dir = Path(__file__).parent

VERSION = '0.5.0' 
DESCRIPTION = 'Topic Modeling Toolkit'
# LONG_DESCRIPTION = 'A topic modeling toolkit from low-code to pro-code'
LONG_DESCRIPTION = (this_dir / "README.rst").read_text()

# Setting up
setup(
        name="cwordtm", 
        version=VERSION,
        author="Dr. Johnny CHENG",
        author_email="<drjohnnycheng@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        project_urls={
            'Homepage': 'https://github.com/drjohnnycheng/cwordtm',
            'Documentation': 'https://drjohnnycheng.github.io/cwordtm',
        },
        include_package_data=True,
        packages=find_packages(),
        package_dir={'': '.'},
        package_data={
            'data': ['*.csv', '*.txt', '*.ttc'],
            'dictionary': ['*.txt'],
            'images': ['*.jpg'],
        },
        install_requires=['numpy', 'pandas', 'importlib_resources', 'regex', 'nltk', \
                    'matplotlib', 'wordcloud', 'pillow', 'jieba', 'gensim', 'pyLDAvis',  \
                    'bertopic',  'transformers', 'spacy', 'seaborn', \
                    'importlib', 'networkx', 'plotly', 'IPython', 'scikit-learn', 'torch'],
        
        keywords=['word', 'scripture', 'topic modeling', 'visualization', \
                  'low-code', 'pro-code', 'network analysis', 'BERTopic', \
                  'LDA', 'NFM', 'Chinese', 'multi-levels', 'abstraction',
                  'meta-programming', 'CWordTM'],

        classifiers= [
            "Intended Audience :: Education",
            "Intended Audience :: Science/Research",
            "Intended Audience :: Religion",
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        ]
)
