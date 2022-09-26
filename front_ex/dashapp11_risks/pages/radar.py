import numpy as np
import os
import seaborn as sns
import pandas as pd
from ..utils import  get_risk_table
def make_sectors(max_p_rank,max_group_rank, x_s=0):# Определяет таблицу секторов
    x=360/max_group_rank
    bar_theta=[(i+1)*x-x_s for j in range(int(max_p_rank)) for i in range(int(max_group_rank))  ]
    return bar_theta
def less_with_toll(x,y,toll=10^7):# Неравенство с заданой погрешностью
    return x+toll<y
def fibonacci(n): #Числа Фибоначи, гипотеза, что последовательности шаров на каждом новом уровне ей соответствуют.
    fn = [0, 1,]
    for i in range(2, n+2):
        fn.append(fn[i-1] + fn[i-2])
    return fn[2:]

def find_level_size(n,i0=0):# Сколько уровней требуется на одну градацию вероятности
    return np. where(np.cumsum(fibonacci(n+100)[i0:]) >= n)[0][0]+1

def find_first_radius(df,max_p_rank): #Сколько уровней(измеренных в максимальном диаметре маркера) требуется для максимальной вероятности
    r_lvl=1
    for i in df['group_id'].unique():
#         print(i)
        df0=df.loc[(df['group_id']==i) & (df['probability']==max_p_rank)]
#         print(int(np.ceil(df0['weight_per_damage'].sum())))
        r_lvl=max(r_lvl, find_level_size(int(np.ceil(df0['weight_per_damage'].sum()))))
    return r_lvl

def find_other_radius(df,max_p_rank,r_lvl0):#Сколько уровней(измеренных в максимальном диаметре маркера) требуется для остальных вероятностей
    l=[]
    for j in range(int(max_p_rank-1)):
        r_lvl=1
#         print('fg',j)
        for i in df['group_id'].unique():
#             print(i)
            df0=df.loc[(df['group_id']==i) & (df['probability']==max_p_rank-j-1)]

#             print(int(np.ceil(df0['weight_per_damage'].sum())))
            r_lvl=max(r_lvl, find_level_size(int(np.ceil(df0['weight_per_damage'].sum())),i0=r_lvl0 ) )
        l.append(r_lvl)
        r_lvl0=r_lvl0+r_lvl
    return l
def set_color(max_p_rank,max_group_rank,palette='Reds'):# Устанавливает цветовую палитру кругов
    cl=sns.color_palette('Reds')[::-1]#"YlOrBr")
    d_c=(np.array ([*cl[-1]]) -np.array ([*cl[0]]))/max_p_rank
    cc=[tuple((255*(np.array ([*cl[0]])+i * d_c)).tolist()) for i in range(int(max_p_rank))]
    bar_color = [tuple((255*(np.array ([*cl[0]])+i * d_c)).tolist()) for i in range(int(max_p_rank)) for j in range(int(max_group_rank)) ]
    bar_color=['rgb'+str(i) for i in bar_color]
    return bar_color
def get_sectors_coordinats(risks,group_disk,max_p_rank,max_group_rank, x_s=34): # Определяет координаты секторов
    bar_theta=make_sectors(max_p_rank,max_group_rank, x_s=x_s)
    f_r=find_first_radius(risks,max_p_rank)
    o_r=find_other_radius(risks,max_p_rank, f_r)

    y=100/(np.sum(o_r)+f_r-0.5+(0.5/np.sin((bar_theta[0]+360-bar_theta[-1])/2*2*np.pi/360)))#y=100/(np.sum(o_r)+f_r-1+(1/np.sin((bar_theta[0]+360-bar_theta[-1])/2*2*np.pi/360)))
#     bar_r = max_group_rank*[y*(f_r-1+(1/np.sin((bar_theta[0]+360-bar_theta[-1])/2*2*np.pi/360)))]
#     bar_bound=[y*(f_r-1+(1/np.sin((bar_theta[0]+360-bar_theta[-1])/2*2*np.pi/360)))]
    bar_r = max_group_rank*[y*(f_r-0.5+(0.5/np.sin((bar_theta[0]+360-bar_theta[-1])/2*2*np.pi/360)))]
    bar_bound=[y*(f_r-0.5+(0.5/np.sin((bar_theta[0]+360-bar_theta[-1])/2*2*np.pi/360)))]
