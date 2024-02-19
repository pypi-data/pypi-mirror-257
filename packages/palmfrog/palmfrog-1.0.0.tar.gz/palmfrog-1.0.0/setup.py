from setuptools import setup, find_packages

setup(
    name='palmfrog',
    version='1.0.0',
    packages=['palmfrog'],  # Explicitly specify your package
    entry_points={
        'console_scripts': [
            'palm=palmfrog.main:main',
        ],
    },
    install_requires=[
        'requests',
        'pycryptodome',
    ],
    author='Palmfrog',
    author_email='hello@palmfrog.net',
    description='ChatGPT for terminal applications with palmfrog.net website.',
    license='MIT',
    keywords='chatgpt terminal chatbot palmfrog camouflage',
)

