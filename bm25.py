# -*- coding: utf-8 -*-
"""Chi muc nghich dao va BM25. Chi dung numpy va collections.

Cac phan can viet duoc danh dau  # CAN VIET. Hop dong cua tung ham ghi
trong docstring cua no; kiem_tra.py kiem dung theo hop dong do.

Khong duoc nap rank_bm25, pyserini, sklearn, gensim hay bat ky thu vien
truy xuat nao trong tep nay.
"""
import math
from collections import defaultdict, Counter

def tach_khoang_trang(van_ban):
    """Tach van ban thanh danh sach token theo khoang trang, ha chu thuong."""
    return van_ban.lower().split()


class ChiMuc:
    """Chi muc nghich dao cua mot kho tai lieu.

    kho  : dict ma tai lieu -> van ban
    tach : ham tach tu; mac dinh la tach_khoang_trang

    Sau khi khoi tao, bon cau truc sau phai dung:
      self.n        tong so tai lieu trong kho
      self.avgdl    do dai trung binh, tinh theo so token
      self.do_dai   dict ma tai lieu -> so token cua tai lieu do
      self.tf       dict ma tai lieu -> dict tu -> tan so tu trong tai lieu
      self.chi_muc  dict tu -> danh sach ma tai lieu co chua tu do
    """

    def __init__(self, kho, tach=None):
        self.tach = tach or tach_khoang_trang
        self.kho = kho
        self.do_dai = {}
        self.tf = {}
        self.chi_muc = defaultdict(list)
        self.n = len(kho) 
        self.avgdl = 0  

        # CAN VIET: duyet kho mot luot va dien nam thuoc tinh tren.
        # Moi tai lieu chi duoc duyet mot lan.
        for ma_tai_lieu, van_ban in self.kho.items():
            cac_tu = self.tach(van_ban)

            #luu do dai cua cac tai lieu KHO
            self.do_dai[ma_tai_lieu] = len(cac_tu)

            #tinh tan so cua cac tu trong KHO, co bao nhieu tu khac se co bay nhieu cap key-val
            self.tf[ma_tai_lieu] = Counter(cac_tu)

            for tu in set(cac_tu):
                self.chi_muc[tu].append(ma_tai_lieu)

        self.avgdl = sum(self.do_dai.values()) / self.n if self.n > 0 else 0.0


    def df(self, t):
        """So tai lieu co chua tu t. Tu khong co trong kho cho 0."""
        return len(self.chi_muc[t])

    def idf(self, t):
        """Trong so idf cua tu t, dang co cong mot:

            idf(t) = ln( 1 + (N - df(t) + 0.5) / (df(t) + 0.5) )

        Tu khong co trong kho cho 0.0, khong bao loi.
        """
        df_t = self.df(t)
        if df_t == 0: return 0.0
        return math.log(1 + (self.n - df_t + 0.5) / (df_t + 0.5))


    def diem(self, truy_van, k1=1.2, b=0.75):
        """Diem BM25 cua truy van tren tung tai lieu.

        Tra ve dict ma tai lieu -> diem, CHI gom cac tai lieu co diem khac
        khong. Khong duoc quet ca kho: chi tai lieu nam trong posting list
        cua mot tu nao do cua truy van moi duoc tinh.

            diem(q, d) = sum  idf(t) * tf(t,d) * (k1 + 1)
                              / ( tf(t,d) + k1*(1 - b + b*|d|/avgdl) )

        voi t chay tren cac tu cua truy van.
        """
        if self.n == 0: return {}
        cac_tu = self.tach(truy_van)
        output = {}

        for tu in cac_tu: #lay posting list
            danh_sach_tai_lieu = self.chi_muc[tu]
            """
                self.chi_muc = {
                "tan": ["d2", "d3", "d7"],
                "so": ["d2", "d3", "d7"],
                "tu": ["d1", "d2", "d3", "d7"]
                    }
                """

            for ma_tai_lieu in danh_sach_tai_lieu:
                tf_t = self.tf[ma_tai_lieu][tu]
                idf_t = self.idf(tu)
                do_dai_d = self.do_dai[ma_tai_lieu]
                avgdl = self.avgdl

                tu_so = idf_t * tf_t * (k1 + 1)

                mau_so = tf_t + k1 * (1 - b + b * do_dai_d/ avgdl)

                diem_tu = tu_so / mau_so

                output[ma_tai_lieu] = output.get(ma_tai_lieu, 0) + diem_tu
        
        return {
            ma_tai_lieu: diem
            for ma_tai_lieu, diem in output.items()
            if diem != 0
        }




    def tim(self, truy_van, k=10, k1=1.2, b=0.75):
        """k tai lieu diem cao nhat, dang danh sach cap (ma, diem).

        Xep giam dan theo diem. Hai tai lieu bang diem thi xep theo ma tang
        dan, de ket qua khong doi giua hai lan chay.
        """
        diem = self.diem(truy_van, k1, b)
        output = sorted(diem.items(), key=lambda x: (-x[1], x[0]))

        return output[:k]
