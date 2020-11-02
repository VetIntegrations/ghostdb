from setuptools import setup, find_packages


setup(
    name='VIS-GhostDB',
    version='0.1',
    packages=find_packages(),
    install_requires=(
        'alembic>=1.3.1,<2',
        'sqlalchemy-utils>=0.36.8,<1',
        # 'google-cloud-pubsub>=1,<2',
        'sentry-sdk',
    ),
    url='https://github.com/VetIntegrations/ghostdb',
    maintainer='Vadym Zakovinko',
    maintainer_email='vadymzakovinko@vetintegrations.com'
)
