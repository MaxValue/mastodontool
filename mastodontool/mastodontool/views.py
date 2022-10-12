from statistics import quantiles
from django.shortcuts import render
from uptime.models import Uptime
import pandas as pd
from plotly.offline import plot
import plotly.express as px
from django.urls import reverse
from django.http import HttpResponseRedirect
import plotly.graph_objects as go
import psycopg2
import requests

mapping={'aa':'Afar','ab':'Abkhazian','af':'Afrikaans','ak':'Akan','am':'Amharic','an':'Aragonese','as':'Assamese','av':'Avaric','ay':'Aymara','az':'Azerbaijani','ay':'Aymara','ar':'Arabic','be':'Belarusian','bm':'Bambara','ba':'Bashkir','be':'Belarusian','bn':'Bengali','bi':'Bislama','bs':'Bosnian','br':'Breton','my':'Burmese','bg':'Bulgarian','eu':'Basque','ca':'Catalan','ce':'Chechen','cv':'Chuvash','cr':'Cree','co':'Corsican','cu':'ChurchSlavic','ch':'Chamorro','cs':'Czech','cy':'Welsh','da':'Danish','de':'German','dv':'Divehi','dz':'Dzongkha','ee':'Ewe','el':'Greek','en':'English','eo':'Esperanto','es':'Spanish','et':'Estonian','eu':'Basque','fa':'Persian','ff':'Fulah','fj':'Fijian','fo':'Faroese','fy':'WesternFrisian','fi':'Finnish','fr':'French','ga':'Irish','gd':'ScottishGaelic','gl':'Galician','gn':'Guarani','gu':'Gujarati','gv':'Manx','ha':'Hausa','he':'Hebrew','hi':'Hindi','ho':'HiriMotu','hr':'Croatian','ht':'Haitian','hu':'Hungarian','hy':'Armenian','hz':'Herero','ia':'Interlingua','ie':'Interlingue','ig':'Igbo','ii':'SichuanYi','ik':'Inupiaq','io':'Ido','iu':'Inuktitut','jv':'Javanese','ka':'Georgian','kg':'Kongo','kj':'Kuanyama','kk':'Kazakh','kl':'Kalaallisut','km':'CentralKhmer','kn':'Kannada','kr':'Kanuri','ks':'Kashmiri','ku':'Kurdish','kv':'Komi','kw':'Cornish','ky':'Kirghiz','la':'Latin','lb':'Luxembourgish','lg':'Ganda','li':'Limburgan','ln':'Lingala','lo':'Lao','mg':'Malagasy','mh':'Marshallese','mi':'Maori','ml':'Malayalam','mr':'Marathi','ms':'Malay','mt':'Maltese','my':'Burmese','na':'Nauru','nd':'NorthNdebele','ng':'Ndonga','no':'Norwegian','nr':'SouthNdebele','nv':'Navajo','ny':'Chichewa','oc':'Occitan','oj':'Ojibwa','om':'Oromo','or':'Oriya','os':'Ossetian','pa':'Punjabi','pi':'Pali','ps':'Pashto','qu':'Quechua','rm':'Romansh','rn':'Rundi','rw':'Kinyarwanda','sa':'Sanskrit','sc':'Sardinian','sd':'Sindhi','se':'NorthernSami','sg':'Sango','sh':'Serbo-Croatian','si':'Sinhala','sm':'Samoan','sn':'Shona','so':'Somali','ss':'Swati','st':'SouthernSotho','su':'Sundanese','sw':'Swahili','ta':'Tamil','te':'Telugu','tg':'Tajik','ti':'Tigrinya','tk':'Turkmen','tl':'Tagalog','tn':'Tswana','to':'Tonga','ts':'Tsonga','tt':'Tatar','tw':'Twi','ty':'Tahitian','ug':'Uighur','ur':'Urdu','uz':'Uzbek','ve':'Venda','vo':'Volapük','wa':'Walloon','wo':'Wolof','xh':'Xhosa','yo':'Yoruba','za':'Zhuang','zu':'Zulu','id':'Indonesian','is':'Icelandic','it':'Italian','ja':'Japanese','ko':'Korean','lt':'Lithuanian','lv':'Latvian','mk':'Macedonian','mn':'Mongolian','mo':'Moldavian','ne':'Nepali','nl':'Dutch','nn':'Norwegian','pl':'Polish','pt':'Portuguese','ro':'Romanian','ru':'Russian','sk':'Slovak','sl':'Slovenian','sq':'Albanian','sr':'Serbian','sv':'Swedish','th':'Thai','tr':'Turkish','uk':'Ukrainian','vi':'Vietnamese','yi':'Yiddish','zh':'Chinese'}

def index(request):
    return render(request, 'index.html')

