############################
#   2023夏休みゲーム制作
#   j2226 髙橋樹生
############################

import tkinter as tk
import openpyxl as xl
import time
import random
from pygame import mixer
import keyboard


# 初期化
def init():
    # BGM
    mixer.init()
    mixer.music.load("sound/bgm.mp3")
    mixer.music.play(-1)
    global correct
    correct = 0
    global wrong
    wrong = 0
    global through
    through = 0
    global Fill
    Fill = "OrangeRed1"
    global result_now
    global game_active
    game_active = False
    result_now = -1
    select_btn1.place_forget()
    select_btn2.place_forget()
    select_btn3.place_forget()
    Choose_btn_white()
    Choose_btn_disable()
    Choose_btn_place_forget()
    textbox.delete("1.0", "end")
    textbox.place_forget()
    btn.place_forget()
    timelabel.place_forget()
    background.itemconfig("back", fill="OrangeRed1")
    background.delete("correct_img")
    background.delete("wrong_img")
    background.delete("rect")
    replay_next.place_forget()
    replay_prev.place_forget()
    background.delete("correct_text")
    background.delete("wrong_text")
    background.delete("mode_text")
    background.delete("difficulity_text")
    if not result:
        replay_btn["state"] = "disable"
    else:
        replay_btn["state"] = "normal"
    background.update()


# モード、難易度選択のボタンを設置
def Select():
    global mode
    mode = 0
    background.create_image(640, 240, image=small_title_img, tag="title")
    select_btn1["command"] = lambda: Select_Mode(0)
    select_btn1["text"] = modes[0]
    select_btn2["command"] = lambda: Select_Mode(1)
    select_btn2["text"] = modes[1]
    select_btn3["command"] = lambda: Select_Mode(2)
    select_btn3["text"] = modes[2]
    select_btn1.place(x=460, y=360)
    select_btn2.place(x=460, y=480)
    select_btn3.place(x=460, y=600)
    replay_btn.place(x=1120, y=590)
    background.update()


def Select_Mode(i):
    pikon = mixer.Sound("sound/enter.mp3")
    pikon.play(0)
    background.update()
    global mode
    mode = i
    select_btn1["command"] = lambda: Select_Difficulity(0)
    select_btn1["text"] = difficulities[0]
    select_btn2["command"] = lambda: Select_Difficulity(1)
    select_btn2["text"] = difficulities[1]
    select_btn3["command"] = lambda: Select_Difficulity(2)
    select_btn3["text"] = difficulities[2]
    background.create_text(
        1100, 60, font=("Ariel", 40), text=modes[mode], fill="white", tag="mode_text"
    )
    background.update()


def Select_Difficulity(i):
    pikon = mixer.Sound("sound/enter.mp3")
    pikon.play(0)
    global difficulity
    difficulity = i
    global is_quiztime
    is_quiztime = 1
    global Fill
    if difficulity == 0:
        Fill = "Green"
    if difficulity == 1:
        Fill = "Blue"
    if difficulity == 2:
        Fill = "OrangeRed1"

    select_btn1.place_forget()
    select_btn2.place_forget()
    select_btn3.place_forget()
    background.itemconfig("back", fill=Fill)
    background.delete("title")
    background.create_text(
        465, 60, font=("Ariel", 60), text=correct, tag="correct_text", fill="white"
    )
    background.create_text(
        820, 60, font=("Ariel", 60), text=wrong, tag="wrong_text", fill="white"
    )
    background.create_image(545, 65, image=small_correct_img, tag="correct_img")
    background.create_image(745, 65, image=small_wrong_img, tag="wrong_img")
    background.create_rectangle(605, 55, 685, 75, fill="white", tag="rect")
    background.create_text(
        100,
        60,
        font=("Ariel", 50),
        text=difficulities[difficulity],
        fill="white",
        tag="difficulity_text",
    )
    background.lift("correct_img")
    replay_btn.place_forget()
    background.update()
    time.sleep(0.5)
    Quiz()


