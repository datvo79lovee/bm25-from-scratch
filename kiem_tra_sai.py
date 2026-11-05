# -*- coding: utf-8 -*-
"""Kiem lai bm25.py va chi_so.py tren kho do choi.

Chay:  python kiem_tra.py

Ba muoi bon phep kiem, chia bay nhom. Moi dong in ra ket qua cua mot phep
kiem, kem gia tri nhan duoc va gia tri phai ra. Phep kiem sai co kem mot
dong chan doan.

Tep nay khong cham diem va khong gui di dau. No chi tra loi mot cau hoi:
cach cai da dung chua.
"""
from __future__ import print_function

import math
import sys

from kho_do_choi import KHO, QRELS, TRUY_VAN

SAI_SO = 1e-6

# Vi du muoi tai lieu dung o muc A4.
THU_HANG = ["x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9", "x10"]
NHAN_NHI_PHAN = {"x2": 1, "x5": 1, "x9": 1, "x11": 1}
NHAN_NHIEU_MUC = {"x1": 2, "x3": 3, "x5": 1, "x8": 1, "x20": 2, "x21": 1}

# Hai gia tri sai thuong gap o nDCG voi nhan nhieu muc.
NDCG_MAU_TU_KET_QUA = 0.809297
NDCG_NEN_NHI_PHAN = 0.666427

so_dat = 0
so_chay = 0


def kiem(ten, nhan_duoc, phai_ra, chan_doan=None):
    global so_dat, so_chay
    so_chay += 1
    if isinstance(phai_ra, float):
        dat = (nhan_duoc is not None
               and abs(float(nhan_duoc) - phai_ra) < SAI_SO)
        hien = "None" if nhan_duoc is None else "%.6f" % float(nhan_duoc)
        can = "%.6f" % phai_ra
    else:
        dat = (nhan_duoc == phai_ra)
        hien, can = repr(nhan_duoc), repr(phai_ra)
    so_dat += 1 if dat else 0
    print("[%s] %-46s %s" % ("DAT " if dat else "SAI ", ten, hien))
    if not dat:
        print("       phai ra : %s" % can)
        if chan_doan:
            print("       %s" % chan_doan)
    return dat


def goi(ham, *tham_so):
    """Goi mot ham chua cai dat xong ma khong lam dung ca tep kiem."""
    try:
        return ham(*tham_so)
    except NotImplementedError:
        return None
    except Exception as loi:
        print("       loi khi goi: %s: %s" % (type(loi).__name__, loi))
        return None


import sys

try:
    loai_loi = sys.argv[1] if len(sys.argv) > 1 else "dung"

    if loai_loi == "1":
        import bm25
        import chi_so_sai_recall as chi_so

    elif loai_loi == "2":
        import bm25
        import chi_so_ndcg_sai as chi_so

    elif loai_loi == "3":
        import bm25_sai as bm25
        import chi_so

    elif loai_loi == "dung":
        import bm25
        import chi_so

    else:
        print("Chi chon: dung, 1, 2 hoac 3")
        sys.exit(1)

except ImportError as loi:
    print("Khong nap duoc module:", loi)
    print("Dat kiem_tra.py cung thu muc voi bm25.py va chi_so.py.")
    sys.exit(1)


print("=" * 64)
print("Nhom 1 --- chi muc nghich dao")
print("=" * 64)
ix = bm25.ChiMuc(KHO)
kiem("so tai lieu", getattr(ix, "n", None), 8)
kiem("so tu khac nhau", len(getattr(ix, "chi_muc", {})), 65,
     "Tach bang .lower().split(); 65 la so tu KHAC NHAU, khong phai"
     " tong so token.")
kiem("do dai trung binh", getattr(ix, "avgdl", None), 12.75,
     "avgdl tinh tren so token, khong phai so tu khac nhau.")
kiem("df('tan')", goi(ix.df, "tan"), 3)
kiem("df('tai')", goi(ix.df, "tai"), 5)
kiem("df tu khong co trong kho", goi(ix.df, "khongcotukhoanay"), 0,
     "Tu ngoai kho phai cho 0, khong duoc bao KeyError.")
kiem("idf('tan')", goi(ix.idf, "tan"), 0.944462,
     "N = 8, df = 3. Dung dang co cong mot: ln(1 + (N-df+0.5)/(df+0.5)).")
kiem("idf('tai')", goi(ix.idf, "tai"), 0.492476)
kiem("idf tu khong co trong kho", goi(ix.idf, "khongcotukhoanay"), 0.0)

print()
print("=" * 64)
print("Nhom 2 --- diem BM25, k1 = 1.2, b = 0.75")
print("=" * 64)
th1 = goi(ix.tim, TRUY_VAN["q1"], 4)
kiem("q1: thu hang", [ma for ma, _ in th1] if th1 else None,
     ["d7", "d3", "d2", "d1"],
     "d7 la dong tieu de, ngan nhat kho, nen duoc chuan hoa do dai uu ai"
     " va len dau. Day la hanh vi dung cua BM25.")
kiem("q1: diem cua d7", th1[0][1] if th1 else None, 3.046354)
th2 = goi(ix.tim, TRUY_VAN["q2"], 5)
kiem("q2: thu hang", [ma for ma, _ in th2] if th2 else None,
     ["d4", "d7", "d2", "d1", "d8"])
kiem("q2: diem cua d4", th2[0][1] if th2 else None, 3.474548)
th3 = goi(ix.tim, TRUY_VAN["q3"], 5)
kiem("q3: so tai lieu co diem khac khong",
     len(th3) if th3 is not None else None, 2,
     "Chi tai lieu nam trong posting list cua tu truy van moi duoc tinh"
     " diem. Ra 8 nghia la dang quet ca kho.")
