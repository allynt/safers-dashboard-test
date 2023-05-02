import environ
import glob
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

from config.types import EnvironmentTypes

#########
# setup #
#########

ROOT_DIR = Path(__file__).resolve(strict=True).parents[2]  # (server dir)

env = environ.Env(
    DJANGO_ENVIRONMENT=(EnvironmentTypes, EnvironmentTypes.DEVELOPMENT)
)

ENVIRONMENT = env("DJANGO_ENVIRONMENT")

############################################################
# load environment variables & appropriate settings module #
############################################################

if ENVIRONMENT == EnvironmentTypes.DEVELOPMENT:
    for env_file in glob.glob(str(ROOT_DIR / ".env*")):
        # variables for development are stored in files
        try:
            env.read_env(env_file)
        except Exception as e:
            raise ImproperlyConfigured(f"Unable to read '{env_file}': {e}.")

    from config.settings.development import *

elif ENVIRONMENT == EnvironmentTypes.DEPLOYMENT:
    pass  # variables for deployment are dynamically created on the server

    from config.settings.deployment import *

elif ENVIRONMENT == EnvironmentTypes.CI:
    pass  # variables for ci are hard-coded in actions

    from config.settings.ci import *

else:
    raise ImproperlyConfigured(f"Unknown ENVIRONMENT: '{ENVIRONMENT}'")
