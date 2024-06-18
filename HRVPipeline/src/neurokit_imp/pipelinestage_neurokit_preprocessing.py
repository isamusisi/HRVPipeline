from HRVPipeline.src.pipeline.pipeline_stage import PipelineStage, PipelineStageType
import HRVPipeline.src.hrv_methods as hm
import HRVPipeline.src.util.plot as p
import neurokit2 as nk

from HRVPipeline.src.validation_methods import make_noise


class NeurokitPipelineStagePreprocessing(PipelineStage):
    def __init__(self, config={}):
        super().__init__(config)
        self.stage_type = PipelineStageType.PRE_PROCESSING
        self.accepted_in = [PipelineStageType.INPUT]

    def __str__(self):
        return "NeurokitPipeline"

    # TODO needed ? accept_input? overwrite?

    def run(self, pipeline_input):
        # TODO interfaces between stages!!!!!!!!!!!

        sr = int(pipeline_input.cd.sampling_rate)
        window = self.config["window"]

        window_samples = window * sr

        # short_input = pipeline_input.rolling(time=window_samples).construct('window', stride=window_samples)[1]
        short_input = pipeline_input[::20]

        resampled_input = nk.signal_resample(short_input, sampling_rate=int(sr/20), desired_sampling_rate=sr)

        # sr = hm.get_sampling_rate(pipeline_input)
        print(f"...................short_input: {short_input}")
        print(f"...................Sampling rate: {sr}")
        print(f"...................pipeline_input: {pipeline_input}")
        noise = make_noise(pipeline_input)
        print(f"...................noised pipeline_input: {noise}")
        # filter raw signal
        filtered_short = short_input.cd.freq_filter(fmin=0.5, fmax=3, butter_order=2)
        # p.plot_signal([short_input], title='raw ppg')
        filtered_input = pipeline_input.cd.freq_filter(fmin=0.5, fmax=3, butter_order=2)
        # filtered_input = pipeline_input.apply(lambda x: nk.signal_filter(x, sampling_rate=sr, lowcut=0.5, highcut=3,
        #                                                                  order=2))

        f_noise = noise.cd.freq_filter(fmin=0.5, fmax=3, butter_order=2)
        print(f"...................noised filtered pipeline_input: {f_noise}")
        # p.plot_signal([pipeline_input], title='ppg')
        # p.plot_signal([filtered_short], title='filtered ppg')
        # p.plot_signal([noise], title='noised ppg')

        n_peaks = hm.get_snirf_ppg_peaks(f_noise, sr)
        # p.plot_snirf_ppg(n_peaks, f'snirf noised ppg,peaks({n_peaks.sum()})')

        peaks = hm.get_snirf_ppg_peaks(filtered_input, sr)
        peaks_raw = hm.get_snirf_ppg_peaks(pipeline_input, sr)
        peaks_short = hm.get_snirf_ppg_peaks(short_input, int(sr/5))
        # resamp_sr = hm.get_sampling_rate(resampled_input.time) / 1000
        print(f"...................resampled signal: {resampled_input}")

        peaks_resampled = hm.get_snirf_ppg_peaks(resampled_input, int(sr))
        # p.plot_snirf_ppg(peaks, f'snirf ppg,peaks({peaks.sum()})')

        # p.plot_signal([filtered_short, peaks_short.peaks.values],
        #               title=f'filtered ppg peaks - {peaks_raw.peaks.values.sum()}')
        p.plot_signal([resampled_input],
                      title=f'resampled_ppg')
        # p.plot_signal([resampled_input, pipeline_input],
        #               title=f'resampled_ppg - raw_ppg')
        result = peaks.peaks.rolling(time=window_samples).construct('window', stride=window_samples)

        print(f"...................filtered_input: {result}")
        # peaks_all = nk.ppg_process(filtered_input,
        #                         sampling_rate=sr)  # TODO via config or better from stage before ...

        return result, sr, peaks_raw.peaks, peaks_resampled.peaks
