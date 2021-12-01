### Anaconda 가상환경

- 만들기
  - conda create --name {envname} python={version}
- 가상화면 Jupyter Notebook 사용
  - conda activate {envname}
  - pip install ipykernel
  - python -m ipykernel install --user --name {envname} --display-name {"name"}

