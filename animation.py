import pygame

class Animation:

    class Frame:
        def __init__(self, duration, rect):
            self.duration=duration
            self.rect=rect

    def __init__(self, frames=[]):
        self.frames=[]
        self.activation_timestamp=0
        self.frame_index=0

        for frame in frames:
            self.add_frame(frame)

    def add_frame(self, frame):
        self.frames.append(frame)
        self.frame_transition_times=self._calculate_frame_transition_times()
        self.loop_duration=self.frame_transition_times[-1]

    def activate(self, starting_index=0):
        self.frame_index=(starting_index % len(self.frames))
        self.activation_time=pygame.time.get_ticks()
        return self.get_frame()

    def get_frame(self):
        time=(pygame.time.get_ticks() - self.activation_time) % self.loop_duration

        if 0 < self.frame_index and time < self.frame_transition_times[0]:
            self._reset_frame_index()
        elif self.frame_transition_times[self.frame_index] < time:
            self._increment_frame_index()
        return self.frames[self.frame_index].rect

    def _reset_frame_index(self):
        self.frame_index=0

    def _increment_frame_index(self):
        self.frame_index += 1
        self.frame_index %= len(self.frames)
                          
    def _calculate_frame_transition_times(self):
        result=[f.duration for f in self.frames]
        for idx in range(1, len(result)):
            result[idx] += result[idx-1]
        return result

