API_VERSION = 'API_v1.0'
MOD_NAME = 'TipDamageShower'

class TipDamageShower(object):
    def __init__(self):
        events.onObserverdShipChanged(self.onObserverdShipChanged)
        events.onBattleQuit(self.onBattleQuit)
        self._uiId = None
        
    def onBattleQuit(self, *args):
        ui.deleteUiElement(self._uiId)
        self._uiId = None
        
    def onObserverdShipChanged(self, *args):
        self._uiId = uiId = ui.createUiElement()
        ui.addDataComponentWithId(uiId, 'sasagcy_TipDamageShower', {})
            
        vehicle = battle.getSelfPlayerShip()
        if vehicle is None:
            return
        modernizations = vehicle.getModernizations()
        signals = vehicle.getSignals()
        skills = battle.getLearnedCrewSkills()
        
        modBurnTimeMult = 1.0
        modFloodTimeMult = 1.0
        modBurnDamageMult = 1.0
        modFloodDamageMult = 1.0
        
        if (len(modernizations) >= 4) and (modernizations[3] is not None) and (modernizations[3].iconPath == 'url:../modernization_icons/icon_modernization_PCM023_DamageControl_Mod_II.png'):
            modBurnTimeMult *= 0.85
            modFloodTimeMult *= 0.85
        if (len(modernizations) >= 5) and (modernizations[4] is not None) and (modernizations[4].iconPath == 'url:../modernization_icons/icon_modernization_PCM047_Special_Mod_I_Montana.png'):
            modBurnTimeMult *= 0.9
            modFloodTimeMult *= 0.9
        if (len(modernizations) >= 5) and (modernizations[4] is not None) and (modernizations[4].iconPath == 'url:../modernization_icons/icon_modernization_PCM049_Special_Mod_I_Hindenburg.png'):
            modBurnTimeMult *= 0.5
            modFloodTimeMult *= 0.5
        if (len(modernizations) >= 6) and (modernizations[5] is not None) and (modernizations[5].iconPath == 'url:../modernization_icons/icon_modernization_PCM044_Special_Mod_I_Republique.png'):
            modBurnTimeMult *= 1.15
            modFloodTimeMult *= 1.15
        if (len(modernizations) >= 2) and (modernizations[1] is not None) and (modernizations[1].iconPath == 'url:../modernization_icons/icon_modernization_PCM100_DamageControl_Mod_III.png'):
            modBurnDamageMult *= 0.95
            modFloodDamageMult *= 0.95
        
        skillBurnTimeMult = 1.0
        skillFloodTimeMult = 1.0
        skillBurnDamageMult = 1.0
        skillFloodDamageMult = 1.0
        
        if 'DefenceCritFireFlooding' in skills:
            skillBurnTimeMult *= 0.85
            skillFloodTimeMult *= 0.85
        if 'ApDamageBb' in skills:
            skillBurnTimeMult *= 1.25
            skillFloodTimeMult *= 1.25
            skillBurnDamageMult *= 0.9
            skillFloodDamageMult *= 0.9
            
        existing_ids = {s.id for s in signals if s is not None}
        IY_exists = 4286410672 in existing_ids
        JYB_exists = 4285362096 in existing_ids
        
        signalBurnTimeMult = 0.8 if IY_exists else 1.0
        signalFloodTimeMult = 0.8 if JYB_exists else 1.0

        data = dict(
            burnDurationMult = modBurnTimeMult * skillBurnTimeMult * signalBurnTimeMult,
            burnDPSMult = modBurnDamageMult * skillBurnDamageMult,
            floodDurationMult = modFloodTimeMult * skillFloodTimeMult * signalFloodTimeMult,
            floodDPSMult = modFloodDamageMult * skillFloodDamageMult,
        )
        ui.updateUiElementData(self._uiId, data)

tipDamageShower = TipDamageShower()