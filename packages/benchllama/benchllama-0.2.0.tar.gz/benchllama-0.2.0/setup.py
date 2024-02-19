# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['benchllama',
 'benchllama.data_io',
 'benchllama.evaluation',
 'benchllama.evaluation.runners',
 'benchllama.inference']

package_data = \
{'': ['*']}

install_requires = \
['datasets>=2.17.0,<3.0.0',
 'joblib>=1.3.2,<2.0.0',
 'ollama>=0.1.6,<0.2.0',
 'pandas>=2.2.0,<3.0.0',
 'typer[all]>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['benchllama = benchllama.main:app']}

setup_kwargs = {
    'name': 'benchllama',
    'version': '0.2.0',
    'description': '',
    'long_description': "# 👀 See it in action\n\n# `benchllama`\n\n**Usage**:\n\n```console\n$ benchllama [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n- `--install-completion`: Install completion for the current shell.\n- `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n- `--help`: Show this message and exit.\n\n**Commands**:\n\n- `clean`\n- `evaluate`\n\n## `benchllama clean`\n\n**Usage**:\n\n```console\n$ benchllama clean [OPTIONS]\n```\n\n**Options**:\n\n- `--run-id TEXT`: Run id\n- `--output PATH`: Output directory [default: /tmp]\n- `--help`: Show this message and exit.\n\n## `benchllama evaluate`\n\n**Usage**:\n\n```console\n$ benchllama evaluate [OPTIONS]\n```\n\n**Options**:\n\n- `--models TEXT`: Names of models that need to be evaluated. [required]\n- `--provider-url TEXT`: The endpoint of the model provider. [default: http://localhost:11434]\n- `--dataset FILE`: By default, bigcode/humanevalpack from Hugging Face will be used. If you want to use your own dataset, specify the path here.\n- `--languages [python|js|java|go|cpp]`: List of languages to evaluate from bigcode/humanevalpack. Ignore this if you are brining your own data [default: Language.python]\n- `--num-completions INTEGER`: Number of completions to be generated for each task. [default: 3]\n- `--k INTEGER`: The k for calculating pass@k. The values shouldn't exceed num_completions [default: 1, 2]\n- `--samples INTEGER`: Number of dataset samples to evaluate. By default, all the samples get processed. [default: -1]\n- `--output PATH`: Output directory [default: /tmp]\n- `--help`: Show this message and exit.\n",
    'author': 'Srikanth Srungarapu',
    'author_email': 'srikanth235@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
