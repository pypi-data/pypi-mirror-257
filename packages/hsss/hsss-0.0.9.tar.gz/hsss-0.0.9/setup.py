# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hsss']

package_data = \
{'': ['*']}

install_requires = \
['einops', 'torch', 'torchvision', 'zetascale']

setup_kwargs = {
    'name': 'hsss',
    'version': '0.0.9',
    'description': 'Paper - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# HSSS\nImplementation of a Hierarchical Mamba as described in the paper: "Hierarchical State Space Models for Continuous Sequence-to-Sequence Modeling" but instead of using traditional SSMs were using Mambas. Basically the flow is single input -> low level mambas -> concat -> high level ssm -> multiple outputs. \n\n\n[Paper link](https://arxiv.org/pdf/2402.10211.pdf)\n\n\nI believe in this architecture alot as it segments local and global learning. \n\n\n## install\n`pip install hsss`\n\n##  usage\n```python\nimport torch\nfrom hsss import LowLevelMamba, HSSS\n\n\n# Reandom tensor\nx = torch.randn(1, 10, 8)\n\n# Low level model\nmamba = LowLevelMamba(\n    dim=8,  # dimension of input\n    depth=6,  # depth of input\n    dt_rank=4,  # rank of input\n    d_state=4,  # state of input\n    expand_factor=4,  # expansion factor of input\n    d_conv=6,  # convolution dimension of input\n    dt_min=0.001,  # minimum time step of input\n    dt_max=0.1,  # maximum time step of input\n    dt_init="random",  # initialization method of input\n    dt_scale=1.0,  # scaling factor of input\n    bias=False,  # whether to use bias in input\n    conv_bias=True,  # whether to use bias in convolution of input\n    pscan=True,  # whether to use parallel scan in input\n)\n\n\n# Low level model 2\nmamba2 = LowLevelMamba(\n    dim=8,  # dimension of input\n    depth=6,  # depth of input\n    dt_rank=4,  # rank of input\n    d_state=4,  # state of input\n    expand_factor=4,  # expansion factor of input\n    d_conv=6,  # convolution dimension of input\n    dt_min=0.001,  # minimum time step of input\n    dt_max=0.1,  # maximum time step of input\n    dt_init="random",  # initialization method of input\n    dt_scale=1.0,  # scaling factor of input\n    bias=False,  # whether to use bias in input\n    conv_bias=True,  # whether to use bias in convolution of input\n    pscan=True,  # whether to use parallel scan in input\n)\n\n\n# Low level mamba 3\nmamba3 = LowLevelMamba(\n    dim=8,  # dimension of input\n    depth=6,  # depth of input\n    dt_rank=4,  # rank of input\n    d_state=4,  # state of input\n    expand_factor=4,  # expansion factor of input\n    d_conv=6,  # convolution dimension of input\n    dt_min=0.001,  # minimum time step of input\n    dt_max=0.1,  # maximum time step of input\n    dt_init="random",  # initialization method of input\n    dt_scale=1.0,  # scaling factor of input\n    bias=False,  # whether to use bias in input\n    conv_bias=True,  # whether to use bias in convolution of input\n    pscan=True,  # whether to use parallel scan in input\n)\n\n\n# HSSS\nhsss = HSSS(\n    layers=[mamba, mamba2, mamba3],\n    dim=12,  # dimension of model\n    depth=3,  # depth of model\n    dt_rank=2,  # rank of model\n    d_state=2,  # state of model\n    expand_factor=2,  # expansion factor of model\n    d_conv=3,  # convolution dimension of model\n    dt_min=0.001,  # minimum time step of model\n    dt_max=0.1,  # maximum time step of model\n    dt_init="random",  # initialization method of model\n    dt_scale=1.0,  # scaling factor of model\n    bias=False,  # whether to use bias in model\n    conv_bias=True,  # whether to use bias in convolution of model\n    pscan=True,  # whether to use parallel scan in model\n    proj_layer=True,\n)\n\n\n# Forward pass\nout = hsss(x)\nprint(out)\n\n```\n## Citation\n```bibtex\n@misc{bhirangi2024hierarchical,\n      title={Hierarchical State Space Models for Continuous Sequence-to-Sequence Modeling}, \n      author={Raunaq Bhirangi and Chenyu Wang and Venkatesh Pattabiraman and Carmel Majidi and Abhinav Gupta and Tess Hellebrekers and Lerrel Pinto},\n      year={2024},\n      eprint={2402.10211},\n      archivePrefix={arXiv},\n      primaryClass={cs.LG}\n}\n```\n\n\n# License\nMIT\n\n\n## Todo \n\n- [ ] Implement the chunking of the tokens by spliting it up the sequence dimension\n\n- [ ] Make the fusion projection layer dynamic and not use just a linear, ffn, or cross attention or even an output head.\n',
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