kiem("q3: diem cua d5", th3[0][1] if th3 else None, 6.820338)

print()
print("=" * 64)
print("Nhom 3 --- bat bien cua hai tham so")
print("=" * 64)
k0 = goi(ix.tim, TRUY_VAN["q1"], 4, 0.0, 0.75)
diem_k0 = sorted(round(d, 6) for _, d in k0) if k0 else None
kiem("k1 = 0: d2, d3, d7 bang diem nhau",
     (len(set(diem_k0[1:])) == 1) if diem_k0 else None, True,
     "k1 = 0 xoa han tan so tu, chi con co chua hay khong, nen ba tai"
     " lieu cung chua du ba tu phai bang diem.")
b0 = goi(ix.tim, TRUY_VAN["q1"], 4, 1.2, 0.0)
kiem("b = 0: d3 len dau", b0[0][0] if b0 else None, "d3",
     "b = 0 bo chuan hoa do dai, nen loi the cua d7 mat.")
kiem("b = 0: diem cua d3", b0[0][1] if b0 else None, 2.936244)

print()
print("=" * 64)
print("Nhom 4 --- bo chi so, nhan nhi phan, vi du muoi tai lieu")
print("=" * 64)
kiem("Precision@5", goi(chi_so.precision_at_k, THU_HANG, NHAN_NHI_PHAN, 5),
     0.4, "Mau so la k, khong phai so tai lieu lien quan.")
kiem("Recall@5", goi(chi_so.recall_at_k, THU_HANG, NHAN_NHI_PHAN, 5), 0.5,
     "Mau so la so tai lieu lien quan TRONG KHO, ke ca x11 khong nam"
     " trong thu hang.")
kiem("Recall@10", goi(chi_so.recall_at_k, THU_HANG, NHAN_NHI_PHAN, 10), 0.75)
kiem("Reciprocal rank", goi(chi_so.reciprocal_rank, THU_HANG,
                            NHAN_NHI_PHAN), 0.5)
kiem("Average precision",
     goi(chi_so.average_precision, THU_HANG, NHAN_NHI_PHAN), 0.308333,
     "Mau so la so tai lieu lien quan trong kho, khong phai so tai lieu"
     " lien quan tim duoc.")
kiem("nDCG@10", goi(chi_so.ndcg_at_k, THU_HANG, NHAN_NHI_PHAN, 10), 0.514838)

print()
print("=" * 64)
print("Nhom 5 --- nDCG voi nhan nhieu muc")
print("=" * 64)
nd = goi(chi_so.ndcg_at_k, THU_HANG, NHAN_NHIEU_MUC, 10)
chan_doan = "Mau so phai dung TOAN BO nhan khac khong cua kho, xep theo"
if nd is not None and abs(nd - NDCG_MAU_TU_KET_QUA) < 1e-4:
    chan_doan = ("Mau so dang lay tu cac nhan da truy xuat duoc, nen ba"
                 " tai lieu bi bo sot khong bi tru diem.")
elif nd is not None and abs(nd - NDCG_NEN_NHI_PHAN) < 1e-4:
    chan_doan = ("Nhan nhieu muc dang bi nen ve nhi phan o ca tu so va"
                 " mau so.")
else:
    chan_doan += " do loi giam dan."
kiem("nDCG@10 nhan nhieu muc", nd, 0.652980, chan_doan)

print()
print("=" * 64)
print("Nhom 6 --- truy van khong co tai lieu lien quan nao")
print("=" * 64)
for ten, ham in (("Precision@5", lambda: chi_so.precision_at_k(
                      THU_HANG, {}, 5)),
                 ("Recall@5", lambda: chi_so.recall_at_k(THU_HANG, {}, 5)),
                 ("Reciprocal rank", lambda: chi_so.reciprocal_rank(
                      THU_HANG, {})),
                 ("Average precision", lambda: chi_so.average_precision(
                      THU_HANG, {})),
                 ("nDCG@10", lambda: chi_so.ndcg_at_k(THU_HANG, {}, 10))):
    kiem(ten + " khi qrels rong", goi(ham), 0.0,
         "Phai tra ve 0.0, khong duoc chia cho khong va khong duoc tra"
         " ve nan.")

print()
print("=" * 64)
print("Nhom 7 --- trung binh tren ba truy van cua kho do choi")
print("=" * 64)
tong = {"ndcg": 0.0, "recall": 0.0, "rr": 0.0, "ap": 0.0}
du = True
for mq in sorted(TRUY_VAN):
    th = goi(ix.tim, TRUY_VAN[mq], 6)
    if not th:
        du = False
        continue
    ds = [ma for ma, _ in th]
    q = QRELS[mq]
    tong["ndcg"] += goi(chi_so.ndcg_at_k, ds, q, 10) or 0.0
    tong["recall"] += goi(chi_so.recall_at_k, ds, q, 6) or 0.0
    tong["rr"] += goi(chi_so.reciprocal_rank, ds, q) or 0.0
    tong["ap"] += goi(chi_so.average_precision, ds, q) or 0.0
n = len(TRUY_VAN)
kiem("nDCG@10 trung binh", tong["ndcg"] / n if du else None, 0.793365)
kiem("Recall@6 trung binh", tong["recall"] / n if du else None, 0.833333)
kiem("MRR", tong["rr"] / n if du else None, 0.833333)
kiem("MAP", tong["ap"] / n if du else None, 0.638889)

print()
print("=" * 64)
print("%d / %d phep kiem dat." % (so_dat, so_chay))
if so_dat == so_chay:
    print("Hai tep da dung tren kho do choi. Di tiep sang muc A5.")
else:
    print("Con phep kiem sai. Dung o day, khong di tiep sang muc A5.")
    sys.exit(1)
