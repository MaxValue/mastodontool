import dash
from dash import dcc
from dash import html
import psycopg2
import pandas as pd
from django_plotly_dash import DjangoDash
import requests
from mastodontool import settings

# Read plotly example dataframe to plot barchart
import plotly.express as px

conn = psycopg2.connect(
    dbname=settings.DATABASES.get("default",{})["NAME"],
    user=settings.DATABASES.get("default",{})["USER"],
    password=settings.DATABASES.get("default",{})["PASSWORD"],
    host=settings.DATABASES.get("default",{})["HOST"],
)
query = "SELECT * FROM uptime2 where status in (200, 400, 403, 404, 500, 503, 502)"

url = 'https://instances.social/api/1.0/instances/list'
key = 'Authorization: bearer xVyfYF0mSOnYS6Zlx34racvGlZwRxGKJsMAPYJndBpcyVCWOxrEUK6WZOg4r3Cmbboz1Jzkp9s2jibqYLQRNtCtKNGkqoA74e7O9TrWUuprX8dGlyrxrwa1Lrq8AKES0'

params = {'min_users': '0' , 'count': '0'} 

response = requests.get(url, params,
                        headers={'Authorization':'Bearer xVyfYF0mSOnYS6Zlx34racvGlZwRxGKJsMAPYJndBpcyVCWOxrEUK6WZOg4r3Cmbboz1Jzkp9s2jibqYLQRNtCtKNGkqoA74e7O9TrWUuprX8dGlyrxrwa1Lrq8AKES0'})

data_dict = response.json()
instances = pd.DataFrame(data_dict['instances'])
instances = instances.drop(instances[instances['name'] == 'you-think-your-fake-numbers-are-impressive.well-this-instance-contains-all-living-humans.lubar.me'].index)



allseries = pd.read_sql_query(query, conn)
d = {200:'OK', 400:'Bad Request', 401:'Unauthorized', 403:'Forbidden', 404:'Not Found', 
        406: 'Not Acceptable', 410: 'Gone', 418: "I'm a teapot", 429: 'Precondition Required',
        500:'Internal Server Error', 502:'Bad Gateway', 503:'Service Unavailable',
        504: 'Gateway Timeout', 520: 'Web Server Returned an Unknown Error',
        521: 'Web Server Is Down', 522: 'Connection Timed Out', 523: 'Origin Is Unreachable',
        525: 'SSL Handshake Failed', 526: 'Invalid SSL Certificate'
        }

mapping={'aa':'Afar','ab':'Abkhazian','af':'Afrikaans','ak':'Akan','am':'Amharic','an':'Aragonese','as':'Assamese','av':'Avaric','ay':'Aymara','az':'Azerbaijani','ay':'Aymara','ar':'Arabic','be':'Belarusian','bm':'Bambara','ba':'Bashkir','be':'Belarusian','bn':'Bengali','bi':'Bislama','bs':'Bosnian','br':'Breton','my':'Burmese','bg':'Bulgarian','eu':'Basque','ca':'Catalan','ce':'Chechen','cv':'Chuvash','cr':'Cree','co':'Corsican','cu':'ChurchSlavic','ch':'Chamorro','cs':'Czech','cy':'Welsh','da':'Danish','de':'German','dv':'Divehi','dz':'Dzongkha','ee':'Ewe','el':'Greek','en':'English','eo':'Esperanto','es':'Spanish','et':'Estonian','eu':'Basque','fa':'Persian','ff':'Fulah','fj':'Fijian','fo':'Faroese','fy':'WesternFrisian','fi':'Finnish','fr':'French','ga':'Irish','gd':'ScottishGaelic','gl':'Galician','gn':'Guarani','gu':'Gujarati','gv':'Manx','ha':'Hausa','he':'Hebrew','hi':'Hindi','ho':'HiriMotu','hr':'Croatian','ht':'Haitian','hu':'Hungarian','hy':'Armenian','hz':'Herero','ia':'Interlingua','ie':'Interlingue','ig':'Igbo','ii':'SichuanYi','ik':'Inupiaq','io':'Ido','iu':'Inuktitut','jv':'Javanese','ka':'Georgian','kg':'Kongo','kj':'Kuanyama','kk':'Kazakh','kl':'Kalaallisut','km':'CentralKhmer','kn':'Kannada','kr':'Kanuri','ks':'Kashmiri','ku':'Kurdish','kv':'Komi','kw':'Cornish','ky':'Kirghiz','la':'Latin','lb':'Luxembourgish','lg':'Ganda','li':'Limburgan','ln':'Lingala','lo':'Lao','mg':'Malagasy','mh':'Marshallese','mi':'Maori','ml':'Malayalam','mr':'Marathi','ms':'Malay','mt':'Maltese','my':'Burmese','na':'Nauru','nd':'NorthNdebele','ng':'Ndonga','no':'Norwegian','nr':'SouthNdebele','nv':'Navajo','ny':'Chichewa','oc':'Occitan','oj':'Ojibwa','om':'Oromo','or':'Oriya','os':'Ossetian','pa':'Punjabi','pi':'Pali','ps':'Pashto','qu':'Quechua','rm':'Romansh','rn':'Rundi','rw':'Kinyarwanda','sa':'Sanskrit','sc':'Sardinian','sd':'Sindhi','se':'NorthernSami','sg':'Sango','sh':'Serbo-Croatian','si':'Sinhala','sm':'Samoan','sn':'Shona','so':'Somali','ss':'Swati','st':'SouthernSotho','su':'Sundanese','sw':'Swahili','ta':'Tamil','te':'Telugu','tg':'Tajik','ti':'Tigrinya','tk':'Turkmen','tl':'Tagalog','tn':'Tswana','to':'Tonga','ts':'Tsonga','tt':'Tatar','tw':'Twi','ty':'Tahitian','ug':'Uighur','ur':'Urdu','uz':'Uzbek','ve':'Venda','vo':'Volapük','wa':'Walloon','wo':'Wolof','xh':'Xhosa','yo':'Yoruba','za':'Zhuang','zu':'Zulu','id':'Indonesian','is':'Icelandic','it':'Italian','ja':'Japanese','ko':'Korean','lt':'Lithuanian','lv':'Latvian','mk':'Macedonian','mn':'Mongolian','mo':'Moldavian','ne':'Nepali','nl':'Dutch','nn':'Norwegian','pl':'Polish','pt':'Portuguese','ro':'Romanian','ru':'Russian','sk':'Slovak','sl':'Slovenian','sq':'Albanian','sr':'Serbian','sv':'Swedish','th':'Thai','tr':'Turkish','uk':'Ukrainian','vi':'Vietnamese','yi':'Yiddish','zh':'Chinese'}