def Quiz():
    global sheet
    sheet = book[difficulities[difficulity]]
    result.clear()
    global result_dif
    result_dif = difficulity
    global result_now
    result_now = 0
    global game_active
    game_active = True

    # 乱数を生成
    lists = []
    for i in range(100):
        lists.append(i + 2)
    rands = random.sample(lists, 100)

    for x in rands:
        if not game_active:
            return
        # 初期化
        textbox.delete("1.0", "end")
        textbox.place_forget()
        global is_thinktime
        is_thinktime = False
        global is_quiztime
        is_quiztime = True
        txt = sheet["B" + str(x)].value
        Choose_btn_place_forget()
        timelabel["fg"] = "black"

        choose_lists = [0, 1, 2, 3]
        global choose_rand
        choose_rand = random.sample(choose_lists, 4)
        btn["command"] = lambda: is_PushBtn(txt)
        Choose_btn_white()
        choose_btn1["text"] = sheet["C" + str(x)].value
        choose_btn2["text"] = sheet["D" + str(x)].value
        choose_btn3["text"] = sheet["E" + str(x)].value
        choose_btn4["text"] = sheet["F" + str(x)].value
        choose_btn1["command"] = lambda: Choose_Correct(choose_btn1)
        choose_btn2["command"] = lambda: Choose_Wrong(choose_btn2)
        choose_btn3["command"] = lambda: Choose_Wrong(choose_btn3)
        choose_btn4["command"] = lambda: Choose_Wrong(choose_btn4)
        Choose_btn_normal()

        if mode == 1:
            if correct >= 7:
                GameClear()
                return
            if wrong >= 3:
                GameOver()
                return
        elif mode == 2:
            if correct >= 5:
                GameClear()
                return
            if wrong >= 2:
                GameOver()
                return

        result.append(x)
        mondai_img = tk.PhotoImage(file="image/mondai.png")
        background.create_image(650, 250, image=mondai_img, tag="mondai")
        background.update()
        mixer.music.stop()
        deden = mixer.Sound("sound/deden.mp3")
        deden.play(0)
        time.sleep(2)
        textbox.place(x=240, y=150, width=800, height=180)
        background.delete("mondai")
        # BGM
        mixer.init()
        mixer.music.load("sound/thinking.mp3")
        mixer.music.play(-1)
        btn.place(x=450, y=400)

        for a in txt:
            if not game_active:
                return
            if is_thinktime == True:
                break
            else:
                time.sleep(0.12)
            if keyboard.is_pressed("space"):
                is_PushBtn(txt)
            textbox.insert(tk.END, a)
            textbox.update()

        if is_quiztime == True:

            for b in range(51):
                time.sleep(0.1)
                timelabel["text"] = "{:.1f}".format(5 - (b / 10))
                timelabel.place(x=1050, y=200)
                background.update()
                if is_quiztime == False:
                    break
            background.update()
            timelabel.place_forget()
            btn.place_forget()
            background.update()
            time.sleep(0.5)
            Choose_btn_disable()
            choose_btn1["bg"] = "RED"
            Choose_btn_place()
            background.update()
            time.sleep(3)
            choose_btn1["bg"] = "RED"
            background.update()
        else:
            background.update()
            time.sleep(3)
            choose_btn1["bg"] = "RED"
            background.update()
        continue
    main()


def Choose_btn_place():
    choose_btn1.place(x=choose_rand[0] * 315 + 15, y=400)
    choose_btn2.place(x=choose_rand[1] * 315 + 15, y=400)
    choose_btn3.place(x=choose_rand[2] * 315 + 15, y=400)
    choose_btn4.place(x=choose_rand[3] * 315 + 15, y=400)


def Choose_btn_place_forget():
    choose_btn1.place_forget()
    choose_btn2.place_forget()
    choose_btn3.place_forget()
    choose_btn4.place_forget()


def Choose_btn_normal():
    choose_btn1["state"] = "normal"
    choose_btn2["state"] = "normal"
    choose_btn3["state"] = "normal"
    choose_btn4["state"] = "normal"


def Choose_btn_disable():
    choose_btn1["state"] = "disable"
    choose_btn2["state"] = "disable"
    choose_btn3["state"] = "disable"
    choose_btn4["state"] = "disable"