#     set_trace()
    for i in  o_r:
        bar_r=bar_r+max_group_rank*[y*i]
        bar_bound=bar_bound+[y*i]
    bar_bound=[0]+np.cumsum(bar_bound)[:-1].tolist()
    l_g=5*[-1]
    for k,p in group_disk.items():
        l_g[p]=k
    hover_sec_text=[ l_g[j] for i in range(int(max_p_rank)) for j in range(int(max_group_rank)) ]
    return bar_theta,bar_r,bar_bound,hover_sec_text
def get_circl_info(bar_theta,bar_r,bar_bound,risks, max_p_rank,max_group_rank,max_dam_rank): # Вся инфо по размещению шариков
    trial_1_r = []
    trial_1_theta=[]
    marker_size=[]
    ball_text =[]
    hover_text=[]
    size_marker0=bigest_size

    for i in range(max_group_rank): # Цикл по секторам
        if i==0: #Угол сектора
            alpa=bar_theta[0]+360-bar_theta[-1]
        else:
            alpa=bar_theta[i]-bar_theta[i-1]
        da=bar_theta[i]-alpa/2
        df0=risks.loc[(risks['group_id']==i) ]
        trial_1_r0 = []
        trial_1_theta0=[]
        marker_size0=[]
        ball_text0 =[]
        hover_text0=[]
        lvl=1
    #     is_new=False
#         if i==1:
#             set_trace() 
        for j in range(1,int(max_p_rank)+1)[::-1]: #Цикл по вероятностям

            df01=df0[(df0['probability']==j)].sort_values(by=[ 'damage','n'], ascending=[False,True])
            is_new=True
            lb=bar_bound[int(max_p_rank)-j]# Нижняя граница радиуса, с которого начинается новый уровень заполнения
    #         set_trace() 
            if ~df01.empty:
                for n,group_name,risk_name,probability,damage,group_id,size_marker,weight_per_damage in df01.values:

                    if (len(trial_1_r0)==0) & (lvl==1): #Если самый первый шарик с макс вероятностью
    #                     set_trace() 
                        alpha0=alpa/2
                        r0=[size_marker/np.sin(alpha0*2*np.pi/360),lvl]
                        trial_1_r0.append(r0)
                        trial_1_theta0.append(alpha0)
                        marker_size0.append(size_marker)
                        lb=r0[0]+size_marker
                        lvl=lvl+1
                        is_new=True
                        size_marker0=size_marker
                        ball_text0.append(int(n))
                        hover_text0.append(risk_name)
                    else: # Шарик не угловой
    #                     set_trace() 
                        if less_with_toll(alpa,trial_1_theta0[-1]+alpha0+alpha0*size_marker/size_marker0, toll=1):
                                lvl=lvl+1
                                is_new=True
                        if is_new:# Первый в новом ряду
                            is_new=False
                            r0=[lb+size_marker,lvl]
    #                         set_trace()
                            alpha0=np.arcsin(size_marker/r0[0])/2/np.pi*360
                            alpha0=alpa/int(alpa/alpha0)
                            trial_1_r0.append(r0)
                            trial_1_theta0.append(alpha0)
                            marker_size0.append(size_marker)
                            size_marker0=size_marker
                            lb=r0[0]+size_marker
                            ball_text0.append(int(n))
                            hover_text0.append(risk_name)
                        else: # Не первый в ряду
    #                         print(trial_1_theta0)
                            trial_1_theta0.append(trial_1_theta0[-1]+alpha0+alpha0*size_marker/size_marker0)
                            alpha0=alpha0*size_marker/size_marker0
                            trial_1_r0.append(trial_1_r0[-1])
                            marker_size0.append(size_marker)
                            size_marker0=size_marker
                            ball_text0.append(int(n))
                            hover_text0.append(risk_name)

                else:
                    lvl=lvl+1
        lvl=1
        is_new=False  
        ball_text=ball_text+ball_text0
        hover_text=hover_text+hover_text0
        if len(trial_1_r)==0:
            trial_1_r = [i[0] for i in trial_1_r0]
            trial_1_theta=(np.array(trial_1_theta0)+da).tolist()
            marker_size=marker_size0
            da=bar_theta[1]-alpa/2
        else:
            trial_1_r=trial_1_r+[i[0] for i in trial_1_r0]
            trial_1_theta=trial_1_theta+(np.array(trial_1_theta0)+da).tolist()
            marker_size=marker_size+marker_size0
            da=da+alpa
    return ball_text,trial_1_r,trial_1_theta,marker_size,hover_text

