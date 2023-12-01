PIXEL_PER_METER = (10.0 / 0.4)  # 10 pixel 25 cm

RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
def kmph_to_pps(kmph):
    mpm = (kmph * 1000.0 / 60.0)
    mps = (mpm / 60.0)
    pps = (mps * PIXEL_PER_METER)
    return pps
