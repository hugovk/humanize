import pkg_resources
from humanize.filesize import naturalsize
from humanize.i18n import activate, deactivate
from humanize.number import (
    apnumber,
    fractional,
    hour,
    intcomma,
    intword,
    minute,
    ordinal,
)
from humanize.time import (
    naturalclock,
    naturaldate,
    naturalday,
    naturaldelta,
    naturaltime,
)

__version__ = VERSION = pkg_resources.get_distribution(__name__).version


__all__ = [
    "__version__",
    "activate",
    "apnumber",
    "hour",
    "deactivate",
    "fractional",
    "intcomma",
    "intword",
    "minute",
    "naturalclock",
    "naturaldate",
    "naturalday",
    "naturaldelta",
    "naturalsize",
    "naturaltime",
    "ordinal",
    "VERSION",
]
