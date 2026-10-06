"""Render public static wireframes from the explicit Design Plan records.
Each domain has screen-specific layouts; illustrations are not live interfaces.
"""
from pathlib import Path
import html,json,textwrap
root=Path(__file__).resolve().parents[1]/'src'
plans=json.loads((root/'_data/designPlans.json').read_text())
E=html.escape
class Screen:
 def __init__(self,plan,step):
  self.items=[f'<svg xmlns="http://www.w3.org/2000/svg" width="800" height="620" viewBox="0 0 800 620" role="img" aria-labelledby="title desc"><title id="title">{E(step["screenTitle"])}</title><desc id="desc">{E(step["alt"])}</desc><rect width="800" height="620" fill="#101013"/><g font-family="Arial,sans-serif" fill="#fafaf7">']
  self.rect(0,0,800,38,'#24242a')
  for x in [18,34,50]:self.items.append(f'<circle cx="{x}" cy="19" r="4" fill="#73737c"/>')
  self.rect(128,8,544,22,'#17171b',None);self.text(400,23,plan['slug']+'.local',11,'#a4a4ac',anchor='middle')
  self.rect(0,38,800,50,'#18181d');self.text(28,69,plan['name'].lower()+'.',17);self.text(770,69,'Menu   /   Your order' if plan['slug']=='coffee-ordering' else 'Classes   /   Your booking' if plan['slug']=='class-booking' else 'Support workspace',12,'#a4a4ac',anchor='end')
  self.line(0,88,800,88)
 def rect(self,x,y,w,h,fill='#18181d',stroke='#43434c'):
  self.items.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"'+(f' stroke="{stroke}"' if stroke else '')+'/>')
 def line(self,x,y,x2,y2,color='#43434c'):
  self.items.append(f'<path d="M{x} {y}L{x2} {y2}" stroke="{color}" fill="none"/>')
 def text(self,x,y,value,size=16,color='#fafaf7',anchor='start'):
  self.items.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}">{E(str(value))}</text>')
 def paragraph(self,x,y,value,width=45,size=15,color='#a4a4ac'):
  for i,line in enumerate(textwrap.wrap(value,width)):self.text(x,y+i*(size+7),line,size,color)
 def placeholder(self,x,y,w,h,label):
  self.rect(x,y,w,h,'#1d1d23');self.line(x,y,x+w,y+h);self.line(x+w,y,x,y+h)
  self.rect(x+8,y+h/2-14,w-16,28,'#1d1d23',None);self.text(x+w/2,y+h/2+5,label,12,'#a4a4ac','middle')
 def label(self,x,y,value):self.text(x,y,value.upper(),11,'#a4a4ac')
 def button(self,x,y,w,value):
  self.rect(x,y,w,42,'#fafaf7',None);self.text(x+16,y+27,value,15,'#101013');self.text(x+w-16,y+27,'↗',18,'#101013','end')
 def choices(self,x,y,items,selected,width=108):
  for i,value in enumerate(items):
   self.rect(x+i*(width+8),y,width,38,'#303038' if value==selected else '#18181d','#fafaf7' if value==selected else '#43434c');self.text(x+i*(width+8)+width/2,y+25,value,14,anchor='middle')
 def check(self,x,y):
  self.items.append(f'<circle cx="{x}" cy="{y}" r="20" fill="none" stroke="#a4a4ac"/><path d="M{x-9} {y}l6 7 13-14" fill="none" stroke="#fafaf7" stroke-width="2"/>')
 def finish(self):return ''.join(self.items)+'</g></svg>'
