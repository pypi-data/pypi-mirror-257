import pandas as pd
import numpy as np
from pypinyin import lazy_pinyin
from tabulate import tabulate
from importlib import resources


class ChineseNonwords:
    def __init__(
        self,
        stroke_min=1,
        stroke_max=25,
        num_nei_min=8,
        num_nei_max=307,
        logfreq_min=0,
        logfreq_max=6.31,
        N=10,
        random_state=42,
    ):

        # Accessing files within a package subdirectory
        data_path = resources.files("chinese_nonwords") / "data"
        subset_file = data_path / "subset.csv"
        word_file = data_path / "word.csv"

        # Reading the files using pandas
        self.subset = pd.read_csv(subset_file)
        self.word = pd.read_csv(word_file)
        self.word_phon = self.word["pinyinword"].value_counts().to_dict()

        """
        ---
        """

        self.stroke_min = stroke_min
        self.stroke_max = stroke_max
        self.num_nei_min = num_nei_min
        self.num_nei_max = num_nei_max
        self.logfreq_min = logfreq_min
        self.logfreq_max = logfreq_max
        self.N = N
        self.random_state = random_state

    def generate_nonwords(self):
        df = self.get_randomized_words(self.get_nonwords())
        table = tabulate(df, headers="keys", tablefmt="grid")
        return table
    
    def generate_words(self):
        df = self.get_words()
        table = tabulate(df, headers="keys", tablefmt="grid")
        return table
    
    def get_words(self):
        stroke_mask = (self.word["Stroke-mean-Sim"] >= self.stroke_min) & (
            self.word["Stroke-mean-Sim"] <= self.stroke_max
        )
        num_nei_mask = (self.word["Neighborhood-mean"] >= self.num_nei_min) & (
            self.word["Neighborhood-mean"] <= self.num_nei_max
        )
        logfreq_mask = (self.word["C&B-Subtitle-log-W"] >= self.logfreq_min) & (
            self.word["C&B-Subtitle-log-W"] <= self.logfreq_max
        )
        select = self.word.loc[(stroke_mask) & (num_nei_mask) & (logfreq_mask)]
        sample = select.sample(n=self.N, random_state=self.random_state)
        wordlist = sample[['Word_Sim', 'C&B-Subtitle-log-W', 'HD_M', 'Stroke-mean-Sim', 'Neighborhood-mean']].reset_index(drop=True)
        wordlist = wordlist.rename(columns={'Word_Sim': 'word',
                                            'C&B-Subtitle-log-W': 'logfreq',
                                            'Stroke-mean-Sim': 'stroke',
                                            'HD_M': 'homophone_density',
                                            'Neighborhood-mean': 'num_neighbor'})
        return wordlist

    def get_nonwords(self):
        stroke_mask = (self.subset["Stroke"] >= self.stroke_min) & (
            self.subset["Stroke"] <= self.stroke_max
        )
        num_nei_mask = (self.subset["Num-neighbor"] >= self.num_nei_min) & (
            self.subset["Stroke"] <= self.num_nei_max
        )
        logfreq_mask = (self.subset["C&B_log"] >= self.logfreq_min) & (
            self.subset["C&B_log"] <= self.logfreq_max
        )
        select = self.subset.loc[(stroke_mask) & (num_nei_mask) & (logfreq_mask)]
        sample = select.sample(n=2 * self.N, random_state=self.random_state)
        return sample

    def get_randomized_words(self, sample):
        N = sample.shape[0]
        df = pd.DataFrame()
        char_1 = []
        char_2 = []
        logfreq_1 = []
        logfreq_2 = []
        stroke_1 = []
        stroke_2 = []
        hd_1 = []
        hd_2 = []
        numnei_1 = []
        numnei_2 = []
        for i in np.arange(0, N, 2):
            nonword_pinyin = "".join(
                lazy_pinyin(sample.iloc[i]["Char"] + sample.iloc[i + 1]["Char"])
            )
            if nonword_pinyin not in self.word_phon.keys():
                char_1.append(sample.iloc[i]["Char"])
                char_2.append(sample.iloc[i + 1]["Char"])
                logfreq_1.append(sample.iloc[i]["C&B_log"])
                logfreq_2.append(sample.iloc[i + 1]["C&B_log"])
                hd_1.append(sample.iloc[i]["HD"])
                hd_2.append(sample.iloc[i + 1]["HD"])
                numnei_1.append(sample.iloc[i]["Num-neighbor"])
                numnei_2.append(sample.iloc[i + 1]["Num-neighbor"])
                stroke_1.append(sample.iloc[i]["Stroke"])
                stroke_2.append(sample.iloc[i + 1]["Stroke"])
        df["Char-1"] = char_1
        df["Char-2"] = char_2
        df["Logfreq-1"] = logfreq_1
        df["Logfreq-2"] = logfreq_2
        df["Stroke-1"] = stroke_1
        df["Stroke-2"] = stroke_2
        df["HD-1"] = hd_1
        df["HD-2"] = hd_2
        df["NumNeighbor-1"] = numnei_1
        df["NumNeighbor-2"] = numnei_2

        return df
