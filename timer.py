
class Timer:
    timer_list = []
    cur_time = 0

    def __init__(self, duration, callback, loop=False):
        self.duration = duration
        self.callback = callback
        self.loop = loop
        self._end_tick = Timer.cur_time + duration

    @staticmethod
    def create_new(timer):
        Timer.timer_list.append(timer)
        return timer

    @staticmethod
    def delete(timer):
        if timer in Timer.timer_list:
            Timer.timer_list.remove(timer)

    @staticmethod
    def update(elapsed):
        Timer.cur_time += elapsed
        for timer in Timer.timer_list:
            if timer._end_tick <= Timer.cur_time:
                timer.callback()
                if timer.loop:
                    timer._end_tick = Timer.cur_time + timer.duration
                else:
                    Timer.timer_list.remove(timer)
