from chi_so import ndcg_at_k, dcg


# Cách 1: Tính nDCG đúng
def cach_1(thu_hang, qrels, k):
    return ndcg_at_k(thu_hang, qrels, k)


# Cách 2: Tính sai IDCG vì chỉ lấy tài liệu đã tìm thấy
def cach_2(thu_hang, qrels, k):

    loi = [
        qrels.get(ma_tai_lieu, 0)
        for ma_tai_lieu in thu_hang
    ]

    dcg_cal = dcg(loi, k)

    loi_sai = []

    for ma_tai_lieu in thu_hang[:k]:
        if qrels.get(ma_tai_lieu, 0) > 0:
            loi_sai.append(qrels[ma_tai_lieu])

    loi_ly_tuong_sai = sorted(loi_sai, reverse=True)

    idcg_sai = dcg(loi_ly_tuong_sai, k)

    if idcg_sai == 0:
        return 0.0

    return dcg_cal / idcg_sai

#cách 3: Nhị phân loi cho cả tử số và mẫu số
def cach_3(thu_hang, qrels, k):
    
    loi_nhi_phan = []
    
    for ma_tai_lieu in thu_hang:
        if qrels.get(ma_tai_lieu, 0) > 0:
            loi_nhi_phan.append(1)
        else:
            loi_nhi_phan.append(0)

    dcg_cal = dcg(loi_nhi_phan, k)

    loi_ly_tuong = []

    for muc_lien_quan in qrels.values():
        if muc_lien_quan > 0:
            loi_ly_tuong.append(1)
        else:
            loi_ly_tuong.append(0)
    loi_ly_tuong = sorted(loi_ly_tuong, reverse=True)
    
    idcg = dcg(loi_ly_tuong, k)

    if idcg == 0: return 0.0

    return dcg_cal/idcg

def main():
    thu_hang = [
        "x1", "x2", "x3", "x4", "x5",
        "x6", "x7", "x8", "x9", "x10"
    ]

    qrels = {
        "x1": 2,
        "x3": 3,
        "x5": 1,
        "x8": 1,
        "x20": 2,
        "x21": 1
    }

    k = 10

    print(f"Cách 1 (đúng): {cach_1(thu_hang, qrels, k):.6f}")
    print(f"Cách 2 (sai):  {cach_2(thu_hang, qrels, k):.6f}")
    print(f"Cách 3 (nhị phân): {cach_3(thu_hang, qrels, k):.6f}")

if __name__ == "__main__":
    main()