def coffee(s,i,step):
 if i==0:
  s.text(32,122,'← Back to menu',12,'#a4a4ac');s.placeholder(32,150,284,316,'Drink image')
  s.text(348,153,'Make it yours',30);s.text(348,188,'Latte',19);s.paragraph(348,214,'Espresso with steamed milk.',40,14)
  s.label(348,265,'Size');s.choices(348,280,['Small','Medium','Large'],'Medium',128)
  s.label(348,353,'Milk');s.choices(348,368,['Whole','Oat','Almond'],'Oat',128)
  s.label(348,442,'Quantity');s.rect(348,456,120,36);s.text(366,480,'−     1     +',16);s.text(760,481,'$5.50',23,anchor='end');s.button(348,525,420,'Add to order')
 elif i==1:
  s.text(32,140,'Your order',30);s.text(32,170,'1 item · pickup',14,'#a4a4ac');s.placeholder(32,205,84,92,'Drink')
  s.text(136,232,'Oat latte',22);s.text(136,260,'Medium · oat milk',15,'#a4a4ac');s.text(136,290,'Quantity 1    ·    Edit    ·    Remove',12,'#a4a4ac')
  s.line(32,326,450,326);s.label(32,363,'Pickup');s.text(32,395,'Ready in 5–8 minutes',22);s.paragraph(32,428,'Collect your drink at the pickup counter.',40)
  s.rect(482,200,286,344);s.text(506,238,'Order summary',20);s.text(506,283,'Oat latte ×1',15);s.text(744,283,'$5.50',15,anchor='end');s.line(506,310,744,310);s.text(506,345,'Total',20);s.text(744,345,'$5.50',23,anchor='end');s.label(506,394,'Pickup estimate');s.text(506,420,'5–8 minutes',18);s.button(506,469,238,'Place order')
 elif i==2:
  s.check(52,139);s.text(88,148,'You’re on the list',30);s.text(88,177,'Order #1042 · submitted',14,'#a4a4ac')
  s.rect(32,214,354,298);s.label(56,249,'Your coffee');s.text(56,282,'Medium oat latte',23);s.text(56,311,'Oat milk · quantity 1',15,'#a4a4ac');s.line(56,336,362,336);s.label(56,370,'Estimated readiness');s.text(56,405,'5–8 minutes',26);s.text(56,443,'Collect at the pickup counter.',14,'#a4a4ac');s.placeholder(414,214,354,236,'Café / pickup location');s.text(414,482,'Pickup counter',20);s.button(32,542,354,'View order')
 elif i==3:
  s.text(32,142,'Latte is unavailable',30);s.placeholder(32,183,220,220,'Unavailable drink');s.text(284,214,'Medium oat latte',24);s.paragraph(284,251,'This drink is unavailable today. Choose an available drink to continue.',48,17);s.line(284,324,768,324);s.label(284,357,'Your order');s.paragraph(284,385,'Other items remain in your order. You can review the new drink and total before placing it.',48,15);s.button(284,477,484,'See alternatives')
 else:
  s.text(32,140,'Choose another drink',30);s.text(32,174,'Configure your replacement, then review the updated order.',16,'#a4a4ac')
  for x,name,detail in [(32,'Flat white','Oat milk available'),(416,'Americano','Milk optional')]:
   s.placeholder(x,205,352,200,'Drink image');s.text(x,441,name,23);s.text(x,470,detail,15,'#a4a4ac');s.button(x,509,352,'Choose '+name.lower())
def classes(s,i,step):
 if i==0:
  s.text(32,140,'Beginner pottery',30);s.placeholder(32,172,296,255,'Class image');s.label(32,465,'No experience needed');s.text(32,495,'2 hours · Clay studio',18)
  s.text(360,202,'Choose a session',23)
  for y,time,places in [(224,'Sat 10 Oct · 10:00','3 places available'),(336,'Sat 10 Oct · 14:00','6 places available')]:
   s.rect(360,y,408,92);s.text(384,y+35,time,21);s.text(384,y+64,places,14,'#a4a4ac');s.text(740,y+51,'◉' if y==224 else '○',23,'#fafaf7' if y==224 else '#a4a4ac','end')
  s.button(360,473,408,'Choose 10:00')
 elif i==1:
  s.text(32,140,'Review your place',30);s.placeholder(32,184,104,98,'Class');s.text(158,214,'Beginner pottery',23);s.text(158,246,'Sat 10 Oct · 10:00–12:00',16,'#a4a4ac');s.label(32,335,'Participant');s.text(32,369,'Alex',21);s.text(32,400,'alex@example.com',16,'#a4a4ac');s.rect(474,184,294,344);s.text(498,227,'Your reservation',22);s.label(498,275,'Places');s.text(498,305,'1 place',20);s.label(498,356,'Location');s.text(498,385,'Clay studio',20);s.button(498,450,246,'Confirm booking')
 elif i==2:
  s.check(52,139);s.text(88,148,'Your place is reserved',30);s.text(88,178,'Booking #208',15,'#a4a4ac');s.text(32,246,'Beginner pottery',24);s.label(32,294,'When');s.text(32,326,'Sat 10 Oct at 10:00',21);s.label(32,376,'Where');s.text(32,408,'Clay studio',21);s.paragraph(32,455,'Bring clothes you can get clay on.',35);s.placeholder(416,220,352,268,'Studio / arrival location');s.button(32,537,352,'View booking')
 elif i==3:
  s.text(32,141,'That session is full',30);s.placeholder(32,185,220,220,'Class image');s.text(284,218,'Beginner pottery',24);s.text(284,253,'Sat 10 Oct · 10:00',19,'#a4a4ac');s.paragraph(284,303,'The last place has been reserved. Choose another available session.',45,17);s.line(284,364,768,364);s.text(284,402,'Your contact details are saved.',15,'#a4a4ac');s.button(284,470,484,'See other sessions')
 else:
  s.placeholder(32,128,80,76,'Class');s.text(136,160,'Another time for pottery',29);s.text(136,191,'Beginner pottery · Alex · 1 place',15,'#a4a4ac')
  for y,time,places in [(244,'Sat 10 Oct · 14:00','6 places available'),(365,'Sat 17 Oct · 10:00','4 places available')]:
   s.rect(32,y,736,96);s.text(56,y+38,time,23);s.text(56,y+69,places,15,'#a4a4ac');s.text(740,y+57,'◉' if y==244 else '○',24,'#fafaf7' if y==244 else '#a4a4ac','end')
  s.button(32,512,736,'Choose 14:00')
