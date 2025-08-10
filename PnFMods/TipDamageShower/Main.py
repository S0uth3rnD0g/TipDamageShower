API_VERSION = 'API_v1.0' # This is Mandatory!
MOD_NAME = 'TipDamageShower' # Your Mod Name

EXCEPTIONAL_SHIP_LIST = [
    # 'SHINANO',
    'VYAZMA',
    'SEVASTOPOL',
    'SIEGFRIED',
    'DEFENCE',
    'PRINZ ADALBERT',
    'MANTEUFFEL',
    'AMIRAL LARTIGUE',
    'MARSEILLE',
    'BREST',
    'LE HAVRE',
    'VARESE',
    'MICHELANGELO',
    'YOSHINO',
    'YOSHINO B',
    'AL AZUMA',
    'AZUMA',
    'AZUMA B',
    'BRENNUS',
    'HILDEBRAND',
    'PUERTO RICO',
    'STALINGRAD',
    'CARNOT',
    'ADMIRAL SCHRÖDER',
    'ÄGIR',
    'AL ÄGIR',
    'MENGCHONG',
    'ALASKA',
    'ALASKA B',
    'CAMBRIDGE',
    'KRONSHTADT',
    'CHERBOURG',
    'METZ',
    'KNESEBECK',
    'CONGRESS',
    'PROTECTOR',
    'TOULON',
    'GOUDEN LEEUW',
    'SCHILL',
    'ADMIRAL SCHEER',
    'ADMIRAL REINHARD',
    'JOHAN DE WITT'
]
GRAF_SPEE_LIST = [
    'ADMIRAL GRAF SPEE',
    'HSF ADMIRAL GRAF SPEE'
]

class TipDamageShower(object):
    def __init__(self):
        events.onObserverdShipChanged(self.onObserverdShipChanged)
        events.onBattleQuit(self.onBattleQuit)
        self._uiId = None
        
    def onBattleQuit(self, *args):
        # Remove entity from DataHub
        # Components in the entity will automatically be cleared
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
        skillList = battle.getLearnedCrewSkills()

        if vehicle.name in GRAF_SPEE_LIST:
            baseBurnDurationTime = 45
            baseBurnDPS = 0.3
            baseFloodDurationTime = 40
            baseFloodDPS = 0.375
        elif (vehicle.subtype == 'Battleship') or (vehicle.name in EXCEPTIONAL_SHIP_LIST):
            baseBurnDurationTime = 60
            baseBurnDPS = 0.3
            baseFloodDurationTime = 40
            baseFloodDPS = 0.5
        elif vehicle.subtype == 'AirCarrier':
            baseBurnDurationTime = 45
            baseBurnDPS = 0.3
            baseFloodDurationTime = 30
            baseFloodDPS = 0.25
        elif vehicle.subtype == 'Submarine':
            baseBurnDurationTime = 30
            baseBurnDPS = 1
            baseFloodDurationTime = 30
            baseFloodDPS = 0.33
        else:
            baseBurnDurationTime = 30
            baseBurnDPS = 0.3
            baseFloodDurationTime = 40
            baseFloodDPS = 0.25
        
        modBurnTimeMult = 1.0
        modFloodTimeMult = 1.0
         
        
        if (len(modernizations) >= 4) and (modernizations[3] is not None) and (modernizations[3].iconPath == 'url:../modernization_icons/icon_modernization_PCM023_DamageControl_Mod_II.png'):
            modBurnTimeMult *= 0.85
            modFloodTimeMult *= 0.85
        if (len(modernizations) >= 5) and (modernizations[4] is not None) and (modernizations[4].iconPath == 'url:../modernization_icons/icon_modernization_PCM047_Special_Mod_I_Montana.png'):
            modBurnTimeMult *= 0.9
            modFloodTimeMult *= 0.9
        if (len(modernizations) >= 5) and (modernizations[4] is not None) and (modernizations[4].iconPath == 'url:../modernization_icons/icon_modernization_PCM049_Special_Mod_I_Hindenburg.png'):
            modBurnTimeMult *= 0.6
            modFloodTimeMult *= 0.3
        
        skillTimeMult1 = 0.85 if 'DefenceCritFireFlooding' in skillList else 1.0
        skillTimeMult2 = 1.25 if 'ApDamageBb' in skillList else 1.0
        skillDamageMult = 0.9 if 'ApDamageBb' in skillList else 1.0

        existing_ids = {s.id for s in signals if s is not None}
        IY_exists = 4286410672 in existing_ids
        JYB_exists = 4285362096 in existing_ids
        
        signalBurnTimeMult = 0.8 if IY_exists else 1.0
        signalFloodTimeMult = 0.8 if JYB_exists else 1.0

        #test = baseBurnDurationTime * modBurnTimeMult * skillTimeMult1 * skillTimeMult2 * signalBurnTimeMult
        data = dict(
            burnDurationTime = baseBurnDurationTime * modBurnTimeMult * skillTimeMult1 * skillTimeMult2 * signalBurnTimeMult,
            burnDPS = baseBurnDPS * skillDamageMult,
            floodDurationTime = baseFloodDurationTime * modFloodTimeMult * skillTimeMult1 * skillTimeMult2 * signalFloodTimeMult,
            floodDPS = baseFloodDPS * skillDamageMult,
        )
        
        #with open('test.txt', 'a') as file:
        #    file.write('%s\n'%(vehicle.name))
        #    file.write('%s\n'%(vehicle.subtype))
        #    file.write('%s\n'%(test))
            
        
        ui.updateUiElementData(self._uiId, data)

tipDamageShower = TipDamageShower()