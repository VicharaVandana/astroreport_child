from fpdf import FPDF
from birthdata import birthdata as bd
from datetime import datetime as dt
import astrological_calculations as astrocalc
from scipy.stats import rankdata

CLR_TRUE = "green"
CLR_FALSE = "red"

def list_intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

signs = [ "Aries",       "Taurus",    "Gemini",   "Cancer",
          "Leo",         "Virgo",     "Libra",    "Scorpio",
          "Saggitarius", "Capricorn", "Aquarius", "Pisces"
        ]
signlords = [ "Mars",    "Venus",     "Mercury",  "Moon",
              "Sun",     "Mercury",   "Venus",    "Mars",
              "Jupiter", "Saturn",    "Saturn",   "Jupiter",
            ]

barrensigns = ["Aries", "Gemini", "Leo", "Virgo"]


lord_of_sign = dict(zip(signs, signlords))

signnum = lambda signstr: signs.index(signstr) + 1

def nth(n):
    if n == 1:
        return "st"
    elif n == 2:
        return "nd"
    elif n == 3:
        return "rd"
    else:
        return "th"

def get_distancebetweenplanets(division, fromplanet, toplanet):
    #Computes whats the distance between from planet to toplanet in given divisional chart in seconds(deg and minutes also converted to seconds)
    fp = division["planets"][fromplanet]
    tp = division["planets"][toplanet]
    #compute distance from start of lagna to from and to planets in seconds.
    sec_fp = (((fp["house-num"]-1)*30*3600) + (fp["pos"]["deg"]*3600) + (fp["pos"]["min"]*60) + (fp["pos"]["sec"]))
    sec_tp = (((tp["house-num"]-1)*30*3600) + (tp["pos"]["deg"]*3600) + (tp["pos"]["min"]*60) + (tp["pos"]["sec"]))

    if(sec_tp >= sec_fp):   #if toplanet is ahead of fromplanet
        dist = sec_tp - sec_fp
    else:   #if toplanet is behind of fromplanet
        gap = sec_fp - sec_tp
        dist = (360*3600) - gap

    return dist

