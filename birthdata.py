#This page contains birthdetails of people. 
#The birth data to be taken has to be updated to birthdata variable.
#sample birthdata is given here
samplebirthdataname = {
    "name" : "",
    "gender" : "", #options: male, female
    "DOB"     : {   "year"     : "",
                    "month"    : "",
                    "day"      : ""
                },
    "TOB"     : {   "hour"     : "",  #in 24 hour format
                    "min"      : "",
                    "sec"      : ""
                }, 
    "POB"     : {   "name"     : "",
                    "lat"      : "",     #+ve for North and -ve for south
                    "lon"      : "",     #+ve for East and -ve for West
                    "timezone" : ""
                }
}


bd_shyambhat = {
    "name" : "Shyam Bhat",
    "gender" : "male", #options: male, female
    "DOB"     : {   "year"     : "1991",
                    "month"    : "10",
                    "day"      : "8"
                },
    "TOB"     : {   "hour"     : "14",  #in 24 hour format
                    "min"      : "47",
                    "sec"      : "9"
                }, 
    "POB"     : {   "name"     : "Honavar",
                    "lat"      : "+14.2798",     #+ve for North and -ve for south
                    "lon"      : "+74.4439",     #+ve for East and -ve for West
                    "timezone" : "+5.5"
                }
}

birthdata = bd_shyambhat