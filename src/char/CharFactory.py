from src.char.Baizhi import Baizhi
from src.char.Calcharo import Calcharo
from src.char.Changli import Changli
from src.char.CharSkillButton import is_float
from src.char.Chixia import Chixia
from src.char.Danjin import Danjin
from src.char.Jinhsi import Jinhsi
from src.char.Jiyan import Jiyan
from src.char.Mortefi import Mortefi
from src.char.ShoreKeeper import ShoreKeeper
from src.char.Xiangliyao import Xiangliyao
from src.char.Yuanwu import Yuanwu
from src.char.Zhezhi import Zhezhi
from src.char.Verina import Verina
from src.char.Yinlin import Yinlin
from src.char.Taoqi import Taoqi
from src.char.BaseChar import BaseChar, UseFullForteState, UseLiberationState, WWRole
from src.char.HavocRover import HavocRover
from src.char.Sanhua import Sanhua
from src.char.Jianxin import Jianxin
from src.char.Encore import Encore
from typing import Type
from dataclasses import dataclass

from src.char._echoes import Echos
@dataclass
class Character:
    char_name: str
    cls: Type
    res_cd: int
    role: WWRole
    full_con_swap_to: WWRole
    has_unswappable_buff: bool
    use_liberation_sate: UseLiberationState
    use_fullforte_state: UseFullForteState
    echo: Echos

def get_char_by_pos(task, box, index):
    char_list = [
        # Healers
        Character('char_verina',        Verina, 12, WWRole.Healer, WWRole.Default,          False,UseLiberationState.Default,UseFullForteState.Default,     Echos.DEFAULT20),
        Character('char_shorekeeper',   ShoreKeeper, 15, WWRole.Healer, WWRole.SubDps,      False,UseLiberationState.Default,UseFullForteState.Default,     Echos.DEFAULT20),
        Character('char_baizhi',        Baizhi, 16, WWRole.Healer, WWRole.MainDps,          False,UseLiberationState.Default,UseFullForteState.Default,     Echos.DEFAULT20),
        # Supportive    
        Character('char_jianxin',       Jianxin, 12, WWRole.Default, WWRole.MainDps,        True,UseLiberationState.Default,UseFullForteState.Default,      Echos.DEFAULT20),
        Character('char_taoqi',         Taoqi, 15, WWRole.Default, WWRole.MainDps,          True,UseLiberationState.Default,UseFullForteState.Default,      Echos.DEFAULT20),
        Character('char_yuanwu',        Yuanwu, 3, WWRole.Default, WWRole.Default,          False,UseLiberationState.Default,UseFullForteState.Default,     Echos.DEFAULT20),
        # Rest  
        Character('char_rover',         HavocRover, 12, WWRole.MainDps, WWRole.Default,     False,UseLiberationState.Default,UseFullForteState.Default,     Echos.DREAMLESS),
        Character('char_rover_male',    HavocRover, 12, WWRole.MainDps, WWRole.Default,     False,UseLiberationState.Default,UseFullForteState.Default,     Echos.DREAMLESS),
        Character('char_encore',        Encore, 10, WWRole.MainDps, WWRole.Default,         False,UseLiberationState.Default,UseFullForteState.Default,     Echos.INFERNO_RIDER),
        Character('char_danjin',        Danjin, 9999999, WWRole.SubDps, WWRole.MainDps,     True,UseLiberationState.Default,UseFullForteState.Default,      Echos.DREAMLESS),
        Character('char_mortefi',       Mortefi, 14, WWRole.SubDps, WWRole.MainDps,         True,UseLiberationState.Default,UseFullForteState.Default,      Echos.IMPERMANENCE_HERON),
        Character('char_yinlin',        Yinlin, 12, WWRole.Default, WWRole.MainDps,         True,UseLiberationState.Default,UseFullForteState.Default,      Echos.DEFAULT20),
        Character('char_sanhua',        Sanhua, 10, WWRole.Default, WWRole.MainDps,         True,UseLiberationState.Default,UseFullForteState.Default,      Echos.IMPERMANENCE_HERON),
        Character('char_jinhsi',        Jinhsi, 3, WWRole.MainDps, WWRole.Default,          False,UseLiberationState.Default,UseFullForteState.Default,     Echos.JUE),
        Character('chang_changli',      Changli, 12, WWRole.Default, WWRole.MainDps,        True,UseLiberationState.Default,UseFullForteState.Default,      Echos.INFERNO_RIDER),
        Character('char_chixia',        Chixia, 9, WWRole.Default, WWRole.Default,          False,UseLiberationState.Default,UseFullForteState.Default,     Echos.INFERNO_RIDER),
        Character('char_calcharo',      Calcharo, 99999, WWRole.Default, WWRole.Default,    False,UseLiberationState.Default,UseFullForteState.Default,     Echos.DEFAULT20),
        Character('char_jiyan',         Jiyan, 16, WWRole.MainDps, WWRole.Healer,           False,UseLiberationState.Default,UseFullForteState.Default,     Echos.FEILIAN_BERINGAL),
        Character('char_zhezhi',        Zhezhi, 6, WWRole.SubDps, WWRole.MainDps,           True,UseLiberationState.Default,UseFullForteState.Default,      Echos.IMPERMANENCE_HERON),
        Character('char_xiangliyao',    Xiangliyao, 5, WWRole.MainDps, WWRole.Default,      False,UseLiberationState.Default,UseFullForteState.Default,     Echos.DEFAULT20),
        #missing characters Aalto,Youhu,Lingyang, Spectro Rover
    ]
    highest_confidence = 0
    found_char = None
    for char in char_list:
        feature = task.find_one(char.char_name, box=box, threshold=0.6)
        if feature:
            task.log_info(f'found char {char.char_name} {feature.confidence} {highest_confidence}')
            if feature.confidence > highest_confidence:
                highest_confidence = feature.confidence
                found_char = char
    if found_char is not None:
        return found_char.cls(task, index, found_char.res_cd, found_char.role,found_char.full_con_swap_to,
            found_char.has_unswappable_buff, found_char.use_liberation_sate,found_char. use_fullforte_state, found_char.echo)
    task.log_info(f'could not find char {found_char} {highest_confidence}')
    has_cd = task.ocr(box=box)
    if has_cd and is_float(has_cd[0].name):
        task.log_info(f'found char {has_cd[0]} wait and reload')
        task.next_frame()
        return get_char_by_pos(task, box, index)
    if task.debug:
        task.screenshot(f'could not find char {index}')
    return BaseChar(task, index)
