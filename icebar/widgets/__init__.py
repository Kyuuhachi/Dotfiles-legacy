try: from .separator import *
except ImportError as e: print("separator:", e)
try: from .clock import *
except ImportError as e: print("clock:", e)
try: from .battery import *
except ImportError as e: print("battery:", e)
try: from .temperature import *
except ImportError as e: print("temperature:", e)
try: from .wifi import *
except ImportError as e: print("wifi:", e)
try: from .ram import *
except ImportError as e: print("ram:", e)
try: from .cpugraph import *
except ImportError as e: print("cpugraph:", e)
try: from .volume_pulse import *
except ImportError as e: print("volume_pulse:", e)
try: from .volume_alsa import *
except ImportError as e: print("volume_alsa:", e)
try: from .feed import *
except ImportError as e: print("feed:", e)
try: from .ibus import *
except ImportError as e: print("ibus:", e)
try: from .mpd import *
except ImportError as e: print("mpd:", e)
