class hit_strength:
    LOW = 0.5
    MEDIUM = 1
    HIGH = 2
    CRITICAL = 8


def get_hit_strength(force):
    if force < hit_strength.LOW:
        return hit_strength.LOW
    elif force < hit_strength.MEDIUM:
        return hit_strength.MEDIUM
    elif force < hit_strength.HIGH:
        return hit_strength.HIGH
    else:
        return hit_strength.CRITICAL