def Choose_btn_white():
    choose_btn1["bg"] = "white"
    choose_btn2["bg"] = "white"
    choose_btn3["bg"] = "white"
    choose_btn4["bg"] = "white"


def is_PushBtn(txt):
    global is_thinktime
    is_thinktime = True
    global is_quiztime
    is_quiztime = False
    pikon = mixer.Sound("sound/push.mp3")
    pikon.play(0)

    btn.place_forget()
    Choose_btn_place()
    background.update()

    for t in range(101):
        timelabel["text"] = (100 - t) / 10
        timelabel.place(x=1080, y=150)
        if is_thinktime == False:
            break
        if (100 - t) / 10 < 3:
            timelabel["fg"] = "red"
        background.update()
        time.sleep(0.1)

    if is_thinktime == True:
        global correct
        global wrong
        textbox.delete("1.0", "end")
        textbox.insert(tk.END, txt)
        batsu = mixer.Sound("sound/batsu.mp3")
        batsu.play(0)
        time.sleep(0.7)
        Choose_btn_disable()
        choose_btn1["bg"] = "red"
        if mode == 2:
            correct = 0
        wrong += 1
    background.itemconfig("correct_text", text=correct)
    background.itemconfig("wrong_text", text=wrong)
    timelabel.place_forget()
    background.update()


def Choose_Correct(self):
    global is_thinktime
    is_thinktime = False
    global correct
    correct = correct + 1
    timelabel.place_forget()
    maru = mixer.Sound("sound/maru.mp3")
    maru.play(0)
    self["bg"] = "RED"
    Choose_btn_disable()
    background.itemconfig("correct_text", text=correct)
    background.update()


def Choose_Wrong(self):
    global is_thinktime
    is_thinktime = False
    global wrong
    wrong = wrong + 1
    global correct
    timelabel.place_forget()
    batsu = mixer.Sound("sound/batsu.mp3")
    batsu.play(0)
    self["bg"] = "BLUE"
    choose_btn1["bg"] = "RED"
    Choose_btn_disable()
    if mode == 2:
        correct = 0
    background.itemconfig("wrong_text", text=wrong)
    background.update()


def GameClear():
    Gclear_label = tk.Label(
        root,
        text="GameClear!!\nおめでとう!!",
        font=("Ariel", 70, "bold"),
        fg="BLACK",
        bg="WHITE",
    )
    Gclear_label.place(x=390, y=270)
    background.update()
    mixer.music.stop()
    clear = mixer.Sound("sound/game_clear.mp3")
    clear.play(0)
    time.sleep(4.5)
    Gclear_label.place_forget()
    # main()
    init()
    Select()


def GameOver():
    Gover_label = tk.Label(
        root, text="GameOver...", font=("Ariel", 70, "bold"), fg="BLACK", bg="WHITE"
    )
    Gover_label.place(x=390, y=280)
    background.update()
    mixer.music.stop()
    over = mixer.Sound("sound/game_over.mp3")
    over.play(0)
    time.sleep(4.5)
    Gover_label.place_forget()
    # main()
    init()
    Select()


def Replay():
    global sheet
    sheet = book[difficulities[result_dif]]
    result_txt = sheet["B" + str(result[result_now])].value
    replay_btn.place_forget()
    select_btn1.place_forget()
    select_btn2.place_forget()
    select_btn3.place_forget()
    background.delete("title")
    textbox.place(x=240, y=150, width=800, height=180)
    result_txt
    textbox.delete("1.0", "end")
    textbox.insert(tk.END, result_txt)
    replay_next.place(x=800, y=600)
    replay_prev.place(x=350, y=600)
    choose_btn1["text"] = sheet["C" + str(result[result_now])].value
    choose_btn2["text"] = sheet["D" + str(result[result_now])].value
    choose_btn3["text"] = sheet["E" + str(result[result_now])].value
    choose_btn4["text"] = sheet["F" + str(result[result_now])].value
    Choose_btn_place()
    choose_btn1["bg"] = "red"
    if result_now == -(len(result)):
        replay_next["state"] = "disable"
    else:
        replay_next["state"] = "normal"
    if result_now == -1:
        replay_prev["state"] = "disable"
    else:
        replay_prev["state"] = "normal"
    Replay_btn_place()


