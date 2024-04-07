from dataclasses import dataclass


@dataclass
class MoiveDto:
    id: int
    adult: bool
    
    """ Example
    {
      "id": 1066974,
      "adult": false
    },    
    """