def compute_pakshatithi4mdegree(deg):
    # Normalize degrees to be within the range [0, 360)
    normalized_deg = deg % 360

    # Determine the paksha (waxing or waning)
    if normalized_deg < 180:
        paksha = "shukla"
    else:
        paksha = "krishna"

    # Determine the tithi
    tithi = ((normalized_deg % 180) // 12) + 1

    return paksha, int(tithi)

def relation(planet1, planet2, div,ad):
    relstr = ""
    p1_friends = ad[div]["planets"][planet1]["friends"]
    p1_enemies = ad[div]["planets"][planet1]["enemies"]
    
    p2_friends = ad[div]["planets"][planet2]["friends"]
    p2_enemies = ad[div]["planets"][planet2]["enemies"]
    

    if(planet1 in p2_friends):
        relstr = f"""{planet1} is friend of {planet2}."""
    elif(planet1 in p2_enemies):
        relstr = f"""{planet1} is enemy of {planet2}."""
    else:
        relstr = f"""{planet1} is neutral to {planet2}."""

    if(planet2 in p1_friends):
        relstr = f"""{relstr} And {planet2} is friend of {planet1}."""
    elif(planet2 in p1_enemies):
        relstr = f"""{relstr} And {planet2} is enemy of {planet1}."""
    else:
        relstr = f"""{relstr} And {planet2} is neutral to {planet1}."""

    return(relstr)
    
def housediff(fromsign, tosign):
  ''' Computes how many houses is difference between from fromsign to tosign
      This function is used to compute housenumber for planets too '''
  if(tosign > fromsign):
    house = tosign - fromsign + 1
  elif(tosign < fromsign):
    house = 12 + tosign - fromsign + 1
  else: #same signs
    house = 1 #first house
  return house   
    

class SapthamsaReportPDF(FPDF):
    def header(self):
        # Logo
        self.image('./report/ganeshalogo.jpeg', 185, 2, h=20, w=20)
        # Times bold 15
        self.set_font('Times', 'B', 18)
        # Title
        self.cell(170, 10, f'Saptamsha Astrology Report for {bd["name"]}',ln=True,border=True, align='C')
        self.ln(1)
        

    def footer(self):
        self.set_y(-15)
        self.set_font('Times', 'I', 12)
        self.cell(0, 10, 'Page %s' % self.page_no(), 0, 0, 'C')

    def add_firstPage(self):
        self.set_font('Helvetica', '', 14)
        htmlsnippet = f'''<p>This is the Saptamsha report of <b><font color="#2229D6">{bd["name"]}</font></b> generated as per analysis provided in <b><font color="#993333">Predict with Saptamsha</font></b> book written by <b><font color="#993333">Shri V.P.Goel</font></b>.</p></br>
        <p>This report analyses the natives <font color="#009900">saptamsha [D7] chart </font> mainly related to children and progeny. 
        In this report, you will see the basic analysis of <b>birth chart [D1]</b> and <b>navamsha chart [D9]</b> and in depth analysis of <b>saptamsha chart [D7]</b> for children related aspect of life.
        Various points will be analysed like: </p>
        <ul>
        <li>Does native have desire for having kids?</li>
        <li>Will children be born to the native?</li>
        <li>How easy or difficult is it for native to have children?</li>
        <li>Number of kids and their gender</li>
        <li>How is the relationship with children</li>
        <li>Health and quality of children and their success.</li>
        </ul><p> </p>
        <p>In this report we employ various techniques and methods provided in the book and Vedic astrological scriptures to determine answers to these questions.
        These methods include: </p>
        <ul>
        <li>Analysis of <b> birth chart </b> and <b> divisional charts </b></li>
        <li>Analysis of <b>Beeja Sphuta</b> or <b>Kshetra Sphuta</b></li>
        <li>Analysis of <b>Santana Tithi</b></li>
        </ul><p> </p>
        <p>The User-Details are as follows: </p>'''
        self.write_html(htmlsnippet)

        #section for User details -TOB, DOB, POB
        self.set_font('Times', '', 16)
        self.set_text_color(0,0,130)
        creationdetails = f'''Created on: {dt.now().strftime("%d/%b/%Y [%A] - %H:%M:%S")}'''
        userdetail = f'''Name: {bd["name"]}
Gender: {bd["gender"]}
Date of birth:  {bd["DOB"]["day"]}/{bd["DOB"]["month"]}/{bd["DOB"]["year"]}
Time Of birth:  {bd["TOB"]["hour"]} : {bd["TOB"]["min"]} : {bd["TOB"]["sec"]} 
Place of Birth:  {bd["POB"]["name"]}
{creationdetails}'''
        self.multi_cell(w=0,h=8, txt=userdetail, align='C', border=True)
        self.ln(15)

        #Disclaimer section
        self.set_font('Times', '', 10)
        self.set_text_color(26,130,130)
        disclaimerhtml = f'''<p><b>Disclaimer:</b> <I>This report is just application of methods provided in the 
        book "Predict with Saptamsha" by V.P.Goel on astrological data of the native details provided. 
        If the predictions and results provided in this report are not inline with natives life events and experience, 
        then we do not take any responsibility for that. It is important to understand that jyotishya is very complex 
        branch of science and limittions of software automation are always to be kept in mind before believing in the results blindly. 
        Please consult an experienced astrologer with this report to get full benefits of this report</I>.</p>'''
        self.write_html(disclaimerhtml)
        self.set_text_color(0,0,0)
        return
    
    def add_astrocharts(self,ad):
        #title of the page
        self.set_font('Arial', 'BU', 16)
        self.set_text_color(230,30,0)
        self.cell(txt="Divisional Charts relevant for report", w=0, h=10, align='C')

        #settings for image caption
        self.set_font('Times', 'BI', 11)
        imageWidth_n = (self.w / 2.5) - 5
        imageWidth_s = (self.w * 3 / 5) - 8
        self.set_fill_color(255,255,0)  #yellow colour
        self.set_text_color(20,30,200)

        #first comes Lagna chart 
        # North chart on left takes 2/5 of place       
        self.image("./charts/NorthChart_D1.png", x=5, y=30, w=imageWidth_n)
        #setting caption 
        self.set_xy(5,30+imageWidth_n)    #caption position
        self.cell(txt="D1 - North Lagna Chart", w=imageWidth_n, h=3, align='C', ln=1)

        # South chart on right takes 3/5 of place
        self.image("./charts/SouthChart_D1.png", x=5 + imageWidth_n, y=30, w=imageWidth_s)
        #setting caption 
        self.set_xy(5 + imageWidth_n,30+imageWidth_n)    #caption position
        self.cell(txt="D1 - South Lagna Chart", w=imageWidth_s, h=3, align='C', ln=1)

        #Brief description of Lagna chart in childbirth
        self.set_font('Helvetica', '', 12)
        self.set_text_color(0,20,20)
        brief = f'''<p>In <i>Vedic astrology</i>, the <b>Lagna Chart (D1)</b> plays a pivotal role 
        in predicting <b>childbirth</b> and progeny. The <b>fifth house [here of sign {ad["D1"]["houses"][4]["sign"]}]</b>, representing <b>children</b>, 
        is scrutinized along with its planetsry influences. 
        The <b>lord of the fifth house [{ad["D1"]["houses"][4]["sign-lord"]}]</b> becomes a key factor, indicating the native's potential for having 
        <b>children</b>. The <b>ninth house [here of sign {ad["D1"]["houses"][8]["sign"]}]</b>, associated with <b>fortune</b>, also contributes insights. 
        <i>Jupiter</i> is considered a favorable influence for <b>childbirth</b>, and <b>Dasha periods</b> and <b>transits</b> are examined for timing predictions. 
        <b>Malefic planets</b> may suggest challenges. However, it's essential to approach these predictions with caution, 
        considering individual variations and using complementary charts for a more comprehensive analysis.</p>'''
        self.set_xy(5,30+imageWidth_n)
        self.write_html(brief)
        self.set_text_color(0,0,0)
        self.ln()
        self.line(5, 70+imageWidth_n, self.w-5, 70+imageWidth_n)
        self.line(0, 71+imageWidth_n, self.w, 71+imageWidth_n)
        self.line(5, 72+imageWidth_n, self.w-5, 72+imageWidth_n)

        #Second is Saptamsha chart
        self.set_font('Times', 'BI', 11)
        self.set_text_color(20,30,200)
        # North chart on left takes 2/5 of place       
        self.image("./charts/NorthChart_D7.png", x=5, y=75+imageWidth_n, w=imageWidth_n)
        #setting caption 
        self.set_xy(5,75+(2*imageWidth_n))    #caption position
        self.cell(txt="D7 - North Saptamsha Chart", w=imageWidth_n, h=3, align='C', ln=1)

        # South chart on right takes 3/5 of place
        self.image("./charts/SouthChart_D7.png", x=5 + imageWidth_n, y=75+imageWidth_n, w=imageWidth_s)
        #setting caption 
        self.set_xy(5 + imageWidth_n,75+(2*imageWidth_n))    #caption position
        self.cell(txt="D7 - South Saptamsha Chart", w=imageWidth_s, h=3, align='C', ln=1)

        #Brief description of Lagna chart in childbirth
        self.set_font('Helvetica', '', 12)
        self.set_text_color(0,20,20)
        brief = f'''<p>In Vedic astrology, the <b>Saptamsha Chart (D7)</b> 
        takes center stage in predicting matters of childbirth and progeny. 
        This specialized chart zeros in on the seventh house, intricately tied to themes of fruits of marriage which are progeny, and children. 
        Analyzing planetsry positions within this chart offers insights into the number and well-being of children.  
        Timing predictions for childbirth are deduced through careful scrutiny of <b>Dasha periods</b> and planetsry transits within the Saptamsha Chart. 
        As always, acknowledging individual nuances and potentially consulting complementary charts enriches the depth of astrological interpretations.</p>'''
        self.set_xy(5,77+(2*imageWidth_n))
        self.write_html(brief)
        self.set_text_color(0,0,0)

        self.add_page()
        #title of the page
        self.set_font('Arial', 'BU', 16)
        self.set_text_color(230,30,0)
        self.cell(txt="Divisional Charts relevant for report (continued...)", w=0, h=10, align='C')

        self.set_font('Times', 'BI', 11)
        self.set_text_color(20,30,200)

        #Next comes Navamsha chart 
        # North chart on left takes 2/5 of place       
        self.image("./charts/NorthChart_D9.png", x=5, y=30, w=imageWidth_n)
        #setting caption 
        self.set_xy(5,30+imageWidth_n)    #caption position
        self.cell(txt="D9 - North Navamsha Chart", w=imageWidth_n, h=3, align='C', ln=1)

        # South chart on right takes 3/5 of place
        self.image("./charts/SouthChart_D9.png", x=5 + imageWidth_n, y=30, w=imageWidth_s)
        #setting caption 
        self.set_xy(5 + imageWidth_n,30+imageWidth_n)    #caption position
        self.cell(txt="D9 - South Navamsha Chart", w=imageWidth_s, h=3, align='C', ln=1)

        #Brief description of Lagna chart in childbirth
        self.set_font('Helvetica', '', 12)
        self.set_text_color(0,20,20)
        brief = f'''<p>The <b>Navamsha Chart (D9)</b> in Vedic astrology is pivotal for predicting 
        aspects of children and marriage. Focused on the ninth house, representing dharma and fortune, 
        this chart examines planetsry placements and the influence of benefic planets, 
        especially <i>Jupiter</i>, for insights into the potential for progeny. 
        Analysis of the ninth house lord and its interactions with other planets, along with timing predictions 
        derived from <b>Dasha periods</b> and planetsry transits, provides a comprehensive understanding of 
        an individual's familial journey. Complementary charts and consideration of individual variations 
        enhance the accuracy of these predictions.</p>'''
        self.set_xy(5,30+imageWidth_n)
        self.write_html(brief)
        self.set_text_color(0,0,0)
        self.ln()
        self.line(5, 70+imageWidth_n, self.w-5, 70+imageWidth_n)
        self.line(0, 71+imageWidth_n, self.w, 71+imageWidth_n)
        self.line(5, 72+imageWidth_n, self.w-5, 72+imageWidth_n)

        legendtext = "This legend explains the colors given to planets associated with its placement in above given astrological charts [D1, D7 and D9]:"
        self.ln(5)
        self.set_font('Times', 'I', 16)
        self.set_text_color(230,30,0)
        self.multi_cell(w=0,h=7, txt=legendtext, align='C', border=False)
        # Calculate position and size for centered image
        page_width = self.w
        image_width = page_width / 4
        x_position = (page_width - image_width) / 2 # Add centered image
        self.image("./report/planetcolourlegend.png", x=x_position, y=None, w=image_width)
        self.set_text_color(0,0,0)

        return
    
    def add_analysis_D1chart(self,ad):
        #title of the page
        self.set_font('Arial', 'BU', 16)
        self.set_text_color(230,30,0)
        self.cell(txt=f'''Analysis of {bd["name"]}'s Lagna chart''', w=0, h=10, align='C')
        self.ln()
        #Section for areas to consider
        html_text = f"""
        <p><b>A simple approach to analyze fifth house for children using D1 chart only is given. The parameters are:</b></p>
        <ol>
        <li>Fifth house</li>
        <li>Lord of fifth house - <font color="SlateBlue"><b>{ad["D1"]["houses"][4]["sign-lord"]}</b></font></li>
        <li>Karaka of fifth house - <font color="MediumSeaGreen"><b>Jupiter</b></font></li>
        </ol>
        <p> Now let us check each of these parameters individually.</p>
        """
        self.set_font('Helvetica', '', 13)
        self.set_text_color(10,10,10)
        self.write_html(html_text)
        self.ln()
        self.line(5, self.get_y(), self.w-5, self.get_y())
        self.ln()

        #Parameter of Fifth House        
        cause_cnt = 0
        #Check if Lord of the house is placed in the house or aspects the house
        fifthhouse = ad["D1"]["houses"][4].copy()
        fifthlord = fifthhouse["sign-lord"]
        fifthlord_house = ad["D1"]["planets"][fifthlord]["house-num"]
        fifthlord_placerelation = ad["D1"]["planets"][fifthlord]["house-rel"]
        if(fifthlord in fifthhouse["planets"]):
            clr1 = CLR_TRUE
            cause_cnt = cause_cnt + 1
            response1 = f'''<b><U>Satisfied</U></b>. Fifth House is <b>{fifthhouse["sign"]} [{fifthhouse["sign-num"]}]</b> which is ruled by <b>{fifthlord}</b> and is placed in fifth house only.'''
        elif (fifthlord in fifthhouse["aspect-planets"]):
            clr1 = CLR_TRUE
            cause_cnt = cause_cnt + 1
            response1 = f'''<b><U>Satisfied</U></b>. Fifth House is <b>{fifthhouse["sign"]} [{fifthhouse["sign-num"]}]</b> which is ruled by <b>{fifthlord}</b>. <b>{fifthlord}</b> is placed in <b>house number - {fifthlord_house}</b> and is aspecting fifth house. Note: {fifthlord} is placed in his <I>{fifthlord_placerelation}</I>.'''
        else:
            clr1 = CLR_FALSE
            response1 = f'''<b><U>Unsatisfied</U></b>. Fifth House is <b>{fifthhouse["sign"]} [{fifthhouse["sign-num"]}]</b> which is ruled by <b>{fifthlord}</b>. <b>{fifthlord}</b> is placed in <b>house number - {fifthlord_house}</b>. So he is neither placed in nor aspecting fifth house. Note: {fifthlord} is placed in his <I>{fifthlord_placerelation}</I>.'''

        #Check if Lord of the lagan is placed in the house or aspects the house.
        lagna = ad["D1"]["houses"][0].copy()
        lagnalord = lagna["sign-lord"]
        lagnalord_house = ad["D1"]["planets"][lagnalord]["house-num"]
        lagnalord_placerelation = ad["D1"]["planets"][lagnalord]["house-rel"]
        if(lagnalord in fifthhouse["planets"]):
            clr2 = CLR_TRUE
            cause_cnt = cause_cnt + 1
            response2 = f'''<b><U>Satisfied</U></b>. First House or lagan is <b>{lagna["sign"]} [{lagna["sign-num"]}]</b> which is ruled by <b>{lagnalord}</b>. Fifth House is <b>{fifthhouse["sign"]} [{fifthhouse["sign-num"]}]</b>. Lagan lord <b>{lagnalord}</b> is placed in fifth house. Note: Lagan lord {lagnalord} is placed in his <I>{lagnalord_placerelation}</I>.'''
        elif (lagnalord in fifthhouse["aspect-planets"]):
            clr2 = CLR_TRUE
            cause_cnt = cause_cnt + 1
            response2 = f'''<b><U>Satisfied</U></b>. First House or lagan is <b>{lagna["sign"]} [{lagna["sign-num"]}]</b> which is ruled by <b>{lagnalord}</b>. And Fifth House is <b>{fifthhouse["sign"]} [{fifthhouse["sign-num"]}]</b>. <b>{lagnalord}</b> is placed in <b>house number - {lagnalord_house}</b> and is aspecting fifth house. Note: Lagan lord {lagnalord} is placed in his <I>{lagnalord_placerelation}</I>.'''
        else:
            clr2 = CLR_FALSE
            response2 = f'''<b><U>Unsatisfied</U></b>. First House or lagan is <b>{lagna["sign"]} [{lagna["sign-num"]}]</b> which is ruled by <b>{lagnalord}</b>. And Fifth House is <b>{fifthhouse["sign"]} [{fifthhouse["sign-num"]}]</b>. <b>{lagnalord}</b> is placed in <b>house number - {lagnalord_house}</b>. So he is neither placed in nor aspecting fifth house. Note: Lagan lord {lagnalord} is placed in his <I>{lagnalord_placerelation}</I>.'''

        #Check if Karaka of the house is placed in the house or aspects the house.
        karaka = "Jupiter"  #Always karaka of 5th house for children is Jupiter
        karaka_house = ad["D1"]["planets"][karaka]["house-num"]
        karaka_placerelation = ad["D1"]["planets"][karaka]["house-rel"]
        if(karaka in fifthhouse["planets"]):
            clr3 = CLR_TRUE
            cause_cnt = cause_cnt + 1
            response3 = f'''<b><U>Satisfied</U></b>. The Karaka of fifth house for children is <b>{karaka}</b>. Fifth House is <b>{fifthhouse["sign"]} [{fifthhouse["sign-num"]}]</b>. Santana karaka <b>{karaka}</b> is placed in fifth house. Note: {karaka} is placed in his <I>{karaka_placerelation}</I>.'''
        elif (karaka in fifthhouse["aspect-planets"]):
            clr3 = CLR_TRUE
            cause_cnt = cause_cnt + 1
            response3 = f'''<b><U>Satisfied</U></b>. The Karaka of fifth house for children is <b>{karaka}</b>. And Fifth House is <b>{fifthhouse["sign"]} [{fifthhouse["sign-num"]}]</b>. <b>{karaka}</b> is placed in <b>house number - {karaka_house}</b> and is aspecting fifth house. Note: {karaka} is placed in his <I>{karaka_placerelation}</I>.'''
        else:
            clr3 = CLR_FALSE
            response3 = f'''<b><U>Unsatisfied</U></b>. The Karaka of fifth house for children is <b>{karaka}</b>. And Fifth House is <b>{fifthhouse["sign"]} [{fifthhouse["sign-num"]}]</b>. <b>{karaka}</b> is placed in <b>house number - {karaka_house}</b>. So he is neither placed in nor aspecting fifth house. Note: {karaka} is placed in his <I>{karaka_placerelation}</I>.'''

        #Check if The house is occupied or aspected by benefics.
        benefics = ad["D1"]["classifications"]["natural-benefics"]
        #benefics = ad["D1"]["classifications"]["benefics"]
        #print(f"The functional benefics are: {benefics}")
        planetsin_fifthhouse = fifthhouse["planets"]
        planetsaspecting_fifthhouse = fifthhouse["aspect-planets"]
        beneficsin_fifthhouse = list_intersection(benefics,planetsin_fifthhouse)
        beneficsaspecting_fifthhouse = list_intersection(benefics,planetsaspecting_fifthhouse)
        clr4 = CLR_FALSE

        if(len(beneficsin_fifthhouse) > 0):
            clr4 = CLR_TRUE
            cause_cnt = cause_cnt + 1
            response4 = f'''The fifth house occupied by benefics : <b>{beneficsin_fifthhouse}.</b>.'''
        if (len(beneficsaspecting_fifthhouse) > 0):
            clr4 = CLR_TRUE
            cause_cnt = cause_cnt + 1
            response4 = f'''The fifth house aspected by benefics : <b>{beneficsaspecting_fifthhouse}.</b>.'''
        if(clr4 == CLR_FALSE):
            response4 = f'''<b><U>Unsatisfied</U></b>. The fifth house is neither occupied by any benefics nor aspected by benefics.'''
        else:
            response4 = f'''<b><U>Satisfied</U></b>. {response4}'''

        #Check if The house is empty of planets and aspects.
        if((len(planetsin_fifthhouse) == 0) and (len(planetsaspecting_fifthhouse) == 0)):
            clr5 = CLR_TRUE
            cause_cnt = cause_cnt + 1
            response5 = f'''<b><U>Satisfied</U></b>. The fifth house is empty and devoid of any aspect too.</b>.'''
        else:
            clr5 = CLR_FALSE
            response5 = f'''<b><U>Unsatisfied</U></b>. The fifth house is not empty. There are <b>{len(planetsin_fifthhouse)}</b> planets in fifth house: <b>{planetsin_fifthhouse}</b> and <b>{len(planetsaspecting_fifthhouse)}</b> planets aspecting fifth house: <b>{planetsaspecting_fifthhouse}</b>.'''

        cnt_fifthhouse_D1 = cause_cnt
        html_text = f"""<p><font color="blue" size="19"><b><U>Fifth House</U></b></font></p>
        <p>The fifth house should promise the birth of children in the horoscope. 
        It is the primary house and indicates the fulfillment of promise. To grant the promise, any house should be strong. 
        For a house to be strong, any of the following conditions should be met:</p>
        <ul>
        <li><font color={clr1} size="16">Lord of the house must be placed in the house or aspect the house.</font>: {response1}</li>
        </ul>
        <ul>
        <li><font color={clr2} size="16">Lord of the lagan must be placed in the house or aspect the house.</font>: {response2}</li>
        </ul>
        <ul>
        <li><font color={clr3} size="16">Karaka of the house must be placed in the house or aspect the house.</font>: {response3}</li>
        </ul>
        <ul>
        <li><font color={clr4} size="16">The house must be occupied or aspected by benefics.</font>: {response4}</li>
        </ul>
        <ul>
        <li><font color={clr5} size="16">When the house is not occupied or aspected by any planet, it can still promise the results.</font>: {response5}</li>
        </ul>
        <p> So when the <b>fifth house</b> of <b>Lagna chart [D1]</b> is analysed for promise of children in {bd["name"]}'s life, <b>{cnt_fifthhouse_D1}</b> out of above given 5 indications are positive. We need atleast 1 indication for positive outcome.</p>
        """
        self.set_font('Helvetica', '', 13)
        self.set_text_color(20,20,20)
        self.write_html(html_text)
        self.ln()
        self.line(5, self.get_y(), self.w-5, self.get_y())
        self.ln()

        #Parameter of Fifth House Lord       
        cause_cnt = 0

        #Check if Lord of the house is with the lord of lagan or is aspected by it
        fifthlord_aspectedby = ad["D1"]["planets"][fifthlord]["Aspected-by"]
        if(fifthlord_house == lagnalord_house):
            clr1 = CLR_TRUE
            cause_cnt = cause_cnt + 1
            response1 = f'''<b><U>Satisfied</U></b>. Fifth House is <b>{fifthhouse["sign"]} [{fifthhouse["sign-num"]}]</b> which is ruled by <b>{fifthlord}</b>. First House or lagan is <b>{lagna["sign"]} [{lagna["sign-num"]}]</b> which is ruled by <b>{lagnalord}</b>. In <I>D1 chart</I>, <b>{lagnalord}</b> and <b>{fifthlord}</b> are together in house number - {lagnalord_house}.'''
        elif (lagnalord in fifthlord_aspectedby):
            clr1 = CLR_TRUE
            cause_cnt = cause_cnt + 1
            response1 = f'''<b><U>Satisfied</U></b>. Fifth House is <b>{fifthhouse["sign"]} [{fifthhouse["sign-num"]}]</b> which is ruled by <b>{fifthlord}</b>. First House or lagan is <b>{lagna["sign"]} [{lagna["sign-num"]}]</b> which is ruled by <b>{lagnalord}</b>. In <I>D1 chart</I>, <b>{lagnalord}</b> placed in house number - {lagnalord_house} is aspecting <b>{fifthlord}</b> placed in house number - {fifthlord_house}.'''
        else:
            clr1 = CLR_FALSE
            response1 = f'''<b><U>Unsatisfied</U></b>. Fifth House is <b>{fifthhouse["sign"]} [{fifthhouse["sign-num"]}]</b> which is ruled by <b>{fifthlord}</b>. First House or lagan is <b>{lagna["sign"]} [{lagna["sign-num"]}]</b> which is ruled by <b>{lagnalord}</b>. In <I>D1 chart</I>, <b>{lagnalord}</b> placed in house number - {lagnalord_house} is neither conjunct nor aspecting <b>{fifthlord}</b> placed in house number - {fifthlord_house}..'''

        #Check if Lord of the house is in lagan.
        if(fifthlord_house == 1):
            clr2 = CLR_TRUE
            cause_cnt = cause_cnt + 1
            response2 = f'''<b><U>Satisfied</U></b>. Fifth House is <b>{fifthhouse["sign"]} [{fifthhouse["sign-num"]}]</b> which is ruled by <b>{fifthlord}</b> is placed in <I>lagna or first house</I>. Note: {fifthlord} is placed in his <I>{fifthlord_placerelation}.</I>.'''
        else:
            clr2 = CLR_FALSE
            response2 = f'''<b><U>Unsatisfied</U></b>. Fifth House is <b>{fifthhouse["sign"]} [{fifthhouse["sign-num"]}]</b> which is ruled by <b>{fifthlord}</b> is placed in <I>house number - {fifthlord_house}</I> and not in lagan. Note: {fifthlord} is placed in his <I>{fifthlord_placerelation}</I>.</I>.'''

        #Check if Karaka of the house is placed with the lord of the house or aspects the lord.
        if(karaka_house == fifthlord_house):
            clr3 = CLR_TRUE
            cause_cnt = cause_cnt + 1
            response3 = f'''<b><U>Satisfied</U></b>. The Karaka of fifth house for children is <b>{karaka}</b>. And Fifth House is <b>{fifthhouse["sign"]} [{fifthhouse["sign-num"]}]</b> which is ruled by <b>{fifthlord}</b>. Santana karaka <b>{karaka}</b> is conjunct with <b>{fifthlord}</b> in house number - {fifthlord_house}. Note: {karaka} is placed in his <I>{karaka_placerelation}</I>.'''
        elif (karaka in ad["D1"]["planets"][fifthlord]["Aspected-by"]):
            clr3 = CLR_TRUE
            cause_cnt = cause_cnt + 1
            response3 = f'''<b><U>Satisfied</U></b>. The Karaka of fifth house for children is <b>{karaka}</b>. And Fifth House is <b>{fifthhouse["sign"]} [{fifthhouse["sign-num"]}]</b>which is ruled by <b>{fifthlord}</b>. Santana karaka <b>{karaka}</b> is aspecting <b>{fifthlord}</b> in house number - {fifthlord_house}. Note: {karaka} is placed in house number - {karaka_house} in his <I>{karaka_placerelation}</I>.'''
        else:
            clr3 = CLR_FALSE
            response3 = f'''<b><U>Unsatisfied</U></b>. The Karaka of fifth house for children is <b>{karaka}</b>. And Fifth House is <b>{fifthhouse["sign"]} [{fifthhouse["sign-num"]}]</b>which is ruled by <b>{fifthlord}</b>. Santana karaka <b>{karaka}</b> is neither conjoint nor aspecting <b>{fifthlord}</b>.'''

        #Check if The lord is with or aspected by benefics.
        benefics = ad["D1"]["classifications"]["natural-benefics"]
        #benefics = ad["D1"]["classifications"]["benefics"]
        #print(f"The functional benefics are: {benefics}")
        planetswith_fifthlord = ad["D1"]["planets"][fifthlord]["conjuncts"]
        planetsaspecting_fifthlord = ad["D1"]["planets"][fifthlord]["Aspected-by"]
        beneficswith_fifthlord = list_intersection(benefics,planetswith_fifthlord)
        beneficsaspecting_fifthlord = list_intersection(benefics,planetsaspecting_fifthlord)
        clr4 = CLR_FALSE

        if(len(beneficswith_fifthlord) > 0): #if benefics conjunct with fifth lord
            clr4 = CLR_TRUE
            cause_cnt = cause_cnt + 1
            response4 = f'''The fifth lord <b>{fifthlord}</b> is conjunct with benefics : <b>{beneficswith_fifthlord}.</b>.'''
        if (len(beneficsaspecting_fifthlord) > 0): #If benefics are aspecting fifth lord
            clr4 = CLR_TRUE
            cause_cnt = cause_cnt + 1
            response4 = f'''The fifth lord <b>{fifthlord}</b> aspected by benefics : <b>{beneficsaspecting_fifthlord}.</b>.'''
        if(clr4 == CLR_FALSE):
            response4 = f'''<b><U>Unsatisfied</U></b>. The fifth lord <b>{fifthlord}</b> is neither conjunct with any benefics nor aspected by benefics.'''
        else:
            response4 = f'''<b><U>Satisfied</U></b>. {response4}'''

        #Check if the fifth lord is alone - no conjuncts and no aspects.
        if((len(planetswith_fifthlord) == 0) and (len(planetsaspecting_fifthlord) == 0)):
            clr5 = CLR_TRUE
            cause_cnt = cause_cnt + 1
            response5 = f'''<b><U>Satisfied</U></b>. The fifth lord <b>{fifthlord}</b> is independant which means no planet is conjoint or aspecting it.</b>.'''
        else:
            clr5 = CLR_FALSE
            response5 = f'''<b><U>Unsatisfied</U></b>. The fifth lord <b>{fifthlord}</b> is not independant. There are <b>{len(planetswith_fifthlord)}</b> planets in conjoint with fifth lord: <b>{planetswith_fifthlord}</b> and <b>{len(planetsaspecting_fifthlord)}</b> planets aspecting fifth lord: <b>{planetsaspecting_fifthlord}</b>.'''

        cnt_fifthlord_D1 = cause_cnt
        html_text = f'''<p><font color="blue" size="19"><b><U>Fifth Lord</U></b></font></p>
            <p>The fifth lord is the owner of the fifth house. His role is like any house owner in daily life. He is required to take care of the house. If the owner is good and is in good company, he will take care of the house. If he is careless and also is in bad company, he will not take care of the house. For a lord to be strong, any of the following conditions should be met:</p>
            <ul>
            <li><font color={clr1} size="16">Lord of the house is with the lord of lagan or is aspected by it.</font>: {response1}</li>
            </ul>
            <ul>
            <li><font color={clr2} size="16">Lord of the house is in lagan.</font>: {response2}</li>
            </ul>
            <ul>
            <li><font color={clr3} size="16">Karaka of the house is placed with the lord of the house or aspects the lord.</font>: {response3}</li>
            </ul>
            <ul>
            <li><font color={clr4} size="16">The lord is with or aspected by benefics.</font>: {response4}</li>
            </ul>
            <ul>
            <li><font color={clr5} size="16">When the lord is not associated or aspected by any planet, it can still promise the results.</font>: {response5}</li>
            </ul>
            <p>A good lord will make efforts to harness the fruits of the house. A bad lord will make no efforts to maintain the house and can destroy it.</p>
            <p> So when the <b>fifth lord</b> of <b>Lagna chart [D1]</b> is analysed with respect to children in {bd["name"]}'s life, <b>{cnt_fifthlord_D1}</b> out of above given 5 indications are positive. We need atleast 1 indication for positive outcome.</p>
            '''
        
        self.set_font('Helvetica', '', 13)
        self.set_text_color(30,40,30)
        self.write_html(html_text)
        self.ln()
        self.line(5, self.get_y(), self.w-5, self.get_y())
        self.ln()

        #Parameter of Karaka       
        cause_cnt = 0

        #Check if Karaka is in lagan
        if(karaka_house == 1):
            clr1 = CLR_TRUE
            cause_cnt = cause_cnt + 1
            response1 = f'''<b><U>Satisfied</U></b>. The Karaka of fifth house for children is <b>{karaka}</b> and is placed in <I>lagna or first house</I>. Note: {karaka} is placed in his <I>{karaka_placerelation}.</I>.'''
        else:
            clr1 = CLR_FALSE
            response1 = f'''<b><U>Unsatisfied</U></b>. The Karaka of fifth house for children is <b>{karaka}</b> and is not placed in <I>lagna or first house</I>.'''


        #Check if Karaka is with lord of lagan or aspected by it.
        karaka_aspectedby = ad["D1"]["planets"][karaka]["Aspected-by"]
        if(karaka == lagnalord):
            clr2 = CLR_TRUE
            cause_cnt = cause_cnt + 1
            response2 = f'''<b><U>Satisfied</U></b>. First House or lagan is <b>{lagna["sign"]} [{lagna["sign-num"]}]</b> which is ruled by <b>{lagnalord}</b>. In <I>D1 chart</I>, <b>{lagnalord}</b> himself is karaka Jupiter.'''
        elif(karaka_house == lagnalord_house):
            clr2 = CLR_TRUE
            cause_cnt = cause_cnt + 1
            response2 = f'''<b><U>Satisfied</U></b>. First House or lagan is <b>{lagna["sign"]} [{lagna["sign-num"]}]</b> which is ruled by <b>{lagnalord}</b>. In <I>D1 chart</I>, <b>{lagnalord}</b> and <b>{karaka}</b> are together in house number - {lagnalord_house}.'''
        elif (lagnalord in karaka_aspectedby):
            clr2 = CLR_TRUE
            cause_cnt = cause_cnt + 1
            response2 = f'''<b><U>Satisfied</U></b>. First House or lagan is <b>{lagna["sign"]} [{lagna["sign-num"]}]</b> which is ruled by <b>{lagnalord}</b>. In <I>D1 chart</I>, <b>{lagnalord}</b> placed in house number - {lagnalord_house} is aspecting <b>{karaka}</b> placed in house number - {karaka_house}.'''
        else:
            clr2 = CLR_FALSE
            response2 = f'''<b><U>Unsatisfied</U></b>. First House or lagan is <b>{lagna["sign"]} [{lagna["sign-num"]}]</b> which is ruled by <b>{lagnalord}</b>. In <I>D1 chart</I>, <b>{lagnalord}</b> placed in house number - {lagnalord_house} is neither conjunct nor aspecting <b>{karaka}</b> placed in house number - {karaka_house}.'''

        #check if Karaka is with lord of house or aspected by it.
        karaka_aspectedby = ad["D1"]["planets"][karaka]["Aspected-by"]
        if(karaka == fifthlord):
            clr3 = CLR_TRUE
            cause_cnt = cause_cnt + 1
            response3 = f'''<b><U>Satisfied</U></b>. Fifth House is <b>{fifthhouse["sign"]} [{fifthhouse["sign-num"]}]</b> which is ruled by <b>{fifthlord}</b>. In <I>D1 chart</I>, <b>{fifthlord}</b> himself is karaka Jupiter.'''
        elif(karaka_house == fifthlord_house):
            clr3 = CLR_TRUE
            cause_cnt = cause_cnt + 1
            response3 = f'''<b><U>Satisfied</U></b>. Fifth House is <b>{fifthhouse["sign"]} [{fifthhouse["sign-num"]}]</b> which is ruled by <b>{fifthlord}</b>. In <I>D1 chart</I>, <b>{fifthlord}</b> and <b>{karaka}</b> are together in house number - {fifthlord_house}.'''
        elif (fifthlord in karaka_aspectedby):
            clr3 = CLR_TRUE
            cause_cnt = cause_cnt + 1
            response3 = f'''<b><U>Satisfied</U></b>. Fifth House is <b>{fifthhouse["sign"]} [{fifthhouse["sign-num"]}]</b> which is ruled by <b>{fifthlord}</b>. In <I>D1 chart</I>, <b>{fifthlord}</b> placed in house number - {fifthlord_house} is aspecting <b>{karaka}</b> placed in house number - {karaka_house}.'''
        else:
            clr3 = CLR_FALSE
            response3 = f'''<b><U>Unsatisfied</U></b>. Fifth House is <b>{fifthhouse["sign"]} [{fifthhouse["sign-num"]}]</b> which is ruled by <b>{fifthlord}</b>. In <I>D1 chart</I>, <b>{fifthlord}</b> placed in house number - {fifthlord_house} is neither conjunct nor aspecting <b>{karaka}</b> placed in house number - {karaka_house}.'''

        #Check if Karaka is associated with benefics.
        benefics = ad["D1"]["classifications"]["natural-benefics"]
        #benefics = ad["D1"]["classifications"]["benefics"]
        #print(f"The functional benefics are: {benefics}")
        planetswith_karaka = ad["D1"]["planets"][karaka]["conjuncts"]
        planetsaspecting_karaka = ad["D1"]["planets"][karaka]["Aspected-by"]
        beneficswith_karaka = list_intersection(benefics,planetswith_karaka)
        beneficsaspecting_karaka = list_intersection(benefics,planetsaspecting_karaka)
        clr4 = CLR_FALSE

        if(len(beneficswith_karaka) > 0): #if benefics conjunct with karaka
            clr4 = CLR_TRUE
            cause_cnt = cause_cnt + 1
            response4 = f'''The karaka <b>{karaka}</b> is conjunct with benefics : <b>{beneficswith_karaka}.</b>.'''
        if (len(beneficsaspecting_karaka) > 0): #If benefics are aspecting fifth lord
            clr4 = CLR_TRUE
            cause_cnt = cause_cnt + 1
            response4 = f'''The karaka <b>{karaka}</b> aspected by benefics : <b>{beneficsaspecting_karaka}.</b>.'''
        if(clr4 == CLR_FALSE):
            response4 = f'''<b><U>Unsatisfied</U></b>. The karaka <b>{karaka}</b> is neither conjunct with any benefics nor aspected by benefics.'''
        else:
            response4 = f'''<b><U>Satisfied</U></b>. {response4}'''

        cnt_karaka_D1 = cause_cnt
        html_text = f'''<p><font color="blue" size="19"><b><U>Karaka</U></b></font></p>
            <p>Jupiter is the karaka for children. Karaka is seen for beauty. Beauty is not the looks but the devotion and respect a child gives to the parents. It determines the care given by children to the parent. A karaka is considered favorable when any of the following conditions are met:</p>
            <ul>
            <li><font color={clr1} size="16">Karaka is in lagan.</font>: {response1}</li>
            </ul>
            <ul>
            <li><font color={clr2} size="16">Karaka is with lord of lagan or aspected by it.</font>: {response2}</li>
            </ul>
            <ul>
            <li><font color={clr3} size="16">Karaka is with lord of house or aspected by it.</font>: {response3}</li>
            </ul>
            <ul>
            <li><font color={clr4} size="16">Karaka is associated with benefics.</font>: {response4}</li>
            </ul>
            <p> So when the <b>Santana Karaka Jupiter</b> in <b>Lagna chart [D1]</b> is analysed with respect to children in {bd["name"]}'s life, <b>{cnt_karaka_D1}</b> out of above given 5 indications are positive.</p>
            '''
        
        self.set_font('Helvetica', '', 13)
        self.set_text_color(30,40,30)
        self.write_html(html_text)
        self.ln()
        self.line(5, self.get_y(), self.w-5, self.get_y())
        self.ln()

        minshadbala = {"Sun": 390, "Moon": 360, "Mars": 300, "Mercury": 420, "Jupiter": 390, "Venus": 330, "Saturn": 300}
        shadbala = ad["Balas"]["Shadbala"]["Total"]
        bhavbalas = ad["Balas"]["BhavaBala"]["Total"].copy()
        rankorderofbhavabalas = rankdata(bhavbalas, method='dense')
        maxrank = max(rankorderofbhavabalas)
        bhavabalarank = [(maxrank+1)-x for x in rankorderofbhavabalas]
        # Define HTML code for the table
        html_text = f""" <p> Apart from above given details its is better to also notice shadbalas of relevant planets which are shown below. </p>
        <table border="1">
        <thead>
            <tr>
            <th>Planet</th>
            <th>Shadbala</th>
            <th>Min Req</th>
            </tr>
        </thead>
        <tbody>
            <tr>
            <td>Lagnesh - {lagnalord}</td>
            <td>{shadbala[lagnalord]}</td>
            <td>{minshadbala[lagnalord]}</td>
            </tr>
            <tr>
            <td>FifthLord - {fifthlord}</td>
            <td>{shadbala[fifthlord]}</td>
            <td>{minshadbala[fifthlord]}</td>
            </tr>
            <tr>
            <td>Karaka - {karaka}</td>
            <td>{shadbala[karaka]}</td>
            <td>{minshadbala[karaka]}</td>
            </tr>
        </tbody>
        </table>
        <p> Also the strength of houses in astrology is measured by bhavabala and rank is decided from 1 to 12 for 12 bhavas. 
        Usually bhavas of first 5 ranks will be good in a persons life. In {bd["name"]}'s birth chart Fifth house is having 
        bhava-bala of {bhavbalas[4]} virupas and is given rank number {bhavabalarank[4]}.</p>
        """

        self.set_font('Times', '', 14)
        self.set_text_color(0,0,0)
        self.set_fill_color(250,250,250)
        self.write_html(html_text)
        self.ln()
        self.line(5, self.get_y(), self.w-5, self.get_y())
        self.ln()

        return
    
    def add_analysis_Sphuta(self,ad):
        #title of the page
        self.set_font('Arial', 'BU', 16)
        self.set_text_color(230,30,0)
        sphuta = ad["special_points"]["sphuta"]
        sphuta["D3"]["signlord"] = lord_of_sign[sphuta["D3"]["sign"]]
        sphuta["D7"]["signlord"] = lord_of_sign[sphuta["D7"]["sign"]]
        sphuta["D9"]["signlord"] = lord_of_sign[sphuta["D9"]["sign"]]
        self.cell(txt=f'''Analysis of {bd["name"]}'s Sphuta''', w=0, h=10, align='C')
        self.ln()
        cnt_sphuta = 0
        response = f""""""
        #Section for areas to consider
        html_text = f"""
        <p><font color="blue" size="19"><b><U>BEEJA SPHUTA AND KSHETRA SPHUTA</U></b></font></p>
        <p><b>Beeja Sphuta (BS)</b> and <b>Kshetra Sphuta (KS)</b> are mathematically derived points for a horoscope. 
        BS is worked out for a male horoscope and KS for a female horoscope. 
        Beeja means seed and Kshetra means field. This point indicates the capability to produce a child and the worthiness of children.</p>"""
        

        if sphuta['type'] == "Beeja":
            if (signnum(sphuta["D1"]["sign"])%2 == 1):
                clr_D1 = CLR_TRUE
                cnt_sphuta = cnt_sphuta + 1
                response = response + f"""In <b>Rashi chart</b>, BS is in odd sign. """
            else:
                clr_D1 = CLR_FALSE
                response = response + f"""In <b>Rashi chart</b>, BS is in even sign. """

            if (signnum(sphuta["D7"]["sign"])%2 == 1):
                clr_D7 = CLR_TRUE
                cnt_sphuta = cnt_sphuta + 1
                response = response + f"""In <b>Saptamsha chart</b>, BS is in odd sign. """
            else:
                clr_D7 = CLR_FALSE
                response = response + f"""In <b>Saptamsha chart</b>, BS is in even sign. """

            if (signnum(sphuta["D9"]["sign"])%2 == 1):
                clr_D9 = CLR_TRUE
                cnt_sphuta = cnt_sphuta + 1
                response = response + f"""In <b>Navamsha chart</b>, BS is in odd sign. """
            else:
                clr_D9 = CLR_FALSE
                response = response + f"""In <b>Navamsha chart</b>, BS is in even sign. """

            html_text = html_text + f"""<p><b>Beeja Sphuta</b> is the sum of the longitude of <b>Jupiter, Venus and Sun</b>. 
            The longitudes are taken from <I>first point of Aries</I>. The BS should be in an <I>odd sign</I> in <b>Rashi chart, 
            navamsha</b> and <b>saptamsha</b> charts to promise progeny. We examine the <b>BS</b> and <b>its lord</b> in all three charts.
            For {bd["name"]}, when we calculate <I>Beeja Sphuta</I> in all 3 charts we get below results:</p>
            <table border="3" cellpadding="5">
            <thead>
                <tr>
                <th>Chart</th>
                <th>Sign</th>
                <th>Signlord</th>
                <th>degree</th>
                <th>Nakshatra</th>
                <th>Nakshatra lord</th>
                <th>House</th>
                </tr>
            </thead>
            <tbody>
                <tr><font color={clr_D1}>
                <td>D1</td>
                <td>{sphuta["D1"]["sign"]}</td>
                <td>{sphuta["D1"]["signlord"]}</td>
                <td>{round(sphuta["D1"]["pos"]["dec_deg"],2)}</td>
                <td>{sphuta["D1"]["nakshatra"]}</td>
                <td>{sphuta["D1"]["nak-ruler"]}</td>
                <td>{sphuta["D1"]["house-num"]}</td>
                </font></tr>
                <tr><font color={clr_D7}>
                <td>D7</td>
                <td>{sphuta["D7"]["sign"]}</td>
                <td>{sphuta["D7"]["signlord"]}</td>
                <td>{round(sphuta["D7"]["pos"]["dec_deg"],2)}</td>
                <td>{sphuta["D7"]["nakshatra"]}</td>
                <td>{sphuta["D7"]["nak-ruler"]}</td>
                <td>{sphuta["D7"]["house-num"]}</td>
                </font></tr>
                <tr><font color={clr_D9}>
                <td>D9</td>
                <td>{sphuta["D9"]["sign"]}</td>
                <td>{sphuta["D9"]["signlord"]}</td>
                <td>{round(sphuta["D9"]["pos"]["dec_deg"],2)}</td>
                <td>{sphuta["D9"]["nakshatra"]}</td>
                <td>{sphuta["D9"]["nak-ruler"]}</td>
                <td>{sphuta["D9"]["house-num"]}</td>
                </font></tr>
            </tbody>
            </table>
            <p>As you can see, {response}. So there are <b>{cnt_sphuta} out of 3 points</b> indicating capability of producing a child.</p>
            """
        
        else:
            if (signnum(sphuta["D1"]["sign"])%2 == 0):
                clr_D1 = CLR_TRUE
                cnt_sphuta = cnt_sphuta + 1
                response = response + f"""In <b>Rashi chart</b>, KS is in even sign. """
            else:
                clr_D1 = CLR_FALSE
                response = response + f"""In <b>Rashi chart</b>, KS is in odd sign. """

            if (signnum(sphuta["D7"]["sign"])%2 == 0):
                clr_D7 = CLR_TRUE
                cnt_sphuta = cnt_sphuta + 1
                response = response + f"""In <b>Saptamsha chart</b>, KS is in even sign. """
            else:
                clr_D7 = CLR_FALSE
                response = response + f"""In <b>Saptamsha chart</b>, KS is in odd sign. """

            if (signnum(sphuta["D9"]["sign"])%2 == 0):
                clr_D9 = CLR_TRUE
                cnt_sphuta = cnt_sphuta + 1
                response = response + f"""In <b>Navamsha chart</b>, KS is in even sign. """
            else:
                clr_D9 = CLR_FALSE
                response = response + f"""In <b>Navamsha chart</b>, KS is in odd sign. """

            html_text = html_text + f"""<p><b>Kshetra Sphuta</b> is the sum of the longitudes of 
            <b>Jupiter, Mars</b> and <b>Moon</b> in female chart. The KS and its lord should occupy even sign 
            in Rashi chart, navamsha and saptamsha chart.
            For {bd["name"]}, when we calculate <I>Kshetra Sphuta</I> in all 3 charts we get below results:</p>
            <table border="3" cellpadding="5">
            <thead>
                <tr>
                <th>Chart</th>
                <th>Sign</th>
                <th>Signlord</th>
                <th>degree</th>
                <th>Nakshatra</th>
                <th>Nakshatra lord</th>
                <th>House</th>
                </tr>
            </thead>
            <tbody>
                <tr><font color={clr_D1}>
                <td>D1</td>
                <td>{sphuta["D1"]["sign"]}</td>
                <td>{sphuta["D1"]["signlord"]}</td>
                <td>{round(sphuta["D1"]["pos"]["dec_deg"],2)}</td>
                <td>{sphuta["D1"]["nakshatra"]}</td>
                <td>{sphuta["D1"]["nak-ruler"]}</td>
                <td>{sphuta["D1"]["house-num"]}</td>
                </font></tr>
                <tr><font color={clr_D7}>
                <td>D7</td>
                <td>{sphuta["D7"]["sign"]}</td>
                <td>{sphuta["D7"]["signlord"]}</td>
                <td>{round(sphuta["D7"]["pos"]["dec_deg"],2)}</td>
                <td>{sphuta["D7"]["nakshatra"]}</td>
                <td>{sphuta["D7"]["nak-ruler"]}</td>
                <td>{sphuta["D7"]["house-num"]}</td>
                </font></tr>
                <tr><font color={clr_D9}>
                <td>D9</td>
                <td>{sphuta["D9"]["sign"]}</td>
                <td>{sphuta["D9"]["signlord"]}</td>
                <td>{round(sphuta["D9"]["pos"]["dec_deg"],2)}</td>
                <td>{sphuta["D9"]["nakshatra"]}</td>
                <td>{sphuta["D9"]["nak-ruler"]}</td>
                <td>{sphuta["D9"]["house-num"]}</td>
                </font></tr>
            </tbody>
            </table>
            <p>As you can see, {response}. So there are <b>{cnt_sphuta} out of 3 points</b> indicating capability of producing a child.</p>
            """
        self.set_font('Helvetica', '', 13)
        self.set_text_color(10,10,10)
        self.write_html(html_text)


        #laganlord and fifth lord and karaka of birthchart analysis in  saptamsha chart
        D1_laganlord = ad["D1"]["houses"][0]["sign-lord"]
        D1_fifthlord = ad["D1"]["houses"][4]["sign-lord"]

        html_text = f"""<p>The lagan lord, fifth lord of birth chart and Jupiter are seen in the saptamsha for their placement, conjunction and aspect received by them.</p>
        <p>In <b>{bd["name"]}'s</b> birth chart [leftside], the <b>lagan lord is {D1_laganlord}[lord of {ad["D1"]["houses"][0]["sign"]}]</b>. The <b>fifth lord is {D1_fifthlord}[lord of {ad["D1"]["houses"][4]["sign"]}]</b>.</p>        
        <p>In <b>Saptamsha chart</b> which is displayed rightside below of native, 
        D1 lagan lord <b>{D1_laganlord}</b> is placed in <b>house number {ad["D7"]["planets"][D1_laganlord]["house-num"]}</b> in the sign of <b>{ad["D7"]["planets"][D1_laganlord]["sign"]}</b> which is his <b>{ad["D7"]["planets"][D1_laganlord]["house-rel"]} sign</b>. The lagan lord is conjunct with <b>{len(ad["D7"]["planets"][D1_laganlord]["conjuncts"])} planets {ad["D7"]["planets"][D1_laganlord]["conjuncts"]}</b> and aspected by <b>{len(ad["D7"]["planets"][D1_laganlord]["Aspected-by"])} planets {ad["D7"]["planets"][D1_laganlord]["Aspected-by"]}</b>.
        D1 fifth lord <b>{D1_fifthlord}</b> is placed in <b>house number {ad["D7"]["planets"][D1_fifthlord]["house-num"]}</b> in the sign of <b>{ad["D7"]["planets"][D1_fifthlord]["sign"]}</b> which is his <b>{ad["D7"]["planets"][D1_fifthlord]["house-rel"]} sign</b>. The fifth lord is conjunct with <b>{len(ad["D7"]["planets"][D1_fifthlord]["conjuncts"])} planets {ad["D7"]["planets"][D1_fifthlord]["conjuncts"]}</b> and aspected by <b>{len(ad["D7"]["planets"][D1_fifthlord]["Aspected-by"])} planets {ad["D7"]["planets"][D1_fifthlord]["Aspected-by"]}</b>.
        And Santana karaka <b>Jupiter</b> is placed in <b>house number {ad["D7"]["planets"]["Jupiter"]["house-num"]}</b> in the sign of <b>{ad["D7"]["planets"]["Jupiter"]["sign"]}</b> which is his <b>{ad["D7"]["planets"]["Jupiter"]["house-rel"]} sign</b>. Jupiter is conjunct with <b>{len(ad["D7"]["planets"]["Jupiter"]["conjuncts"])} planets {ad["D7"]["planets"]["Jupiter"]["conjuncts"]}</b> and aspected by <b>{len(ad["D7"]["planets"]["Jupiter"]["Aspected-by"])} planets {ad["D7"]["planets"]["Jupiter"]["Aspected-by"]}</b>.
        </p>
        <table cellpadding="5">
        <tr>
            <td><img src="./charts/NorthChart_D1.png" width="50"></td>
            <td><img src="./charts/NorthChart_D7.png" width="50"></td>
        </tr>
        </table>
        """
        #self.add_page()
        self.set_font('Helvetica', '', 13)
        self.set_text_color(10,10,100)
        self.write_html(html_text)

        D7_sphutalord = sphuta["D7"]["signlord"]
        D7_housediff_D1lagnesh2D7Sphutalord = housediff(ad["D7"]["planets"][D1_laganlord]["house-num"],ad["D7"]["planets"][D7_sphutalord]["house-num"])
        D7_housediff_D1panchamesh2D7Sphutalord = housediff(ad["D7"]["planets"][D1_fifthlord]["house-num"],ad["D7"]["planets"][D7_sphutalord]["house-num"])
        
        html_text = f'''<p>The lord of BS or KS in saptamsha chart is seen for luxuries. 
        It should have good relation with Lagan lord and fifth lord of birth chart in saptamsha 
        and well placed in D7 to grant a luxurious life.</p>
        <p>In {bd["name"]},s kundali, the lord of {sphuta["symbol"]} in saptamsha chart is <b>{D7_sphutalord}</b> who is placed in <b>house number {ad["D7"]["planets"][D7_sphutalord]["house-num"]}</b> in the sign of <b>{ad["D7"]["planets"][D7_sphutalord]["sign"]}</b> which is his <b>{ad["D7"]["planets"][D7_sphutalord]["house-rel"]} sign</b>. He is conjunct with <b>{len(ad["D7"]["planets"][D7_sphutalord]["conjuncts"])} planets {ad["D7"]["planets"][D7_sphutalord]["conjuncts"]}</b> and aspected by <b>{len(ad["D7"]["planets"][D7_sphutalord]["Aspected-by"])} planets {ad["D7"]["planets"][D7_sphutalord]["Aspected-by"]}</b>.
        The lagan lord of birth chart <b>{D1_laganlord}</b>. In D7-Saptamsha chart, {relation(D1_laganlord,D7_sphutalord,"D7", ad)}. 
        The fifth lord of birth chart <b>{D1_fifthlord}</b>. In D7-Saptamsha chart, {relation(D1_fifthlord,D7_sphutalord,"D7", ad)}. </p>
        <p>If it is in 6,8,12 from birth Lagan lord it gives physical problems, when it is in 6,8,12 from fifth lord of birth chart then problems due to poorva punya.
        D7 sphuta lord <b>{D7_sphutalord}</b> is in <b>{D7_housediff_D1lagnesh2D7Sphutalord}{nth(D7_housediff_D1lagnesh2D7Sphutalord)}</b> house from D1 lagnesh <b>{D1_laganlord}</b> 
        and is <b>{D7_housediff_D1panchamesh2D7Sphutalord}{nth(D7_housediff_D1lagnesh2D7Sphutalord)}</b> house from D1 fifth house lord <b>{D1_fifthlord}</b>.</p>'''

        self.set_font('Helvetica', '', 13)
        self.set_text_color(10,10,100)
        self.write_html(html_text)
        self.ln()

        #Section for Bahu putra yoga
        cnt_bahuputra = 0
        #Check if Sun and Jupiter are in the navamsha of Sagittarius and Gemini. 
        #They can be singly or together in any of these signs
        D9_sunsign = ad["D9"]["planets"]["Sun"]["sign"]
        D9_jupitersign = ad["D9"]["planets"]["Jupiter"]["sign"]
        if(((D9_sunsign == "Saggitarius") and (D9_jupitersign == "Gemini")) or
           ((D9_sunsign == "Gemini") and (D9_jupitersign == "Saggitarius")) or
           ((D9_sunsign == "Gemini") and (D9_jupitersign == "Gemini")) or
           ((D9_sunsign == "Saggitarius") and (D9_jupitersign == "Saggitarius"))):
            clr1 = CLR_TRUE
            cnt_bahuputra = cnt_bahuputra + 1
            response1 = f"""<b><U>Satisfied</U></b>. In <b>Navamsha chart</b> of <b>{bd["name"]}'s</b> kundali, 
            <b>Sun</b> is in <b>{D9_sunsign} sign</b> and <b>Jupiter</b> is in <b>{D9_jupitersign} sign</b>."""
        else:
            clr1 = CLR_FALSE
            response1 = f"""<b><U>Unsatisfied</U></b>. In <b>Navamsha chart</b> of <b>{bd["name"]}'s</b> kundali, 
            <b>Sun</b> is in <b>{D9_sunsign} sign</b> and <b>Jupiter</b> is in <b>{D9_jupitersign} sign</b>."""

        #check if Rahu is in the fifth house in navamsha but not in the sign of Saturn.
        D9_rahudispositor = ad["D9"]["planets"]["Rahu"]["dispositor"]
        D9_rahuhouse = ad["D9"]["planets"]["Rahu"]["house-num"]
        if ((D9_rahuhouse == 5) and (D9_rahudispositor != "Saturn")):
            clr2 = CLR_TRUE
            cnt_bahuputra = cnt_bahuputra + 1
            response2 = f"""<b><U>Satisfied</U></b>. In <b>Navamsha chart</b> of <b>{bd["name"]}'s</b> kundali, 
            <b>Rahu</b> is in <b>{D9_rahuhouse}{nth(D9_rahuhouse)} house</b> and in the sign of <b>{D9_rahudispositor}</b>."""
        else:
            clr2 = CLR_FALSE
            response2 = f"""<b><U>Unsatisfied</U></b>. In <b>Navamsha chart</b> of <b>{bd["name"]}'s</b> kundali, 
            <b>Rahu</b> is in <b>{D9_rahuhouse}{nth(D9_rahuhouse)} house</b> and in the sign of <b>{D9_rahudispositor}</b>."""

        #check if the seventh lord of D1 or D9 joins lord of 
        #first, second or fifth of D1 in birth horoscope.
        D1_seventhlord = ad["D1"]["houses"][6]["sign-lord"]
        D9_seventhlord = ad["D9"]["houses"][6]["sign-lord"]
        D1_secondlord = ad["D1"]["houses"][1]["sign-lord"]
        clr3 = CLR_FALSE
        response3 = ""
        #check if seventh lord of D1 joins first lord of D1 in lagna chart
        if (D1_seventhlord in ad["D1"]["planets"][D1_laganlord]["conjuncts"]):
            clr3 = CLR_TRUE
            cnt_bahuputra = cnt_bahuputra + 1
            response3 = f"""Seventh Lord of D1 chart <b>{D1_seventhlord}</b> is conjunct with lord of first house of D1 chart {D1_laganlord} in birth chart. """
        #check if seventh lord of D9 joins first lord of D1 in lagna chart
        if (D9_seventhlord in ad["D1"]["planets"][D1_laganlord]["conjuncts"]):
            clr3 = CLR_TRUE
            cnt_bahuputra = cnt_bahuputra + 1
            response3 = f"""Seventh Lord of D9 chart <b>{D9_seventhlord}</b> is conjunct with lord of first house of D1 chart {D1_laganlord} in birth chart. """
        #check if seventh lord of D1 joins second lord of D1 in lagna chart
        if (D1_seventhlord in ad["D1"]["planets"][D1_secondlord]["conjuncts"]):
            clr3 = CLR_TRUE
            cnt_bahuputra = cnt_bahuputra + 1
            response3 = f"""Seventh Lord of D1 chart <b>{D1_seventhlord}</b> is conjunct with lord of second house of D1 chart {D1_secondlord} in birth chart. """
        #check if seventh lord of D9 joins second lord of D1 in lagna chart
        if (D9_seventhlord in ad["D1"]["planets"][D1_secondlord]["conjuncts"]):
            clr3 = CLR_TRUE
            cnt_bahuputra = cnt_bahuputra + 1
            response3 = f"""Seventh Lord of D9 chart <b>{D9_seventhlord}</b> is conjunct with lord of second house of D1 chart {D1_secondlord} in birth chart. """
        #check if seventh lord of D1 joins fifth lord of D1 in lagna chart
        if (D1_seventhlord in ad["D1"]["planets"][D1_fifthlord]["conjuncts"]):
            clr3 = CLR_TRUE
            cnt_bahuputra = cnt_bahuputra + 1
            response3 = f"""Seventh Lord of D1 chart <b>{D1_seventhlord}</b> is conjunct with lord of fifth house of D1 chart {D1_fifthlord} in birth chart. """
        #check if seventh lord of D9 joins fifth lord of D1 in lagna chart
        if (D9_seventhlord in ad["D1"]["planets"][D1_fifthlord]["conjuncts"]):
            clr3 = CLR_TRUE
            cnt_bahuputra = cnt_bahuputra + 1
            response3 = f"""Seventh Lord of D9 chart <b>{D9_seventhlord}</b> is conjunct with lord of fifth house of D1 chart {D1_fifthlord} in birth chart. """
        
        if(clr3 == CLR_TRUE):
            response3 = f"""<b><U>Satisfied</U></b>. In <b>Lagna chart</b> of <b>{bd["name"]}'s</b> kundali, {response3}."""
        else:
            response3 = f"""<b><U>Unsatisfied</U></b>. In <b>Lagna chart</b> of <b>{bd["name"]}'s</b> kundali, None of these combination is met."""
        
        
        html_text = f"""
        <p><font color="blue" size="19"><b><U>BAHU PUTRA YOGA</U></b></font></p>
        <p>Birth of many children born to a person goes with the name of <b>Bahu Purta Yoga</b>. 
        Classics gives many combinations for this yoga. These yogas are given in birth horoscope.</p>
        <ul>
        <li><font color={clr1} size="16">Sun and Jupiter are in the navamsha of Sagittarius and Gemini. They can be singly or together in any of these signs.</font>: {response1}</li>
        </ul>
        <ul>
        <li><font color={clr2} size="16">Rahu is in the fifth house in navamsha but not in the sign of Saturn.</font>: {response2}</li>
        </ul>
        <ul>
        <li><font color={clr3} size="16">The seventh lord of D1 or D9 joins lord of first, second or fifth of D1 in birth horoscope.</font>: {response3}</li>
        </ul>
        <p>So In total, <b>{cnt_bahuputra} out of 3</b> combinations indicating <I>Bahu Putra Yoga</I> are met. Atleast one combination need to be met for possibility of having multiple children as per Vedic astrology.</p>
        """

        self.set_font('Times', '', 13)
        self.set_text_color(10,10,10)
        self.write_html(html_text)
        self.ln()
        self.line(5, self.get_y(), self.w-5, self.get_y())
        self.ln(5)
        return
    
    def add_santanatithi(self,ad):

        #Step 1: Subtract the longitude of Sun from that of Moon.
        sun_pos = f"""{ad["D1"]["planets"]["Sun"]["sign"]} sign {round(ad["D1"]["planets"]["Sun"]["pos"]["dec_deg"],2)} degrees"""
        moon_pos = f"""{ad["D1"]["planets"]["Moon"]["sign"]} sign {round(ad["D1"]["planets"]["Moon"]["pos"]["dec_deg"],2)} degrees"""
        sun2moon = round(get_distancebetweenplanets(ad["D1"], "Sun", "Moon") / 3600,2)
        
        #Step 2:  multiply by 5
        deg = sun2moon * 5

        #Step 3: Expunge multiples of 360 from the product till the remainder is 360 or less than 360.
        finaldeg = deg % 360

        #Step 4: Find out the paksha and tithi from this remainder.
        paksha,tithi = compute_pakshatithi4mdegree(finaldeg)

        html_text = f"""
        <p><font color="blue" size="20"><b><U>SANTANA TITHI</U></b></font></p>
        <p><b>Jatakdesamarga</b> gives concept of <b>Santana tithi</b> for assessing the possibility of child birth 
        and the problems which can be faced by a person in this regard. A step by step method of calculation is given to work out Santana tithi for a horoscope:</p>
        <ol>
        <li><font color="purple" size="16">Subtract the longitude of Sun from that of Moon.</font> 
        In D1 chart the Sun position is {sun_pos} and moon position is {moon_pos}. The difference between their longitudes is {sun2moon} degrees.</li>
        <li><font color="purple" size="16">Multiply the difference by 5</font> The answer is {deg} degrees.</li>
        <li><font color="purple" size="16">Expunge multiples of 360 from the product till the remainder is 360 or less than 360.</font> The answer is {finaldeg} degrees.</li>
        <li><font color="purple" size="16">Find out the paksha and tithi from this remainder.</font> When computed the paksha is <b>{paksha} paksha</b> and <b>{tithi}{nth(tithi)} tithi</b>.</li>
        </ol>
        <p><b>Rules for Examination of Santana Tithi:</b></p>
        <ol>
            <li>When the paksha is Shukla paksha (SP), there will be progeny.</li>
            <li>If the paksha is Krishna paksha (KP), there will be difficulty in getting progeny.</li>
            <li>For tithi prior to the sixth in SP, there will be progeny but slowly and gradually.</li>
            <li>For tithi after the tenth of SP, it will be quick.</li>
            <li>If tithi is prior to the sixth in KP, there will be progeny after worshiping GOD Subramanian.</li>
            <li>For four tithi from the seventh in KP, he may have progeny after the second marriage and by feeding Brahmins.</li>
            <li>For the eleventh and twelfth tithi of KP, there may be conception, but no issue is possible.</li>
            <li>For the thirteenth and fourteenth tithi of KP, he should adopt a child.</li>
            <li>If it is amavasya, even adoption is not possible.</li>
            <li>The Rikta tithi of both paksha are not conducive to any auspicious results.</li>
        </ol>
        """

        self.set_font('Times', '', 13)
        self.set_text_color(10,10,10)
        self.write_html(html_text)
        self.ln()
        self.line(5, self.get_y(), self.w-5, self.get_y())
        self.ln()
        return




    


#Generate Astrological data and plot charts
astrodata = astrocalc.generate_astrodata(bd)
astrocalc.plot_astrocharts(astrodata,"./charts/")



# Create PDF Report
pdf = SapthamsaReportPDF()
pdf.set_left_margin(10)
pdf.set_right_margin(10)

#Adding first page of Report details
pdf.add_page()
pdf.add_firstPage()

#Adding section for astrocharts
pdf.add_page()
pdf.add_astrocharts(astrodata)

#Adding section related to D1 chart 
pdf.add_page()
pdf.add_analysis_D1chart(astrodata)

#Adding section related to Beeja Sphuta or Kshetra Sphuta
pdf.add_page()
pdf.add_analysis_Sphuta(astrodata)

#Add section related to santana tithi
#pdf.add_page()
pdf.add_santanatithi(astrodata)

# Save PDF to a file
pdf_output_path = f'./report/sapthamsa_report_{bd["name"]}.pdf'
pdf.output(pdf_output_path)
print(f'PDF report generated and saved to: {pdf_output_path}')
print("\n*****************SUCCESS*****************\n")
