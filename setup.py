from setuptools import setup, find_packages


setup(
    name='GhostDB',
    version='0.1',
    packages=find_packages(),
    install_requires=(
        'alembic>=1.3.2,<2',
        'google-cloud-pubsub>=1.3,<2',
        'mysqlclient>=1.4,<2',
        'sentry-sdk',
    ),
    url='https://github.com/VetIntegrations/ghostdb',
    maintainer='Vadym Zakovinko',
    maintainer_email='vadymzakovinko@vetintegrations.com'
)
