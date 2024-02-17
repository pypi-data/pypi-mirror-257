# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hsss']

package_data = \
{'': ['*']}

install_requires = \
['swarms', 'torch', 'torchvision', 'zetascale']

setup_kwargs = {
    'name': 'hsss',
    'version': '0.0.2',
    'description': 'Paper - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# HSSS\nImplementation of a Hierarchical Mamba as described in the paper: "Hierarchical State Space Models for Continuous Sequence-to-Sequence Modeling".\n\n\n## install\n`pip install hsss`\n\n##  usage\n```python\nimport torch \nfrom hsss.model import HSSSMamba\n\nx = torch.randn(1, 10, 8)\n\nmodel = HSSSMamba(\n    dim_in = 8,\n    depth_in = 6,\n    dt_rank_in = 4,\n    d_state_in = 4,\n    expand_factor_in = 4,\n    d_conv_in = 6,\n    dt_min_in = 0.001,\n    dt_max_in = 0.1,\n    dt_init_in = "random",\n    dt_scale_in = 1.0,\n    bias_in = False,\n    conv_bias_in = True,\n    pscan_in = True,\n    dim = 4,\n    depth = 3,\n    dt_rank = 2,\n    d_state = 2,\n    expand_factor = 2,\n    d_conv = 3,\n    dt_min = 0.001,\n    dt_max = 0.1,\n    dt_init = "random",\n    dt_scale = 1.0,\n    bias = False,\n    conv_bias = True,\n    pscan = True,\n)\n\n\nout = model(x)\nprint(out)\n```\n\n# License\nMIT\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/HSSS',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
