# -*- coding: utf-8 -*-
"""Bo chi so danh gia truy xuat, cai tu cong thuc.

Khong duoc nap pytrec_eval, ir_measures, sklearn.metrics hay ham danh gia
cua BEIR trong tep nay. Bon chi so o day se duoc doi chieu voi chung o
muc A5, nen phai doc lap voi chung.

Quy uoc chung cho moi ham:
  thu_hang : danh sach ma tai lieu, xep theo thu tu he thong tra ve
  qrels    : dict ma tai lieu -> muc lien quan, chi gom muc khac khong.
             Tai lieu khong co trong dict nay coi nhu muc 0.
             qrels la nhan cua CA KHO, khong phai nhan cua thu_hang.
  k        : so vi tri dau duoc tinh

Truy van khong co tai lieu lien quan nao thi moi chi so tra ve 0.0.
"""
import math


def precision_at_k(thu_hang:list, qrels, k:int):
    
    """Ty le tai lieu lien quan trong k vi tri dau."""

    if k <= 0: return 0.0

    so_tai_lieu_lien_quan = 0

    for ma_tai_lieu in thu_hang[:k]:
        if qrels.get(ma_tai_lieu, 0) > 0:
            so_tai_lieu_lien_quan += 1
    
    return so_tai_lieu_lien_quan / k

def recall_at_k(thu_hang, qrels, k):

    """Phan tai lieu lien quan cua CA KHO bat duoc trong k vi tri dau."""

    if k <= 0 or len(qrels) == 0: return 0.0

    so_tai_lieu_lien_quan = 0

    for ma_tai_lieu in thu_hang[:k]:
        if qrels.get(ma_tai_lieu, 0) > 0:
            so_tai_lieu_lien_quan += 1

    return so_tai_lieu_lien_quan / len(qrels)

def reciprocal_rank(thu_hang, qrels):

    """Nghich dao thu hang cua tai lieu lien quan dau tien."""

    for index, ma_tai_lieu in enumerate(thu_hang, start = 1):
        if ma_tai_lieu in qrels:
            return 1/ index 

    return 0.0


def average_precision(thu_hang, qrels)->float:
    """Trung binh precision tinh tai moi vi tri co tai lieu lien quan.

    Mau so la so tai lieu lien quan cua ca kho.
    """
    if len(qrels) == 0: return 0.0

    tong_precision = 0.0

    for index, ma_tai_lieu in enumerate(thu_hang, start = 1):
        if ma_tai_lieu in qrels:
            precision = precision_at_k(thu_hang, qrels, index)
            tong_precision += precision

    return tong_precision/len(qrels)


def dcg(loi:list[int], k:int)->float: 

    """DCG@k cua mot day do loi:  sum_{i=1..k}  loi[i] / log2(i + 1)."""

    tong_dcg = 0.0

    for index, muc_lien_quan in enumerate(loi[:k], start = 1):
        tong_dcg += muc_lien_quan / math.log2(index+1)

    return tong_dcg


def ndcg_at_k(thu_hang, qrels, k):

    """DCG@k cua thu hang, chia cho DCG@k cua xep hang ly tuong.

    Xep hang ly tuong lay tu TOAN BO nhan khac khong cua qrels, xep theo
    do loi giam dan - khong lay tu cac nhan tim duoc trong thu_hang.
    """
    if k <= 0 or len(qrels) == 0: return 0.0

    loi = [
        qrels.get(ma_tai_lieu, 0)
        for ma_tai_lieu in thu_hang
    ]
    dcg_cal = dcg(loi, k)

    loi_ly_tuong = sorted(
        [qrels.get(ma, 0) for ma in thu_hang[:k]],
        reverse=True
    )
    idcg = dcg(loi_ly_tuong, k)

    if idcg == 0: return 0.0

    return dcg_cal/idcg


