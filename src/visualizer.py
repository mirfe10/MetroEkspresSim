import pygame

# ─── RENKLER ───────────────────────────────────────────────────────────────────
BG           = (14, 17, 23)
LINE_COLOR   = (70, 85, 100)
POCKET_FILL  = (20, 32, 48)
POCKET_WALL  = (40, 110, 150)
EXPR_WALL    = (220, 180, 40)
STATION_DOT  = (190, 210, 235)
TEXT_COLOR   = (160, 185, 210)
LOCAL_CLR    = (247, 127,   0)
EXPRESS_CLR  = (214,  40,  40)
WAIT_GLOW    = ( 50, 200, 110)
WHITE        = (255, 255, 255)
CONNECTOR    = ( 55,  70,  88)

# ─── LAYOUT ────────────────────────────────────────────────────────────────────
# 24 istasyon → 3 satır × 8 istasyon
# Satır 0: sol→sağ  (indeks  0-7 )
# Satır 1: sağ→sol  (indeks  8-15)
# Satır 2: sol→sağ  (indeks 16-23)
ROW_SPLIT  = 8          # Satır başına istasyon
ROW_YS     = [140, 340, 540]   # Her satırın Y konumu
LEFT_X     = 90
RIGHT_X    = 1190
POCKET_H   = 35         # Cep derinliği (aşağı doğru)
POCKET_W   = 14         # Cep yarı genişliği


def _station_screen_pos(idx):
    """İstasyon indeksini (0-23) ekran koordinatına çevir."""
    row = idx // ROW_SPLIT
    col = idx %  ROW_SPLIT
    total_cols = ROW_SPLIT - 1

    # Çift satır: sol→sağ, tek satır: sağ→sol (yılan)
    if row % 2 == 0:
        x = int(LEFT_X + col / total_cols * (RIGHT_X - LEFT_X))
    else:
        x = int(RIGHT_X - col / total_cols * (RIGHT_X - LEFT_X))

    y = ROW_YS[row]
    return x, y


def _train_screen_pos(train, stations):
    """Trenin position_m'sine göre iki istasyon arasında enterpolasyon yap."""
    pos = train.position_m

    # Hangi iki istasyon arasında?
    for i in range(len(stations) - 1):
        a = stations[i]
        b = stations[i + 1]
        a_m = a.km * 1000
        b_m = b.km * 1000
        if a_m <= pos <= b_m:
            t = (pos - a_m) / (b_m - a_m) if b_m != a_m else 0
            ax, ay = _station_screen_pos(i)
            bx, by = _station_screen_pos(i + 1)

            # Satır değişimi varsa tam başlangıç/bitiş noktasına çivile
            if ay != by:
                # Bağlantı geçişi – trenin konumuna göre hangi satırda olduğunu belirle
                if t < 0.5:
                    return ax, ay
                else:
                    return bx, by

            return int(ax + t * (bx - ax)), ay

    # Hat sonu
    return _station_screen_pos(len(stations) - 1)