# view(same as your question)
def instance_info(request):

    if request.method == 'GET':
        id = request.GET.get('id')


        url = 'https://instances.social/api/1.0/instances/show'
        key = 'Authorization: bearer xVyfYF0mSOnYS6Zlx34racvGlZwRxGKJsMAPYJndBpcyVCWOxrEUK6WZOg4r3Cmbboz1Jzkp9s2jibqYLQRNtCtKNGkqoA74e7O9TrWUuprX8dGlyrxrwa1Lrq8AKES0'

        params = {'name': id} 

        response = requests.get(url, params,
                                headers={'Authorization':'Bearer xVyfYF0mSOnYS6Zlx34racvGlZwRxGKJsMAPYJndBpcyVCWOxrEUK6WZOg4r3Cmbboz1Jzkp9s2jibqYLQRNtCtKNGkqoA74e7O9TrWUuprX8dGlyrxrwa1Lrq8AKES0'})

        
        #data_dict = response.json()
        instanceinfo = response.json()
        #instancedf = pd.DataFrame.from_dict(data_dict, orient ='index')
        #instancedf.reset_index(inplace=False)
        #instancedf = instancedf.transpose()

        #allinstances = pd.read_pickle('static/data/instances')

        
        #currinstance = allinstances[allinstances['id']==id]
        #currinstance = allinstances[allinstances['name']==id]
        #instanceinfo = instancedf.to_dict('r')[0]
        try:
            lang = instanceinfo.get('info').get('languages')
            instanceinfo['languages'] = [mapping[word] for word in lang]
        except:
            AttributeError
        

        conn = psycopg2.connect("dbname=dorina user=postgres password=1234")

        #query = "SELECT * FROM uptime where instance = '" + instanceinfo['name'] + "' and date < '2022-08-31' "
        #instanceseries = pd.read_sql_query(query, conn)

        query = "SELECT * FROM uptime2 where instance = '" + instanceinfo['name'] + "'"
        instanceseries = pd.read_sql_query(query, conn)

        query = "SELECT * FROM banned where source = '" + instanceinfo['name'] + "'"
        bannedinstances = pd.read_sql_query(query, conn)

        query = "SELECT source FROM banned where banned = '" + instanceinfo['name'] + "'"
        bannedby = pd.read_sql_query(query, conn)

        d = {200:'OK', 400:'Bad Request', 401:'Unauthorized', 403:'Forbidden', 404:'Not Found', 
        406: 'Not Acceptable', 410: 'Gone', 418: "I'm a teapot", 429: 'Precondition Required',
        500:'Internal Server Error', 502:'Bad Gateway', 503:'Service Unavailable',
        504: 'Gateway Timeout', 520: 'Web Server Returned an Unknown Error',
        521: 'Web Server Is Down', 522: 'Connection Timed Out', 523: 'Origin Is Unreachable',
        525: 'SSL Handshake Failed', 526: 'Invalid SSL Certificate'
        }

        #instanceseries2.drop('rtime', axis=1, inplace=True)
        #todrop = instanceseries2[(instanceseries2.date > '2022-09-03 12:00:00.00000') & (instanceseries2.date < '2022-09-04')].index
        #instanceseries2.drop(todrop, inplace = True)
        #instanceseries2['date'] = pd.to_datetime(instanceseries2['date']).dt.date
        #instanceseries = pd.concat([instanceseries, instanceseries2], axis=0)
        
        instanceseries["statusname"] = instanceseries["status"].apply(lambda x: d.get(x))

        instanceinfo['banned'] = bannedinstances['banned'].tolist()  
        instanceinfo['bannedby'] = bannedby['source'].tolist() 
        instanceinfo['resp_time'] = round(instanceseries.rtime.mean(), 4)
        instanceinfo['calcuptime'] = round((instanceseries['status'].value_counts()[200]/len(instanceseries.index))*100,2)
        instanceinfo['status_per_user'] = round(int(instanceinfo['statuses'])/int(instanceinfo['users']),0)
        instanceinfo['connections_per_user'] = round(int(instanceinfo['connections'])/int(instanceinfo['users']),0)

        figure = go.Figure(data=[go.Pie(labels=instanceseries["statusname"], values=instanceseries["status"], textinfo='label+percent', 
        title="Up-Time of " + instanceinfo['name']
                            )])
        #context['graph'] = 
        graphtest = figure.to_html()

        figure2 = go.Figure(data=[go.Line(x=instanceseries["date"].unique(), y=instanceseries["status"])])
        figure2.update_layout(yaxis_range=[100,550], width=1000, title="HTTP Responses of " + instanceinfo['name'])
        figure2.update_xaxes(title_text = "Date")
        figure2.update_yaxes(title_text = "HTTP Response")
        figure2.write_image("static/img/timeline.png")
        
        #graphtest2 = figure2.to_html()

    context= {
        'instanceinfo': instanceinfo,
        'graph': graphtest, 
        #'graph2': graphtest2
    }
    
    # rest of the code
    #url = '{}?id={}'.format(reverse('instance_info'), id)
    #return HttpResponseRedirect(url)
    return render(request, "instance_info.html", context)