def support(s,i,step):
 s.rect(0,88,148,532,'#18181d');s.line(148,88,148,620)
 for y,label in [(132,'Inbox'),(178,'Unassigned'),(224,'In progress'),(270,'Awaiting'),(292,'customer')]:s.text(18,y,label,13,'#fafaf7' if y==132 else '#a4a4ac')
 s.text(174,119,'Requests / #314',12,'#a4a4ac');s.text(174,154,'Invoice will not download',26)
 if i==0:
  s.rect(174,190,366,192);s.label(194,218,'Alex Rivera');s.paragraph(194,253,'The invoice download fails after I open the invoice. Can you help?',36,17);s.text(194,348,'Customer message',12,'#a4a4ac');s.placeholder(174,405,180,126,'Attachment preview');s.text(174,564,'View customer history ↗',14);s.rect(564,190,210,330);s.label(584,224,'Customer');s.text(584,252,'Alex Rivera',18);s.label(584,302,'Status');s.text(584,329,'New',18);s.label(584,379,'Owner');s.text(584,407,'Unassigned',18);s.button(584,450,170,'Assign agent')
 elif i==1:
  s.text(174,196,'Give this request an owner',22);s.label(174,233,'Current owner: unassigned')
  s.rect(174,268,600,122);s.rect(198,294,48,48,'#25252c');s.text(222,324,'SL',16,'#a4a4ac','middle');s.text(270,306,'Sam Lee',23);s.text(270,337,'Available · billing support',15,'#a4a4ac');s.text(744,333,'◉',23,'#fafaf7','end');s.text(174,430,'After assignment: In progress · Sam Lee',16,'#a4a4ac');s.button(174,496,600,'Assign to Sam')
 elif i in [2,4]:
  s.text(174,194,'Update Alex' if i==2 else 'Ask Alex for the reference',23);s.text(174,229,'To: alex@example.com',15,'#a4a4ac');s.line(174,252,774,252);s.rect(174,278,600,186)
  message='We are checking the invoice download issue. We will update you when we know more.' if i==2 else 'Which invoice reference fails to download?'
  s.paragraph(196,313,message,54,18);s.text(196,437,'Message draft',12,'#a4a4ac');s.text(174,495,'Owner: Sam Lee' if i==2 else 'After sending: Awaiting customer · Sam Lee',14,'#a4a4ac');s.button(174,535,600,'Send update' if i==2 else 'Send question')
 else:
  s.rect(174,191,600,98);s.label(194,222,'Customer message');s.text(194,254,'Invoice download fails.',21);s.text(174,335,'Which invoice is affected?',26);s.paragraph(174,374,'The request is missing the affected invoice reference. Keep the conversation and ask Alex for that detail.',58,17);s.text(174,475,'Owner: Sam Lee · In progress',15,'#a4a4ac');s.button(174,522,600,'Request details')
for plan in plans:
 steps=[step for flow in plan['flows'] for step in flow['steps']]
 render={'coffee-ordering':coffee,'class-booking':classes,'support-workspace':support}[plan['slug']]
 for i,step in enumerate(steps):
  screen=Screen(plan,step);render(screen,i,step);(root/step['image'].lstrip('/')).write_text(screen.finish())
print('Rendered 15 screen-specific wireframes with browser frames.')
