class hit_strength:
    LOW = 2771
    MEDIUM = 5542
    HIGH = 8313
    CRITICAL = 11085


def get_hit_strength(force):
    if force < hit_strength.LOW:
        return hit_strength.LOW
    elif force < hit_strength.MEDIUM:
        return hit_strength.MEDIUM
    elif force < hit_strength.HIGH:
        return hit_strength.HIGH
    else:
        return hit_strength.CRITICAL
