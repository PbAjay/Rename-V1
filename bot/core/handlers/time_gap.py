import time
from typing import Optional, Tuple

GAP = {}


async def check_time_gap(user_id: int) -> Tuple[bool, Optional[int]]:
    """A function for checking user time gap!
    :parameter user_id: Telegram User ID"""

    str_user_id = str(user_id)

    if str_user_id in GAP:
        current_time = time.monotonic()
        previous_time = GAP[str_user_id]

        if round(current_time - previous_time) < 120:
            return True, round(previous_time - current_time + 120)
        elif round(current_time - previous_time) >= 120:
            del GAP[str_user_id]
            return False, None
    elif str_user_id not in GAP:
        GAP[str_user_id] = time.monotonic()
        return False, None
    
