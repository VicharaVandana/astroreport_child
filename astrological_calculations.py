import jyotishyamitra as jsm
import jyotichart as jc
from html2image import Html2Image

#declare constants related to planet sign placement 
DEBILITATED = "Debilitated / Neecha"
ENEMYSIGN = "Enemy sign / Shatru rashi"
NEUTRALSIGN = "Neutral sign / Sama rashi"
FRIENDSIGN = "Friends sign / Mitra rashi"
OWNSIGN = "Own sign / Swa rashi"
MOOLTRIKONA = "Prime sign / Moolatrikona rashi"
EXHALTED = "Exhalted / Uchha"


def generate_astrodata(bd):

    #step 1 :clear past input data
    jsm.clear_birthdata()

    #Step 2: Providing input birth data - here multiple times the API input_birthdata are invoked but you can do it in single shot too.
    #providing Name and Gender
    inputdata = jsm.input_birthdata(name=bd["name"], gender=bd["gender"])

    #providing Date of birth details
    inputdata = jsm.input_birthdata(year=bd["DOB"]["year"], month=bd["DOB"]["month"], day=bd["DOB"]["day"])

    #Providing Place of birth details
    inputdata = jsm.input_birthdata(place=bd["POB"]["name"], longitude=bd["POB"]["lon"], lattitude=bd["POB"]["lat"], timezone=bd["POB"]["timezone"])

    #Providing Time of birth details
    inputdata = jsm.input_birthdata(hour=bd["TOB"]["hour"], min=bd["TOB"]["min"], sec=bd["TOB"]["sec"])

    #Step 3: Validate Birthdata
    jsm.validate_birthdata()

    #Step 4: If Birthdata is valid then get birthdata
    if(jsm.IsBirthdataValid()):
        birthdata = jsm.get_birthdata()


    #Step 5: Invoke the API generate_astrologicalData with retrunval desired to be dictionary and get astrological data in dictionary format.
    astrodata = jsm.generate_astrologicalData(birthdata, returnval = "ASTRODATA_DICTIONARY") 

    return astrodata   

def plot_astrocharts(astrodata, chartslocaton):
    #Now since the astrodata is computed, let us plot all divisional charts
    #for div in ["D1", "D2", "D3", "D4", "D7", "D9", "D10", "D12", "D16", "D20", "D24", "D27", "D30", "D40", "D45", "D60"]:
    for div in ["D1", "D7", "D9"]:
        chart_nc = jc.NorthChart(f'NorthChart_{div}',"Shyam Bhat")
        chart_sc = jc.SouthChart(f'SouthChart_{div}',"Shyam Bhat")
        #Fetching and Setting ascendant sign
        ascendantsign = astrodata[div]["ascendant"]["sign"]
        chart_nc.set_ascendantsign(ascendantsign)
        chart_sc.set_ascendantsign(ascendantsign)
        #Fetching and Adding all 9 planet of division to the chart
        for planet in astrodata[div]["planets"]:
            pdata = astrodata[div]["planets"][planet]
            if (pdata["house-rel"] == EXHALTED):
                clr = 'gold'
            elif (pdata["house-rel"] == MOOLTRIKONA):
                clr = 'lightgreen'
            elif (pdata["house-rel"] == OWNSIGN):
                clr = 'lime'
            elif (pdata["house-rel"] == FRIENDSIGN):
                clr = 'cyan'
            elif (pdata["house-rel"] == NEUTRALSIGN):
                clr = 'white'
            elif (pdata["house-rel"] == ENEMYSIGN):
                clr = 'red'
            elif (pdata["house-rel"] == DEBILITATED):
                clr = 'pink'
            else:
                clr = 'white'
            chart_nc.add_planet(planet,pdata["symbol"], pdata["house-num"], retrograde=pdata["retro"], colour=clr)
            chart_sc.add_planet(planet,pdata["symbol"], pdata["house-num"], retrograde=pdata["retro"], colour=clr)
            
        #Drawing the chart
        chart_nc.updatechartcfg(clr_sign='papayawhip')
        chart_sc.updatechartcfg(clr_Asc='papayawhip')
        chart_nc.draw(chartslocaton, f'NorthChart_{div}')
        chart_sc.draw(chartslocaton, f'SouthChart_{div}')
        for planet in astrodata[div]["planets"]:
            chart_nc.delete_planet(planet)
            chart_sc.delete_planet(planet)

        #Converting svg to png file
        hti = Html2Image()
        hti.output_path = './charts/'
        hti.browser.flags = ['--default-background-color=00000000']
        hti.screenshot(other_file=f"./charts/NorthChart_{div}.svg", size=(500, 500), save_as=f"NorthChart_{div}.png")
        hti.screenshot(other_file=f"./charts/SouthChart_{div}.svg", size=(490, 330), save_as=f"SouthChart_{div}.png")
        
    
    return
    
