# fmt: off
code2hai = [
    "  ",
    # 萬子
    "一", "二", "三", "四", "五", "五", "六", "七", "八", "九",
    # 筒子
    "(1", "(2", "(3", "(4", "(5", "(5", "(6", "(7", "(8", "(9",
    # 索子
    "[1", "[2", "[3", "[4", "[5", "[5", "[6", "[7", "[8", "[9",
    # 東南西北白発中
    "東", "南", "西", "北", "白", "発", "中",
]
# fmt : on

sutehai_flags = {
    "tedashi": 0,
    "tsumogiri": 1,
    "naki": 2,
    "richi": 4,
}

class Player:
    def __init__(self, name, kyoku):
        self.name = name
        self.tehai = []
        self.tsumo = 0
        self.furo = []
        self.sutehai = []
        self.sutehai_flags = []
        self.richi = False
        self.tsumogiri = False
        self.point = 0
        self.kaze = 0
        self.kyoku = kyoku

    def do_ripai(self):
        self.tehai.sort()

    def do_haipai(self, haipai):
        self.tehai.extend(haipai)
        self.do_ripai()

    def do_tsumo(self, tsumo):
        self.tsumo = tsumo
        # self.tehai.append(tsumo)
        self.tsumogiri = False

    def do_sutehai(self, sutehai, tsumogiri):
        self.sutehai.append(sutehai)
        if tsumogiri:
            self.sutehai_flags.append(sutehai_flags["tsumogiri"])
        else:
            self.tehai.append(self.tsumo)
            self.tehai.remove(sutehai)
            self.sutehai_flags.append(sutehai_flags["tedashi"])
        self.tsumo = 0
        self.tsumogiri = tsumogiri
        self.do_ripai()
    
    def do_richi(self):
        self.richi = True
        self.sutehai_flags[-1] += sutehai_flags["richi"]

    def do_open_kakan(self, tedashi, naki):
        if self.kyoku.teban[-2] != self:
            # self.kyoku.teban[-2].sutehai.pop() # remove the last sutehai
            self.kyoku.teban[-2].sutehai_flags[-1] += sutehai_flags["naki"]
        else:
            self.tehai.remove(naki)
            self.tsumo = 0
        self.furo.append(naki)

    def do_open_ankan(self, tedashi, naki):
        for hai in tedashi:
            if hai in self.tehai:
                self.tehai.remove(hai)
            elif hai == self.tsumo:
                self.tsumo = 0
            self.furo.append(hai)

    def do_open_ponchi(self, tedashi, naki):
        for hai in tedashi:
            self.tehai.remove(hai)
            self.furo.append(hai)
        # self.kyoku.teban[-2].sutehai.pop() # remove the last sutehai
        self.kyoku.teban[-2].sutehai_flags[-1] += sutehai_flags["naki"]
        self.furo.append(naki)


    def show(self):
        def is_tsumogiri(flag):
            return 0 < (flag % 2)
        
        def is_naki(flag):
            return 0 < ((flag % 4) // 2)
        
        def is_richi(flag):
            return 0 < ((flag % 8) // 4)

        disp_tehai = [code2hai[self.tehai[idx] if idx < len(self.tehai) else 0] for idx in range(13)]
        disp_furo = [code2hai[self.furo[idx] if idx < len(self.furo) else 0] for idx in range(16)]
        # sutehai display
        disp_sutehai = [code2hai[self.sutehai[idx] if idx < len(self.sutehai) else 0] for idx in range(25)]
        disp_richi_flags = [is_richi(self.sutehai_flags[idx]) if idx < len(self.sutehai_flags) else 0 for idx in range(25)]
        disp_naki_flags = [is_naki(self.sutehai_flags[idx]) if idx < len(self.sutehai_flags) else 0 for idx in range(25)]
        disp_tsumogiri_flags = [is_tsumogiri(self.sutehai_flags[idx]) if idx < len(self.sutehai_flags) else 0 for idx in range(25)]
        disp_sutehai_flags = ["R" if r else "v" if n else "*" if t else " " for r, n, t in zip(disp_richi_flags, disp_naki_flags, disp_tsumogiri_flags)]
        disp_sutehai = [hai + flag for hai, flag in zip(disp_sutehai, disp_sutehai_flags)]

        disp_rich = "R" if self.richi else " "
        disp_str = "".join(disp_tehai) + "|" + code2hai[self.tsumo] + "|" + "".join(disp_furo) + "|" + "".join(disp_sutehai) + "|" + disp_rich + "|" + str(self.point)
        print(self.name + ":" + disp_str)

    def __str__(self):
        # fmt: off
        str_array = [
            "tehai:",     str(self.tehai),
            "tsumo:",     str(self.tsumo),
            "furo:",      str(self.furo),
            "sutehai:",   str(self.sutehai),
            "richi:",     str(self.richi),
            "tsumogiri:", str(self.tsumogiri),
            "point:",     str(self.point),
            "kaze:",      str(self.kaze),
        ]
        # fmt: on
        return " ".join(str_array)