def upload_risks_xslx():
    path_xlsx = os.getcwd()+'/front_ex/files/reestr_risk.xlsx' 
    risks_cols = ['n', 'group_name', 'risk_name', 'probability', 'damage']
    risks=get_risk_table()
    risks.columns = risks_cols
    return risks

koef_resize_markers=0.85
p=5.5
bigest_size=8
b=bigest_size
koef=0.95
koef_r=0.05
try_resize_radius_bounds=True
resize_balles=0.5

 
def main0(risks0,  bigest_size,b,koef,koef_r,try_resize_radius_bounds,resize_balles, masks=None):
    if masks is None:
        risks=risks0
    else:
        risks=risks0[np.array(masks)==1]
    risks.columns = ['n', 'group_name', 'risk_name', 'probability', 'damage']
    risks=risks.loc[(~risks['probability'].isnull() ) & ((~risks['damage'].isnull() ))]
    risks['group_name'] = risks['group_name'].apply(lambda x: str(x).strip())
    group_disk = {}
    l_n=np.sort(risks['group_name'].unique())
    for i in range(len(l_n)):
        group_disk[l_n[i]]=i
    risks['group_id'] = risks['group_name'].apply(lambda x: group_disk.get(x))

    max_p_rank=risks['probability'].max()
    max_dam_rank=risks['damage'].max()
    max_group_rank=l_n.shape[0]


    while True:
        b=bigest_size
        size_per_damage={}
        weight_per_damage={}
        w=1
        for i in range(1,int(max_dam_rank)+1)[::-1]:
            size_per_damage[i]=b
            weight_per_damage[i]=w
            b=b*resize_balles
            w=w*resize_balles
        risks['size_marker'] = risks['damage'].apply(lambda x: size_per_damage.get(x))    
        risks['weight_per_damage'] = risks['damage'].apply(lambda x: weight_per_damage.get(x))  

        bar_theta,bar_r,bar_bound,hover_sec_text=get_sectors_coordinats(risks,group_disk, max_p_rank,max_group_rank, x_s=34)
        ball_text,trial_1_r,trial_1_theta,marker_size,hover_text=get_circl_info(bar_theta,bar_r,bar_bound,risks, max_p_rank,max_group_rank,max_dam_rank)
        bar_color=set_color(max_p_rank,max_group_rank)
        if (np.array ((trial_1_r) + np.array(marker_size)).max())<=100:
            break
        else:
            if try_resize_radius_bounds:
                while try_resize_radius_bounds:
                    try_resize_radius_bounds=False
                    for i in list(range(len(bar_bound)))[-1:0:-1]:
                        df2=pd.DataFrame(np.transpose([trial_1_r,marker_size]), columns=['r','m_s'])
                        df2['end_circl']=df2.sum(axis=1)
                        if  less_with_toll(df2[df2['r']<bar_bound[i]]['end_circl'].max(),bar_bound[i], toll=koef_r*bigest_size ):
                            try_resize_radius_bounds=True
                            bar_bound[i]=df2[df2['r']<bar_bound[i]]['end_circl'].max()+koef_r*bigest_size
                            bar_r=[]
                            bar_bound0=np.diff(bar_bound+[100])
                            for  j in bar_bound0:
                                bar_r=bar_r+max_group_rank*[j]
                            ball_text,trial_1_r,trial_1_theta,marker_size,hover_text=get_circl_info(bar_theta,bar_r,bar_bound,risks, max_p_rank,max_group_rank,max_dam_rank)
                            bar_color=set_color(max_p_rank,max_group_rank)
                if (np.array ((trial_1_r) + np.array(marker_size)).max())<=100:
                    break
            else:
                bigest_size=koef*bigest_size
                try_resize_radius_bounds=True
    return bar_theta,bar_r,bar_bound,hover_sec_text,ball_text,trial_1_r,\
            trial_1_theta,marker_size,hover_text,bar_color
            # risks= pd.read_excel('Реестр рисков.xlsx', engine='openpyxl', header=1)
risks = get_risk_table()#upload_risks_xslx()
bar_theta,bar_r,bar_bound,hover_sec_text,ball_text,trial_1_r,trial_1_theta,marker_size,hover_text,bar_color=main0(risks, bigest_size,b,koef,koef_r,try_resize_radius_bounds,resize_balles)