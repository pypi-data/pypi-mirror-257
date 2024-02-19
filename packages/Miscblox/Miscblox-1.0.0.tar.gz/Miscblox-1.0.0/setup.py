import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Miscblox",                 
    version="1.0.0",                     
    author="mark.api",                    
    description="An API wrapper for the Roblox that supports endpoints that other API wrappers don't.",
    long_description=long_description,      
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                     
    python_requires='>=3.6',               
    install_requires=["httpx","asyncio"]                  
)