def Replay_Next():
    global result_now
    result_now = result_now - 1
    Replay()


def Replay_Prev():
    global result_now
    result_now = result_now + 1
    Replay()


def Replay_btn_place():
    choose_btn1.place(x=0 * 315 + 15, y=400)
    choose_btn2.place(x=1 * 315 + 15, y=400)
    choose_btn3.place(x=2 * 315 + 15, y=400)
    choose_btn4.place(x=3 * 315 + 15, y=400)


def Exit():
    root.destroy()


win_width = 1280
win_height = 800
# 初期化
FONT = ("Ariel", 25)
# WHITE = (255,255,255)
root = tk.Tk()
root.title("お試し")
root.geometry("1280x800")
root.state("zoomed")
background = tk.Canvas(root, width=win_width, height=win_height, bg="WHITE")
background.pack()
book = xl.load_workbook("Quiz_data.xlsx")
btn_img = tk.PhotoImage(file="image/button.png")
small_btn_img = btn_img.subsample(2, 2)
btn = tk.Button(background, image=small_btn_img, command=is_PushBtn)
Fill = "OrangeRed1"

# 終了ボタン
exit_btn = tk.Button(
    background, text="終了", font=FONT, command=Exit, width=7, height=3
)
exit_btn.place(x=10, y=590)
is_thinktime = False
is_quiztime = False

# ホームに戻るボタン
home_img = tk.PhotoImage(file="image/home.png")
small_home_img = home_img.subsample(5, 5)
home_button = tk.Button(background, image=small_home_img, command=lambda: main())
home_button.place(x=150, y=588)

# モード、難易度表示
title_img = tk.PhotoImage(file="image/title3.png")
small_title_img = title_img.subsample(2, 2)
modes = ("フリープレイ", "7マル3バツ", "5 UP-DOWN")
difficulities = ("初級", "中級", "上級")
background.create_rectangle(0, 0, win_width, 125, fill=Fill, tag="back")

# 復習
replay_btn = tk.Button(
    background, text="復習", font=FONT, width=7, height=3, command=lambda: Replay()
)
replay_next = tk.Button(
    background, text="＞", font=FONT, width=5, height=2, command=lambda: Replay_Next()
)
replay_prev = tk.Button(
    background, text="＜", font=FONT, width=5, height=2, command=lambda: Replay_Prev()
)
# 問題履歴
result = []
result_dif = []
result_now = 0
result_txt = 0

# textbox
textbox = tk.Text(background, font=FONT)
# timelabel
timelabel = tk.Label(background, font=("Ariel", 80))
timelabel["bg"] = "white"

# 難易度選択のボタン変数
select_btn1 = tk.Button(background, font=("Ariel", 22), width=20, height=3)
select_btn2 = tk.Button(background, font=("Ariel", 22), width=20, height=3)
select_btn3 = tk.Button(background, font=("Ariel", 22), width=20, height=3)

# 四択選択肢のボタン変数
choose_btn1 = tk.Button(background, font=("Ariel", 20), width=21, height=6)
choose_btn2 = tk.Button(background, font=("Ariel", 20), width=21, height=6)
choose_btn3 = tk.Button(background, font=("Ariel", 20), width=21, height=6)
choose_btn4 = tk.Button(background, font=("Ariel", 20), width=21, height=6)

choose_btn1["command"] = lambda: Choose_Correct(choose_btn1)
choose_btn2["command"] = lambda: Choose_Wrong(choose_btn2)
choose_btn3["command"] = lambda: Choose_Wrong(choose_btn3)
choose_btn4["command"] = lambda: Choose_Wrong(choose_btn4)


# マルとバツのカウント表示
correct = 0
wrong = 0
correct_img = tk.PhotoImage(file="image/maru.png")
small_correct_img = correct_img.subsample(4, 4)
wrong_img = tk.PhotoImage(file="image/batsu.png")
small_wrong_img = wrong_img.subsample(4, 4)

game_active = False


def main():
    init()
    Select()
    # root.mainloop()


if __name__ == "__main__":
    main()
    root.mainloop()
