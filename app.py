# -*- coding: utf-8 -*-
from linepy import *
import json, random, tempfile, os, sys, urllib.request
from gtts import gTTS


line = LINE('EtDUqFz4UDnIj7dWb2zd.oT3/6Uoh2biElhXIRpcphq.D6madJDfDsE9Z7/vW1Oo1IFUZ31HuIz2y4g8L9VET8U=')
#line = LINE('AUTHTOKEN')

line.log("Auth Token : " + str(line.authToken))
#line.log("Timeline Token : " + str(line.tl.channelAccessToken))

spam=True
# Initialize OEPoll with LINE instance
oepoll = OEPoll(line)
ciduk = {
         'state':{},
         'mem':{}
}
sholat=False
admin = ['uaf3ee63c94eb3c3f520f2cc8cb73082a']
while True:
    try:
        ops=oepoll.singleTrace(count=50)
        
        for op in ops:
            # Receive messages
            if op.type == OpType.RECEIVE_MESSAGE:
                msg = op.message
                #print(msg)
                text = msg.text
                msg_id = msg.id
                receiver = msg.to
                sender = msg._from
                try:
                    # Check content only text message
                    if msg.contentType == 0:
                        # Check only group chat
                        if msg.toType == 2:
                            if (sender in admin) and spam==False :
                                #CommandListAdmin
                                try:
                                    if text.lower() == ".botoff":
                                        spam=False
                                        line.sendMessage(receiver, "Shuting down.")
                                    elif text.lower() ==".boton":
                                        spam=True
                                        line.sendMessage(receiver, "Turning On.")
                                except Exception as e:
                                    line.log('ADMIN_Err '+srr(e))
                            elif spam==True:
                                # Chat checked request
                                line.sendChatChecked(receiver, msg_id)
                                # Get sender contact
                                #contact = line.getContact(sender)
                                # Command list-not-admin
                                if  msg.location !=None:
                                    line.sendMessage(msg.to, 'Lokasi Diterima')
                                    lok=msg.location
                                    lat = lok.latitude
                                    lon = lok.longitude
                                    if sholat==True:
                                        ur=urllib.request
                                        url='https://time.siswadi.com/pray/'+str(lat)+'/'+str(lon)
                                        object=json.loads(ur.urlopen(url).read().decode())
                                        pesan='[Jadwal Sholat]\n\nSubuh %s\nDzuhur %s\nAshar %s\nMaghrib %s\nIsya %s\n\nPukul %s Waktu setempat' %(object['data']['Fajr'],object['data']['Dhuhr'],object['data']['Asr'],object['data']['Maghrib'],object['data']['Isha'],object['time']['time'])
                                        sholat=False
                                        line.sendMessage(msg.to, pesan)
                                elif text.lower() == '.jadwal.sholat':
                                    line.sendMessage(receiver, 'Kirimkan Lokasi Anda')
                                    sholat=True
                                elif 'apakah ' in text.lower():
                                    try:
                                        pref=['iya','tidak','bisa jadi']
                                        jawab=random.choice(pref)
                                        tts = gTTS(text=jawab,lang='id',slow=False)
                                        tts.save('temp.mp3')
                                        line.sendAudio(receiver, 'temp.mp3')
                                    except Exception as e:
                                        line.sendMessage(msg.to, 'Send Audio Failed ' + str(e))
                                elif '.yt.audio ' in text.lower():
                                    try:
                                        ur=urllib.request
                                        query=text.lower().replace('.yt.audio ','')
                                        url='http://rahandiapi.herokuapp.com/youtubeapi/search?key=betakey&q=%s'%(query)
                                        output=json.loads(ur.urlopen(url).read().decode())
                                        mp3=output['result']['audiolist'][4]['url']
                                        line.sendAudioWithUrl(msg.to, mp3)
                                    except Exception as e:
                                    	line.sendMessage(msg.to, str(e))
                                elif text.lower() == '.set':
                                    try:
                                        del ciduk['state'][receiver]
                                        del ciduk['mem'][receiver]
                                    except:
                                        pass
                                    ciduk['state'][receiver] = True
                                    ciduk['mem'][receiver] = ''
                                    #print('Ciduk Mode On')
                                    txt='Ciduk Mode On'
                                    line.sendMessage(receiver,txt)
                                elif text.lower()=='.off':
                                    ciduk['state'][receiver]=False
                                    #print('Ciduk Mode Off')
                                    txt='Ciduk Mode Off'
                                    line.sendMessage(receiver, txt)
                                elif text.lower()=='.tagall':
                                    group=line.getGroup(msg.to)
                                    mids=[contact.mid for contact in group.members]
                                    line.sendMessageWithMention(msg.to,'',mids)
                                    line.sendMessage(msg.to,'Guys!!')
                                elif msg.text.lower()=='.creator':
                                    group=line.getGroup(msg.to)
                                    creator = group.creator
                                    '''print(group)
                                    print('\n\n\n')
                                    print(creator)'''
                                    print(creator.mid)
                                    line.sendMessage(msg.to, 'Our Creator')
                                    line.sendContact(msg.to, creator.mid)
                                elif text.lower()=='.botoff':
                                    if sender in admin:
                                        spam=False
                                        line.sendMessage(receiver,'Shuting Down.')
                                    else : line.sendMessage(receiver, 'You Are not Admin')
                                elif text.lower()=='.boton':
                                    if sender in admin : line.sendMessage(receiver, 'You Already On')
                                    else: line.sendMessage(receiver, 'You Are not Admin')
                                else:
                                    pass
                            else:
                                pass 
                except Exception as e:
                    line.log("[RECEIVE_MESSAGE] ERROR : " + str(e))
            # Auto join if BOT invited to group
            elif op.type == OpType.NOTIFIED_INVITE_INTO_GROUP:
                try:
                    group_id=op.param1
                    # Accept group invitation
                    line.acceptGroupInvitation(group_id)
                    line.sendMessage(group_id, 'Hai!!\nSaya botnya Rafi.\nSalam kenal :)')
                    line.sendContact(group_id, mid=admin[0])
                except Exception as e:
                    line.log("[NOTIFIED_INVITE_INTO_GROUP] ERROR : " + str(e))
            elif op.type == OpType.SEND_MESSAGE:
                msg = op.message
                msg_id = msg.id
                text = msg.text
                sender = msg._from
                receiver = msg.to

                try:
                    if msg.contentType == 0 :
                       if msg.toType == 2 :
                           if text.lower()=='.spamon':
                               spam==True
                               print('Spam ON')
                           elif text.lower()=='.spamoff':
                               spam==False
                               print('Spam OFF')
                           
                           else:
                               pass
                except Exception as e:
                    line.log("[SEND_MESSAGE] ERROR : " + str(e))
            #Sider
            elif op.type == OpType.NOTIFIED_READ_MESSAGE :
                group_id=op.param1
                terciduk=op.param2
                kontak=line.getContact(terciduk)
                #msg=op.message
                try:
                    if ciduk['state'][group_id] == True:
                        if terciduk in ciduk['mem'][group_id]:
                            pass
                        else:
                            txt = 'Tercyduk kamu ' + kontak.displayName
                            ciduk['mem'][group_id] += '\n' + terciduk
                            line.sendMessage(group_id,txt)
                            print(txt)
                    else :
                        pass
                    pass
                except:
                    pass
            else:
                pass

            # Don't remove this line, if you wan't get error soon!
            oepoll.setRevision(op.revision)
            
    except Exception as e:
        line.log("[SINGLE_TRACE] ERROR : " + str(e))