allseries["statusname"] = allseries["status"].apply(lambda x: d.get(x))
freq = allseries['statusname'].value_counts() / len(allseries)
uniquenames = allseries['statusname'].unique()
query = "select banned, count(banned) as ban_count from banned group by banned order by ban_count desc"
bannedinstances = pd.read_sql_query(query, conn)
top20 = bannedinstances[0:20]


instances['statuses_per_user']=round(instances['statuses'].astype(float)/instances['users'].astype(float),0)
mostactive = instances[['name', 'statuses_per_user']]
mostactive = mostactive.sort_values(by='statuses_per_user', ascending=False)
mostactive = mostactive[0:20]


query = "SELECT status, count(status) as freq FROM uptime2  where date::date=CURRENT_DATE group by status order by freq desc"
countuptime = pd.read_sql_query(query, conn)
countuptime["statusname"] = countuptime["status"].apply(lambda x: d.get(x))

query = "select source, count(source) as source_count from banned2 group by source order by source_count desc limit 20"
banning20 = pd.read_sql_query(query, conn)


langlist = []
for i in range(len(data_dict.get('instances'))):
    try:
        langlist.extend(data_dict.get('instances')[i].get('info').get('languages'))
    except:
        AttributeError

langdf = pd.DataFrame(langlist, columns = ['languages'])
langdf = langdf.groupby(['languages']).size()
langdf = langdf.to_frame()
langdf = langdf.rename(columns = {0:'langcount'}) 
langdf = langdf.reset_index()
langdf['languages'] = langdf['languages'].replace(mapping)

external_stylesheets=['https://codepen.io/amyoshino/pen/jzXypZ.css']

# Important: Define Id for Plotly Dash integration in Django
app = DjangoDash('dash_integration_id')

app.css.append_css({
"external_url": external_stylesheets
})
app.layout = html.Div(
    html.Div([
        # Adding one extar Div
        #html.Div([
        #    html.Div(children='Dash: Python framework to build web application'),
        #], className = 'row'),

        html.Div([
            html.Div([
                dcc.Graph(
                    id='daily-uptime',
                    figure={
                        'data': [
                            {'x': countuptime.statusname, 'y': countuptime.freq, 'type': 'bar', 'name': 'SF'},
                        ],
                        'layout': {
                            'title': 'HTTP Status count of today'
                        }
                    }
                )
            ], className = 'six columns'),
            html.Div([
                dcc.Graph(
                    #style={'width': '150%', 'height': '500px', 'background-color': '#cceff0'},
                    id='pie-chart',
                    figure={
                        'data': [
                            {'labels': freq.index, 'values' : freq, 'names' : freq.index, 'type': 'pie', 'name': 'SF'},
                        ],
                        'layout': {
                            'title': 'Up-Time of Mastodon instances'
                        }
                    }
                ),
            ], className = 'six columns'),
             html.Div([
                dcc.Graph(
                    #style={'width': '150%', 'height': '500px', 'background-color': '#cceff0'},
                    id='bar-chart',
                    figure={
                        'data': [
                            {'x': langdf.languages, 'y' : langdf.langcount,'type': 'bar', 'name': 'SF'},
                        ],
                        'layout': {
                            'title': 'Languages used in the Mastodon universe'
                        }
                    }
                ),
            ], className = 'six columns'),
            html.Div([
                dcc.Graph(
                    id='line-chart',
                    figure={
                        'data': [
                            {'x': top20.banned, 'y': top20.ban_count, 'type': 'bar', 'name': 'SF'},
                        ],
                        'layout': {
                            'title': '20 most banned instances'
                        }
                    }
                )
            ], className = 'six columns'),
            html.Div([
                dcc.Graph(
                    id='line-chart',
                    figure={
                        'data': [
                            {'x': banning20.source, 'y': banning20.source_count, 'type': 'bar', 'name': 'SF'},
                        ],
                        'layout': {
                            'title': '20 instances carrying out most bans'
                        }
                    }
                )
            ], className = 'six columns'),
            html.Div([
                dcc.Graph(
                    id='line-chart',
                    figure={
                        'data': [
                            {'x': mostactive.name, 'y': mostactive.statuses_per_user, 'type': 'bar', 'name': 'SF'},
                        ],
                        'layout': {
                            'title': '20 most active instances'
                        }
                    }
                )
            ], className = 'six columns'),

        ], className = 'row')
    ])
)