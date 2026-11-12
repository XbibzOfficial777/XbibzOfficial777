import base64, datetime, json, os, pathlib, urllib.request
root=pathlib.Path(__file__).resolve().parent.parent
user='XbibzOfficial777'
headers={'User-Agent':'Xbibz-profile-generator','Accept':'application/vnd.github+json'}
if os.getenv('GITHUB_TOKEN'): headers['Authorization']='Bearer '+os.environ['GITHUB_TOKEN']
def get(url, github=True):
 req=urllib.request.Request(url,headers=headers if github else {'User-Agent':'Xbibz-profile-generator'})
 with urllib.request.urlopen(req,timeout=30) as res: return res.read()
def api(path): return json.loads(get('https://api.github.com/'+path))
profile=api('users/'+user)
repos=api('users/'+user+'/repos?per_page=100&type=owner')
if not isinstance(repos,list): raise RuntimeError('Cannot obtain repositories')
langs={}
for repo in repos:
 if repo['fork']: continue
 for key,val in api('repos/'+user+'/'+repo['name']+'/languages').items(): langs[key]=langs.get(key,0)+val
now=datetime.datetime.now(datetime.timezone.utc).date(); year=now.year
contrib=json.loads(get(f'https://github-contributions-api.jogruber.de/v4/{user}?y={year}',False))
days=[d for d in contrib['contributions'] if d['date'] <= now.isoformat()]
if not days: raise RuntimeError('No contribution history available')
# Three calendar weeks aligned to Sunday, with future and unavailable dates blank.
lookup={d['date']:d for d in days}
start=now-datetime.timedelta(days=(now.weekday()+1)%7+14)
matrix=[]
for week in range(3):
 row=[]
 for weekday in range(7):
  date=start+datetime.timedelta(days=week*7+weekday); item=lookup.get(date.isoformat())
  row.append({'c':item['count'],'day':date.day,'today':date==now} if item else None)
 matrix.append(row)
streak=0
for i,item in enumerate(reversed(days)):
 if item['count']>0: streak+=1
 elif i==0: continue
 else: break
longest=run=0
for item in days:
 run=run+1 if item['count']>0 else 0; longest=max(longest,run)
selected=['Mochy-Music','evillimiter','whatsbibz','telebibz','plinteng-ai','Bibz-Islamic-App']
by={r['name'].lower():r for r in repos}
descriptions={
 'Mochy-Music':'Pemutar musik Android modern.',
 'evillimiter':'Monitor bandwidth jaringan lokal.',
 'whatsbibz':'Library WhatsApp Web multi-device.',
 'telebibz':'Framework bot Telegram untuk Node.js.',
 'plinteng-ai':'AI agent dan platform otomasi.',
 'Bibz-Islamic-App':'Aplikasi Al-Quran offline-first.'
}
pins=[]
for name in selected:
 r=by[name.lower()]; pins.append({'name':r['name'],'url':r['html_url'],'text':descriptions[name],'fork':r['fork'],'stars':r['stargazers_count'],'language':r['language'] or '', 'topics':r.get('topics',[])})
stats={'stars':sum(r['stargazers_count'] for r in repos),'contributions':sum(d['count'] for d in days),'repos':profile['public_repos'],'followers':profile['followers'],'languages':sorted(langs.items(),key=lambda x:-x[1])[:8],'days':matrix,'pins':pins,'streak':{'currentStreakCount':streak,'longestStreakCount':longest}}
(root/'src/data/stats.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2)+'\n')
avatar=get('https://avatars.githubusercontent.com/u/215938563?v=4',False)
(root/'src/data/avatar.json').write_text(json.dumps({'avatar':'data:image/jpeg;base64,'+base64.b64encode(avatar).decode()}))
print('Updated real public stats for',user,'year',year,'and profile avatar')
