import itertools


class EvaluationConfig():
    # dataset_path = path = r".\src\data\NIRxData_compact\2024-04-09_001\2024-04-09_001.snirf" # squat
    dataset_path = path = r".\data\NIRxData_compact\2024-04-09_004\2024-04-09_004.snirf"  # sit
    sampling_rates = [20]#[3,5,10,20,25,50,100,500]  # [5, 10, 20, 25, 50, 100, 250, 500]
    no_channels = [40]  # [40, 20, 3, 1]
    snrs = [None,25,50,100,200]  # [2, 4, 6, 8, 10, 15, 20, 30, 50]

    cross_options = False

    def __str__(self):
        return f"EVAL_CONFIG({self.dataset_path}; {self.current_sampling_rate}; {self.current_no_channels}; {self.current_snr})"

    def __init__(self):
        self.i = 0
        self.current_sampling_rate = None
        self.current_no_channels = None
        self.current_snr = None

        vari_sr = [(sr, None, None) for sr in self.sampling_rates]
        vari_snr = [(None, None, snr) for snr in self.snrs]
        vari_channels = [(None, c, None) for c in self.no_channels]
        combinations = []
        combinations.extend(vari_sr)
        combinations.extend(vari_snr)
        combinations.extend(vari_channels)  # vari one parameter individually and keep other config fixed ..
        if self.cross_options:
            self.combinations = list(itertools.product(self.sampling_rates, self.no_channels, self.snrs))  # or that
        else:

            self.combinations = combinations # this



    def __iter__(self):
        self.i = 0
        self.current_sampling_rate = None
        self.current_no_channels = None
        self.current_snr = None
        return self

    def __next__(self):
        if self.i < len(self.combinations):
            config = self.current_sampling_rate = self.combinations[self.i]
            self.current_sampling_rate, self.current_no_channels, self.current_snr = config
            self.i += 1
            return self
        raise StopIteration


if __name__ == "__main__":
    evaluation_config = EvaluationConfig()
    for x in evaluation_config:
        print(x)
