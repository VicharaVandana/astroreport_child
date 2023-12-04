from fpdf import FPDF
from birthdata import birthdata as bd
from datetime import datetime as dt
import astrological_calculations as astrocalc

class SapthamsaReportPDF(FPDF):
    def header(self):
        # Logo
        self.image('./report/ganeshalogo.jpeg', 185, 2, h=20, w=20)
        # Times bold 15
        self.set_font('Times', 'B', 18)
        # Title
        self.cell(170, 10, f'Saptamsha Astrology Report for {bd["name"]}',ln=True,border=True, align='C')
        

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
        is scrutinized along with its planetary influences. 
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
        Analyzing planetary positions within this chart offers insights into the number and well-being of children.  
        Timing predictions for childbirth are deduced through careful scrutiny of <b>Dasha periods</b> and planetary transits within the Saptamsha Chart. 
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
        this chart examines planetary placements and the influence of benefic planets, 
        especially <i>Jupiter</i>, for insights into the potential for progeny. 
        Analysis of the ninth house lord and its interactions with other planets, along with timing predictions 
        derived from <b>Dasha periods</b> and planetary transits, provides a comprehensive understanding of 
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

# Save PDF to a file
pdf_output_path = f'./report/sapthamsa_report_{bd["name"]}.pdf'
pdf.output(pdf_output_path)
print(f'PDF report generated and saved to: {pdf_output_path}')
print("\n*****************SUCCESS*****************\n")
