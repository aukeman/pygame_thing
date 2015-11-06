import pygame

class Image:
    
    NONE=0
    FLIPPED_H=1
    FLIPPED_V=2
    FLIPPED_BOTH=FLIPPED_H | FLIPPED_V

    def __init__(self, file, color_key=None, flags=NONE):

        self.surface=pygame.image.load(file)
        self.surface=self.surface.convert()

        if color_key is not None:
            self.surface.set_colorkey(color_key, pygame.RLEACCEL)
        
        self.flipped_h=None
        self.flipped_v=None
        self.flipped_hv=None

        if flags & Image.FLIPPED_H:
            self.flipped_h=pygame.transform.flip(self.surface,True,False)

        if flags & Image.FLIPPED_V:
            self.flipped_v=pygame.transform.flip(self.surface,False,True)

        if flags == Image.FLIPPED_BOTH:
            self.flipped_hv=pygame.transform.flip(self.surface,True,True)

        self.src_rect_buffer=[0,0,0,0]
        self.dest_coord_buffer=[0,0]

        self.width,self.height=self.surface.get_size()

            
    def blit(self, src_rect, x, y, dest_surf, flags=NONE):
        if flags == Image.FLIPPED_H and self.flipped_h is not None:
            self.src_rect_buffer[0] = self.width-src_rect[0]-src_rect[2]
            self.src_rect_buffer[1] = src_rect[1]
            self.src_rect_buffer[2] = src_rect[2]
            self.src_rect_buffer[3] = src_rect[3]
            src_surf=self.flipped_h
        elif flags == Image.FLIPPED_V and self.flipped_v is not None:
            self.src_rect_buffer[0] = src_rect[0]
            self.src_rect_buffer[1] = self.height-src_rect[1]-src_rect[3]
            self.src_rect_buffer[2] = src_rect[2]
            self.src_rect_buffer[3] = src_rect[3]
            src_surf=self.flipped_v
        elif flags == Image.FLIPPED_BOTH and self.flipped_hv is not None:
            self.src_rect_buffer[0] = self.width-src_rect[0]-src_rect[2]
            self.src_rect_buffer[1] = self.height-src_rect[1]-src_rect[3]
            self.src_rect_buffer[2] = src_rect[2]
            self.src_rect_buffer[3] = src_rect[3]
            src_surf=self.flipped_hv
        else:
            self.src_rect_buffer[0] = src_rect[0]
            self.src_rect_buffer[1] = src_rect[1]
            self.src_rect_buffer[2] = src_rect[2]
            self.src_rect_buffer[3] = src_rect[3]
            src_surf=self.surface

        self.dest_coord_buffer[0] = x
        self.dest_coord_buffer[1] = y

        dest_surf.blit(src_surf, self.dest_coord_buffer, self.src_rect_buffer)

