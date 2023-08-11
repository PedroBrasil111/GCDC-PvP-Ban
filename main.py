import random
import cv2
import numpy as np
import mss
import os
import pyautogui
import time

def screen_shot(left=0, top=0, width=1600, height=900):
    stc = mss.mss()
    scr = stc.grab({
        'left': left,
        'top': top,
        'width': width,
        'height': height
    })
    img = np.array(scr)
    img = cv2.cvtColor(img, cv2.IMREAD_COLOR)
    return img

def clicar_botao(screenshot, img):
    result = cv2.matchTemplate(screenshot, img, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if (max_val < 0.8):
        return False
    posicao_centro_y, posicao_centro_x, _ = [size / 2 + random.randint(15, 25) for size in botao_desafio_img.shape]
    pyautogui.moveTo(max_loc[0] + posicao_centro_x, max_loc[1] + posicao_centro_y, duration=random.random())
    pyautogui.click(max_loc[0] + posicao_centro_x, max_loc[1] + posicao_centro_y)
    return True

def banir_personagens(screenshot):
    bans = 0
    personagem = "a"
    with open("ultima_batalha.txt", "w+") as data:
        with open("prioridades.txt", "r") as prioridades:
            while personagem != None and bans < 2:
                personagem = prioridades.readline().strip()
                try:
                    result = cv2.matchTemplate(screenshot, cv2.imread(os.path.join("assets", personagem + ".jpg"), cv2.IMREAD_UNCHANGED), cv2.TM_CCOEFF_NORMED)
                except cv2.error:
                    continue
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                if max_val > 0.8:
                    pyautogui.moveTo(max_loc[0] + 10, max_loc[1] + 20)
                    pyautogui.click(max_loc[0] + 10, max_loc[1] + 20)
                    bans += 1
                    time.sleep(2)
                data.write(f"{personagem}: {max_val}\n")

if __name__ == "__main__":
    botao_desafio_img = cv2.imread(os.path.join("assets", "botao_desafio.jpg"), cv2.IMREAD_UNCHANGED)
    botao_batalha_enabled = cv2.imread(os.path.join("assets", "botao_iniciar_batalha_enabled.jpg"), cv2.IMREAD_UNCHANGED)
    botao_batalha_disabled = cv2.imread(os.path.join("assets", "botao_iniciar_batalha_disabled.jpg"), cv2.IMREAD_UNCHANGED)
    botao_continuar = cv2.imread(os.path.join("assets", "botao_continuar.jpg"), cv2.IMREAD_UNCHANGED)

    time_jitter = random.randint(-1, 1)

    fase = "pick"
    while True:
        cv2.waitKey(2 + time_jitter)
        screenshot = screen_shot()

        if fase == "pick":
            if clicar_botao(screenshot, botao_desafio_img):
                fase = "ban"
                time.sleep(2)

        elif fase == "ban":
            banir_personagens(screenshot)
            time.sleep(2)
            if clicar_botao(screenshot, botao_batalha_enabled):
                fase = "fim"
                time.sleep(30)

        elif fase == "fim":
            if clicar_botao(screenshot, botao_continuar):
                fase = "pick"
                time.sleep(2)

'''
screenshot_tela_img = cv2.imread(os.path.join("assets", "Screenshot_tela.jpg"), cv2.IMREAD_UNCHANGED)
botao_desafio_img = cv2.imread(os.path.join("assets", "botao_desafio.jpg"), cv2.IMREAD_UNCHANGED)
# botao_batalha_img = cv2.imread('', cv2.IMREAD_UNCHANGED)

result = cv2.matchTemplate(screenshot_tela_img, botao_desafio_img, cv2.TM_CCOEFF_NORMED)

# min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
# print(max_val, max_loc)
h = botao_desafio_img.shape[0]
w = botao_desafio_img.shape[1]
# cv2.rectangle(screenshot_tela_img, max_loc, (max_loc[0] + w, max_loc[1] + h), (0, 255, 255), 2)

threshlod = .80
yloc, xloc = np.where(result >= threshlod)

rectangles = []
for (x, y) in zip(xloc, yloc):
    rectangles.append([int(x), int(y), int(w), int(h)])
    rectangles.append([int(x), int(y), int(w), int(h)])

rectangles, weigths = cv2.groupRectangles(rectangles, 1, 0.2)
print(len(rectangles))
for (x, y, w, h) in rectangles:
    cv2.rectangle(screenshot_tela_img, (x, y), (x + w, y + h), (0, 255, 255), 2)



# cv2.imshow("Result", result)
cv2.imshow("screenshot", screenshot_tela_img)
cv2.waitKey()
cv2.destroyAllWindows()
'''