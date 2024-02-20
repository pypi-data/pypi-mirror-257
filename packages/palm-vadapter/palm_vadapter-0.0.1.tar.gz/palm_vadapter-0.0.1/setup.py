# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['palm_vadapter']

package_data = \
{'': ['*']}

install_requires = \
['einops', 'torch', 'zetascale']

setup_kwargs = {
    'name': 'palm-vadapter',
    'version': '0.0.1',
    'description': 'Paper - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# Palm2 Adapter\nImplementation of "PaLM2-VAdapter:" from the multi-modal model paper: "PaLM2-VAdapter: Progressively Aligned Language Model Makes a Strong Vision-language Adapter".\n\nThis model uses a perceiver resampler with a depth of 1 + a tiny palm to efficiently learn the features behind the images and then map them  to the same space as the big model.\n\n## install\n`$ pip install palm2-vadapter`\n\n\n## usage\n```python\nimport torch\nfrom palm_vadapter.main import PaLM2VAdapter\n\n# Random text and image tensors\ntext = torch.randint(0, 1000, (1, 32), dtype=torch.long)\n\n\n# Image tensor\nimg = torch.randn(1, 3, 224, 224)\n\n# Initialize PaLM2VAdapter model\nmodel = PaLM2VAdapter(\n    tiny_dim=512,\n    dim=512,\n    num_tokens=10000,\n    seq_length=32,\n    depth=6,\n    heads=8,\n    image_size=224,\n    patch_size=16,\n)\n\n# Forward pass through the model\nout = model(text, img)\n\n# Print the shape of the output\nprint(out.shape)\n```\n\n\n# License\nMIT\n\n## Citation\n```bibtex\n@misc{xiao2024palm2vadapter,\n    title={PaLM2-VAdapter: Progressively Aligned Language Model Makes a Strong Vision-language Adapter}, \n    author={Junfei Xiao and Zheng Xu and Alan Yuille and Shen Yan and Boyu Wang},\n    year={2024},\n    eprint={2402.10896},\n    archivePrefix={arXiv},\n    primaryClass={cs.CV}\n}\n```',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/PaLM2-VAdapter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
