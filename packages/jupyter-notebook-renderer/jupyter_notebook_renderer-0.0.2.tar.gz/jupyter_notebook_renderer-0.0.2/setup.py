import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

__version__ = "0.0.2"
Repo_name = "Jupyter-Notebook-renderer"
author_name = "HimanshuChoudhary3004"
author_email = "hchoudhary525@gmail.com"
src_repo = "jupyter_notebook_renderer"


setuptools.setup(
    name=src_repo,
    version=__version__,
    author=author_name,
    author_email=author_email,
    description="A small python package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{author_name}/{Repo_name}",
    project_urls={
        "Bug Tracker": f"https://github.com/{author_name}/{Repo_name}/issues",
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
)
