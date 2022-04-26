from glob import escape
import auto_derby
from auto_derby.constants import TrainingType
from auto_derby.single_mode.commands import Command, TrainingCommand, RaceCommand, GoOutCommand
from auto_derby.single_mode import Context, condition
from auto_derby.single_mode.item import EffectSummary


class Plugin(auto_derby.Plugin):
    def install(self) -> None:

        buff2_list = ["スイートカップケーキ","プレーンカップケーキ","バイタル20","バイタル40"]
        hammers_list = ["蹄鉄ハンマー・極","蹄鉄ハンマー・匠"]
        buff3_list = ["パワーアンクルウェイト","ブートキャンプメガホン","スピードアンクルウェイト","スイートカップケーキ","プレーンカップケーキ","バイタル20","バイタル40"]
        purchase_list = ["スピードのメモ帳","スタミナのメモ帳","パワーのメモ帳","根性のメモ帳","賢さのメモ帳","賢さ戦術書","根性戦術書","パワー戦術書","スタミナ戦術書","スピード戦術書",\
        "スピード戦術書","スピード秘伝書","スタミナ秘伝書","パワー秘伝書","根性秘伝書","賢さ秘伝書","パワートレーニング嘆願書","スピードトレーニング嘆願書",\
        "蹄鉄ハンマー・極","蹄鉄ハンマー・匠","ブートキャンプメガホン","スピードアンクルウェイト","パワーアンクルウェイト","プレーンカップケーキ","にんじんBBQセット","博学帽子","スイートカップケーキ",\
        "バイタル40","バイタル20","三色ペンライト"]
        critical_list = [33,35,45,67,71]
    
        class Item(auto_derby.config.single_mode_item_class):
            def exchange_score(self, ctx: Context) -> float:
                ret = super().exchange_score(ctx)
                es = self.effect_summary()
                if self.name in purchase_list:
                    ret = 110
                else:
                    ret -= 70

                if (
                    self.name in buff3_list
                    and ctx.items.get(self.id).quantity >= 3
                ):
                    ret = -110        
                return ret                              

            def effect_score(
                self, ctx: Context, command: Command, summary: EffectSummary
            ) -> float:
                ret = super().effect_score(ctx, command, summary)
                if (
                    isinstance(command, RaceCommand)
                    and command.race.grade == command.race.GRADE_G1
                    and self.name == "蹄鉄ハンマー・極"
                ):
                    return 70
                elif (
                    isinstance(command, RaceCommand)
                    and ctx.date[0] < 4
                    and command.race.grade > command.race.GRADE_G1
                    and self.name == "蹄鉄ハンマー・極"
                ):
                    return 0

                if (
                    isinstance(command, RaceCommand)
                    and command.race.grade == command.race.GRADE_G1
                    and ctx.items.get(52).quantity == 0
                    and self.name == "蹄鉄ハンマー・匠"
                ):
                    ret = 70

                if (
                    isinstance(command, RaceCommand)
                    and self.name in hammers_list
                    and ctx.date[0] == 4
                ):
                    ret = 70
                
                if (
                    self.name in buff3_list
                    and ctx.date[0] < 4
                ):
                    ret = 0

                if (
                    isinstance(command, RaceCommand)
                    and ctx.turn_count() in critical_list
                    and self.name == "三色ペンライト"
                    or ctx.turn_count() == ctx.total_turn_count()
                    and self.name == "三色ペンライト"
                ):
                    ret += 70

                if (
                    isinstance(command, RaceCommand)
                    and self.name == "三色ペンライト"
                    and ctx.turn_count() not in critical_list
                    and ctx.turn_count() != ctx.total_turn_count()
                ):
                    ret = 0
                    
                return ret

            def should_use_directly(self, ctx: Context) -> bool:
                # use max vitality item directly after exchange
                es = self.effect_summary()   
                if (
                    self.name in buff2_list 
                    and ctx.turn_count() == 71
                ):
                    return True
                    
                return super().should_use_directly(ctx)

        auto_derby.config.single_mode_item_class = Item


auto_derby.plugin.register(__name__, Plugin())
