import pygame
from src.line import Line
from src.simulation import Simulation
from src.visualizer import draw


def main():
    line = Line()
    line.load_stations("data/station.csv")
    line.load_segments("data/segments.csv")

    sim = Simulation(line)

    pygame.init()  # Pygame'i başlattığından emin ol

    # Ekranı oluştur (Eğer bunu visualizer.py içinde yapmıyorsan burada yapmalısın)
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("MetroExpressSim - M5 Üsküdar-Sultanbeyli")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        sim.tick()

        # 1. EKRANI TEMİZLE (Siyah arka plan için 0,0,0. Beyaz istersen 255,255,255 yap)
        screen.fill((0, 0, 0))

        # 2. YENİ KAREYİ ÇİZ
        # Not: draw fonksiyonunun içine screen değişkenini göndermen gerekebilir!
        # Örn: draw(screen, line, sim.trains)
        draw(screen, line, sim.trains)

        # 3. EKRANI GÜNCELLE (Bunu yazmazsan ekranda hiçbir değişiklik göremezsin)
        pygame.display.flip()

        pygame.time.delay(30)

    pygame.quit()


if __name__ == "__main__":
    main()