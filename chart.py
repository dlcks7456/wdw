import io
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.ticker as ticker
matplotlib.rcParams['font.family'] = 'NanumGothic'
matplotlib.rcParams['font.size'] = 11 # 글자 크기
matplotlib.rcParams['axes.unicode_minus'] = False # 한글 폰트 사용 시, 마이너스 글자가 깨지는 현상을 방지
import dbconn
from math import pi


def spider_chart(dicts) :
    df = pd.DataFrame(dicts)
    sp = df.shape[0]
    labels = df.columns[1:]
    num_labels = len(labels)
    angles = [x / float(num_labels) * (2 * pi) for x in range(num_labels)]  ## 각 등분점
    angles += angles[:1]  ## 시작점으로 다시 돌아와야하므로 시작점 추가

    my_palette = plt.cm.get_cmap("Set2", len(df.index))

    fig = Figure()
    FigureCanvas(fig)

    fig = plt.figure(figsize=(7, 5))
    fig.set_facecolor('white')
    ax = fig.add_subplot(polar=True)
    for i, row in df.iterrows():
        color = my_palette(i)
        data = df.iloc[i].drop('pname').tolist()
        data += data[:1]

        ax.set_theta_offset(pi / 2)  ## 시작점
        ax.set_theta_direction(-1)  ## 그려지는 방향 시계방향

        plt.xticks(angles[:-1], labels, fontsize=13)  ## 각도 축 눈금 라벨
        ax.tick_params(axis='x', which='major', pad=15)  ## 각 축과 눈금 사이에 여백을 준다.

        ax.set_rlabel_position(0)  ## 반지름 축 눈금 라벨 각도 설정(degree 단위)
        plt.yticks([1, 2, 3, 4, 5], ['1', '2', '3', '4', '5'], fontsize=10)  ## 반지름 축 눈금 설정
        plt.ylim(0, 5)

        ax.plot(angles, data, color=color, linewidth=2, linestyle='solid', label=row.pname)  ## 레이더 차트 출력
        ax.fill(angles, data, color=color, alpha=0.4)  ## 도형 안쪽에 색을 채워준다.

    if sp >= 2 :
        plt.legend(loc=(0.8, 0.8))

    img = io.StringIO()
    plt.savefig(img, format='svg', transparent = True)
    spider = '<svg' + img.getvalue().split('<svg')[1]
    plt.cla()

    return spider

def custom_autopct(pct) :
    return ('%.1f%%' % pct) if pct >= 10 else ''
    #return '{:.1f}%'.format(pct) if pct >= 10 else ''
    #return '{:.0f}%'.format(pct) if pct >= 10 else ''

def gender_pie() :
    all_data = dbconn.Database().executeAll(f"select * from sunny where status='complete';")
    df = pd.DataFrame(all_data)
    gender = {
        1 : "남자",
        2 : "여자"
    }


    values = []
    labels = []
    for value, label in gender.items() :
        values.append(df[df['gender'] == value].shape[0])
        labels.append(label)

    fig = Figure()
    FigureCanvas(fig)

    wedeprops = {'width': 0.6, 'edgecolor': 'w', 'linewidth': 3}
    plt.pie(values,
            labels=labels,
            autopct=custom_autopct,
            colors=['#66b3ff','#ff9999'],
            wedgeprops=wedeprops,
            pctdistance=0.7)

    img = io.StringIO()
    plt.savefig(img, format='svg')
    pie = '<svg' + img.getvalue().split('<svg')[1]
    plt.cla()

    return pie

def position_by_gender() :
    all_data = dbconn.Database().executeAll(f"select * from sunny where status='complete';")
    df = pd.DataFrame(all_data)
    gender = {
        1 : "남자",
        2 : "여자"
    }
    position = {
        "Type1" : "Position1",
        "Type2" : "Position2",
        "Type3" : "Position3",
        "Type4" : "Position4",
        "Type5" : "Position5",
        "Type6" : "Position6"
    }

    fig = Figure()
    FigureCanvas(fig)

    labels = np.arange(len(position.keys()))
    xname = [value for value in position.values() ]

    man_values = []
    woman_values = []
    for pos_val in position.keys() :
        man_filt = (df['position']==pos_val) & (df['gender']==1)
        woman_filt = (df['position'] == pos_val) & (df['gender'] == 2)

        man_values.append(df[man_filt].shape[0])
        woman_values.append((df[woman_filt].shape[0]))

    plt.figure(figsize=(4, 4.8))
    plt.bar(labels - 0.15, man_values, width=0.3, color='#66b3ff', label="남자")
    plt.bar(labels + 0.15, woman_values, width=0.3, color='#ff9999', label="여자")
    plt.legend(loc="upper left")
    plt.xticks(labels, xname, rotation=60)
    plt.ylim(0, 10)
    plt.grid(alpha=0.5)
    plt.gcf().subplots_adjust(bottom=0.3)

    img = io.StringIO()

    plt.savefig(img, format='svg')

    bar = '<svg' + img.getvalue().split('<svg')[1]
    plt.cla()

    return bar