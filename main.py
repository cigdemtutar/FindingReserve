import re
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from shapely.geometry import Polygon, box


def satiri_oku(dosya, satir_no):
    """'2B(20,20)(30,20)...F' satırını okuyup çokgen listesi döndürür."""
    with open(dosya, encoding="utf-8") as f:
        for satir in f:
            satir = satir.strip()
            m = re.match(r"^(\d+)B(.*)F$", satir)
            if m and int(m.group(1)) == satir_no:
                noktalar = [(int(a), int(b))
                            for a, b in re.findall(r"\((\d+),(\d+)\)", m.group(2))]
                return noktalari_bol(noktalar)
    raise ValueError(f"{satir_no}. satır bulunamadı")


def noktalari_bol(noktalar):
    """İlk noktaya dönülünce çokgen kapanır; yeni çokgen başlar."""
    cokgenler, mevcut = [], []
    for p in noktalar:
        mevcut.append(p)
        if len(mevcut) >= 4 and p == mevcut[0]:
            cokgenler.append(mevcut[:-1])  # tekrar eden son noktayı at
            mevcut = []
    return cokgenler


def kapladigi_hucreler(cokgen_noktalari):
    """Çokgenin sınırından geçtiği ve içinde kalan tüm birim hücreler."""
    poly = Polygon(cokgen_noktalari)
    minx, miny, maxx, maxy = poly.bounds
    hucreler = set()
    for x in range(int(minx), int(maxx) + 1):
        for y in range(int(miny), int(maxy) + 1):
            # yalnızca kenar/köşe teması sayılmasın, iç kesişim olsun
            if poly.intersection(box(x, y, x + 1, y + 1)).area > 1e-9:
                hucreler.add((x, y))
    return hucreler


def ciz1(cokgenler, hucre_kumeleri, rezerv):
    fig, ax = plt.subplots(figsize=(8, 8))
    for hucreler in hucre_kumeleri:
        for (x, y) in hucreler:
            ax.add_patch(Rectangle((x, y), 1, 1, facecolor="lightgray",
                                   edgecolor="none"))
    for c in cokgenler:
        xs = [p[0] for p in c] + [c[0][0]]
        ys = [p[1] for p in c] + [c[0][1]]
        ax.plot(xs, ys, "k-", lw=1.5)
        ax.scatter(xs, ys, c="red", s=15, zorder=3)
    ax.set_xlim(0, 60)
    ax.set_ylim(60, 0)          # (0,0) sol üst, y aşağı doğru artar
    ax.set_aspect("equal")
    ax.grid(True, lw=0.3)
    ax.set_title(f"Rezerv bölgesi | Rezerv değeri = {rezerv}")
    plt.show()


if __name__ == "__main__":
    satir_no = int(input("Kaçıncı satır? "))
    birim_sondaj = float(input("Birim sondaj maliyeti (1-10): "))
    birim_platform = float(input("Birim platform maliyeti: "))

    cokgenler = satiri_oku("koordinatlar.txt", satir_no)
    hucre_kumeleri = [kapladigi_hucreler(c) for c in cokgenler]

    toplam_alan = sum(len(h) for h in hucre_kumeleri)
    rezerv = toplam_alan * 10

    for i, h in enumerate(hucre_kumeleri, 1):
        print(f"Çokgen {i}: {len(h)} br²")
    print(f"Toplam alan: {toplam_alan} br² | Rezerv değeri: {rezerv}")

    ciz1(cokgenler, hucre_kumeleri, rezerv)