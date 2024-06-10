from nameko.extensions import DependencyProvider
from dotenv import load_dotenv
import os

# Initialize environ
load_dotenv()


class Config(DependencyProvider):
    """ Static base configuration settings. """

    def __init__(self, config_dict):
        self.config = config_dict

    def setup(self):
        # Update the container config with the static settings
        self.container.config.update(self.config)

    def get_dependency(self, worker_ctx):
        # Provide the updated configuration as a dependency
        return self.container.config


class DynamicConfig(Config):
    """ Dynamic configuration that adjusts settings based on external factors. """

    def __init__(self, base_config):
        super().__init__(base_config)
        # Update the initial configuration with dynamic values
        self.config.update({
            'AMQP_URI': os.getenv('AMQP_URI', 'amqp://guest:guest@localhost')
            # You can add more dynamic settings here
        })

    def setup(self):
        # Apply both static and dynamic settings to the container's configuration
        self.container.config.update(self.config)


class TextImageServiceConfig:
    """ Base service class using dynamic configuration. """
    config = Config({
        'AMQP_URI': os.getenv('AMQP_URI'),
        'WEB_SERVER_ADDRESS': '0.0.0.0:8000',
        'rpc_exchange': 'nameko-rpc',
        'max_workers': 10,
        'parent_calls_tracked': 10
    })