def draw(screen, line, trains):
    screen.fill(BG)
    pygame.font.init()
    font_sm  = pygame.font.SysFont("Arial", 10, bold=True)
    font_st  = pygame.font.SysFont("Arial",  9)
    font_inf = pygame.font.SysFont("Arial", 12, bold=True)

    stations = line.stations
    n = len(stations)
    if n < 2:
        return

    # ── 1. SATIR ÇİZGİLERİ ─────────────────────────────────────────────────────
    for i in range(n - 1):
        ax, ay = _station_screen_pos(i)
        bx, by = _station_screen_pos(i + 1)

        if ay == by:
            # Aynı satır → düz çizgi
            pygame.draw.line(screen, LINE_COLOR, (ax, ay), (bx, by), 4)
        else:
            # Farklı satır → bağlantı köşesi (dikey + yatay)
            # Dikey bağlantı: ax üzerinden ay→by
            pygame.draw.line(screen, CONNECTOR, (ax, ay), (ax, by), 3)
            # Yatay bağlantı: ax'ten bx'e by'de
            pygame.draw.line(screen, CONNECTOR, (ax, by), (bx, by), 3)

    # ── 2. CEP KUTULARI ────────────────────────────────────────────────────────
    for i, st in enumerate(stations):
        sx, sy = _station_screen_pos(i)

        pw, ph = POCKET_W, POCKET_H
        rect = pygame.Rect(sx - pw, sy, pw * 2, ph)
        pygame.draw.rect(screen, POCKET_FILL, rect)
        border = EXPR_WALL if st.express_stop else POCKET_WALL
        pygame.draw.rect(screen, border, rect, 2)

        # İstasyon noktası
        pygame.draw.circle(screen, STATION_DOT, (sx, sy), 5)
        if st.express_stop:
            pygame.draw.circle(screen, EXPR_WALL, (sx, sy), 9, 2)

        # İstasyon adı
        row = i // ROW_SPLIT
        col = i %  ROW_SPLIT
        # Zikzak: çift indeks üstte, tek indeks altta
        if row % 2 == 0:
            name_y = sy - 28 if col % 2 == 0 else sy + ph + 6
        else:
            name_y = sy - 28 if col % 2 == 1 else sy + ph + 6

        lbl = font_st.render(st.name, True, TEXT_COLOR)
        screen.blit(lbl, lbl.get_rect(center=(sx, name_y)))

    # ── 3. TRENLERİ ÇİZ ────────────────────────────────────────────────────────
    for train in trains:
        color    = EXPRESS_CLR if train.train_type == "EXPRESS" else LOCAL_CLR
        in_dwell = train.state in ("DWELL", "WAITING_FOR_EXPRESS")

        if in_dwell and train.current_station:
            # Cep içine yerleştir
            idx = next((i for i, s in enumerate(stations)
                        if s.id == train.current_station.id), None)
            if idx is None:
                continue
            sx, sy = _station_screen_pos(idx)
            tw, th = 22, 14
            dx = sx - tw // 2
            dy = sy + (POCKET_H - th) // 2

            if train.state == "WAITING_FOR_EXPRESS":
                pygame.draw.rect(screen, WAIT_GLOW,
                                 (dx - 2, dy - 2, tw + 4, th + 4), 2)
            pygame.draw.rect(screen, color, (dx, dy, tw, th))
            lbl = font_sm.render(train.id, True, WHITE)
            screen.blit(lbl, (dx + 1, dy + 2))

        else:
            # Ana hat üzerinde hareket – satır Y'sinin 10px üstünde
            tx, ty = _train_screen_pos(train, stations)
            tw, th = 20, 12
            dx = tx - tw // 2
            dy = ty - th - 6
            pygame.draw.rect(screen, color, (dx, dy, tw, th))
            lbl = font_sm.render(train.id, True, WHITE)
            screen.blit(lbl, (dx + 1, dy + 1))

    # ── 4. BİLGİ PANELİ ────────────────────────────────────────────────────────
    local_c   = sum(1 for t in trains if t.train_type == "LOCAL")
    express_c = sum(1 for t in trains if t.train_type == "EXPRESS")
    running_c = sum(1 for t in trains if t.state == "RUNNING")
    waiting_c = sum(1 for t in trains if t.state == "WAITING_FOR_EXPRESS")

    for i, txt in enumerate([
        f"Aktif Tren : {len(trains)}",
        f"  LOCAL    : {local_c}",
        f"  EXPRESS  : {express_c}",
        f"Hareket    : {running_c}",
        f"Bekliyor   : {waiting_c}",
    ]):
        screen.blit(font_inf.render(txt, True, TEXT_COLOR), (14, 12 + i * 18))

    # ── 5. AÇIKLAMA ─────────────────────────────────────────────────────────────
    legend = [
        ("■ LOCAL",        LOCAL_CLR),
        ("■ EXPRESS",      EXPRESS_CLR),
        ("● Ekspres Durağı", EXPR_WALL),
        ("[W] Kapı Açık",  WAIT_GLOW),
    ]
    ly = 12
    for txt, clr in legend:
        s = pygame.font.SysFont("Arial", 11).render(txt, True, clr)
        screen.blit(s, (RIGHT_X - 160, ly))
        ly += 16