# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['limoe']

package_data = \
{'': ['*']}

install_requires = \
['einops', 'torch', 'torchvision', 'zetascale']

setup_kwargs = {
    'name': 'limoe',
    'version': '0.0.2',
    'description': 'LiMoE - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# LiMoE\nImplementation of the "the first large-scale multimodal mixture of experts models." from the paper: "Multimodal Contrastive Learning with LIMoE: the Language-Image Mixture of Experts". [CLICK HERE FOR THE PAPER LINK:](https://arxiv.org/abs/2206.02770)\n\n\n# install\n`pip install limoe`\n\n\n\n# License\nMIT\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/LIMoE',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
