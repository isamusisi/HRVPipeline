class CommonConfig:
    def __init__(self,eval_sampling_rate):

        self.plot = False
        self.target_sampling_rate = 500
        self.snr_thresh = 16
        self.amp_threshs = [0.1, 3]

        self.eval_sampling_rate = eval_sampling_rate
