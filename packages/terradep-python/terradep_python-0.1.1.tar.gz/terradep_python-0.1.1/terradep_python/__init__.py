from importlib import metadata

# TODO: I really hate this as it uses the installed version which isn't
#   necessarily the one being run => put static version here once tool for
#   https://softwarerecs.stackexchange.com/questions/86673 exists
__version__ = metadata.version(__package__)
__distribution_name__ = metadata.metadata(__package__)["Name"]
