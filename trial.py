from html2image import Html2Image
hti = Html2Image()

svg_code = """
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"/>
        <line x1="12" y1="8" x2="12" y2="12"/>
        <line x1="12" y1="16" x2="12" y2="16"/>
    </svg>
"""

hti.output_path = './charts/'
hti.browser.flags = ['--default-background-color=00000000']
hti.screenshot(other_file="./charts/NorthChart_D1.svg", size=(500, 500), save_as="NorthChart_D1.png")






