# Import the main class from the miner module
from .miner import TextMiner
from .extractor import KeywordsExtractor

# Optionally define an __all__ for explicitness on what is exported
__all__ = ['TextMiner','KeywordsExtractor']