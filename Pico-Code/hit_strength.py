class hit_strength:
    LOW = 2
    MEDIUM = 4
    HIGH = 8
    CRITICAL = 16


def get_hit_strength(force):
    if force < hit_strength.LOW:
        return hit_strength.LOW
    elif force < hit_strength.MEDIUM:
        return hit_strength.MEDIUM
    elif force < hit_strength.HIGH:
        return hit_strength.HIGH
    else:
        return hit_strength.CRITICAL
