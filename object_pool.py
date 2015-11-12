class ObjectPool:
    
    def __init__(self, size, pooled_type, *init_args):
        self.pool=[ pooled_type(*init_args) for i in range(0,size) ]
        self.current_idx=0

    def __call__(self,*args):
        result=self.pool[ self.current_idx ]

        self.current_idx += 1
        if self.current_idx == len(self.pool):
            self.current_idx=0

        result.__init__(*args)
        return result
        
