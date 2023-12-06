PIXEL_PER_METER = (10.0 / 0.25)  # 10 pixel 25 cm

RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


def kmph_to_pps(kmph):
    mpm = (kmph * 1000.0 / 60.0)
    mps = (mpm / 60.0)
    pps = (mps * PIXEL_PER_METER)
    return pps
